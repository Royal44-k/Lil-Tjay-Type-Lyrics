"""Render an original eight-bar topline and instrumental sketch, without samples."""
from pathlib import Path
import csv
import json
import math
import struct
import wave
import numpy as np

OUT = Path(__file__).resolve().parent
SR = 44100
BPM = 72  # Render on the half-time grid; MIDI and CSV export at 144 BPM.
SPB = 60 / BPM
PPQ = 480
END_BEAT = 32
DURATION = END_BEAT * SPB + 2.0
SIZE = math.ceil(DURATION * SR)
RNG = np.random.default_rng(14411)

# Each syllable has its own new note; onset/duration are quarter-note beats.
LINES = [
    ('Still got me Still got me'.split(), [(0,73,.5),(.5,71,.25),(.75,69,1),(2,66,.5),(2.5,68,.25),(2.75,69,.75)]),
    ('New scars same heart un- der- neath'.split(), [(0,66,.5),(.5,69,.5),(1,73,.5),(1.5,71,.75),(2.25,69,.25),(2.5,68,.25),(2.75,66,1)]),
    ('Whole world wants a piece wants a piece of me'.split(), [(0,69,.25),(.25,73,.5),(.75,71,.25),(1,69,.25),(1.25,68,.75),(2,69,.25),(2.25,68,.25),(2.5,66,.5),(3,64,.25),(3.25,66,.625)]),
    ("They don't get it all I still got me".split(), [(0,68,.25),(.25,68,.25),(.5,71,.25),(.75,69,.25),(1,68,.75),(1.75,64,.25),(2,66,.5),(2.5,64,.25),(2.75,61,.875)]),
    ('Still got me Still got me'.split(), [(0,73,.5),(.5,71,.25),(.75,69,1),(2,66,.5),(2.5,68,.25),(2.75,69,.75)]),
    ('Got my eyes up high got my roots down deep'.split(), [(.25,66,.25),(.5,68,.25),(.75,69,.5),(1.25,71,.25),(1.5,73,.5),(2,71,.25),(2.25,69,.25),(2.5,68,.25),(2.75,66,.25),(3,64,.875)]),
    ('If it all falls down let it fall on beat'.split(), [(0,64,.25),(.25,66,.25),(.5,69,.5),(1,68,.5),(1.5,66,.5),(2,64,.25),(2.25,66,.25),(2.5,69,.5),(3,68,.25),(3.25,66,.625)]),
    ('Lost a lot of shit but I still got me'.split(), [(0,68,.25),(.25,66,.25),(.5,64,.25),(.75,66,.25),(1,68,.75),(1.75,71,.25),(2,68,.25),(2.25,66,.5),(2.75,64,.25),(3,66,.875)]),
]
CHORDS = [(38,[54,57,61,62]), (45,[57,59,61,64]), (42,[57,61,64,68]), (40,[52,54,59,64])]
STEMS = {name:np.zeros((SIZE,2),dtype=np.float64) for name in ['lead','keys','pluck','bass','drums']}
EVENTS = {name:[] for name in STEMS}

def place(name, signal, beat, pan=0.0, gain=1.0):
    start = int(round(beat * SPB * SR))
    end = min(SIZE,start+len(signal))
    n = end-start
    if n <= 0:
        return
    angle = (pan + 1) * np.pi / 4
    STEMS[name][start:end,0] += signal[:n]*gain*np.cos(angle)
    STEMS[name][start:end,1] += signal[:n]*gain*np.sin(angle)

