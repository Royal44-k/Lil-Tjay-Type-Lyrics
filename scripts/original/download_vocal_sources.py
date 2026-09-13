from pathlib import Path
import json
import urllib.request

root = Path(__file__).resolve().parent
for gender in ('female', 'male'):
    meta = json.loads((root / f'vocal-{gender}-source.json').read_text(encoding='utf-8'))
    target = root / f'vocal-{gender}-source.wav'
    if not target.exists():
        with urllib.request.urlopen(meta['audio_url'], timeout=60) as response:
            payload = response.read()
        print(f'{gender}: header={payload[:16]!r}, bytes={len(payload)}')
        if payload[:4] != b'RIFF' and payload[:3] != b'ID3' and payload[0] != 255:
            raise ValueError(f'Unexpected audio format: {payload[:96]!r}')
        target.write_bytes(payload)
    print(f'{gender}: {target.stat().st_size} bytes')
