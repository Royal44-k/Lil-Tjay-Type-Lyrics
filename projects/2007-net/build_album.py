"""Build lyric books, original hook/source MIDI and a portable preproduction pack."""
from pathlib import Path
import csv, json, re, struct, hashlib, zipfile
from project_spec import TRACKS, SOURCES

ROOT=Path(__file__).resolve().parent
PPQ=480

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.rstrip()+'\n',encoding='utf-8')

def csvwrite(path,fields,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def pitch(name):
    m=re.fullmatch(r'([A-G])([#b]?)(-?\d+)',name)
    assert m,name
    return 12*(int(m[3])+1)+{'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[m[1]]+{'':0,'#':1,'b':-1}[m[2]]

def vlq(n):
    values=[n&127];n>>=7
    while n: values.insert(0,(n&127)|128);n>>=7
    return bytes(values)

def meta(kind,value):return b'\xff'+bytes([kind])+vlq(len(value))+value

def make_midi(path,title,bpm,notes,length):
    events=[(0,-5,meta(3,title.encode())),(0,-4,meta(81,round(60000000/bpm).to_bytes(3,'big'))),
            (0,-3,meta(88,bytes([4,2,24,8]))),(0,-2,bytes([0xc0,0]))]
    previous_end=0
    rows=[]
    for syllable,note,start,duration in notes:
        assert duration>0 and start>=previous_end and start+duration<=length,(title,note,start)
        midi=pitch(note);assert 0<=midi<=127
        on=round(start*PPQ);off=round((start+duration)*PPQ)
        events.extend([(on,2,bytes([0x90,midi,84])),(off,0,bytes([0x80,midi,0]))])
        if syllable:events.append((on,1,meta(5,syllable.encode())))
        rows.append(dict(syllable=syllable,pitch=note,midi_note=midi,start_beat=start,duration_beats=duration))
        previous_end=start+duration
    events.append((round(length*PPQ),9,meta(47,b'')))
    stream=bytearray();prev=0
    for tick,_,body in sorted(events,key=lambda e:(e[0],e[1])):
        stream.extend(vlq(tick-prev));stream.extend(body);prev=tick
    path.write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,PPQ)+b'MTrk'+struct.pack('>I',len(stream))+stream)
    return rows

def sections(lyrics):
    blocks=[]
    for line in lyrics.splitlines():
        if line.startswith('['):blocks.append(dict(label=line[1:-1],lines=[]))
        elif line.strip():blocks[-1]['lines'].append(line)
    return blocks

def fenced(label,value):return f'### {label}\n\n```text\n{value.strip()}\n```\n'
def mmss(seconds):
    total=round(seconds);return f'{total//60}:{total%60:02d}'

songbook=['# 2007.net — Complete English Songbook\n','Original fictional writing. All seven complete songs; repeated choruses are printed in full.\n']
sunobook=['# 2007.net — Suno 输入总稿\n',
 '每首单独制作。Title、Style、Exclude、Lyrics 分栏使用；所有可复制输入均为英文。每首约 1000 字符以内的 Style 是本项目的简洁预算，不代表平台统一上限。\n',
 'Suno Custom 可输入自写歌词；Exclude 位于 Advanced Options。官方说明：[Custom lyrics](https://help.suno.com/en/articles/2415873)、[Exclude](https://help.suno.com/en/articles/3161921)，2026-09-29 核查。\n',
 'BPM、调性、男女标签与小节数属于制作目标。模型生成不保证逐条复现；先比对歌词与人声，选好后再修 Hook 和编排。MIDI 是 DAW/演唱参考，不作为此处已确认支持的直接上传类型。要用音频参考，先实际演奏或渲染。真正的 voice reuse 要保留同一条录音，重新生成同一句只能算新 take。\n']
production=['# 2007.net — 编曲、旋律与演唱制作总谱说明\n',
 '这是可进入 demo 制作的文字与动机谱。七首都有完整歌词、和声方案、精确核心 Hook 动机与段落计划；主歌全旋律、完整伴奏和最终演唱仍需编曲/录音实现。MIDI 用通用钢琴事件表示音符，不是人声录音。\n',
 '所有拍号为 4/4。BPM 指四分音符；半拍感不改变小节计算。CSV 的 start_beat 从 0 开始。休止已保留在 MIDI 总长度中；Hook MIDI 只涵盖下文列明的标题动机，后续句子的方向另列。\n',
 '数字感主要作用于背景素材和角色分身，主体歌词保持可懂。每首一次只突出一件标志性音色，让鼓、低频、主唱与采样各有空间。\n']
