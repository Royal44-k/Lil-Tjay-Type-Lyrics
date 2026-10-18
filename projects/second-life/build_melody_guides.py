"""Export original hook sketches as standard MIDI and syllable CSV.

No source recordings, synthesized singing, or third-party music libraries.
Middle C = C4 = MIDI 60. Times are quarter-note beats. MIDI is format 1.
"""
from pathlib import Path
import csv
import json
import math
import re
import struct
import zipfile

ROOT = Path(__file__).resolve().parent
PPQ = 480


def pitch(name):
    m = re.fullmatch(r"([A-G])([#b]?)(-?\d+)", name)
    assert m, name
    step = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)[m[1]]
    step += 1 if m[2] == "#" else -1 if m[2] == "b" else 0
    return 12 * (int(m[3]) + 1) + step


def vlq(n):
    assert n >= 0
    result = [n & 127]
    while n >> 7:
        n >>= 7
        result.insert(0, (n & 127) | 128)
    return bytes(result)


def meta(kind, data):
    return b"\xff" + bytes([kind]) + vlq(len(data)) + data


def track(events, end_tick):
    # Note offs precede onsets at the same tick.
    ordered = sorted(events, key=lambda e: (e[0], e[1]))
    body, previous = bytearray(), 0
    for tick, priority, payload in ordered:
        assert tick >= previous and tick <= end_tick
        body += vlq(tick - previous) + payload
        previous = tick
    body += vlq(end_tick - previous) + meta(0x2F, b"")
    return b"MTrk" + struct.pack(">I", len(body)) + body


def phrase(syllables, notes, starts, durations, offset, role="lead"):
    syllables, notes = syllables.split("|"), notes.split()
    assert len(syllables) == len(notes) == len(starts) == len(durations)
    return [dict(syllable=s, note=n, pitch=pitch(n), start=offset+t,
                 duration=d, role=role)
            for s, n, t, d in zip(syllables, notes, starts, durations)]


def materialize(name, folder, bpm, sf, minor, lead, chords, bass, bars=8):
    end_tick = bars * 4 * PPQ
    tempo = round(60_000_000 / bpm)
    conductor = [
        (0, 0, meta(0x03, name.encode())),
        (0, 0, meta(0x51, tempo.to_bytes(3, "big"))),
        (0, 0, meta(0x58, bytes([4, 2, 24, 8]))),
        (0, 0, meta(0x59, struct.pack("bb", sf, minor))),
    ]
    tracks = [track(conductor, end_tick)]
    for channel, role, program in [(0, "lead", 0), (3, "sample", 11)]:
        notes = [n for n in lead if n["role"] == role]
        if not notes:
            continue
        events = [(0, 0, meta(3, (role + " melody guide; no vocal audio").encode())),
                  (0, 0, bytes([0xC0 | channel, program]))]
        previous_end = -1
        for n in sorted(notes, key=lambda n: n["start"]):
            start = round(n["start"] * PPQ)
            end = round((n["start"] + n["duration"]) * PPQ)
            assert start >= previous_end and end <= end_tick, (name, n)
            previous_end = end
            events += [(start, 1, meta(5, n["syllable"].encode("utf-8"))),
                       (start, 3, bytes([0x90 | channel, n["pitch"], 89])),
                       (end, 2, bytes([0x80 | channel, n["pitch"], 0]))]
        tracks.append(track(events, end_tick))
    for channel, name_suffix, program, values in [
        (1, "open harmony", 4, chords), (2, "bass reference", 33, bass)
    ]:
        if not values:
            continue
        events = [(0, 0, meta(3, name_suffix.encode())),
                  (0, 0, bytes([0xC0 | channel, program]))]
        for start, duration, names in values:
            for note in names.split():
                events += [(round(start * PPQ), 3, bytes([0x90 | channel, pitch(note), 52])),
                           (round((start + duration) * PPQ), 2,
                            bytes([0x80 | channel, pitch(note), 0]))]
        tracks.append(track(events, end_tick))
    midi = b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks), PPQ) + b"".join(tracks)
    destination = ROOT / folder
    destination.mkdir(exist_ok=True)
    (destination / "HOOK-GUIDE.mid").write_bytes(midi)
    with (destination / "HOOK-NOTES.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["bar", "beat_in_bar", "role", "syllable", "note", "midi_pitch",
                  "start_beats", "duration_beats", "start_seconds", "duration_seconds"]
        w = csv.DictWriter(f, fields)
        w.writeheader()
        for n in sorted(lead, key=lambda n: n["start"]):
            w.writerow(dict(bar=math.floor(n["start"] / 4) + 1,
                            beat_in_bar=round(n["start"] % 4 + 1, 3),
                            role=n["role"], syllable=n["syllable"], note=n["note"],
                            midi_pitch=n["pitch"], start_beats=n["start"],
                            duration_beats=n["duration"],
                            start_seconds=round(n["start"] * 60 / bpm, 4),
                            duration_seconds=round(n["duration"] * 60 / bpm, 4)))
    return dict(name=name, folder=folder, bpm=bpm, bars=bars,
                guide_seconds=round(bars * 240 / bpm, 3),
                lead_note_count=len(lead), midi_bytes=len(midi),
                track_count=len(tracks))


