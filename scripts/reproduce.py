"""Reproduce the retained sketches offline without overwriting the archive."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def stage_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT/source,target)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=('instrumental','vocals','all'),default='all')
    args=parser.parse_args()
    work=ROOT/'.cache/render'
    work.mkdir(parents=True,exist_ok=True)
    for name in ('render_still_got_me.py','render_vocal_hooks.py','export_vocal_previews.py'):
        stage_file('scripts/original/'+name,work/name)
    def run(name):
        subprocess.run([sys.executable,str(work/name)],cwd=work,check=True)
    if args.stage in ('instrumental','all'):
        run('render_still_got_me.py')
    if args.stage in ('vocals','all'):
        if args.stage=='vocals':
            stage_file('audio/instrumental/still-got-me-hook-backing.wav',work/'still-got-me-hook-backing.wav')
            stage_file('scores/still-got-me-hook-notes.csv',work/'still-got-me-hook-notes.csv')
        for gender in ('female','male'):
            stage_file(f'data/vocals/vocal-{gender}-source.json',work/f'vocal-{gender}-source.json')
            # The historical renderer expects .wav names, but soundfile detects the actual MP3 content.
            stage_file(f'audio/vocal-experiments/rejected/sources/vocal-{gender}-source.mp3',work/f'vocal-{gender}-source.wav')
        run('render_vocal_hooks.py')
        run('export_vocal_previews.py')
    print('Generated files:',work)

if __name__=='__main__':
    main()