def tone(note, duration, timbre):
    sec = duration*SPB
    tail = .25 if timbre == 'bass' else .55
    t = np.arange(int((sec+tail)*SR))/SR
    freq = 440*2**((note-69)/12)
    gate = np.minimum(t/.012,1)*np.exp(-np.maximum(t-sec,0)/(.055 if timbre=='bass' else .13))
    if timbre == 'lead':
        phase = 2*np.pi*freq*t + .018*np.sin(2*np.pi*5.1*t)*np.minimum(t/.35,1)
        s = np.sin(phase)+.26*np.sin(phase*2)*np.exp(-t*4)+.07*np.sin(phase*3)
        s *= gate*(.72+.28*np.exp(-t*5))
    elif timbre == 'keys':
        phase = 2*np.pi*freq*t
        s = (np.sin(phase+.6*np.sin(phase*2)*np.exp(-t*3))+.18*np.sin(phase*3))*np.exp(-t*1.3)*gate
    elif timbre == 'pluck':
        phase = 2*np.pi*freq*t
        s = sum((.58**(k-1))*np.sin(k*phase)*np.exp(-t*(2+k)) for k in range(1,5))*gate
    else:
        phase = 2*np.pi*(freq*t + freq*.15*.018*(1-np.exp(-t/.018)))
        s = np.tanh(1.45*(np.sin(phase)+.19*np.sin(phase*2)))*np.exp(-t*.4)*gate
    return s

def pitched(name,note,beat,duration,velocity=75,pan=0,lyric=''):
    EVENTS[name].append((beat,duration,note,velocity,lyric))
    amps = {'lead':.20,'keys':.07,'pluck':.07,'bass':.26}
    place(name,tone(note,duration,name),beat,pan,amps[name]*(velocity/90))

def drum(note,beat,velocity):
    EVENTS['drums'].append((beat,.12,note,velocity,''))
    amp = velocity/100
    if note==36:
        t=np.arange(int(SR*.55))/SR
        phase=2*np.pi*(46*t+95*.02*(1-np.exp(-t/.02)))
        s=np.sin(phase)*np.exp(-t*10)+RNG.standard_normal(len(t))*.07*np.exp(-t*160)
        place('drums',s,beat,0,.34*amp)
    elif note==38:
        t=np.arange(int(SR*.26))/SR
        noise=RNG.standard_normal(len(t))
        noise=np.concatenate(([0],np.diff(noise)))*.45
        s=(noise*.75+np.sin(2*np.pi*185*t)*.28)*np.exp(-t*19)
        place('drums',s,beat,-.05,.22*amp)
    else:
        dur=.16 if note==46 else .06
        t=np.arange(int(SR*dur))/SR
        noise=RNG.standard_normal(len(t))
        s=np.concatenate(([0],np.diff(noise)))*np.exp(-t*(28 if note==46 else 80))
        place('drums',s,beat,.25,.035*amp)

