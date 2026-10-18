"""Export original melodic-trap composition guides, not an audio performance."""
from pathlib import Path
import csv
import hashlib
import json
import re
import struct

ROOT=Path(__file__).resolve().parent
BPM=148
PPQ=480
# Positions below use the 74 BPM half-time grid. Exports multiply them by two.
HOOK=[
    ("Don't hang up don't hang up".split(),[0,.5,.75,2,2.5,2.75],[55,60,63,55,58,60],[.4,.2,1,.4,.2,.75]),
    ('Let me hear you breathe when the words get stuck'.split(),[0,.25,.5,.75,1,1.75,2,2.25,2.75,3],[60,60,63,65,67,65,63,62,58,60],None),
    ('Got a room with a view still the blinds stay shut'.split(),[0,.25,.5,.75,1,1.25,2,2.25,2.5,3,3.25],[60,60,63,62,60,58,60,63,65,63,60],None),
    ("I don't need the right words just don't hang up".split(),[0,.25,.5,.75,1.25,1.5,2,2.5,2.75,3],[55,58,60,63,65,63,62,55,58,60],None),
    ("Don't hang up don't hang up".split(),[0,.5,.75,2,2.5,2.75],[58,63,67,58,65,63],[.4,.2,1,.4,.2,.75]),
    ("You ain't got- ta fix what you did- n't fuck up".split(),[0,.25,.5,.75,1,1.5,1.75,2,2.25,2.5,3],[63,63,65,67,67,65,63,62,60,58,63],None),
    ("We can let the clock run we ain't got- ta rush".split(),[0,.25,.5,.75,1,1.5,2,2.25,2.5,2.75,3],[62,62,65,67,65,62,60,62,60,59,62],None),
    ("Stay a lit- tle stay a lit- tle don't hang up".split(),[0,.25,.5,.75,1.5,1.75,2,2.25,2.75,3,3.25],[62,60,59,55,62,60,59,55,55,59,60],None),
]
SAMPLE=("If your words run out I'll be lis- ten- ing".split(),[0,.25,.5,1.25,1.5,4,4.5,5,5.75,6],[67,70,72,70,67,67,70,75,74,72],[.2,.2,.65,.2,1.5,.4,.4,.65,.2,1.5])
FORM=[('Intro',4),('Hook 1',16),('Verse 1',16),('Pre-Hook',4),('Hook 2',16),('Verse 2',16),('Bridge',8),('Final Hook',16),('Outro',4)]
CHORDS={'Cm9':(36,[48,55,58,62,63]),'Abmaj7':(32,[48,51,55,56]),'Ebmaj7':(39,[51,55,58,62]),'G7sus4':(31,[43,48,50,53]),'G7':(31,[43,47,50,53])}
TRACKS={'male_hook':[],'female_sample_guide':[],'harmony':[],'bass_guide':[],'drum_guide':[]}
ROWS=[]
SECTIONS=[]

