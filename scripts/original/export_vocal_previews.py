from pathlib import Path
import sys
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root/'vocal_deps'))
import numpy as np
import soundfile as sf

for gender in ('female','male'):
    wav = root/f'still-got-me-hook-{gender}-synthetic-vocal.wav'
    data, sr = sf.read(wav)
    target = wav.with_suffix('.mp3')
    sf.write(target, data, sr, format='MP3', subtype='MPEG_LAYER_III', bitrate_mode='CONSTANT', compression_level=.15)
    decoded, decoded_sr = sf.read(target)
    assert decoded_sr == sr and len(decoded) == len(data)
    assert np.isfinite(decoded).all() and np.max(np.abs(decoded)) < 1
    print(target.name, target.stat().st_size, 'bytes;', round(len(decoded)/sr,3), 'seconds; peak',round(float(np.max(np.abs(decoded))),3))
