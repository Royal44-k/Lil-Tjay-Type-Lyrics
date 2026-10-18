"""Build the self-contained DBE preproduction pack; no account calls or audio synthesis."""
from pathlib import Path
import csv, json, re, hashlib, zipfile
import xml.etree.ElementTree as ET
from album_data import ALBUM, TRACKS
from score_material import HOOKS, SAMPLES
from music_io import dump, write_csv, write_midi, musicxml, pitch, canonical_words, hash_file, validate_midi

ROOT=Path(__file__).resolve().parent

def sections(text):
    result=[]
    for line in text.splitlines():
        line=line.strip()
        if line.startswith('[') and line.endswith(']'):
            result.append({'tag':line[1:-1],'name':line[1:-1].split(' - ')[0],'lines':[]})
        elif line:
            assert result
            result[-1]['lines'].append(line)
    return result

def oldrows(name,key):
    p=ROOT/name
    if not p.exists():return {}
    with p.open(encoding='utf-8-sig',newline='') as f:return {x[key]:x for x in csv.DictReader(f)}

def role(tid,section,i):
    if tid=='DBE03':
        if section in ['Verse 2','Post-Chorus']:return 'F1 female reply'
        if section=='Bridge':return 'M1 male lead' if i<2 else 'F1 female reply'
        if section=='Final Chorus':return 'M1 + F1 duet'
    if tid=='DBE06':
        if section in ['Verse 2','Outro']:return 'F2 female guest'
        if section=='Bridge':return 'M1' if i%2==0 else 'F2'
        if section=='Final Chorus':return 'M1 + F2 shared hook'
    return 'M1 male lead'

meta_old=oldrows('TRACK-METADATA.csv','track_id')
sample_old=oldrows('SAMPLE-REGISTER.csv','sample_id')
meta=[];vocal=[];reviews=[];total=0
songbook=['# D1fferent but Excellent — 完整歌词\n','七首原创英文歌曲。词曲预制作 v1.0；人物与场景为虚构。\n']
paste=['# D1fferent but Excellent — Suno 导入总稿\n',
       '每首单独制作，将 Title、Style、Exclude、Lyrics 分别复制到对应字段。不要将整份文件一次粘入歌词框。数字 1 只用于标题概念，歌词按普通单词 different 演唱。\n',
       '速度、调性、声部分配为制作目标；MIDI 是旋律参考，未保证文本生成能精确复现。详细路径见 SUNO-WORKFLOW.md。\n']
