"""Original compositions. Beat units are quarter notes; C4 = MIDI 60."""
def phr(words, notes, offset, starts=None, durations=None):
    words,notes=words.split('|'),notes.split()
    assert len(words)==len(notes),(words,notes)
    n=len(words)
    # Reserve a real breath at the end of every two-bar phrase.
    starts=starts if starts is not None else ([i*.5 for i in range(n-1)]+[max((n-1)*.5,5.5)])
    durations=durations if durations is not None else [min(.38,starts[i+1]-starts[i]-.05) for i in range(n-1)]+[min(1.3,7.25-starts[-1])]
    assert len(starts)==len(durations)==n
    return [dict(text=w,note=p,start=offset+s,duration=d,velocity=87) for w,p,s,d in zip(words,notes,starts,durations)]

HOOKS={
'DBE01':(
 phr('One|of|one|one|of|one','G#3 B3 C#4 E4 D#4 C#4',0,[0,.75,1,4,4.75,5],[.6,.2,1.8,.6,.2,1.8])+
 phr("They|can't|put|a|num|ber|on|what|I've|be|come",'C#4 E4 D#4 C#4 B3 C#4 E4 F#4 E4 D#4 C#4',8)+
 phr('One|of|one|let|it|run','G#3 B3 C#4 E4 F#4 E4',16,[0,.75,1,4,4.75,5],[.6,.2,1.8,.6,.2,1.8])+
 phr("I|was|do|ing|too|much|now|it|ain't|e|nough",'B3 D#4 F#4 E4 D#4 C#4 D#4 F#4 E4 D#4 B3',24)),
'DBE02':(
 phr('Af|ter|the|flash|af|ter|the|flash','F#4 E4 C#4 A3 C#4 B3 A3 F#3',0,[0,.5,.75,1.5,4,4.5,4.75,5.5],[.35,.2,.35,1.7,.35,.2,.35,1.5])+
 phr('Who|am|I|when|the|room|goes|black','A3 C#4 D4 E4 F#4 E4 C#4 D4',8)+
 phr('All|of|that|light|none|of|it|lasts','C#4 B3 A3 E4 D4 C#4 B3 A3',16)+
 phr("You|know|my|name|do|you|know|where|I'm|at",'B3 C#4 E4 G#4 F#4 E4 C#4 B3 G#3 B3',24)),
'DBE03':(
 phr("Don't|make|it|cool|don't|make|it|cool",'E4 G#4 F#4 E4 G#4 F#4 E4 C#4',0,[0,.5,1,1.5,4,4.5,5,5.5],[.35,.35,.35,1.8,.35,.35,.35,1.5])+
 phr('I|like|you|bet|ter|when|you|tell|the|truth','E4 G#4 A4 G#4 E4 C#4 E4 G#4 E4 C#4',8)+
 phr("Don't|play|it|smooth|don't|play|it|smooth",'F#4 A4 G#4 F#4 A4 G#4 F#4 E4',16,[0,.5,1,1.5,4,4.5,5,5.5],[.35,.35,.35,1.8,.35,.35,.35,1.5])+
 phr('Say|you|want|me|I|can|want|you|too','G#4 F#4 E4 C#4 D4 F#4 E4 D4 C#4',24)),
'DBE04':(
 phr('Side|door|side|door','D4 D4 C4 A3',0,[0,1.5,4,5.5],[.7,1.4,.7,1.4])+
 phr('Knock|first|like|you|did|be|fore','A3 Bb3 D4 F4 D4 C4 Bb3',8,[0,1,2.5,3,4,4.5,5.5],[.7,.9,.35,.7,.35,.7,1.3])+
 phr('Same|love|new|lock','G3 Bb3 D4 C4',16,[0,1.5,4,5.5],[.7,1.4,.7,1.4])+
 phr('We|can|still|be|close|with|the|cam|ras|off','A3 C#4 D4 E4 G4 E4 D4 C#4 Bb3 A3',24)),
'DBE05':(
 phr('Wear|it|out|wear|it|out','D4 F4 G4 F4 D4 Bb3',0,[0,.75,1.5,4,4.75,5.5],[.6,.4,1.5,.6,.4,1.5])+
 phr("You'd|hate|to|see|it|hang|ing|in|an|emp|ty|house",'Eb4 G4 F4 Eb4 D4 Eb4 G4 F4 Eb4 G4 F4 G4',8)+
 phr('Take|it|down|town|let|it|catch|some|rain','Eb4 G4 F4 Eb4 D4 C4 D4 Eb4 G4',16)+
 phr('I|can|keep|you|close|and|let|the|co|lor|change','D4 F#4 A4 G4 F#4 E4 D4 C4 D4 F#4 A4',24)),
'DBE06':(
 phr('Good|on|me|good|on|me','G4 E4 B3 G4 E4 B3',0,[0,.5,1,3.5,4,4.5],[.35,.35,1.4,.35,.35,2])+
 phr('That|lit|tle|bit|of|weird|looks|good|on|me','E4 G4 E4 D4 C4 E4 G4 E4 D4 C4',8)+
 phr('Too|much|wait|till|you|see','B3 D4 G4 A4 G4 D4',16,[0,.5,2.5,3,3.5,5],[.35,1.3,.35,.35,1,1.5])+
 phr("I|don't|tone|it|down|it|looks|good|on|me",'F#4 A4 G4 F#4 E4 D4 E4 F#4 E4 D4',24)),
'DBE07':(
 phr('Dif|ferent|but|ex|cel|lent','Db4 C4 Ab3 F4 Eb4 Db4',0,[0,1.5,2.5,3.5,4.5,5],[1.2,.6,.5,.7,.35,1.6])+
 phr('I|can|put|my|whole|chest|in|it','Ab3 Bb3 C4 Eb4 Db4 C4 Bb3 Ab3',8)+
 phr('One|of|one|still|work|ing|on|it','Ab3 C4 Db4 F4 F4 Eb4 Db4 C4',16,[0,.75,1,2.5,3.5,4,4.5,5.5],[.6,.2,1.1,.7,.35,.35,.7,1.3])+
 phr("I|know|what|I|got|I|ain't|fi|nished|with|it",'Db4 Eb4 F4 Ab4 F4 Eb4 Db4 Bb3 Db4 F4 Gb4',24))
}