def harmony(voicings, roots, durations=None):
    durations = durations or [7.8] * 4
    chords = [(i * 8, durations[i], v) for i, v in enumerate(voicings)]
    bass = [(i * 8, durations[i], v) for i, v in enumerate(roots)]
    return chords, bass


manifest = []
lead = []
a = [0, .5, 1, 3, 3.5, 4]
d = [.35, .35, 1.25, .35, .35, 2.5]
lead += phrase("No|re|ceipt|no|re|turn", "F#3 F#3 C#4 C#4 B3 A3", a, d, 0)
lead += phrase("Can't|buy|back|what|I|had|to|learn", "A3 B3 C#4 B3 A3 G#3 A3 F#3",
               [0,.5,1,2,2.5,3,3.5,4], [.35,.35,.7,.35,.35,.35,.35,2.6], 8)
lead += phrase("Cut|the|tag|let|it|burn", "A3 A3 E4 E4 C#4 A3", a, d, 16)
lead += phrase("I'm|still|me|when|the|num|bers|turn", "B3 C#4 E4 C#4 B3 C#4 B3 G#3",
               [0,.5,1,2,2.5,3,3.5,4], [.35,.35,.7,.35,.35,.35,.35,2.6], 24)
chords, bass = harmony(["F#3 C#4 F#4", "D3 A3 D4", "A3 E4 A4", "E3 B3 E4"],
                      ["F#1", "D2", "A1", "E2"])
manifest.append(materialize("NO RECEIPT", "01-NO-RECEIPT", 154, 3, 1, lead, chords, bass))

lead = []
a = [0,.25,.5,1.5,1.75,2,3.5,4.5,5.5]
d = [.2,.2,.65,.2,.2,.65,.55,.55,.55]
for offset in [0, 16]:
    lead += phrase("Fast|for|ward|fast|for|ward|wait|wait|wait",
                   "F#4 F#4 D4 F#4 F#4 D4 E4 D4 B3", a, d, offset)
lead += phrase("I|got|to|to|mor|row|but|I|missed|to|day",
               "F#4 A4 F#4 E4 F#4 E4 D4 C#4 E4 C#4 D4",
               [0,.5,1,1.5,2,2.5,3,3.5,4.5,5,5.5],
               [.35,.35,.35,.35,.35,.35,.35,.55,.35,.35,1.2], 8)
lead += phrase("Ev|ry|bod|y|loves|me|when|I|run|this|pace",
               "E4 E4 F#4 E4 C#4 B3 C#4 E4 F#4 C#4 B3",
               [0,.25,.5,.75,1.5,2,2.5,3,4,4.5,5.5],
               [.2,.2,.2,.45,.35,.35,.35,.65,.35,.65,1.5], 24)
chords, bass = harmony(["D3 A3 C#4 F#4", "F#3 A3 C#4 D4", "B3 D4 F#4 G4", "B3 C#4 E4 F#4"],
                      ["B1", "D2", "G1", "F#1"], [7, 7.8, 7, 7.8])
manifest.append(materialize("FAST FORWARD", "02-FAST-FORWARD", 146, 2, 1, lead, chords, bass))

lead = []
lead += phrase("Stay|for|the|qui|et|qui|et", "C#4 E4 F#4 G#4 F#4 E4 C#4",
               [0,.75,1.25,2,2.75,4,4.75], [.55,.35,.55,.6,.9,.6,1.8], 0)
lead += phrase("You|don't|have|to|fill|the|air", "C#4 B3 C#4 D4 C#4 B3 A3",
               [0,.5,1,1.5,2.5,3,4], [.35,.35,.35,.7,.35,.7,2.75], 8)
lead += phrase("We|don't|need|to|call|it|for|ev|er", "G#3 B3 C#4 D4 C#4 B3 G#3 F#3 G#3",
               [0,.5,1,1.5,2.5,3,4,4.5,5.25], [.35,.35,.35,.65,.35,.65,.35,.55,1.25], 16)
lead += phrase("For|to|night|to|mean|we|care", "A3 B3 C#4 B3 C#4 E4 C#4",
               [0,.5,1,2.5,3,4,4.5], [.35,.35,1.2,.35,.75,.35,1.75], 24)
chords, bass = harmony(["A3 C#4 E4 G#4", "A3 C#4 D4 F#4", "G#3 D4 F#4 C#5", "G#3 B3 C#4 E4"],
                      ["F#2", "B1", "E2", "A1"])
manifest.append(materialize("ROOM TONE", "03-ROOM-TONE", 92, 3, 1, lead, chords, bass))

lead = []
lead += phrase("Sec|ond|life|same|heart|beat", "C#4 B3 A3 E4 F#4 E4",
               [0,.5,1,3,4,5], [.35,.35,1.5,.75,.75,1.8], 0)
lead += phrase("Scuffed|up|shoes|still|miles|in|me", "C#4 B3 A3 C#4 E4 F#4 E4",
               [0,.5,1,2.5,3.5,4.5,5], [.35,.35,1.2,.75,.75,.35,1.8], 8)
