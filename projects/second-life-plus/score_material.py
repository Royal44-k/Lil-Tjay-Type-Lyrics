"""Original pitched hooks and instrumental source sketches, not recorded audio.
All offsets/durations are quarter-note beats. C4 = MIDI 60.
"""


def phr(words, notes, offset, starts=None, durations=None):
    words, notes = words.split('|'), notes.split()
    n = len(words)
    assert n == len(notes), (words, notes)
    patterns = {
        4: ([0, 1, 3, 4], [.7, 1.4, .7, 2.8]),
        5: ([0, .75, 1.25, 3, 4.5], [.6, .35, 1.1, 1.1, 2]),
        6: ([0, .5, 1, 3, 3.5, 4], [.35, .35, 1.3, .35, .35, 2.5]),
        7: ([0, .5, 1, 2, 3, 3.5, 4.5], [.35, .35, .7, .7, .35, .65, 2]),
        8: ([0, .5, 1, 2, 2.5, 3, 3.5, 4.5], [.35, .35, .7, .35, .35, .35, .7, 2]),
        9: ([0, .5, 1, 1.5, 2.5, 3, 3.5, 4, 5], [.35, .35, .35, .7, .35, .35, .35, .7, 1.8]),
        10: ([0, .5, 1, 1.5, 2, 2.5, 3, 4, 4.5, 5.5], [.35, .35, .35, .35, .35, .35, .7, .35, .7, 1.4]),
        11: ([0, .25, .5, 1, 1.5, 2, 2.5, 3, 4, 4.5, 5.5], [.2,.2,.35,.35,.35,.35,.35,.7,.35,.7,1.4]),
        12: ([0,.25,.5,1,1.5,1.75,2,2.5,3,4,4.5,5.5], [.2,.2,.35,.35,.2,.2,.35,.35,.7,.35,.7,1.4]),
    }
    default_starts, default_durations = patterns[n]
    starts, durations = starts or default_starts, durations or default_durations
    assert len(starts) == len(durations) == n
    return [dict(text=w,note=p,start=offset+t,duration=d,velocity=86)
            for w,p,t,d in zip(words,notes,starts,durations)]


HOOKS = {}
HOOKS['SLP01'] = (
    phr('No|re|ceipt|no|re|turn','F#3 F#3 C#4 C#4 B3 A3',0,
        [0,.5,1,3,3.5,4],[.35,.35,1.25,.35,.35,2.5]) +
    phr('Put|our|names|be|side|the|work','A3 B3 C#4 E4 C#4 B3 A3',8) +
    phr('You|said|we|when|the|rent|came|due','A3 A3 C#4 B3 A3 B3 C#4 E4',16) +
    phr("Don't|say|I|when|the|mon|ey|moves",'G#3 B3 C#4 B3 G#3 F#3 G#3 C#4',24)
)
HOOKS['SLP02'] = (
    phr('I|vo|ry|hours|no|bo|dy|claps','F4 E4 D4 F4 E4 D4 C4 D4',0,
        [0,.75,1,1.5,3,3.75,4,4.5],[.6,.2,.3,1.2,.6,.2,.3,2]) +
    phr('I|let|the|last|note|find|its|way|back','F4 G4 F4 D4 C4 D4 F4 E4 D4',8) +
    phr('You|ne|ver|said|sor|ry|I|still|hear|you|laugh','Bb3 D4 C4 D4 F4 E4 D4 C4 Bb3 A3 Bb3',16) +
    phr('Both|things|can|fit|in|the|song|that|I|have','C#4 E4 D4 C#4 Bb3 A3 G3 A3 C#4 E4',24)
)
fast_anchor = lambda off: phr('Fast|for|ward|fast|for|ward|wait|wait|wait',
    'A4 A4 F4 A4 A4 F4 G4 F4 D4',off,
    [0,.25,.5,1.5,1.75,2,3.5,4.5,5.5],[.2,.2,.65,.2,.2,.65,.55,.55,.55])