def inst(name,seq,program=0):
    return dict(name=name,program=program,notes=[dict(start=s,note=p,duration=d,velocity=v,text='') for s,p,d,v in seq])

SAMPLES=[
 dict(id='G01',title='Crooked Cuff',bpm=73,meter=4,bars=4,sf=4,minor=1,instrument='picked electric guitar',
  tracks=[inst('clean guitar source',[(0,'C#4',.7,72),(.75,'G#4',.6,66),(1.5,'B4',.7,76),(2.5,'E4',1,67),(4,'C#4',.7,73),(5,'E4',.7,67),(6,'G#4',1.3,70),(8,'B3',.7,70),(8.75,'E4',.7,66),(9.75,'G#4',.7,75),(11,'F#4',.7,69),(12,'B3',.7,68),(13,'F#4',.7,72),(14,'E4',1.5,65)],27)]),
 dict(id='P02',title='Empty Hall',bpm=66,meter=4,bars=4,sf=3,minor=1,instrument='felt piano',
  tracks=[inst('piano right hand',[(0,'C#5',.7,58),(1,'A4',.7,53),(2,'F#4',1.5,50),(4,'A4',.7,59),(5.5,'F#4',.7,54),(6.5,'E4',1,49),(8,'C#4',.7,54),(9,'E4',.7,60),(10,'G#4',1.5,51),(12,'B3',.7,55),(13,'E4',.7,52),(14,'C#4',1.5,48)]),
          inst('piano left hand',[(0,'F#2',3.5,52),(4,'D2',3.5,51),(8,'C#2',3.5,49),(12,'E2',3.5,50)])]),
 dict(id='EP03',title='Eighty Percent',bpm=104,meter=4,bars=4,sf=3,minor=0,instrument='electric piano',
  tracks=[inst('electric piano right hand',[(.5,'C#4',.5,70),(1.5,'E4',.5,77),(2.5,'B4',.6,67),(4.5,'E4',.5,68),(5.5,'G#4',.5,76),(6.5,'B4',.6,66),(8.5,'F#4',.5,72),(9.5,'A4',.5,75),(10.5,'E5',.6,69),(12.5,'G#4',.5,70),(13.5,'D5',.5,74),(14.5,'C#5',.6,65)],4),
          inst('electric piano left hand',[(0,'A2',1,58),(3,'E3',.5,50),(4,'C#3',1,57),(7,'G#2',.5,49),(8,'D3',1,61),(11,'A2',.5,51),(12,'E3',1,58),(15,'B2',.5,50)],4)]),
 dict(id='V04',title='Latch',bpm=142,meter=4,bars=2,sf=-1,minor=1,instrument='violin short bow',
  tracks=[inst('solo violin short bow',[(0,'D5',.4,78),(.75,'A4',.25,63),(1.5,'F5',.4,74),(2.5,'E5',.25,62),(3,'D5',.4,69),(4,'Bb4',.4,74),(4.75,'F5',.25,62),(5.5,'A5',.4,77),(6.5,'F5',.25,64),(7,'D5',.4,70)],40)]),
 dict(id='P05',title='Worn Sleeve',bpm=84,meter=4,bars=4,sf=-2,minor=1,instrument='upright piano',
  tracks=[inst('piano right hand',[(0,'D4',.7,69),(1,'G4',.7,72),(2,'F4',1.5,63),(4,'Eb4',.7,64),(5,'G4',.7,70),(6,'Bb4',1.5,65),(8,'G4',.7,63),(9,'Eb4',.7,60),(10,'D4',1.5,62),(12,'F#4',.7,70),(13,'A4',.7,74),(14,'D4',1.5,60)]),
          inst('piano left hand',[(0,'G2',3.5,55),(4,'Eb2',3.5,51),(8,'C2',3.5,53),(12,'D2',3.5,56)])]),
 dict(id='V05',title='Loose Thread',bpm=84,meter=4,bars=4,sf=-2,minor=1,instrument='solo violin answers',
  tracks=[inst('violin response',[(2,'D5',.7,61),(3,'Bb4',.7,54),(6,'G4',.7,57),(7,'Bb4',.7,60),(10,'Eb5',.7,65),(11,'D5',.7,58),(14,'C5',.7,59),(15,'A4',.7,53)],40)]),
 dict(id='SYN06',title='Lime Lining',bpm=152,meter=4,bars=2,sf=1,minor=1,instrument='gated saw synth',
  tracks=[inst('synth rhythmic cell',[(0,'E5',.35,95),(.5,'B4',.25,75),(1.5,'G5',.35,90),(2.5,'F#5',.25,72),(3.5,'E5',.25,82),(4,'C5',.35,89),(4.75,'E5',.25,74),(5.5,'G5',.35,94),(6.5,'B5',.25,73),(7.5,'G5',.25,84)],81)]),
 dict(id='P07',title='Blue Ink',bpm=70,meter=4,bars=4,sf=-5,minor=0,instrument='warm piano',
  tracks=[inst('piano right hand',[(0,'Ab3',.5,68),(.5,'Db4',.5,72),(1,'F4',.7,77),(2.5,'Eb4',1,64),(4,'Ab3',.5,66),(4.5,'C4',.5,72),(5,'Eb4',.7,74),(6.5,'Ab4',1,68),(8,'Ab3',.5,69),(8.5,'Db4',.5,73),(9,'F4',.7,76),(10.5,'C4',1,63),(12,'Bb3',.5,67),(12.5,'Db4',.5,73),(13,'F4',.7,75),(14.5,'Ab4',1,66)]),
          inst('piano left hand',[(0,'Db2',3.5,59),(4,'C2',3.5,53),(8,'Bb1',3.5,56),(12,'Gb2',3.5,55)])]),
 dict(id='VC01',title='One of one original cell',bpm=146,meter=4,bars=1,sf=4,minor=1,instrument='vocal composition guide, no voice recorded',
  tracks=[dict(name='three-note original vocal cell',program=0,notes=HOOKS['DBE01'][:3])])
]
