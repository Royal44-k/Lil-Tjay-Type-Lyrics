"""Validate this asset archive; add --audio for decoded-media checks."""
from pathlib import Path
import argparse
import ast
import csv
import hashlib
import json
import re
import struct
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
IGNORED={'.git','.cache','.venv','venv','__pycache__'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def included_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not (set(p.relative_to(ROOT).parts)&IGNORED))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio',action='store_true')
    args=parser.parse_args()
    manifest=json.loads((ROOT/'manifests/assets.json').read_text(encoding='utf-8'))
    assert len(manifest['assets'])==manifest['asset_count']==31
    allfiles=included_files()
    for p in allfiles:
        assert p.stat().st_size<100_000_000, f'Unexpected large file: {p}'
        assert 'vocal_deps' not in p.parts and p.suffix!='.npz', f'Unexpected runtime/cache: {p}'
        if p.suffix in ('.md','.py','.json','.txt','.csv'):
            text=p.read_text(encoding='utf-8-sig')
            assert ('resource2.heygen.ai/'+'text_to_speech/') not in text, f'Provider delivery URL: {p}'
            assert not re.search(r'github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY',text), f'Credential marker: {p}'
        if p.suffix=='.json':
            json.loads(p.read_text(encoding='utf-8'))
        if p.suffix=='.py':
            ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    for asset in manifest['assets']:
        p=ROOT/asset['path']
        assert p.is_file() and p.stat().st_size==asset['bytes'],asset['path']
        assert digest(p)==asset['sha256'],f"Asset hash mismatch: {asset['path']}"
    checksum_path=ROOT/'manifests/checksums.sha256'
    checksums={}
    for line in checksum_path.read_text(encoding='utf-8').splitlines():
        sha,name=line.split('  ',1)
        checksums[name]=sha
        assert digest(ROOT/name)==sha,f'File hash mismatch: {name}'
    actual={p.relative_to(ROOT).as_posix() for p in allfiles if p!=checksum_path}
    assert set(checksums)==actual, 'Checksum file list is incomplete or stale'
    links=0
    for p in allfiles:
        if p.suffix!='.md':
            continue
        for match in re.finditer(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',p.read_text(encoding='utf-8')):
            url=match.group(1).strip('<>')
            parsed=urlsplit(url)
            if parsed.scheme or url.startswith('#'):
                continue
            target=(p.parent/unquote(parsed.path)).resolve()
            assert target.is_relative_to(ROOT) and target.exists(),f'Broken local link: {p.name}: {url}'
            links+=1
    notes=list(csv.DictReader((ROOT/'scores/still-got-me-hook-notes.csv').open(encoding='utf-8-sig')))
    assert len(notes)==68
    for n in notes:
        onset=(int(n['bar_144_bpm'])-1)*4+float(n['start_beat_in_bar_144_bpm'])
        assert 0<=onset<64 and onset+float(n['duration_beats_144_bpm'])<=64
        assert 61<=int(n['midi_note'])<=73
    midi=(ROOT/'midi/still-got-me-hook.mid').read_bytes()
    assert midi[:4]==b'MThd' and struct.unpack('>IHHH',midi[4:14])==(6,1,6,480)
    cursor=14
    tracks=0
    while cursor<len(midi):
        assert midi[cursor:cursor+4]==b'MTrk'
        length=struct.unpack('>I',midi[cursor+4:cursor+8])[0]
        cursor+=8+length
        tracks+=1
    assert cursor==len(midi) and tracks==6
    for gender in ('female','male'):
        data=json.loads((ROOT/f'data/vocals/vocal-{gender}-source.json').read_text(encoding='utf-8'))
        assert 'audio_url' not in data and (ROOT/data['local_audio_file']).is_file()
        words=[w for w in data['word_timestamps'] if not w['word'].startswith('<')]
        alignment=json.loads((ROOT/f'data/vocals/vocal-{gender}-alignment.json').read_text(encoding='utf-8'))
        assert len(words)==len(alignment)==66
    audio=[]
    if args.audio:
        import numpy as np
        import soundfile as sf
        for p in allfiles:
            if p.suffix not in ('.wav','.mp3'):
                continue
            data,sr=sf.read(p,always_2d=True)
            assert sr==44100 and np.isfinite(data).all() and np.max(np.abs(data))<=1
            duration=len(data)/sr
            if 'sources' not in p.parts:
                assert data.shape[1]==2 and abs(duration-28.6666666667)<.002
            audio.append(dict(path=p.relative_to(ROOT).as_posix(),seconds=round(duration,3),channels=data.shape[1]))
        assert len(audio)==14
    print(json.dumps(dict(status='passed',assets=31,files=len(allfiles),local_links=links,
                          midi_tracks=tracks,note_events=len(notes),decoded_audio=len(audio),audio=audio),indent=2))

if __name__=='__main__':
    main()