def add(track,beat,duration,note,velocity=78,lyric='',section='',line=0):
    assert duration>0 and beat>=0 and 0<=note<=127
    TRACKS[track].append(dict(beat=beat,duration=duration,note=note,velocity=velocity,lyric=lyric))
    if track in ('male_hook','female_sample_guide'):
        ROWS.append(dict(section=section,part=track,line=line,syllable=lyric,
                         bar_148_bpm=int(beat//4)+1,beat_in_bar_0_based=round(beat%4,4),
                         duration_beats_148_bpm=round(duration,4),midi_note=note,
                         pitch=['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B'][note%12]+str(note//12-1)))

def vocal_line(track,base,line_spec,section,line=0):
    words,positions,notes,durations=line_spec
    assert len(words)==len(positions)==len(notes)
    if durations is None:
        durations=[max(.10,nextpos-p-.045) for p,nextpos in zip(positions,positions[1:]+[3.92])]
    assert len(durations)==len(words)
    for w,p,n,d in zip(words,positions,notes,durations):
        add(track,base+p*2,d*2,n,84 if track=='male_hook' else 60,w,section,line)

def final_line(index):
    words,pos,notes,dur=HOOK[index]
    if index in (0,4):
        return ("I won't hang up won't hang up".split(),[0,.125,.5,.75,2,2.5,2.75],
                [notes[0],notes[0],notes[1],notes[2],notes[3],notes[4],notes[5]],[.10,.30,.20,1,.4,.2,.75])
    if index==2:
        return ('Got a room with a view let the blinds come up'.split(),pos,notes,dur)
    if index==3:
        return ("You don't need the right words I won't hang up".split(),pos,notes,dur)
    if index==5:
        return ("We don't got- ta fix it all be- fore the sun's up".split(),
                [0,.25,.5,.75,1,1.25,1.5,1.75,2,2.25,2.75,3.25],
                [63,63,65,67,67,65,63,62,60,58,62,63],None)
    if index==7:
        return ("Stay a lit- tle stay a lit- tle I won't hang up".split(),
                [0,.25,.5,.75,1.5,1.75,2,2.25,2.625,2.875,3.125,3.375],
                [62,60,59,55,62,60,59,55,55,55,59,60],None)
    return words,pos,notes,dur

def chord(name,beat,duration,velocity=48):
    root,notes=CHORDS[name]
    for n in notes:
        add('harmony',beat,duration-.08,n,velocity)
    # Sparse bass outline; production should replace this with a tuned 808 performance.
    for p in range(0,int(duration),4):
        add('bass_guide',beat+p,min(2.75,duration-p-.05),root,72)

def progression(start,length,section):
    if section=='Intro':
        chord('Cm9',start,8); chord('Abmaj7',start+8,8)
    elif section=='Bridge':
        chord('Cm9',start,16,40); chord('Abmaj7',start+16,16,40)
    elif section=='Outro':
        chord('Cm9',start,length,40)
    elif section=='Pre-Hook':
        chord('Abmaj7',start,8); chord('G7',start+8,8)
    else:
        for offset,name,duration in [(0,'Cm9',16),(16,'Abmaj7',16),(32,'Ebmaj7',16),(48,'G7sus4',8),(56,'G7',7),(63,'Cm9',1)]:
            chord(name,start+offset,duration)

offset=0
for section,bars in FORM:
    length=bars*4
    SECTIONS.append(dict(name=section,start_bar=offset//4+1,bars=bars,start_seconds=round(offset*60/BPM,3)))
    progression(offset,length,section)
    if section in ('Intro','Bridge'):
        vocal_line('female_sample_guide',offset,SAMPLE,section)
    elif section=='Outro':
        vocal_line('female_sample_guide',offset,(SAMPLE[0][-3:],[0,.75,1],SAMPLE[2][-3:],[.65,.2,2.5]),section)
    if section.startswith('Hook') or section=='Final Hook':
        for i,spec in enumerate(HOOK):
            vocal_line('male_hook',offset+i*8,final_line(i) if section=='Final Hook' else spec,section,i+1)
        # Placeholders for single-vowel sample tails, only in the lead's title rests.
        for line_index in (0,4):
            add('female_sample_guide',offset+line_index*8+7.35,.40,67,42,'out [tail]',section,line_index+1)
    if section not in ('Intro','Bridge','Outro'):
        for bar in range(bars):
            p=offset+bar*4
            add('drum_guide',p,0.15,36,95)
            if bar%2==0:
                add('drum_guide',p+1.5,0.12,36,73)
            else:
                add('drum_guide',p+3.25,0.12,36,83)
            add('drum_guide',p+2,0.16,38,87)
            step=1.0 if section=='Verse 2' and bar<4 else .5
            for h in range(int(4/step)):
                if bar in (7,15) and h*step>=3.5:
                    continue  # The triplet fill replaces the regular last hat.
                add('drum_guide',p+h*step,.08,42,46 if h%2 else 64)
            if bar in (7,15):
                for a in (3.5,3.666667,3.833333):
                    add('drum_guide',p+a,.06,42,44)
    offset+=length
assert offset==400

def vlq(value):
    out=[value&127]
    value>>=7
    while value:
        out.insert(0,(value&127)|128); value>>=7
    return bytes(out)

def meta(kind,text):
    value=text.encode('utf-8') if isinstance(text,str) else text
    return b'\xff'+bytes([kind])+vlq(len(value))+value

def encode_track(events,endbeat):
    out=b''; previous=0
    for tick,order,data in sorted(events,key=lambda x:(x[0],x[1])):
        assert tick>=previous
        out+=vlq(tick-previous)+data; previous=tick
    out+=vlq(max(0,round(endbeat*PPQ)-previous))+meta(0x2f,b'')
    return b'MTrk'+struct.pack('>I',len(out))+out

def write_midi(filename,endbeat):
    tempo=int(round(60_000_000/BPM)).to_bytes(3,'big')
    conductor=[(0,0,meta(3,'DON\'T HANG UP - original composition guide')),
               (0,1,meta(0x51,tempo)),(0,2,meta(0x58,bytes([4,2,24,8]))),
               (0,3,meta(0x59,bytes([253,1])))]
    for s in SECTIONS:
        beat=(s['start_bar']-1)*4
        if beat<endbeat:
            conductor.append((round(beat*PPQ),4,meta(6,s['name'])))
    chunks=[encode_track(conductor,endbeat)]
    for name,channel,program in [('male_hook',0,0),('female_sample_guide',1,11),('harmony',2,4),('bass_guide',3,38),('drum_guide',9,0)]:
        events=[(0,0,meta(3,name)),(0,1,bytes([0xc0|channel,program]))]
        for n in TRACKS[name]:
            if n['beat']>=endbeat:
                continue
            begin=round(n['beat']*PPQ); end=round(min(endbeat,n['beat']+n['duration'])*PPQ)
            if n['lyric']:
                events.append((begin,2,meta(5,n['lyric'])))
            events.append((begin,4,bytes([0x90|channel,n['note'],n['velocity']])))
            events.append((end,3,bytes([0x80|channel,n['note'],0])))
        chunks.append(encode_track(events,endbeat))
    data=b'MThd'+struct.pack('>IHHH',6,1,len(chunks),PPQ)+b''.join(chunks)
    (ROOT/filename).write_bytes(data)
    # Independently walk chunk boundaries to detect malformed binary framing.
    cursor=14;count=0
    while cursor<len(data):
        assert data[cursor:cursor+4]==b'MTrk'
        size=struct.unpack('>I',data[cursor+4:cursor+8])[0]
        cursor+=size+8;count+=1
    assert cursor==len(data) and count==6
    return dict(file=filename,tracks=count,bytes=len(data),seconds=round(endbeat*60/BPM,3),sha256=hashlib.sha256(data).hexdigest())

reports=[write_midi('dont-hang-up-composition.mid',400),write_midi('dont-hang-up-hook.mid',80)]
with (ROOT/'dont-hang-up-score.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=ROWS[0].keys());writer.writeheader();writer.writerows(ROWS)
lyric_text=(ROOT/'DONT-HANG-UP.md').read_text(encoding='utf-8')
lyrics={}
for heading,body in re.findall(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',lyric_text,re.M|re.S):
    if heading.startswith(('Intro','Hook','Verse','Pre-Hook','Bridge','Final Hook','Outro')):
        lyrics[heading]=[line for line in body.strip().splitlines() if line.strip()]
assert len(lyrics)==9
data=dict(title="DON'T HANG UP",bpm=BPM,half_time_bpm=74,key='C minor',status='composition and recording plan; no recorded vocal sample or finished audio',
          sections=SECTIONS,lyrics=lyrics,hook_half_time_note_spec=HOOK,sample_mother_half_time_note_spec=SAMPLE,tracks=TRACKS)
(ROOT/'composition-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for track,notes in TRACKS.items():
    assert all(0<=n['beat']<400 and n['beat']+n['duration']<=400 for n in notes)
    ends={}
    for n in sorted(notes,key=lambda n:n['beat']):
        assert ends.get(n['note'],-1)<=n['beat'],(track,n['note'],n['beat'])
        ends[n['note']]=n['beat']+n['duration']
    if track!='drum_guide':
        assert all(n['note']%12 in (0,2,3,5,7,8,10,11) for n in notes)
voice_notes=TRACKS['male_hook']
first_hook=[n for n in voice_notes if 16<=n['beat']<80]
assert len([n for n in TRACKS['female_sample_guide'] if n['beat']<16])==10
report=dict(status='passed',bpm=BPM,bars=100,first_hook_seconds=round(16*60/BPM,3),
            hook_syllables=len(first_hook),male_midi_range=[min(n['note'] for n in voice_notes),max(n['note'] for n in voice_notes)],
            score_rows=len(ROWS),midi=reports,limitations=['No reference-track transcription or audio listening analysis','Verse vocal pitches not specified','No singer or sample mother audio recorded','No commercial performance prediction'])
(ROOT/'composition-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
