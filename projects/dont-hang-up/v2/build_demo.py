"""Original instrumental and instrument-voiced topline demo; no synthesized speech."""
from pathlib import Path
import csv, hashlib, json, math, re, struct, wave
import numpy as np

ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/'source-v1-composition.json').read_text(encoding='utf-8'))
SR=44100
BPM=148
BEAT=60/BPM
PPQ=480
TOTAL_BEATS=400
N=round((TOTAL_BEATS*BEAT+3)*SR)
RNG=np.random.default_rng(91217)
TRACKS=BASE['tracks']
TRACKS['male_topline']=TRACKS.pop('male_hook')
TRACKS['plucked_keys']=[]
ROWS=[]

V1=[
 'Key card bent third try green light',
 'Same jeans red eyes third late flight',
 'Sold- out room eve- ry- bod- y knew my lines',
 "One call from you and I can't find mine",
 'Sent Mom rent she sent three hearts',
 "Typed I'm tired then e- rased that part",
 "I learned I'm good from watch- in' her",
 'Work two shifts with her back still hurt',
 'Saw your name flash let it fade to black',
 'Kept my dis- tance got mad when you stepped back',
 "You said You want me when your night's gone bad",
 "Where you at when I'm the one who cracks",
 'Had a whole speech lined up in my head',
 'You cut it short You eat- en yet',
 'I let a laugh out then I lost my breath',
 "You heard the part I had- n't said",
]
V2=[
 'New couch still wrapped in plas- tic',
 'Four seats one plate old hab- its',
 "Spent three weeks pick- in' out the fab- ric",
 "Still eat by the sink coat on stand- in'",
 "Pay for qui- et still can't sleep straight",
 "T- V talks I don't know what's play- in'",
 'Same old re- runs just a big- ger place',
 "I can change the locks can't make my- self feel safe",
 'Your name lit up at a quar- ter to three',
 "Your I'm good sound- ed just like me",
 'Had a joke read- y let it go let you breathe',
 'Heard your chair scrape back then you start- ed to speak',
 "Ket- tle clicked we were both talk- in' soft",
 'Stayed till your five a m a- larm went off',
 "Noth- in' got solved we still said good- night",
 'I slept with the T- V off for the first time',
]
GRIDS={
 7:[0,.5,.875,1.5,2,2.625,3.125],
 8:[0,.375,.75,1.25,1.75,2.25,2.75,3.25],
 9:[0,.25,.625,1,1.375,1.875,2.25,2.75,3.25],
 10:[0,.25,.5,.875,1.25,1.625,2,2.375,2.75,3.25],
 11:[0,.25,.5,.75,1.125,1.5,1.875,2.125,2.5,2.875,3.375],
}
PALETTES=[[55,58,60,62,63],[56,58,60,63],[55,58,62,63],[55,59,60,62]]
V1_END=[55,55,60,60,60,60,56,56,58,58,63,63,62,62,59,60]
V2_END=[60,60,63,60,60,63,60,56,63,63,58,58,62,62,59,60]

def add(track,beat,duration,note,velocity=78,lyric=''):
    TRACKS[track].append(dict(beat=beat,duration=duration,note=note,velocity=velocity,lyric=lyric))

def phrase(text,start,notes,positions,length=8,velocity=78):
    words=text.split()
    assert len(words)==len(notes)==len(positions)
    for i,(w,n,p) in enumerate(zip(words,notes,positions)):
        nextp=positions[i+1] if i+1<len(words) else length-.16
        add('male_topline',start+p,max(.1,nextp-p-.065),n,velocity,w)