index=[];qa=[]
for t in TRACKS:
    p=ROOT/'tracks'/t['folder'];ly=(p/'LYRICS.txt').read_text(encoding='utf-8').strip()
    ss=sections(ly);assert len(ss)==len(t['bars']),(t['title'],len(ss),len(t['bars']))
    assert len(t['style'])<=1000 and not re.search(r'[\u4e00-\u9fff]',ly+t['style']+t['exclude'])
    for name,value in [('TITLE.txt',t['title']),('STYLE.txt',t['style']),('EXCLUDE.txt',t['exclude'])]:write(p/name,value)
    bars=sum(t['bars']);seconds=bars*240/t['bpm']
    arrangement=[];start=1
    for s,n in zip(ss,t['bars']):
        lines=len(s['lines'])
        if t['id']=='07' and s['label'].startswith('Final Chorus'):allocation=[1]*8+[2,2]
        elif lines:assert n%lines==0,(t['title'],s['label'],n,lines);allocation=[n//lines]*lines
        else:allocation=[]
        assert sum(allocation)==n or not lines
        arrangement.append(dict(section=s['label'],start_bar=start,bars=n,lyric_lines=lines,line_bar_allocation=' '.join(map(str,allocation)) if lines else 'instrumental'))
        start+=n
    csvwrite(p/'ARRANGEMENT.csv',list(arrangement[0]),arrangement)
    notes=make_midi(p/'HOOK-MOTIF.mid',t['title']+' original hook motif',t['bpm'],t['motif'],t['motif_beats'])
    csvwrite(p/'HOOK-NOTES.csv',list(notes[0]),notes)
    phrase=' '.join(n[0] for n in t['motif'])
    notestr=' – '.join(n[1] for n in t['motif'])
    note=f"# {t['id']} — {t['title']}\n\n{t['genre']} · {t['bpm']} BPM · {t['key']} · {bars} 小节 · 计划 {mmss(seconds)}\n\n## 人物、演唱与 Flow\n\n{t['voice']}\n\n{t['flow']}\n\n## 韵脚与句法\n\n{t['rhyme']}\n\n## 和声与编排\n\n{t['chords']}\n\n{t['sound']}\n\n## 原创 Hook 动机\n\n文本：{phrase}\n\n音高：{notestr}\n\n长度：{t['motif_beats']/4:g} 小节。逐音节拍与时值见 HOOK-NOTES.csv，MIDI 包含句尾休止。\n\n{t['hook_rest']}\n\n## 段落表\n\n"
    note+=' | '.join(['段落','起始小节','小节数','歌词行数','每行占用小节'])+'\n|---|---:|---:|---:|---|\n'
    note+='\n'.join(f"|{x['section']}|{x['start_bar']}|{x['bars']}|{x['lyric_lines']}|{x['line_bar_allocation']}|" for x in arrangement)
    write(p/'SONG-NOTES.md',note)
    production.append(note.replace('# '+t['id'],'## '+t['id'],1).replace('\n## ','\n### '))
    songbook.extend([f"## {t['id']} — {t['title']}\n",'```text\n'+ly+'\n```\n'])
    card=[f"## {t['id']} — {t['title']}\n",f"目标：{t['bpm']} BPM，{t['key']}，{mmss(seconds)}。\n"]
    for label,value in [('Title',t['title']),('Style',t['style']),('Exclude',t['exclude']),('Lyrics',ly)]:card.append(fenced(label,value))
    write(p/'SUNO-CARD.md','\n'.join(card));sunobook+=card
    index.append(dict(number=t['id'],title=t['title'],bpm=t['bpm'],key=t['key'],genre=t['genre'],bars=bars,planned_seconds=round(seconds,3),planned_time=mmss(seconds),folder=t['folder']))
    qa.append(dict(track=t['id'],sections=len(ss),lyrics_lines=sum(len(s['lines']) for s in ss),words=len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?",' '.join(' '.join(s['lines']) for s in ss))),style_characters=len(t['style']),hook_notes=len(notes)))

write(ROOT/'03-SONGBOOK.md','\n'.join(songbook))
write(ROOT/'04-PRODUCTION-BIBLE.md','\n'.join(production))
write(ROOT/'06-SUNO-IMPORT.md','\n'.join(sunobook))
csvwrite(ROOT/'TRACKLIST.csv',list(index[0]),index)
write(ROOT/'album.json',json.dumps(dict(title='2007.net',date='2026-09-29',version='composition-v1.0',language='English',status='PREPRODUCTION_NO_AUDIO',tracks=index,total_planned_seconds=round(sum(x['planned_seconds'] for x in index),3)),ensure_ascii=False,indent=2))

for s in SOURCES:
    p=ROOT/'sources'/s['id'];p.mkdir(parents=True,exist_ok=True)
    notes=make_midi(p/'SOURCE-MOTIF.mid',s['title'],s['bpm'],s['notes'],s['beats'])
    csvwrite(p/'SOURCE-NOTES.csv',list(notes[0]),notes)
    write(p/'DIRECTION.txt',s['direction'])
    write(p/'STATUS.md',f"# {s['id']}\n\n{s['title']}\n\n{s['bpm']} BPM · {s['key']} · {s['beats']/4:g} bars\n\n{s['kind']}\n\n原创乐谱/MIDI，仅用于演奏与制作参考；没有附带已录制或已渲染音频。")

if not (ROOT/'GENERATION-LOG.csv').exists():
    csvwrite(ROOT/'GENERATION-LOG.csv',['track','candidate','actual_model','actual_url','settings','input_version','listening_notes','decision'],[])
write(ROOT/'BUILD-CHECK.json',json.dumps(dict(status='PASS',songs=len(TRACKS),original_hook_motifs=len(TRACKS),original_source_motifs=len(SOURCES),total_planned_time=mmss(sum(x['planned_seconds'] for x in index)),tracks=qa,audio_generated=False),indent=2))

files=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.json']
write(ROOT/'MANIFEST.json',json.dumps(dict(version='composition-v1.0',files=files),indent=2))
archive=ROOT.parent/'2007-NET-COMPLETE-PREPRODUCTION.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)+1
    for e in files:assert hashlib.sha256(z.read(e['path'])).hexdigest()==e['sha256']
print(json.dumps({'status':'PASS','tracks':index,'archive_files':len(files)+1,'archive':str(archive)},ensure_ascii=False,indent=2))