rows=[]
for bar,(text,notes) in enumerate(LINES):
    assert len(text)==len(notes),(bar,text)
    for syllable,(onset,note,duration) in zip(text,notes):
        assert 0 <= onset and onset+duration <= 4.0001
        pitched('lead',note,bar*4+onset,duration*.92,84,0,syllable)
        pitch_names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        rows.append({'hook_line':bar+1,'bar_144_bpm':bar*2+int(onset//2)+1,'lyric':syllable,'start_beat_in_bar_144_bpm':(onset*2)%4,'duration_beats_144_bpm':duration*2,'pitch':pitch_names[note%12]+str(note//12-1),'midi_note':note})

for bar in range(8):
    root,chord=CHORDS[bar%4]
    for j,note in enumerate(chord):
        pitched('keys',note,bar*4+j*.012,3.65,58,-.25+j*.15)
    for idx,offset in enumerate([0,.75,1.5,2.75,3.25]):
        pitched('pluck',chord[[0,2,1,3,2][idx]]+12,bar*4+offset,.45,53,-.5 if idx%2==0 else .5)
    for offset,dur,vel in [(0,1.25,89),(1.75,.5,67),(2.5,1.25,84)]:
        pitched('bass',root if root<42 else root-12,bar*4+offset,dur,vel,0)
    for offset,vel in [(0,98),(1.75,70),(2.5,89)]:
        drum(36,bar*4+offset,vel)
    if bar%2:
        drum(36,bar*4+3.5,62)
    for offset in [1,3]:
        drum(38,bar*4+offset,84)
    for step in range(16):
        drum(42,bar*4+step*.25,48 if step%2 else 70)
    if bar in [3,7]:
        for offset in [3.5+1/12,3.5+1/6,3.75,3.875]:
            drum(42,bar*4+offset,43)
    if bar in [1,5]:
        drum(46,bar*4+2.75,55)

# Short stereo echoes for the tonal voices; every sound is synthesized here.
for name,mix in [('lead',.12),('keys',.10),('pluck',.15)]:
    dry=STEMS[name].copy()
    for delay,amount in [(SPB*.75,mix),(.11,mix*.55),(.23,mix*.30)]:
        shift=int(delay*SR)
        STEMS[name][shift:]+=dry[:-shift,::-1]*amount

backing=sum(STEMS[n] for n in ['keys','pluck','bass','drums'])
demo=backing+STEMS['lead']
scale=.88/max(np.max(np.abs(demo)),np.max(np.abs(backing)))

def write_wav(filename,data):
    data=data*scale
    fade=int(.4*SR)
    data[-fade:]*=np.linspace(1,0,fade)[:,None]
    assert np.isfinite(data).all()
    pcm=np.round(data*32767).astype('<i2')
    with wave.open(str(OUT/filename),'wb') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes(pcm.tobytes())
    return {'file':filename,'seconds':round(len(data)/SR,3),'peak':round(float(np.max(np.abs(data))),4),'rms':round(float(np.sqrt(np.mean(data**2))),4)}

def varlen(value):
    out=[value&127]
    value>>=7
    while value:
        out.insert(0,(value&127)|128)
        value>>=7
    return bytes(out)

def meta(kind,payload):
    return b'\xff'+bytes([kind])+varlen(len(payload))+payload

def midi_track(events):
    data=b''; previous=0
    for tick,order,event in sorted(events,key=lambda e:(e[0],e[1])):
        data+=varlen(tick-previous)+event
        previous=tick
    data+=varlen(max(0,END_BEAT*2*PPQ-previous))+b'\xff\x2f\x00'
    return b'MTrk'+struct.pack('>I',len(data))+data

tempo=int(round(60000000/(BPM*2)))
chunks=[midi_track([(0,0,meta(3,b'STILL GOT ME - original English hook, 144 BPM')),(0,1,meta(0x51,tempo.to_bytes(3,'big'))),(0,2,meta(0x58,bytes([4,2,24,8]))),(0,3,meta(0x59,bytes([3,1])))])]
for name,channel,program in [('lead',0,0),('keys',1,4),('pluck',2,24),('bass',3,38),('drums',9,0)]:
    ev=[(0,0,meta(3,name.encode())),(0,1,bytes([0xc0|channel,program]))]
    for beat,dur,note,vel,lyric in EVENTS[name]:
        tick=round(beat*PPQ*2)
        if lyric:
            ev.append((tick,1,meta(5,lyric.encode('utf-8'))))
        ev.append((tick,3,bytes([0x90|channel,note,vel])))
        ev.append((round((beat+dur)*PPQ*2),2,bytes([0x80|channel,note,0])))
    chunks.append(midi_track(ev))
(OUT/'still-got-me-hook.mid').write_bytes(b'MThd'+struct.pack('>IHHH',6,1,len(chunks),PPQ)+b''.join(chunks))
with (OUT/'still-got-me-hook-notes.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
report={'bpm':BPM*2,'half_time_bpm':BPM,'bars':16,'lead_syllables':len(rows),'audio':[write_wav('still-got-me-hook-demo.wav',demo),write_wav('still-got-me-hook-backing.wav',backing)],'midi_tracks':len(chunks),'note_range':'C#4-C#5','status':'Timing, syllable alignment, finite waveform and PCM range checked; no vocal performance or listening review.'}
(OUT/'still-got-me-render-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
