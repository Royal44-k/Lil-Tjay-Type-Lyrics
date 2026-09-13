"""Build explicit synthetic singing prototypes from public TTS voices and the original score.

No artist recordings, cloned identities, or artist-specific voice models are used.
WORLD preserves the source spectral envelope while changing pitch and vowel duration.
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'vocal_deps'))
import csv
import json
import re
import numpy as np
import soundfile as sf
import pyworld as pw
from scipy import signal, ndimage

SR = 24000
OUT_SR = 44100
FRAME = .005
BPM = 144
BEAT = 60 / BPM
RNG = np.random.default_rng(919144)

def normalize_word(word):
    return re.sub(r"[^a-z']", '', word.lower())

def get_score():
    rows = list(csv.DictReader((ROOT / 'still-got-me-hook-notes.csv').open(encoding='utf-8-sig')))
    notes = []
    for row in rows:
        start = ((int(row['bar_144_bpm'])-1)*4 + float(row['start_beat_in_bar_144_bpm'])) * BEAT
        notes.append(dict(word=row['lyric'], start=start, duration=float(row['duration_beats_144_bpm'])*BEAT,
                          midi=int(row['midi_note']), line=int(row['hook_line'])))
    groups = []
    for n in notes:
        if n['word'] == 'un-':
            groups.append(dict(word='underneath', notes=[n]))
        elif n['word'] in ('der-', 'neath'):
            groups[-1]['notes'].append(n)
        else:
            groups.append(dict(word=normalize_word(n['word']), notes=[n]))
    return groups

def source_analysis(gender):
    src, sr = sf.read(ROOT / f'vocal-{gender}-source.wav', dtype='float64')
    if src.ndim > 1:
        src = src.mean(axis=1)
    # The service labels MPEG audio .wav; retain the original and also decode a genuine PCM source.
    sf.write(ROOT / f'vocal-{gender}-source-pcm.wav', src, sr, subtype='PCM_16')
    src = signal.resample_poly(src, SR, sr)
    src = np.ascontiguousarray(src, dtype=np.float64)
    cache = ROOT / f'vocal-{gender}-world.npz'
    if cache.exists():
        data = np.load(cache)
        return {k:data[k] for k in data.files}
    raw, t = pw.dio(src, SR, f0_floor=65, f0_ceil=650, frame_period=5, allowed_range=.2)
    f0 = pw.stonemask(src, raw, t, SR)
    sp = pw.cheaptrick(src, f0, t, SR, fft_size=2048)
    ap = pw.d4c(src, f0, t, SR, fft_size=2048)
    # Keep a smoothed energy reference for locating a stable vowel, never for inventing missing words.
    energy = np.sqrt(np.maximum(0,ndimage.uniform_filter1d(src*src, int(.02*SR))))
    energy = np.interp(t, np.arange(len(src))/SR, energy)
    data = dict(f0=f0, t=t, sp=sp, ap=ap, energy=energy)
    np.savez_compressed(cache, **data)
    print(gender, 'source voiced frames', round(float((f0>0).mean()),3), flush=True)
    return data

def longest_voiced_run(mask):
    padded = np.r_[False, mask, False].astype(int)
    begin = np.flatnonzero(np.diff(padded)==1)
    end = np.flatnonzero(np.diff(padded)==-1)
    if len(begin) == 0:
        return None
    j = int(np.argmax(end-begin))
    return int(begin[j]), int(end[j]-1)

def warp_word(data, source_start, source_end, notes, octave, previous_midi, gender):
    base = notes[0]['start']
    duration = notes[-1]['start'] + notes[-1]['duration'] - base
    # Small releases preserve separation in the dense rap phrases.
    duration = max(.095, duration - .015)
    frames = max(8, int(round(duration / FRAME)))
    source_times = np.arange(source_start, source_end, FRAME)
    source_voice = np.interp(source_times, data['t'], (data['f0']>0).astype(float)) > .5
    run = longest_voiced_run(source_voice)
    dst = np.arange(frames)*FRAME
    if len(notes) == 3:
        # Underneath has three syllables; retain its consonant transitions and give 'neath' the long note.
        sd = source_end-source_start
        src_knots = np.array([source_start, source_start+.28*sd, source_start+.53*sd, source_end])
        dst_knots = np.array([0, notes[1]['start']-base, notes[2]['start']-base, duration])
        mapped = np.interp(dst, dst_knots, src_knots)
    elif run is not None and duration > source_end-source_start:
        a, b = run
        # Stretch the vowel nucleus rather than smearing the initial or final consonants.
        vs = source_times[a] + .15 * max(0, source_times[b]-source_times[a])
        ve = source_times[b] - .15 * max(0, source_times[b]-source_times[a])
        if ve-vs < .025:
            vs = source_times[a]
            ve = source_times[min(b+1,len(source_times)-1)]
        onset = min(vs-source_start, duration*.32)
        ending = min(source_end-ve, duration*.3)
        mapped = np.interp(dst, [0,onset,duration-ending,duration], [source_start,vs,ve,source_end])
    else:
        mapped = np.linspace(source_start, source_end, frames)
    pos = np.clip(mapped/FRAME, 0, len(data['t'])-1.001)
    lo = pos.astype(int)
    hi = lo+1
    frac = (pos-lo)[:,None]
    sp = data['sp'][lo]*(1-frac)+data['sp'][hi]*frac
    ap = data['ap'][lo]*(1-frac)+data['ap'][hi]*frac
    voiced = np.interp(mapped, data['t'], (data['f0']>0).astype(float)) > .45
    pitch = np.zeros(frames)
    prev = previous_midi + octave
    for note in notes:
        local = note['start']-base
        active = dst >= local
        since = np.maximum(0, dst-local)
        target = note['midi']+octave
        # Fast slides give a melodic-trap contour; a small late vibrato prevents frozen held vowels.
        cents = (prev-target)*100*np.exp(-since/.022)
        cents += (9 if gender=='female' else 7)*np.sin(2*np.pi*5.4*since)*np.clip((since-.18)/.22,0,1)
        pitch[active] = 440*2**((target-69+cents[active]/100)/12)
        prev = target
    pitch[~voiced] = 0
    # A small breath component, with the source's consonants and formants retained.
    if gender == 'female':
        high = np.linspace(0,1,sp.shape[1])
        ap[voiced] = np.minimum(.99,ap[voiced]+.035*high)
    return pitch, np.ascontiguousarray(sp), np.ascontiguousarray(ap), duration

def render_word(f0, sp, ap, gain=1):
    y = pw.synthesize(np.ascontiguousarray(f0),sp,ap,SR,frame_period=5)
    y -= np.mean(y)
    ramp = min(int(.009*SR),len(y)//3)
    y[:ramp] *= np.sin(np.linspace(0,np.pi/2,ramp))**2
    y[-ramp:] *= np.sin(np.linspace(np.pi/2,0,ramp))**2
    rms = np.sqrt(np.mean(y*y)) + 1e-8
    return y * min(3.5,.135/rms) * gain

def add(dest, mono, start, pan=0, gain=1):
    i = int(round(start*SR))
    if i < 0:
        mono=mono[-i:]
        i=0
    n = min(len(mono),len(dest)-i)
    if n <= 0:
        return
    a = (pan+1)*np.pi/4
    dest[i:i+n,0] += mono[:n]*np.cos(a)*gain
    dest[i:i+n,1] += mono[:n]*np.sin(a)*gain

def band(y, lo, hi):
    return signal.sosfilt(signal.butter(2,[lo,hi],btype='bandpass',fs=SR,output='sos'), y, axis=0)

def vocal_effects(dry, doubles, throws, gender):
    voice = dry+doubles
    voice = signal.sosfilt(signal.butter(2,110 if gender=='female' else 85,btype='highpass',fs=SR,output='sos'),voice,axis=0)
    # Gentle saturation and restrained presence keep the synthetic take legible in the existing arrangement.
    voice = np.tanh(voice*1.35)/1.35
    voice += .10*band(voice,1700,4000)
    sib=band(voice,5500,10500)
    sib_env=np.sqrt(np.maximum(0,ndimage.uniform_filter1d(np.mean(sib*sib,axis=1),int(.015*SR))))
    voice -= sib*np.clip((sib_env-.02)*6,0,.42)[:,None]
    wet=np.zeros_like(voice)
    # Dotted-eighth throws, alternating left/right, mostly on the memorable line endings.
    delaysource=band(throws,450,4200)
    for repeat in range(1,5):
        offset=int(.3125*repeat*SR)
        if offset>=len(wet):
            break
        block=delaysource[:-offset]
        if repeat%2:
            block=block[:,::-1]
        wet[offset:] += block*(.28*(.47**(repeat-1)))
    for channel in range(2):
        ir=np.zeros(int(1.4*SR))
        taps=np.sort(RNG.uniform(.025,1.35,1200))
        signs=RNG.normal(0,1,len(taps))
        ir[(taps*SR).astype(int)] = signs*np.exp(-taps/0.31)
        ir/=max(np.sqrt(np.sum(ir*ir)),1e-8)
        reverb=signal.fftconvolve(voice[:,channel],ir)[:len(voice)]
        wet[:,channel] += reverb*.13
    return voice+wet

def render(gender,score,backing):
    meta=json.loads((ROOT/f'vocal-{gender}-source.json').read_text(encoding='utf-8'))
    words=[w for w in meta['word_timestamps'] if not w['word'].startswith('<')]
    assert len(words)==len(score),(len(words),len(score))
    data=source_analysis(gender)
    dry=np.zeros_like(backing)
    layers=np.zeros_like(backing)
    throws=np.zeros_like(backing)
    octave=0 if gender=='female' else -12
    previous=score[0]['notes'][0]['midi']
    report=[]
    for i,(word,group) in enumerate(zip(words,score)):
        assert normalize_word(word['word'])==group['word'],(word,group)
        s=max(0,word['start']-.045)
        e=min(data['t'][-1],word['end']+.04)
        if i:
            s=max(s,(words[i-1]['end']+word['start'])/2)
        if i+1<len(words):
            e=min(e,(word['end']+words[i+1]['start'])/2)
        f0,sp,ap,duration=warp_word(data,s,e,group['notes'],octave,previous,gender)
        target=group['notes'][0]
        start=target['start']
        # Function words sit slightly back; hook keywords receive emphasis.
        gain=.85 if group['word'] in ('a','of','it','my','on','but') else 1.0
        if group['word'] in ('still','me','heart','roots','deep','beat'):
            gain=1.06
        y=render_word(f0,sp,ap,gain)
        add(dry,y,start)
        if target['line'] in (1,5,8):
            for pan,cents,offset in [(-.72,-7,.014),(.72,7,.023)]:
                double=render_word(f0*2**(cents/1200),sp,ap,gain)
                add(layers,double,start+offset,pan,.14)
        if group['word'] in ('me','underneath','deep','beat'):
            add(throws,y,start)
        # Diatonic harmony only at selected cadences, allowing the central take to lead.
        if group['word'] in ('me','deep') and target['line'] in (1,5,6,8):
            scale=np.array([54,56,57,59,61,62,64,66,68,69,71,73,74,76,78,80,81])
            note=target['midi']+octave
            ix=int(np.argmin(abs(scale-note)))
            interval=scale[min(ix+2,len(scale)-1)]-note
            harmony=render_word(f0*2**(interval/12),sp,ap,.8)
            add(layers,harmony,start+.02,-.42,.18)
        previous=group['notes'][-1]['midi']
        report.append(dict(word=group['word'],start=round(start,4),duration=round(duration,4),
                           voiced_fraction=round(float((f0>0).mean()),3),source_start=round(s,4),source_end=round(e,4)))
    wet=vocal_effects(dry,layers,throws,gender)
    # Match the active vocal level between the two versions before applying a shared mix gain.
    env=np.sqrt(np.maximum(0,ndimage.uniform_filter1d(np.mean(wet*wet,axis=1),int(.025*SR))))
    active=env>.018
    vocal_rms=np.sqrt(np.mean(wet[active]**2))
    wet*=.105/max(vocal_rms,1e-8)
    dry*=.105/max(vocal_rms,1e-8)
    # Make a small amount of space around diction frequencies; keep the same bass and drum arrangement.
    envelope=ndimage.uniform_filter1d(np.clip(env/.08,0,1),int(.06*SR))
    music=backing-.13*band(backing,850,3800)*envelope[:,None]
    mix=music*.86+wet
    sf.write(ROOT/f'still-got-me-{gender}-vocal-dry.wav',signal.resample_poly(dry,OUT_SR,SR),OUT_SR,subtype='PCM_16')
    sf.write(ROOT/f'still-got-me-{gender}-vocal-wet.wav',signal.resample_poly(wet,OUT_SR,SR),OUT_SR,subtype='PCM_16')
    (ROOT/f'vocal-{gender}-alignment.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return mix,report

def main():
    backing,sr=sf.read(ROOT/'still-got-me-hook-backing.wav')
    assert sr==OUT_SR and backing.ndim==2
    backing=signal.resample_poly(backing,SR,sr)
    score=get_score()
    outputs={}
    for gender in ('female','male'):
        print('Rendering',gender,flush=True)
        outputs[gender]=render(gender,score,backing)
    # One gain for both mixes; neither receives a loudness advantage from independent peak normalization.
    peak=max(float(abs(x[0]).max()) for x in outputs.values())
    common_gain=min(1.25,.88/max(peak,1e-8))
    verification={}
    for gender,(mix,report) in outputs.items():
        final=signal.resample_poly(mix*common_gain,OUT_SR,SR)
        assert np.isfinite(final).all() and abs(final).max()<.99
        name=f'still-got-me-hook-{gender}-synthetic-vocal.wav'
        sf.write(ROOT/name,final,OUT_SR,subtype='PCM_16')
        verification[gender]=dict(file=name,sample_rate=OUT_SR,channels=2,duration_seconds=len(final)/OUT_SR,
            peak=float(abs(final).max()),rms=float(np.sqrt(np.mean(final**2))),words=len(report),
            words_without_detected_voicing=[r['word'] for r in report if r['voiced_fraction']==0],
            pitch_octave_offset=0 if gender=='female' else -12)
    verification['method']='Public stock TTS + score-aligned WORLD pitch/vowel resynthesis; synthetic prototype, not a natural sung performance.'
    verification['common_mix_gain']=common_gain
    (ROOT/'vocal-mix-verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
    print(json.dumps(verification,indent=2),flush=True)

if __name__=='__main__':
    main()
