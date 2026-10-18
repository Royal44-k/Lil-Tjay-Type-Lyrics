"""Local standard-library music file utilities reused from this workspace. No runtime dependency on the earlier album."""
from pathlib import Path
import csv, json, re, struct, hashlib
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
PPQ=480

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

def canonical_words(text):
    return re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?",text.lower())

def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

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
