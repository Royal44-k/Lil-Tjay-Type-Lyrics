# Reproducing and checking the archive

The original media is retained for playback without installing anything. The historical scripts are preserved byte-for-byte in [scripts/original](../scripts/original). A portable wrapper stages their expected flat directory layout under `.cache/render`, so reproduction does not overwrite the archived files.

## Environment

The session used Python 3.12 on Windows. Use a virtual environment and install [requirements.txt](../requirements.txt):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On macOS/Linux, activate the virtual environment or replace the interpreter path with `.venv/bin/python`. Package availability on those platforms has not been tested in this archive.

## Render

```powershell
.\.venv\Scripts\python.exe scripts/reproduce.py --stage instrumental
.\.venv\Scripts\python.exe scripts/reproduce.py --stage vocals
```

Use `--stage all` for both. Instrumental reproduction requires NumPy only; vocal reproduction requires the full requirements file. A render may create roughly 115 MB of WORLD feature caches plus new audio in `.cache/render`; these remain ignored by Git.

- Instrumental output: two WAVs, a MIDI file, a note CSV and the original parameter report.
- Vocal output: dry/wet stems, two experimental mixes in WAV/MP3, decoded source WAVs, alignment data and the original parameter report.
- The copied source speech and its word timestamps make the process offline. The historical download helper is retained only for provenance; the wrapper does not call it.
- No HeyGen generation is repeated. No celebrity recording or voice model is required.
- WORLD resynthesis can differ between runtime versions or runs. The archived checksums verify the delivered assets; fresh experimental vocal renders are not promised to match byte-for-byte.

The original scripts prepend a sibling `vocal_deps` directory to Python's search path. The wrapper does not create that directory; installed packages are resolved from the active Python environment.

## Verification

```powershell
python scripts/verify_archive.py
.\.venv\Scripts\python.exe scripts/verify_archive.py --audio
```

The standard-library check verifies asset hashes, complete file checksums, MIDI chunks, note count/timing, JSON and Python syntax, local Markdown links and excluded runtime/cache files. `--audio` additionally decodes all media with soundfile and checks finite sample values, sample rate, duration and PCM range.

[data/verification](../data/verification) holds the original production reports. Those reports are historical and contain original flat filenames. [manifests/assets.json](../manifests/assets.json) maps every original filename to its repository location. Passing parameter checks does not establish good musical performance; the user rejected the synthetic vocal mixes.
