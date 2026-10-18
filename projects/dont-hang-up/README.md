# DON’T HANG UP

An original English American melodic trap song project, developed on 2026-09-17 and organized for this repository on 2026-10-18. The story follows a rising musician who struggles to ask for help, then learns to listen when someone else needs him. The final hook changes **“Don’t hang up”** to **“I won’t hang up.”**

**Current state:** the v2 lyrics, full topline MIDI, arrangement data, original instrumental, instrumental-timbre melody guide, and a Suno manual import kit are present. No finished human-sung recording, Suno-generated vocal take, or final master is included. The melody-guide WAV uses instruments to represent vocal notes; it is not a vocal performance.

## Start here

| Need | File |
| --- | --- |
| Paste the current style prompt and lyrics into Suno | [Style](v2/suno-import/STYLE.txt) · [Lyrics](v2/suno-import/LYRICS.txt) · [Exclude](v2/suno-import/EXCLUDE.txt) |
| Understand the Suno setup and targeted revisions | [Import guide](v2/suno-import/README.md) · [Settings](v2/suno-import/SETTINGS.txt) · [Refinement prompts](v2/suno-import/REFINEMENT-PROMPTS.md) |
| Read the current song and production plan | [v2 lyrics](v2/LYRICS.txt) · [Creative direction](v2/CREATIVE-DIRECTION.md) |
| Hear the current arrangement | [32-second hook guide](v2/DONT-HANG-UP-v2-HOOK-PREVIEW-NO-VOCALS.wav) · [full melody guide](v2/DONT-HANG-UP-v2-MELODY-GUIDE-NO-VOCALS.wav) · [instrumental](v2/DONT-HANG-UP-v2-INSTRUMENTAL.wav) |
| Edit melody and timing | [Full topline MIDI](v2/DONT-HANG-UP-v2-full-topline.mid) · [syllable score](v2/TOPLINE-SCORE.csv) · [composition data](v2/composition-v2.json) |
| Review research and the first draft | [Verified background](v1/verified-background.md) · [craft review](v1/CRAFT-REVIEW-v2.md) · [producer notebook](v1/PRODUCER-NOTEBOOK.md) · [v1 guide](v1/README.md) |
| Download the original handoff packages | [Releases](releases/) |

The intended production is 148 BPM with a 74 BPM half-time feel in C minor. A close male melodic-rap lead carries the story. A short original female response appears in the intro and bridge and leaves room for the lead in the hooks. Sparse keys, plucked guitar, warm 808, restrained half-time drums, and a wider final hook support the narrative turn. These are composition targets; a generative rendition may interpret them differently.

The work began with research into Lil Tjay’s *Scared 2 Be Lonely* and American melodic trap. The lyrics, MIDI, and instrumental here are independently created. This repository does not contain Lil Tjay or Halsey recordings, their vocal models, or an extracted sample from the reference song. The female “sample-like” part is an original proposed refrain, not a recording taken from another work.

## Layout and status

- `v1/` preserves the first complete writing and composition snapshot, its source data, MIDI, notes, and verification output.
- `v2/` contains the revised song, full syllable-level topline, three WAV exports, and the generation guide. Run `build_demo.py` from this directory with Python and NumPy if you want to recreate the exports.
- `v2/suno-import/` contains the current manually entered Suno prompt kit. The user chose to operate Suno in their own browser; no account access or completed Suno render is part of this archive.
- `releases/` preserves the three original ZIP handoff packages. Their contents intentionally overlap with the browsable files above.
- [ASSET-INVENTORY.md](ASSET-INVENTORY.md) explains every category and the archive overlap; [SHA256SUMS](SHA256SUMS) records the exact bytes of the 36 copied source assets and packages.

Some preserved v1/v2 notes describe the state at their September creation date, including an earlier Suno login plan. This README records the current handoff status as of 2026-10-18. No direct listening assessment of a finished sung version is claimed.