HOOKS['SLP03'] = (fast_anchor(0) +
    phr('You|got|out|of|town|I|still|work|this|place','F4 A4 G4 F4 E4 F4 E4 D4 C4 D4',8) +
    fast_anchor(16) +
    phr('Some|bo|dy|stays|up|so|you|get|a|way','D4 E4 G4 E4 D4 E4 G4 E4 D4 E4',24)
)
HOOKS['SLP04'] = (
    phr('Wrong|foot|right|time','G3 Bb3 D4 D4',0) +
    phr('Let|the|whole|room|catch|this|slide','Bb3 C4 D4 F4 D4 C4 Bb3',8) +
    phr('Coun|ter|step|switch|sides','D4 C4 Bb3 C4 D4',16) +
    phr('If|you|came|to|watch|you|can|get|in|side','A3 C4 D4 F#4 D4 C4 A3 F#3 A3 D4',24)
)
HOOKS['SLP05'] = (
    phr('Stay|for|the|qui|et|qui|et','C#4 E4 F#4 G#4 F#4 E4 C#4',0,
        [0,.75,1.25,2,2.75,4,4.75],[.55,.35,.55,.6,.9,.6,1.8]) +
    phr('Let|me|fin|ish|what|I|say','A3 C#4 E4 C#4 B3 A3 G#3',8) +
    phr('We|can|leave|a|lit|tle|dis|tance','B3 C#4 D4 F#4 E4 D4 C#4 B3',16) +
    phr('With|out|lea|ving|things|this|way','B3 C#4 D4 C#4 B3 A3 F#3',24)
)
HOOKS['SLP06'] = (
    phr('Soft|land|ing|take|your|time','Bb3 Eb4 D4 C4 Bb3 G3',0) +
    phr("Tell|me|what|you|want|I'll|tell|you|mine",'Bb3 C4 D4 G4 F4 D4 C4 Bb3 G3',8) +
    phr('Soft|land|ing|pull|me|near','C4 Eb4 D4 C4 Bb3 Ab3',16) +
    phr('We|got|no|where|else|to|be|but|here','Bb3 C4 Eb4 D4 C4 Bb3 Ab3 Bb3 Eb4',24)
)
HOOKS['SLP07'] = (
    phr('Last|train|first|light','E4 G4 A4 G4',0) +
    phr('I|can|love|this|place|and|leave|to|night','G4 F#4 E4 G4 A4 G4 E4 D4 E4',8) +
    phr('Last|train|first|light','E4 G4 A4 G4',16) +
    phr("There's|a|life|I|have|n't|met|on|the|oth|er|side",'A4 G4 A4 G4 E4 D4 E4 G4 A4 G4 E4 D4',24)
)


def inst(sequence, program=0, name='instrument', duration=.8):
    """Sequence is (start, note, duration[, velocity])."""
    return dict(name=name, program=program, notes=[dict(start=t,note=n,duration=d,velocity=v[0] if v else 72,text='')
                                                 for t,n,d,*v in sequence])