for t in TRACKS:
    folder=ROOT/'tracks'/t['folder'];folder.mkdir(parents=True,exist_ok=True)
    raw=(folder/'LYRICS.txt').read_text(encoding='utf-8')
    ss=sections(raw);assert len(ss)==len(t['form'])
    assert not re.search(r'[\u4e00-\u9fff]',raw)
    plain='\n\n'.join('\n'.join(s['lines']) for s in ss)+'\n'
    stream='\n\n'.join('\n'.join(x.rstrip('.,;:!?') for x in s['lines']) for s in ss)+'\n'
    assert canonical_words(plain)==canonical_words(stream)
    for name,text in [('STYLE.txt',t['style']),('EXCLUDE.txt',t['exclude']),('REFINEMENT.txt',t['revise']),('LYRICS-PLAIN.txt',plain),('LYRICS-STREAMING-DRAFT.txt',stream)]:
        (folder/name).write_text(text.strip()+'\n',encoding='utf-8')
    assert len(t['style'])<=1000
    assert not re.search('Lil Tjay|Halsey|Polo G|6LACK',t['style'],re.I)
    cursor=0;arr=[]
    for s,(name,bars) in zip(ss,t['form']):
        assert s['name']==name,(t['id'],s['name'],name)
        assert s['lines'] and bars%len(s['lines'])==0,(t['id'],name)
        per=bars//len(s['lines'])
        if name.startswith('Verse'):assert per==t['verse_bars']
        arr.append(dict(section=name,start_bar=cursor+1,end_bar=cursor+bars,bars=bars,
                        planned_start_seconds=round(cursor*240/t['bpm'],3),planned_end_seconds=round((cursor+bars)*240/t['bpm'],3)))
        for i,line in enumerate(s['lines']):
            vocal.append(dict(track_id=t['id'],section=name,line_in_section=i+1,role=role(t['id'],name,i),
              start_bar=cursor+i*per+1,bars=per,planned_start_seconds=round((cursor+i*per)*240/t['bpm'],3),words=len(canonical_words(line)),lyrics=line))
        cursor+=bars
    write_csv(folder/'ARRANGEMENT.csv',list(arr[0]),arr)
    seconds=cursor*240/t['bpm'];total+=seconds
    hook=HOOKS[t['id']]
    previous=-1
    for n in hook:
        assert n['start']>=previous-1e-8 and n['duration']>0
        previous=n['start']+n['duration']
    assert previous<=32
    chorus=next(s for s in ss if s['name']=='Chorus')
    for li,line in enumerate(chorus['lines']):
        syll=''.join(n['text'] for n in hook if li*8<=n['start']<(li+1)*8).lower()
        syll=syll.replace('camras','cameras')
        clean=lambda value:re.sub(r'[^a-z]','',value.lower())
        assert clean(syll)==clean(line),(t['id'],line,syll)
    chords=[];bass=[]
    for i,(chord,bn) in enumerate(zip(t['voicings'],t['bass'])):
        for note in chord.split():chords.append(dict(start=8*i,note=note,duration=7.5,velocity=48,text=''))
        bass.append(dict(start=8*i,note=bn,duration=7.5,velocity=60,text=''))
    parts=[dict(name='original hook melody; guide only',program=0,notes=hook),
           dict(name='harmony reference',program=4,notes=chords),dict(name='bass reference',program=33,notes=bass)]
    write_midi(folder/'HOOK-GUIDE.mid',t['title'],t['bpm'],4,8,t['sf'],t['minor'],parts)
    musicxml(folder/'HOOK-LEAD.musicxml',t['title'],t['bpm'],4,8,t['sf'],t['minor'],parts[:1])
    rows=[dict(bar=int(n['start']//4)+1,beat=round(n['start']%4+1,3),syllable=n['text'],note=n['note'],midi_pitch=pitch(n['note']),start_beats=n['start'],duration_beats=n['duration'],start_seconds=round(n['start']*60/t['bpm'],4)) for n in hook]
    write_csv(folder/'HOOK-NOTES.csv',list(rows[0]),rows)
    drum=[]
    for bar in range(1,9):
        slow=t['id'] in ['DBE03','DBE05']
        sn=[2,4] if slow else ([3.5] if t['id']=='DBE04' and bar%2==0 else [3])
        kick=[1,2.75] if bar%2 else [1,3.75]
        if t['id']=='DBE06':kick.append(2)
        if t['id']=='DBE02' and bar in [4,8]:kick=[1]
        hats=[1+.5*i for i in range(8)]
        if t['id'] in ['DBE02','DBE05']:hats=[1,2.5,3,4.5]
        for sound,beats in [('kick',kick),('snare_or_clap',sn),('closed_hat',hats)]:
            for i,b in enumerate(beats):drum.append(dict(bar=bar,beat=b,sound=sound,velocity=(100 if sound=='kick' else 92 if sound=='snare_or_clap' else 64 if i%2==0 else 42),purpose='eight-bar starting pattern; adapt to real vocals'))
    write_csv(folder/'DRUM-GRID.csv',list(drum[0]),drum)
    doc=[f'# {t["title"]}\n',f'{t["id"]} · {t["bpm"]} BPM · {t["key"]} · 4/4 · {cursor} 小节 · 计划 {int(seconds//60)}:{round(seconds%60):02d}\n',
         f'风格：{t["genres"]}。能量目标：{t["energy"]}/10。当前状态：完整词曲预制作，音频与演唱听检待完成。\n']
    for field,label in [('premise','人物与命题'),('arc','主歌如何推进'),('rhyme','韵脚与内部节奏'),('delivery','演唱与重音'),('arrangement','编曲动作'),('sample','采样与配器'),('watch','优先听检问题')]:
        doc+=['\n## '+label+'\n',t[field]+'\n']
    doc+=['\n## Hook 与节拍资产\n',' → '.join(t['chords'])+'。每个和声两个网格小节。HOOK-GUIDE.mid 包含主旋律、和声、根音参考；不是已经录制的人声或完整伴奏。主歌由 VOCAL-MAP.csv 分配角色和小节，主歌完整音高表演在 Suno 或演唱排练时定稿。DRUM-GRID.csv 是八小节起始鼓型，非从参考歌曲转录。\n',
      'MusicXML 为可编辑主旋律谱，门限按十六分音符量化；MIDI 保留更细时值。歌手可整曲移调，须同步修改器乐与版本记录。\n',
      '\n## Suno Style\n','```text\n'+t['style']+'\n```\n','\n## Exclude\n','```text\n'+t['exclude']+'\n```\n',
      '\n## 针对性修改\n','```text\n'+t['revise']+'\n```\n']
    (folder/'PRODUCTION.md').write_text('\n'.join(doc),encoding='utf-8')
    songbook += [f'\n## {t["id"]} — {t["title"]}\n','```text\n'+raw.strip()+'\n```\n']
    paste += [f'\n## {t["id"]} — {t["title"]}\n']
    for label,text in [('Title',t['title']),('Style',t['style']),('Exclude',t['exclude']),('Lyrics',raw)]:paste += ['### '+label+'\n','```text\n'+text.strip()+'\n```\n']
    wc=len(canonical_words(plain));assert 180<=wc<=650
    row=dict(track_number=int(t['id'][-2:]),track_id=t['id'],title=t['title'],language='en',bpm_target=t['bpm'],key_target=t['key'],meter='4/4',bars=cursor,planned_seconds=round(seconds,3),word_count=wc,explicit_written_lyrics=False,primary_artist='',featured_artists='',songwriters='',producers='',performers='',isrc='',upc='',release_date='',audio_file='',suno_url='',status='PREPRODUCTION_READY_AUDIO_PENDING')
    for field in ['primary_artist','featured_artists','songwriters','producers','performers','isrc','upc','release_date','audio_file','suno_url']:
        row[field]=meta_old.get(t['id'],{}).get(field,'')
    meta.append(row)
    reviews.append(dict(track_id=t['id'],words=wc,bars=cursor,hook_notes=len(hook),hook_pitch_range_midi=[min(pitch(n['note']) for n in hook),max(pitch(n['note']) for n in hook)],style_characters=len(t['style']),text_structure='PASS',hook_syllables_match='PASS',bar_allocation='PASS',sung_prosody='PENDING_AUDIO',catchiness='PENDING_LISTENING',mix_master='PENDING_AUDIO'))

(ROOT/'SONGBOOK.md').write_text('\n'.join(songbook),encoding='utf-8')
(ROOT/'SUNO-PASTEBOOK.md').write_text('\n'.join(paste),encoding='utf-8')
write_csv(ROOT/'TRACK-METADATA.csv',list(meta[0]),meta)
write_csv(ROOT/'VOCAL-MAP.csv',list(vocal[0]),vocal)
sample_rows=[]
for s in SAMPLES:
    folder=ROOT/'samples'/s['id'];folder.mkdir(parents=True,exist_ok=True)
    write_midi(folder/'SOURCE-SKETCH.mid',s['title'],s['bpm'],s['meter'],s['bars'],s['sf'],s['minor'],s['tracks'])
    musicxml(folder/'SOURCE-SKETCH.musicxml',s['title'],s['bpm'],s['meter'],s['bars'],s['sf'],s['minor'],s['tracks'])
    rows=[dict(part=p['name'],**n) for p in s['tracks'] for n in p['notes']]
    write_csv(folder/'SOURCE-NOTES.csv',list(rows[0]),rows)
    row=dict(sample_id=s['id'],title=s['title'],instrument=s['instrument'],bpm=s['bpm'],meter=f"{s['meter']}/4",bars=s['bars'],planned_seconds=round(s['bars']*s['meter']*60/s['bpm'],4),source_type='original composition MIDI, not a recording',composer_credit='',performer='',master_owner='',source_audio='',license_document='',status='SCORE_READY_RECORDING_PENDING')
    for field in ['composer_credit','performer','master_owner','source_audio','license_document','status']:
        if sample_old.get(s['id'],{}).get(field):row[field]=sample_old[s['id']][field]
    sample_rows.append(row)
write_csv(ROOT/'SAMPLE-REGISTER.csv',list(sample_rows[0]),sample_rows)
assert all(sid in {s['id'] for s in SAMPLES} for t in TRACKS for sid in t['samples'])
motif=[]
for a,b in zip(HOOKS['DBE01'][:3],[n for n in HOOKS['DBE07'] if 16<=n['start']<18]):
    motif.append(dict(first_note=a['note'],finale_note=b['note'],pitch_change=pitch(b['note'])-pitch(a['note']),first_start=a['start'],finale_relative_start=b['start']-16,first_gate=a['duration'],finale_gate=b['duration']))
assert len(motif)==3 and [m['pitch_change'] for m in motif]==[0,1,0]
assert all(abs(m['first_start']-m['finale_relative_start'])<1e-8 for m in motif)
write_csv(ROOT/'MOTIF-COMPARISON.csv',list(motif[0]),motif)
midi=[validate_midi(p) for p in sorted(ROOT.rglob('*.mid'))]
xml=[]
for p in sorted(ROOT.rglob('*.musicxml')):
    tree=ET.parse(p)
    for part in tree.findall('part'):
        div=int(part.findtext('measure/attributes/divisions'));beats=int(part.findtext('measure/attributes/time/beats'))
        for m in part.findall('measure'):assert sum(int(n.findtext('duration')) for n in m.findall('note'))==div*beats
    xml.append(str(p.relative_to(ROOT)))
for name,fields in [
 ('GENERATION-LOG.csv',['track_id','candidate_id','date','model','settings','prompt_version','source_audio','suno_url','actual_duration','hook_score','diction_score','voice_roles_score','arrangement_score','decision','notes']),
 ('AUDIO-QC.csv',['track_id','version','file','sample_rate','bit_depth','channels','actual_bpm','actual_key','duration','lufs_i','max_dbtp','lra','lyrics_match','mono_check','codec_check','reviewer','decision','notes']),
 ('CREDITS-AND-SPLITS.csv',['track_id','person_legal_name','display_name','role','composition_share_percent','master_share_percent','agreement_reference','status']),
 ('LEARNING-LOG.csv',['date','track_id','hypothesis','candidate_A','candidate_B','changed_variable','observation','decision','reviewer'])]:
    if not (ROOT/name).exists():write_csv(ROOT/name,fields,[])
dump(ROOT/'QC-REPORT.json',dict(stage='PREPRODUCTION',audio_exists=False,release_ready=False,tracks=reviews,planned_album_seconds=round(total,3),vocal_lines=len(vocal),midi=midi,musicxml=xml,motif_variation='middle note rises one semitone; relative onsets match; final gate shortened'))
dump(ROOT/'album.json',dict(**ALBUM,tracks=TRACKS))
entries=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hash_file(p)) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='DELIVERY-MANIFEST.json']
dump(ROOT/'DELIVERY-MANIFEST.json',dict(album=ALBUM['title'],version=ALBUM['version'],files=entries))
archive=ROOT.parent/'D1FFERENT-BUT-EXCELLENT-PREPRODUCTION-PACK.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(entries)+1
    for e in entries:
        data=z.read(e['path'].replace('\\','/'))
        assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256']
print(json.dumps(dict(tracks=len(TRACKS),planned_seconds=round(total,3),word_counts={x['track_id']:x['words'] for x in reviews},midi_files=len(midi),musicxml_files=len(xml),vocal_lines=len(vocal),archive_files=len(entries)+1,zip_and_hash_readback='PASS',archive=str(archive)),indent=2))