lead += phrase("Sec|ond|life|save|a|seat", "C#4 B3 A3 B3 C#4 E4",
               [0,.5,1,3,3.5,4], [.35,.35,1.5,.35,.35,2.8], 16)
lead += phrase("Not|brand|new", "C#4 B3 A3", [0,.5,1], [.35,.35,.6], 24)
lead += phrase("There's|still|life|in|me", "C#5 C#5 A4 F#4 E4",
               [2,2.75,3.5,5,6.5], [.525,.525,1.125,1.125,1.275], 24, "sample")
chords, bass = harmony(["A3 B3 C#4 E4", "B3 E4 G#4", "A3 C#4 E4 F#4", "A3 C#4 E4 F#4"],
                      ["A1", "G#1", "F#1", "D2"])
manifest.append(materialize("SECOND LIFE", "04-SECOND-LIFE", 144, 3, 0, lead, chords, bass))

lead = phrase("There's|still|life|in|me", "C#5 C#5 A4 F#4 E4",
              [0,.5,1,2,3], [.35,.35,.75,.75,.85], 0, "sample")
manifest.append(materialize("V01 ORIGINAL VOCAL SEED", "00-ORIGINAL-SAMPLE", 96, 3, 1,
                            lead, [], [], bars=1))

forms = {
    "01-NO-RECEIPT": (154, [("Intro",4),("Hook",8),("Verse 1",24),("Hook",8),
                            ("Verse 2",24),("Breakdown",8),("Final Hook",16),("Outro",4)]),
    "02-FAST-FORWARD": (146, [("Intro",4),("Hook",8),("Verse 1",24),("Pre",4),("Hook",8),
                              ("Verse 2",24),("Bridge",8),("Final Hook",16),("Outro",4)]),
    "03-ROOM-TONE": (92, [("Intro",4),("Hook",8),("Verse 1",12),("Pre",4),("Hook",8),
                         ("Verse 2",12),("Bridge",4),("Final Hook",8),("Outro",4)]),
    "04-SECOND-LIFE": (144, [("Intro",4),("Hook",8),("Verse 1",24),("Hook",8),
                             ("Verse 2",24),("Bridge",8),("Final Hook",16),("Outro",4)]),
}
total_seconds = 0
for folder, (bpm, sections) in forms.items():
    cursor = 0
    with (ROOT / folder / "ARRANGEMENT.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["section", "start_bar", "end_bar", "bars", "start_seconds", "end_seconds"])
        for section, bars in sections:
            w.writerow([section, cursor+1, cursor+bars, bars,
                        round(cursor*240/bpm,3), round((cursor+bars)*240/bpm,3)])
            cursor += bars
    total_seconds += cursor * 240 / bpm
    style = (ROOT / folder / "STYLE.txt").read_text(encoding="utf-8").strip()
    assert len(style) <= 1000, (folder, len(style))
    for item in manifest:
        if item["folder"] == folder:
            item.update(song_bars=cursor, planned_song_seconds=round(cursor*240/bpm,3),
                        style_characters=len(style))

# Validate physical MIDI chunks and track endings, separate from note assertions above.
for item in manifest:
    data = (ROOT / item["folder"] / "HOOK-GUIDE.mid").read_bytes()
    assert data[:4] == b"MThd" and struct.unpack(">I", data[4:8])[0] == 6
    cursor, count = 14, 0
    while cursor < len(data):
        assert data[cursor:cursor+4] == b"MTrk"
        size = struct.unpack(">I", data[cursor+4:cursor+8])[0]
        assert data[cursor+8:cursor+8+size][-3:] == b"\xff\x2f\x00"
        cursor += 8 + size
        count += 1
    assert cursor == len(data) and count == item["track_count"]

report = dict(status="composition_and_hook_guides_only",
              vocals_recorded=False, finished_audio_rendered=False,
              planned_ep_seconds=round(total_seconds,3),
              checks=["syllable/note counts", "monophonic lead timing", "note bounds",
                      "MIDI chunk lengths and track endings", "style text <= 1000 characters",
                      "arrangement totals"], items=manifest)
(ROOT / "DELIVERY-MANIFEST.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

# Complete reading copy. Per-track plain text stays suitable for custom lyrics fields.
book = ["# SECOND LIFE — 完整歌词册\n",
        "原创英文歌词，2026-09-18。方括号为演唱提示。制作细节见 ALBUM-BLUEPRINT.md。\n"]
for folder in forms:
    book += ["\n## " + folder.replace("-", " ") + "\n",
             "```text\n" + (ROOT/folder/"LYRICS.txt").read_text(encoding="utf-8").strip() + "\n```\n"]
(ROOT / "SECOND-LIFE-SONGBOOK.md").write_text("\n".join(book), encoding="utf-8")

archive = ROOT.parent / "SECOND-LIFE-EP-CREATIVE-PACK.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for file in sorted(ROOT.rglob("*")):
        if file.is_file() and "__pycache__" not in file.parts:
            z.write(file, file.relative_to(ROOT))
print(json.dumps(report, indent=2))
print(f"ZIP: {archive}")