for label,lines,start,ends in [('Verse 1',V1,80,V1_END),('Verse 2',V2,224,V2_END)]:
    for line,syllables in enumerate(lines):
        words=syllables.split(); grid=GRIDS[len(words)]
        palette=PALETTES[line//4]
        contour=[0,0,1,2,1,0,1,2,1,0,1]
        notes=[palette[min(contour[i],len(palette)-1)] for i in range(len(words))]
        if label=='Verse 2' and line%4 in (1,2):
            notes=[palette[min(contour[i]+1,len(palette)-1)] for i in range(len(words))]
        notes[-1]=ends[line]
        if line==15:notes[-2]=59
        phrase(syllables,start+line*4,notes,grid,length=4,velocity=74 if label=='Verse 1' else 78)

phrase("I was half- way through I'm fine",144,[56,58,60,63,62,60,60],[0,.5,1,1.5,2.5,4,5.5])
phrase('Then I stopped my- self this time',152,[55,55,59,60,62,59,55],[0,.5,1,2,2.5,4,5.5])
phrase('Call me to- mor- row',304,[55,58,60,62,60],[0,.75,2,2.5,3.25],length=6,velocity=62)
phrase("E- ven if you're al- right",312,[55,58,60,58,55,55],[0,.5,1.5,2.25,3,4],length=6,velocity=62)
phrase("Yeah I'm here",392,[55,58,60],[0,.65,1.5],length=4,velocity=60)

# Sparse upper keys, selected from the current chord, leaving room for a singer.
chord_groups={}
for event in TRACKS['harmony']:
    chord_groups.setdefault(event['beat'],[]).append(event)
for section in BASE['sections']:
    s=(section['start_bar']-1)*4
    for bar in range(section['bars']):
        p=s+bar*4
        chord=chord_groups[max(b for b in chord_groups if b<=p)]
        pitches=sorted(e['note'] for e in chord)
        active=section['name'] not in ('Bridge','Outro') or bar%2==0
        if not active:continue
        positions=[.25,2.75] if bar%2==0 else [1.25]
        for j,onset in enumerate(positions):
            pitch=pitches[(bar+j*2)%len(pitches)]+12
            add('plucked_keys',p+onset,.72 if j==0 else 1.05,pitch,49)
        if section['name'] not in ('Intro','Bridge','Outro') and bar%2==1:
            bass=max((e for e in TRACKS['bass_guide'] if e['beat']<=p),key=lambda e:e['beat'])
            add('bass_guide',p+3.25,.62,bass['note'],63)

def section_at(beat):
    return max((s for s in BASE['sections'] if (s['start_bar']-1)*4<=beat),key=lambda s:s['start_bar'])['name']

for track in ('male_topline','female_sample_guide'):
    for n in sorted(TRACKS[track],key=lambda e:e['beat']):
        ROWS.append(dict(section=section_at(n['beat']),part=track,syllable=n['lyric'],
                         bar=int(n['beat']//4)+1,beat=round(n['beat']%4,4),
                         duration_beats=n['duration'],midi_note=n['note'],
                         pitch=['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B'][n['note']%12]+str(n['note']//12-1)))

# Compare written text and syllables, independently of pitch choices.
text=(ROOT/'LYRICS.txt').read_text(encoding='utf-8')
norm=lambda v:re.sub('[^a-z0-9]','',v.lower())
for key,lines in [('Verse 1',V1),('Verse 2',V2)]:
    body=re.search(r'\['+key+r'[^\]]*\]\s*([^\[]+)',text).group(1)
    assert norm(body)==norm(' '.join(lines)),key
for name,events in TRACKS.items():
    ends={}
    for e in sorted(events,key=lambda e:e['beat']):
        assert 0<=e['beat']<TOTAL_BEATS and e['duration']>0
        assert e['beat']+e['duration']<=TOTAL_BEATS
        assert ends.get(e['note'],-1)<=e['beat'],(name,e)
        ends[e['note']]=e['beat']+e['duration']

def vlq(value):
    b=[value&127];value>>=7
    while value:b.insert(0,(value&127)|128);value>>=7
    return bytes(b)

def meta(kind,value):
    if isinstance(value,str):value=value.encode('utf-8')
    return b'\xff'+bytes([kind])+vlq(len(value))+value

def chunk(events):
    data=bytearray();last=0
    for t,priority,payload in sorted(events,key=lambda e:(e[0],e[1])):
        data+=vlq(t-last)+payload;last=t
    data+=vlq(400*PPQ-last)+meta(47,b'')
    return b'MTrk'+struct.pack('>I',len(data))+data

conductor=[(0,0,meta(3,"DON'T HANG UP v2 - instrumental topline guide")),
           (0,1,meta(81,round(60000000/BPM).to_bytes(3,'big'))),
           (0,2,meta(88,bytes([4,2,24,8]))),(0,3,meta(89,bytes([253,1])))]
for s in BASE['sections']:conductor.append(((s['start_bar']-1)*4*PPQ,4,meta(6,s['name'])))
chunks=[chunk(conductor)]
for channel,(name,events) in enumerate(TRACKS.items()):
    ch=9 if name=='drum_guide' else channel
    ev=[(0,0,meta(3,name)),(0,1,bytes([192|ch,11 if name=='female_sample_guide' else 4]))]
    for e in events:
        begin=round(e['beat']*PPQ);end=round((e['beat']+e['duration'])*PPQ)
        if e['lyric']:ev.append((begin,2,meta(5,e['lyric'])))
        ev.extend([(begin,4,bytes([144|ch,e['note'],e['velocity']])),(end,3,bytes([128|ch,e['note'],0]))])
    chunks.append(chunk(ev))
midi=b'MThd'+struct.pack('>IHHH',6,1,len(chunks),PPQ)+b''.join(chunks)
(ROOT/'DONT-HANG-UP-v2-full-topline.mid').write_bytes(midi)
with (ROOT/'TOPLINE-SCORE.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=ROWS[0]);writer.writeheader();writer.writerows(ROWS)
(ROOT/'composition-v2.json').write_text(json.dumps(dict(bpm=BPM,key='C minor',sections=BASE['sections'],tracks=TRACKS,
  audio_status='Instrumental + instrument-voiced topline only. Singing generation blocked by paid_plan_required.'),indent=2)+'\n',encoding='utf-8')

def edge(x,attack=.005,release=.025):
    a=min(len(x)//2,int(attack*SR));r=min(len(x)//2,int(release*SR))
    if a:x[:a]*=np.linspace(0,1,a)
    if r:x[-r:]*=np.linspace(1,0,r)
    return x.astype(np.float32)

def pitched(kind,note,duration):
    t=np.arange(max(10,round(duration*SR)))/SR;f=440*2**((note-69)/12);p=2*np.pi*f*t
    if kind=='pad':
        x=(np.sin(p)+.32*np.sin(p*1.002)+.18*np.sin(2*p)+.055*np.sin(3*p))
        x*=np.minimum(1,t/.12)*np.exp(-t/4.5)
        return edge(x,.06,.12)
    if kind=='pluck':
        x=np.sin(p+1.2*np.sin(p*2)*np.exp(-t/0.05))*np.exp(-t/.28)
        x+=.18*np.sin(2*p)*np.exp(-t/.08)
        return edge(x,.002,.03)
    if kind=='bass':
        # Audible upper harmonics retain the bass line on small speakers.
        x=np.sin(p+.025*np.sin(2*np.pi*3*t))+.23*np.sin(2*p)+.08*np.sin(3*p)
        x=np.tanh(1.4*x)*np.exp(-t/1.4)
        return edge(x,.005,.06)
    if kind=='bell':
        x=(np.sin(p)+.22*np.sin(2*p)+.10*np.sin(3.99*p)*np.exp(-t/.13))*np.exp(-t/1.1)
        return edge(x,.007,.035)
    # Explicitly an electric-piano guide, not a simulated singer.
    x=np.sin(p+.6*np.sin(2*p)*np.exp(-t/.08))+.13*np.sin(2*p)
    x*=np.exp(-t/1.05)
    return edge(x,.008,.032)

def drum(note):
    seconds={36:.42,38:.21,42:.075}.get(note,.2)
    t=np.arange(round(seconds*SR))/SR
    noise=RNG.normal(0,1,len(t));hp=np.diff(noise,prepend=0)
    if note==36:
        freq=48+130*np.exp(-t/.018)
        x=np.sin(2*np.pi*np.cumsum(freq)/SR)*np.exp(-t/.095)
        x+=.12*hp*np.exp(-t/.004)
    elif note==38:
        body=np.sin(2*np.pi*185*t)*np.exp(-t/.033)
        burst=sum(np.exp(-np.maximum(0,t-d)/.024)*(t>=d) for d in (0,.009,.018))
        x=.21*hp*burst+.25*body
    else:
        x=.15*hp*np.exp(-t/.017)
        x+=.05*(np.sin(2*np.pi*5830*t)+np.sin(2*np.pi*7919*t))*np.exp(-t/.02)
    return edge(x,.0006,.008)

def place(buffer,x,beat,gain,pan=0):
    start=round(beat*BEAT*SR);end=min(N,start+len(x));x=x[:end-start]*gain
    theta=(pan+1)*np.pi/4
    buffer[start:end,0]+=x*math.cos(theta);buffer[start:end,1]+=x*math.sin(theta)

def echo(signal,spacing,gains=(.18,.09,.045)):
    wet=np.zeros_like(signal)
    for j,g in enumerate(gains,1):
        delay=round(spacing*j*SR)
        wet[delay:]+=signal[:-delay,::-1 if j%2 else 1]*g
    return wet

def room(signal,level=.18):
    wet=np.zeros_like(signal)
    delays=[.039,.071,.113,.173,.229,.311,.419,.557,.683,.811,1.013,1.271]
    for i,d in enumerate(delays):
        k=round(d*SR);gain=level*math.exp(-d/0.54)/2.4
        wet[k:]+=signal[:-k,::-1 if i%2 else 1]*gain
    return wet

print('Rendering original instrumental...',flush=True)
bed=np.zeros((N,2),np.float32)
for name,kind,gain in [('harmony','pad',.043),('plucked_keys','pluck',.105)]:
    for e in TRACKS[name]:
        pan=(-.45 if e['note']%2 else .45) if kind=='pad' else (.3 if int(e['beat'])%2 else -.3)
        place(bed,pitched(kind,e['note'],e['duration']*BEAT+.2),e['beat'],gain*e['velocity']/64,pan)
bed+=room(bed,.30)+echo(bed,BEAT*.75,(.12,.045))
duck=np.ones(N,np.float32)
drums=np.zeros((N,2),np.float32)
for e in TRACKS['drum_guide']:
    gain=.43 if e['note']==36 else (.42 if e['note']==38 else .30)
    pan=0 if e['note']!=42 else .28
    place(drums,drum(e['note']),e['beat'],gain*e['velocity']/90,pan)
    if e['note']==36:
        start=round(e['beat']*BEAT*SR);length=min(round(.26*SR),N-start)
        duck[start:start+length]*=1-.40*np.exp(-np.arange(length)/(SR*.07))
bed*=duck[:,None]
bass=np.zeros((N,2),np.float32)
for e in TRACKS['bass_guide']:
    section=section_at(e['beat'])
    gain=.20 if section not in ('Intro','Bridge','Outro') else .055
    place(bass,pitched('bass',e['note'],e['duration']*BEAT),e['beat'],gain*e['velocity']/75)
bass*=duck[:,None]
instrumental=bed+bass+drums
del bed,bass,drums,duck

guide=np.zeros((N,2),np.float32)
for name,kind,gain in [('male_topline','lead',.13),('female_sample_guide','bell',.12)]:
    for e in TRACKS[name]:
        section=section_at(e['beat'])
        g=gain*(.85 if section.startswith('Verse') else 1)
        place(guide,pitched(kind,e['note'],e['duration']*BEAT+.08),e['beat'],g*e['velocity']/80,0 if kind=='lead' else -.15)
guide+=room(guide,.22)+echo(guide,BEAT*.75,(.105,.04))

def finish(x):
    x=np.tanh(x*1.10)
    x*=.87/max(.87,float(np.max(np.abs(x))))
    fade=round(2*SR);x[-fade:]*=np.linspace(1,0,fade,dtype=np.float32)[:,None]
    return x

def write_wav(name,x):
    assert np.isfinite(x).all()
    peak=float(np.max(np.abs(x)));rms=float(np.sqrt(np.mean(x*x,dtype=np.float64)))
    assert peak<1
    pcm=(np.clip(x,-1,1)*32767).astype('<i2')
    path=ROOT/name
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
    with wave.open(str(path),'rb') as f:
        assert f.getnframes()==len(x) and f.getframerate()==SR
    return dict(file=name,seconds=round(len(x)/SR,3),peak_dbfs=round(20*np.log10(max(peak,1e-9)),2),
                rms_dbfs=round(20*np.log10(max(rms,1e-9)),2),clipped_samples=0,sha256=hashlib.sha256(path.read_bytes()).hexdigest())

reports=[]
inst=finish(instrumental.copy())
reports.append(write_wav('DONT-HANG-UP-v2-INSTRUMENTAL.wav',inst))
del inst
mix=finish(instrumental+guide)
reports.append(write_wav('DONT-HANG-UP-v2-MELODY-GUIDE-NO-VOCALS.wav',mix))
preview=mix[:round(80*BEAT*SR)].copy()
preview[-round(.4*SR):]*=np.linspace(1,0,round(.4*SR),dtype=np.float32)[:,None]
reports.append(write_wav('DONT-HANG-UP-v2-HOOK-PREVIEW-NO-VOCALS.wav',preview))
verification=dict(status='passed',bpm=BPM,bars=100,topline_events=len(ROWS),midi_tracks=len(chunks),
                  verse_lyric_alignment='passed',same_pitch_overlaps=0,files=reports,
                  vocal_generation=dict(status='blocked',reason='Runway paid_plan_required',task_created=False),
                  limitations=['Instrument timbres represent vocal notes; no sung audio exists.',
                               'Numerical audio checks do not establish perceived musical quality.',
                               'No reference audio was sampled or transcribed.'])
(ROOT/'VERIFICATION.json').write_text(json.dumps(verification,indent=2)+'\n',encoding='utf-8')
print(json.dumps(verification,indent=2),flush=True)
