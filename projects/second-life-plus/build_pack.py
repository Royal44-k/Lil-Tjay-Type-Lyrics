"""Build a preproduction delivery, preserving the original SECOND LIFE assets.
Uses only Python's standard library. Does not generate or claim finished audio.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import shutil
import struct
import zipfile
import xml.etree.ElementTree as ET
from score_material import HOOKS, SAMPLES

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'second-life-ep-2026-09-18'
PPQ = 480
ALBUM = json.loads((ROOT/'album.json').read_text(encoding='utf-8'))
NOTES = json.loads((ROOT/'track_notes.json').read_text(encoding='utf-8'))


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def pitch(name):
    m=re.fullmatch(r'([A-G])([#b]?)(-?\d+)',name)
    assert m, name
    value=dict(C=0,D=2,E=4,F=5,G=7,A=9,B=11)[m[1]]
    return 12*(int(m[3])+1)+value+({'#':1,'b':-1}.get(m[2],0))


def vlq(n):
    assert n>=0
    b=[n&127]
    while n>>7:
        n>>=7
        b.insert(0,(n&127)|128)
    return bytes(b)


def meta(kind, value):
    return b'\xff'+bytes([kind])+vlq(len(value))+value


def midi_track(events, end):
    out=bytearray(); previous=0
    for tick, priority, data in sorted(events,key=lambda x:(x[0],x[1])):
        assert previous<=tick<=end
        out+=vlq(tick-previous)+data
        previous=tick
    out+=vlq(end-previous)+meta(0x2F,b'')
    return b'MTrk'+struct.pack('>I',len(out))+out


def write_midi(path, title, bpm, meter, bars, sf, minor, parts):
    end=bars*meter*PPQ
    events=[(0,0,meta(3,title.encode('utf-8'))),
            (0,0,meta(0x51,round(60_000_000/bpm).to_bytes(3,'big'))),
            (0,0,meta(0x58,bytes([meter,2,24,8]))),
            (0,0,meta(0x59,struct.pack('bb',sf,minor)))]
    tracks=[midi_track(events,end)]
    for channel,part in enumerate(parts):
        assert channel != 9
        events=[(0,0,meta(3,part['name'].encode('utf-8'))),
                (0,0,bytes([0xC0|channel,part.get('program',0)]))]
        for n in part['notes']:
            start=round(n['start']*PPQ); stop=round((n['start']+n['duration'])*PPQ)
            assert 0<=start<stop<=end, (title,n)
            p=pitch(n['note']); assert 0<=p<=127
            if n.get('text'):
                events.append((start,1,meta(5,n['text'].encode('utf-8'))))
            events.extend([(start,3,bytes([0x90|channel,p,n.get('velocity',70)])),
                           (stop,2,bytes([0x80|channel,p,0]))])
        tracks.append(midi_track(events,end))
    data=b'MThd'+struct.pack('>IHHH',6,1,len(tracks),PPQ)+b''.join(tracks)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)


def musicxml(path,title,bpm,meter,bars,sf,minor,parts):
    """Monophonic staff parts with quantized durations, exact rests and lyric text.
    Chordal hook harmony is supplied in MIDI; XML shows the singable lead only.
    """
    root=ET.Element('score-partwise',version='4.0')
    work=ET.SubElement(root,'work'); ET.SubElement(work,'work-title').text=title
    plist=ET.SubElement(root,'part-list')
    for ix,part in enumerate(parts,1):
        pid=f'P{ix}'; entry=ET.SubElement(plist,'score-part',id=pid)
        ET.SubElement(entry,'part-name').text=part['name']
        xp=ET.SubElement(root,'part',id=pid)
        # Notation snaps note gates to a sixteenth-note grid. MIDI remains exact.
        events=sorted([{**n,'start':round(n['start']*4)/4,
                        'duration':max(.25,round((n['start']+n['duration'])*4)/4-round(n['start']*4)/4)}
                       for n in part['notes']],key=lambda x:x['start'])
        last=-1
        for n in events:
            assert n['start']+1e-8>=last, (title,part['name'],'overlapping XML notes')
            last=n['start']+n['duration']
        for b in range(bars):
            measure=ET.SubElement(xp,'measure',number=str(b+1))
            if b==0:
                attrs=ET.SubElement(measure,'attributes')
                ET.SubElement(attrs,'divisions').text=str(PPQ)
                k=ET.SubElement(attrs,'key'); ET.SubElement(k,'fifths').text=str(sf)
                ET.SubElement(k,'mode').text='minor' if minor else 'major'
                ts=ET.SubElement(attrs,'time'); ET.SubElement(ts,'beats').text=str(meter)
                ET.SubElement(ts,'beat-type').text='4'
                clef=ET.SubElement(attrs,'clef')
                bass='left hand' in part['name']
                ET.SubElement(clef,'sign').text='F' if bass else 'G'
                ET.SubElement(clef,'line').text='4' if bass else '2'
                direction=ET.SubElement(measure,'direction')
                dtype=ET.SubElement(direction,'direction-type')
                met=ET.SubElement(dtype,'metronome')
                ET.SubElement(met,'beat-unit').text='quarter'
                ET.SubElement(met,'per-minute').text=str(bpm)
                ET.SubElement(direction,'sound',tempo=str(bpm))
            bar_start=b*meter*PPQ; bar_end=(b+1)*meter*PPQ; cursor=bar_start
            for n in events:
                start=round(n['start']*PPQ); end=round((n['start']+n['duration'])*PPQ)
                if end<=bar_start or start>=bar_end: continue
                left=max(start,bar_start); right=min(end,bar_end)
                if left>cursor:
                    rest=ET.SubElement(measure,'note');ET.SubElement(rest,'rest')
                    ET.SubElement(rest,'duration').text=str(left-cursor)
                node=ET.SubElement(measure,'note')
                m=re.fullmatch(r'([A-G])([#b]?)(-?\d+)',n['note'])
                p=ET.SubElement(node,'pitch');ET.SubElement(p,'step').text=m[1]
                if m[2]:ET.SubElement(p,'alter').text=str({'#':1,'b':-1}[m[2]])
                ET.SubElement(p,'octave').text=m[3]
                ET.SubElement(node,'duration').text=str(right-left)
                if start<bar_start: ET.SubElement(node,'tie',type='stop')
                if end>bar_end: ET.SubElement(node,'tie',type='start')
                if n.get('text') and start>=bar_start:
                    lyric=ET.SubElement(node,'lyric');ET.SubElement(lyric,'text').text=n['text']
                cursor=right
            if cursor<bar_end:
                rest=ET.SubElement(measure,'note');ET.SubElement(rest,'rest')
                ET.SubElement(rest,'duration').text=str(bar_end-cursor)
            assert sum(int(x.findtext('duration','0')) for x in measure.findall('note'))==meter*PPQ
    ET.indent(root)
    ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)


def sections(text):
    result=[]
    for line in text.splitlines():
        line=line.strip()
        if line.startswith('[') and line.endswith(']'):
            label=line[1:-1]
            # Split descriptive cues; do not split the hyphen inside Pre-Chorus.
            base=re.split(r':| - ',label, maxsplit=1)[0]
            result.append(dict(tag=label,name=base,lines=[]))
        elif line:
            assert result
            result[-1]['lines'].append(line)
    return result


def canonical_words(text):
    return re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?",text.lower())


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def existing_rows(path, key):
    if not path.exists():return {}
    with path.open(encoding='utf-8-sig',newline='') as f:
        return {r[key]:r for r in csv.DictReader(f)}


def role_for(tid,name,line_idx):
    roles={
      'SLP01':{'Intro':'R1 artist / male mid','Chorus':'R2 producer + R3 engineer / joint hook','Verse 1':'R1 artist / male mid','Verse 2':'R2 producer / male low','Verse 3':'R3 engineer / female alto','Bridge':'R1','Outro':'R1'},
      'SLP03':{'Intro':'N2 night worker / female alto','Chorus':'N2 female lead','Final Chorus':'N2 female lead / N1 male harmony','Verse 1':'N1 traveling musician / male tenor','Pre-Chorus':'N1','Verse 2':'N2','Outro':'N2'},
      'SLP05':{'Intro':'D1 partner / male','Chorus':'D1 male + D2 female / duet','Final Chorus':'D1 male + D2 female / duet','Verse 1':'D1','Verse 2':'D2 original narrator / female','Outro':'D2'},
    }
    if name=='Final Chorus' and tid=='SLP01':return 'R1 artist / final commitment' if line_idx==7 else 'R1 + R2 + R3 / collective hook'
    if name=='Bridge' and tid=='SLP03':return ['N1','N2','N1','N2'][line_idx]
    if name=='Bridge' and tid=='SLP05':return ['D2','D1','D2','D1'][line_idx]
    if tid in roles:return roles[tid].get(name,'shared hook; see production notes')
    return {'SLP02':'I1 adult male','SLP04':'C1 playful male','SLP06':'S1 female alto','SLP07':'L1 male tenor','SLP08':'original male lead / female source answer'}[tid]


ROOT.mkdir(exist_ok=True)
preserved=[]
retained=ROOT/'tracks'/'08-second-life'
retained.mkdir(parents=True,exist_ok=True)
for name in ['LYRICS.txt','STYLE.txt','EXCLUDE.txt','HOOK-GUIDE.mid','HOOK-NOTES.csv','ARRANGEMENT.csv']:
    src=OLD/'04-SECOND-LIFE'/name; dst=retained/name
    shutil.copyfile(src,dst)
    assert src.read_bytes()==dst.read_bytes()
    preserved.append(dict(source=str(src),destination=str(dst.relative_to(ROOT)),sha256=hash_file(src),match=True))
seed_dir=ROOT/'samples'/'V01'; seed_dir.mkdir(parents=True,exist_ok=True)
for src in (OLD/'00-ORIGINAL-SAMPLE').iterdir():
    if src.is_file():shutil.copyfile(src,seed_dir/src.name)
dump(ROOT/'PRESERVATION.json',dict(scope='existing composition assets, not a recorded master',files=preserved))

old_metadata=existing_rows(ROOT/'TRACK-METADATA.csv','track_id')
old_samples=existing_rows(ROOT/'SAMPLE-REGISTER.csv','sample_id')
all_metadata=[]; reviews=[]; total_seconds=0; songbook=['# SECOND LIFE+ — 完整英文歌词册\n','版本：preproduction-v1.0。三个 remix、四首新作及一首原作。全部人物为虚构。\n']
pastebook=['# SECOND LIFE+ — Suno 导入总稿\n',
    '逐首制作。每首的 Title、Style、Exclude 和 Lyrics 分开复制到对应字段；不要把本文件一次性粘贴到歌词框。MIDI 与 MusicXML 用作旋律/演奏参考，需要音频参考时先录制或渲染。\n',
    '以下速度、调性、声部分配均为制作目标，实际输出需要听检。第 08 首沿用旧输入；已有定稿音频时直接保留该音频，无需再次生成。具体操作与候选选择见 SUNO-WORKFLOW.md。\n']
line_map=[]
pronunciation=[]
for t in ALBUM['tracks']:
    folder=ROOT/'tracks'/t['folder'];folder.mkdir(parents=True,exist_ok=True)
    if t['kind']!='retained':
        (folder/'STYLE.txt').write_text(t['style']+'\n',encoding='utf-8')
        (folder/'EXCLUDE.txt').write_text(t['exclude']+'\n',encoding='utf-8')
    text=(folder/'LYRICS.txt').read_text(encoding='utf-8')
    parts=sections(text)
    assert len(parts)==len(t['form']), (t['id'],len(parts),len(t['form']))
    plain='\n\n'.join('\n'.join(s['lines']) for s in parts if s['lines'])+'\n'
    (folder/'LYRICS-PLAIN.txt').write_text(plain,encoding='utf-8')
    stream='\n\n'.join('\n'.join(line.rstrip('.,;:!?') for line in s['lines']) for s in parts if s['lines'])+'\n'
    (folder/'LYRICS-STREAMING-DRAFT.txt').write_text(stream,encoding='utf-8')
    assert canonical_words(plain)==canonical_words(stream)
    cursor=0; arrangement=[]
    for sec,(name,bars) in zip(parts,t['form']):
        assert sec['name']==name, (t['id'],sec['name'],name)
        row=dict(section=name,start_bar=cursor+1,end_bar=cursor+bars,bars=bars,
                 start_seconds=round(cursor*240/t['bpm'],3),end_seconds=round((cursor+bars)*240/t['bpm'],3))
        arrangement.append(row)
        if sec['lines']:
            per_line=bars/len(sec['lines'])
            assert per_line.is_integer(), (t['id'],name,bars,len(sec['lines']))
            if name.startswith('Verse'):assert per_line==t['verse_line_bars']
            for li,line in enumerate(sec['lines']):
                line_map.append(dict(track_id=t['id'],section=name,line_in_section=li+1,
                  role=role_for(t['id'],name,li),start_bar=int(cursor+li*per_line+1),bars=int(per_line),
                  planned_start_seconds=round((cursor+li*per_line)*240/t['bpm'],3),
                  words=len(canonical_words(line)),lyrics=line))
        cursor+=bars
    seconds=cursor*240/t['bpm'];total_seconds+=seconds
    if t['kind']!='retained':
        write_csv(folder/'ARRANGEMENT.csv',list(arrangement[0]),arrangement)
        hook=HOOKS[t['id']]
        # All pitched lead notes are monophonic and fit within the eight-bar hook.
        prior=-1
        for n in sorted(hook,key=lambda n:n['start']):
            assert n['start']>=prior-1e-8
            prior=n['start']+n['duration']
        chordnotes=[];bassnotes=[]
        for i,(chord,bass) in enumerate(zip(t['voicings'],t['bass'])):
            for n in chord.split():chordnotes.append(dict(note=n,start=8*i,duration=7.7,velocity=49,text=''))
            bassnotes.append(dict(note=bass,start=8*i,duration=7.7,velocity=55,text=''))
        mp=[dict(name='hook lead; guide only',program=0,notes=hook),
            dict(name='harmony reference',program=4,notes=chordnotes),
            dict(name='bass reference',program=33,notes=bassnotes)]
        write_midi(folder/'HOOK-GUIDE.mid',t['title'],t['bpm'],4,8,t['key_sf'],t['key_minor'],mp)
        musicxml(folder/'HOOK-LEAD.musicxml',t['title'],t['bpm'],4,8,t['key_sf'],t['key_minor'],mp[:1])
        rows=[dict(bar=int(n['start']//4)+1,beat=round(n['start']%4+1,3),syllable=n['text'],note=n['note'],
                   midi_pitch=pitch(n['note']),start_beats=n['start'],duration_beats=n['duration'],
                   start_seconds=round(n['start']*60/t['bpm'],4)) for n in hook]
        write_csv(folder/'HOOK-NOTES.csv',list(rows[0]),rows)
    title=t['title'] + (f" ({t['version']})" if t['kind']=='remix' else '')
    n=NOTES[t['id']]
    doc=[f'# {title}\n',f"Track ID: {t['id']} · {t['bpm']} BPM · {t['key']} · 4/4 · {cursor} bars · 计划 {int(seconds//60)}:{round(seconds%60):02d}\n",
         f"状态：词曲制作稿；未生成完整音频。风格：{' / '.join(t['genres'])}。\n"]
    for field,label in [('premise','叙述者与命题'),('change','版本身份与变化'),('arc','情绪推进'),('rhyme','韵脚'),('prosody','重音与 flow'),('arrangement','段落编排'),('sample','采样与配器'),('risk','第一轮听检重点')]:
        doc += ['\n## '+label+'\n',n[field]+'\n']
    doc+=['\n## 和声与演唱资产\n',' → '.join(t['chords'])+'。Hook 每个和声两快拍小节（慢速曲即常规小节）。\n',
          'HOOK-GUIDE.mid 与 HOOK-NOTES.csv 是 Hook 音高/节奏草案，不是人声录音。主歌逐行进拍见全局 VOCAL-MAP.csv；主歌的完整音高表演需在生成或排练时确定。\n',
          '\n## Suno Style\n','```text\n'+(folder/'STYLE.txt').read_text(encoding='utf-8').strip()+'\n```\n',
          '\n## Exclude\n','```text\n'+(folder/'EXCLUDE.txt').read_text(encoding='utf-8').strip()+'\n```\n',
          '\n## 针对性修改提示\n','```text\n'+n['revision']+'\n```\n']
    (folder/'PRODUCTION.md').write_text('\n'.join(doc),encoding='utf-8')
    (folder/'REFINEMENT.txt').write_text(n['revision']+'\n',encoding='utf-8')
    songbook += [f'\n## {t["id"]} — {title}\n','```text\n'+text.strip()+'\n```\n']
    pastebook += [f'\n## {t["id"]} — {title}\n',
                 '### Title\n','```text\n'+title+'\n```\n',
                 '### Style\n','```text\n'+(folder/'STYLE.txt').read_text(encoding='utf-8').strip()+'\n```\n',
                 '### Exclude\n','```text\n'+(folder/'EXCLUDE.txt').read_text(encoding='utf-8').strip()+'\n```\n',
                 '### Lyrics\n','```text\n'+text.strip()+'\n```\n',
                 f'制作说明与修改提示：[PRODUCTION.md](tracks/{t["folder"]}/PRODUCTION.md)；[REFINEMENT.txt](tracks/{t["folder"]}/REFINEMENT.txt)。\n']
    wc=len(canonical_words(plain));style_len=len((folder/'STYLE.txt').read_text(encoding='utf-8').strip())
    assert style_len<=1000,(t['id'],style_len)
    assert 180<=wc<=650,(t['id'],wc)
    assert not re.search(r'\((?:whisper|sing|instrumental|spoken|screaming)',text,re.I)
    assert not re.search(r'Lil Tjay|Halsey|Sik-K|CHANGMO|ZICO|Paul Blanco|ASH ISLAND', (folder/'STYLE.txt').read_text(encoding='utf-8'),re.I)
    row=dict(track_number=int(t['id'][-2:]),track_id=t['id'],title=t['title'],version=t['version'],
             kind=t['kind'],language='en',bpm=t['bpm'],key=t['key'],meter='4/4',bars=cursor,
             planned_seconds=round(seconds,3),word_count=wc,explicit_lyrics=False,
             primary_artist='',featured_artists='',songwriters='',producers='',performers='',
             isrc='',upc='',release_date='',audio_file='',suno_url='',status='PREPRODUCTION_READY_AUDIO_PENDING')
    for field in ['primary_artist','featured_artists','songwriters','producers','performers','isrc','upc','release_date','audio_file','suno_url']:
        row[field]=old_metadata.get(t['id'],{}).get(field,'')
    all_metadata.append(row)
    reviews.append(dict(track_id=t['id'],section_count=len(parts),verse_line_counts=[len(s['lines']) for s in parts if s['name'].startswith('Verse')],
        word_count=wc,planned_seconds=round(seconds,3),style_characters=style_len,
        text_structure='PASS',bar_line_allocation='PASS',plain_lyrics_word_match='PASS',
        creative_review='DESK_REVIEWED',sung_prosody='PENDING_AUDIO',hook_memory_test='PENDING_LISTENING',
        source_recordings='NOT_RECORDED',mix_qc='PENDING_AUDIO',mastering_qc='PENDING_AUDIO',release_metadata='PENDING_HUMAN_CREDITS'))
    risks=set(re.findall(r'\b(?:ivory|receipt|counterstep|read|live|lead|bass|wound|wind|tear|close)\b',plain,re.I))
    for w in sorted(risks):
        pronunciation.append(dict(track_id=t['id'],word=w,
          decision='Context and intended stress documented in PRONUNCIATION.md; audition before phonetic substitution',
          status='LISTENING_PENDING'))

write_csv(ROOT/'TRACK-METADATA.csv',list(all_metadata[0]),all_metadata)
write_csv(ROOT/'VOCAL-MAP.csv',list(line_map[0]),line_map)
write_csv(ROOT/'PRONUNCIATION-FLAGS.csv',['track_id','word','decision','status'],pronunciation)
(ROOT/'SONGBOOK.md').write_text('\n'.join(songbook),encoding='utf-8')
(ROOT/'SUNO-PASTEBOOK.md').write_text('\n'.join(pastebook),encoding='utf-8')

sample_rows=[]
for s in SAMPLES:
    folder=ROOT/'samples'/s['id']; folder.mkdir(parents=True,exist_ok=True)
    write_midi(folder/'SOURCE-SKETCH.mid',s['title'],s['bpm'],s['meter'],s['bars'],s['key_sf'],s['key_minor'],s['tracks'])
    musicxml(folder/'SOURCE-SKETCH.musicxml',s['title'],s['bpm'],s['meter'],s['bars'],s['key_sf'],s['key_minor'],s['tracks'])
    rows=[]
    for part in s['tracks']:
        for note in part['notes']:rows.append(dict(part=part['name'],**note))
    write_csv(folder/'SOURCE-NOTES.csv',list(rows[0]),rows)
    sample_rows.append(dict(sample_id=s['id'],title=s['title'],source_type='original MIDI composition',
      bpm=s['bpm'],meter=f"{s['meter']}/4",bars=s['bars'],seconds=round(s['bars']*s['meter']*60/s['bpm'],4),
      composer_credit='PENDING_HUMAN_CREDITS',performer='NOT_RECORDED',master_owner='NO_RECORDING_YET',
      source_audio='',license_document='',external_recording_used=False,status='SCORE_READY_RECORDING_PENDING'))
    if s['id']=='V02':
        adjusted=[]
        for part in s['tracks']:
            adjusted.append({**part,'notes':[dict(n,start=n['start']*4/3,duration=n['duration']*4/3) for n in part['notes']]})
        write_midi(folder/'TARGET-144-4-4.mid','Counter Waltz, unchanged seconds on 144 grid',144,4,4,-2,1,adjusted)
        assert abs(4*3*60/108 - 4*4*60/144)<1e-9
sample_rows.append(dict(sample_id='V01',title="There's still life in me",source_type='retained original vocal melody MIDI',bpm=96,meter='4/4',bars=1,seconds=2.5,composer_credit='PENDING_HUMAN_CREDITS',performer='NOT_RECORDED',master_owner='NO_RECORDING_YET',source_audio='',license_document='',external_recording_used=False,status='SCORE_READY_RECORDING_PENDING'))
for sid in ['G01','P01','B01']:
    sample_rows.append(dict(sample_id=sid,title='Retained SECOND LIFE source plan',source_type='production plan only',bpm='',meter='',bars='',seconds='',composer_credit='PENDING_HUMAN_CREDITS',performer='NOT_RECORDED',master_owner='NO_RECORDING_YET',source_audio='',license_document='',external_recording_used=False,status='RECORDING_PENDING'))
for row in sample_rows:
    old=old_samples.get(row['sample_id'],{})
    for field in ['composer_credit','performer','master_owner','source_audio','license_document','external_recording_used','status']:
        if old.get(field):row[field]=old[field]
write_csv(ROOT/'SAMPLE-REGISTER.csv',list(sample_rows[0]),sample_rows)

# Independent readback of MIDI event clocks: each track must finish at its declared bar boundary.
def read_vlq(data,pos):
    value=0
    while True:
        x=data[pos];pos+=1;value=(value<<7)|(x&127)
        if not x&128:return value,pos


def validate_midi(path):
    data=path.read_bytes();assert data[:4]==b'MThd'
    _,fmt,count,division=struct.unpack('>IHHH',data[4:14]);assert fmt==1 and division==PPQ
    pos=14;times=[]
    for _ in range(count):
        assert data[pos:pos+4]==b'MTrk'
        size=struct.unpack('>I',data[pos+4:pos+8])[0];p=pos+8;end=p+size;clock=0;ons={}
        while p<end:
            delta,p=read_vlq(data,p);clock+=delta;status=data[p];p+=1
            if status==255:
                kind=data[p];p+=1;length,p=read_vlq(data,p);p+=length
                if kind==47:assert p==end
            elif status&240 in [128,144]:
                key=(status&15,data[p]);velocity=data[p+1];p+=2
                if status&240==144 and velocity:
                    assert key not in ons;ons[key]=clock
                else:assert key in ons;del ons[key]
            elif status&240==192:p+=1
            else:raise AssertionError((path,status))
        assert not ons
        times.append(clock);pos=end
    assert pos==len(data) and len(set(times))==1
    return dict(path=str(path.relative_to(ROOT)),tracks=count,quarter_beats=times[0]/PPQ)

midi_checks=[validate_midi(p) for p in sorted(ROOT.rglob('*.mid'))]
anchor_checks=[]
for tid,oldfolder,amount,count in [('SLP01','01-NO-RECEIPT',0,6),('SLP03','02-FAST-FORWARD',3,9),('SLP05','03-ROOM-TONE',0,7)]:
    with (OLD/oldfolder/'HOOK-NOTES.csv').open(encoding='utf-8-sig') as f:old=list(csv.DictReader(f))[:count]
    new=HOOKS[tid][:count]
    for a,b in zip(old,new):
        assert pitch(a['note'])+amount==pitch(b['note'])
        assert abs(float(a['start_beats'])-b['start'])<1e-8
        assert abs(float(a['duration_beats'])-b['duration'])<1e-8
    anchor_checks.append(dict(track_id=tid,notes=count,transpose_semitones=amount,relative_rhythm_match=True,pitch_match=True))
dump(ROOT/'QC-REPORT.json',dict(stage='PREPRODUCTION',audio_exists=False,release_ready=False,
       planned_album_seconds=round(total_seconds,3),tracks=reviews,remix_anchors=anchor_checks,midi_checks=midi_checks,
       retained_files_sha256_match=all(x['match'] for x in preserved),xml_files=len(list(ROOT.rglob('*.musicxml')))))

# Keep logs empty until real generation or contributor information exists.
for filename,fields in [
 ('GENERATION-LOG.csv',['track_id','candidate_id','date','model','variety','max_mode','prompt_version','source_audio','suno_url','actual_duration','hook_score','diction_score','voice_roles_score','sample_score','arrangement_score','decision','notes']),
 ('CREDITS-AND-SPLITS.csv',['track_id','person_legal_name','display_name','role','composition_share_percent','master_share_percent','agreement_reference','status']),
 ('AUDIO-QC.csv',['track_id','audio_version','file','native_sample_rate','bit_depth','channels','measured_bpm','measured_key','actual_duration','lufs_i','max_lufs_s','max_dbtp','lra','mono_check','codec_check','lyrics_check','reviewer','decision','notes'])]:
    path=ROOT/filename
    if not path.exists():write_csv(path,fields,[])

files=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.name!='DELIVERY-MANIFEST.json':
        files.append(dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hash_file(p)))
dump(ROOT/'DELIVERY-MANIFEST.json',dict(album='SECOND LIFE+',version=ALBUM['version'],files=files))
archive=ROOT.parent/'SECOND-LIFE-PLUS-PREPRODUCTION-PACK.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    manifest=json.loads(z.read('DELIVERY-MANIFEST.json'))
    assert len(z.namelist())==len(manifest['files'])+1
    for entry in manifest['files']:
        data=z.read(entry['path'].replace('\\','/'))
        assert len(data)==entry['bytes']
        assert hashlib.sha256(data).hexdigest()==entry['sha256']
print(json.dumps(dict(tracks=len(reviews),planned_seconds=round(total_seconds,3),
  word_counts={r['track_id']:r['word_count'] for r in reviews},
  midi_files=len(midi_checks),xml_files=len(list(ROOT.rglob('*.musicxml'))),
  retained_assets=len(preserved),remix_anchors=anchor_checks,archive=str(archive),
  archive_files=len(manifest['files'])+1,archive_readback='PASS',manifest_hashes='PASS'),indent=2))