SAMPLES = [
 dict(id='P01R',title='Ledger Keys',bpm=140,meter=4,bars=2,key_sf=3,key_minor=1,
      tracks=[inst([(0,'F#3',.5),(1,'A3',.25),(1.5,'C#4',.25),(2.5,'E4',.25),(3,'C#4',.5),
                    (4,'D4',.5),(5,'A3',.25),(5.5,'F#3',.25),(6.5,'C#4',.25),(7,'A3',.5)],name='short piano source')]),
 dict(id='STR01R',title='Margin Notes',bpm=140,meter=4,bars=2,key_sf=3,key_minor=1,
      tracks=[inst([(1,'C#5',.25),(1.5,'E5',.25),(3,'F#5',.4),(5,'E5',.25),(5.5,'C#5',.25),(7,'A4',.4)],program=45,name='violin pizzicato source')]),
 dict(id='P02',title='Uneven Key',bpm=88,meter=4,bars=4,key_sf=-1,key_minor=1,
      tracks=[inst([(0,'F4',.75),(1,'E4',.5),(2,'D4',1.5),(4,'F4',.75),(5.5,'D4',.5),(6.5,'C4',1),
                    (8,'Bb3',.5),(9,'D4',.75),(10,'A3',1.5),(12,'C#4',.75),(13,'Bb3',.5),(14,'A3',1.5)],name='piano right hand'),
              inst([(0,'D2',1.5),(2,'A2',1.5),(4,'Bb1',1.5),(6,'F2',1.5),(8,'G1',1.5),(10,'D2',1.5),(12,'A1',1.5),(14,'E2',1.5)],name='piano left hand')]),
 dict(id='V02',title='Counter Waltz',bpm=108,meter=3,bars=4,key_sf=-2,key_minor=1,
      tracks=[inst([(0,'G4',.5),(0.5,'Bb4',.5),(1,'D5',.9),(2,'C5',.5),(2.5,'Bb4',.45),
                    (3,'G4',.5),(3.5,'Bb4',.5),(4,'Eb5',.9),(5,'D5',.5),(5.5,'C5',.45),
                    (6,'A4',.5),(6.5,'C5',.5),(7,'D5',.9),(8,'F#5',.8),
                    (9,'G5',.8),(10,'D5',.5),(10.5,'Bb4',.5),(11,'G4',.8)],program=40,name='solo violin; short bow attacks')]),
 dict(id='P03',title='Lamplight Keys',bpm=76,meter=4,bars=4,key_sf=-3,key_minor=0,
      tracks=[inst([(0,'Bb3',.5),(0.5,'Eb4',.5),(1,'F4',.5),(1.5,'G4',.8),(3,'D4',.8),
                    (4,'Bb3',.5),(4.5,'D4',.5),(5,'F4',.8),(6.5,'G4',1),
                    (8,'C4',.5),(8.5,'Eb4',.5),(9,'G4',.8),(10.5,'Bb4',1),
                    (12,'Ab4',.5),(12.5,'G4',.5),(13,'Eb4',.8),(14.5,'C4',1)],name='felt piano right hand'),
              inst([(0,'Eb2',3.5),(4,'G2',3.5),(8,'Ab2',3.5),(12,'Bb2',3.5)],name='felt piano left hand')]),
 dict(id='V03',title='Small Gestures',bpm=76,meter=4,bars=4,key_sf=-3,key_minor=0,
      tracks=[inst([(2.5,'G5',.25),(3,'Bb5',.25),(6.5,'D5',.25),(7,'F5',.25),
                    (10.5,'Eb5',.25),(11,'G5',.25),(14.5,'C5',.25),(15,'Eb5',.25)],program=45,name='violin pizzicato replies')]),
 dict(id='P04',title='Platform Window',bpm=78,meter=4,bars=4,key_sf=1,key_minor=1,
      tracks=[inst([(0,'E4',.5),(0.5,'F#4',.5),(1,'G4',.5),(1.5,'B4',.8),(3,'G4',.8),
                    (4,'E4',.5),(4.5,'G4',.5),(5,'B4',.5),(5.5,'C5',.8),(7,'G4',.8),
                    (8,'D4',.5),(8.5,'G4',.5),(9,'A4',.5),(9.5,'B4',.8),(11,'G4',.8),
                    (12,'D4',.5),(12.5,'E4',.5),(13,'G4',.5),(13.5,'A4',.8),(15,'D4',.8)],name='piano right hand'),
              inst([(0,'E2',3.5),(4,'C2',3.5),(8,'G2',3.5),(12,'D2',3.5)],name='piano left hand')]),
 dict(id='V04',title='Daybreak Answer',bpm=78,meter=4,bars=4,key_sf=1,key_minor=1,
      tracks=[inst([(1,'B4',1),(2,'A4',.5),(2.5,'G4',1),(5,'G4',1),(6,'E5',1.5),
                    (9,'D5',1),(10,'B4',1.5),(13,'A4',1),(14,'G4',.5),(14.5,'F#4',1)],program=40,name='solo violin; phrase-end replies')]),
]
