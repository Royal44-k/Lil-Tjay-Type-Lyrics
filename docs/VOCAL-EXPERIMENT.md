# STILL GOT ME — female / male synthetic vocal comparison

**Status: rejected experiment.** The user listened to these previews and reported poor quality. Retained only as production history.

These are synthetic singing prototypes, not recordings or cloned voices of Halsey, Lil Tjay, or any other artist.

- Lyrics and note timing: the existing original English hook in `STILL-GOT-ME.md` and `still-got-me-hook-notes.csv`.
- Instrumental: the existing original `still-got-me-hook-backing.wav`.
- Tempo/key: 144 BPM, half-time feel at 72, F-sharp minor.
- Female source: HeyGen public stock voice Aria; melody C-sharp 4 to C-sharp 5.
- Male source: HeyGen public stock voice Shaun; melody shifted down one octave, C-sharp 3 to C-sharp 4.
- Duration: 28.667 seconds, including the instrumental tail.

The available voice API generates speech, not sung performances. The source speech was aligned using its returned word timestamps, then resynthesized to the original score with WORLD. Held vowels were lengthened while consonant transitions were retained where possible. Small pitch slides, late vibrato, selective doubles, diatonic harmony at cadences, dotted-eighth delay throws and short stereo reverb were added. The backing's diction-frequency region is gently ducked during vocal activity. Both versions use a shared final gain and matched active vocal RMS.

This method has audible limits: synthetic sustained vowels, potentially uneven consonants and no singer's natural phrasing or breath control. It is intended for comparing register and arrangement, not as a finished natural vocal master. The output has been checked for numerical validity, duration, clipping and word-to-score alignment; it had not received a human listening review at export. The user subsequently listened and rejected the result as poor quality.

Archived experiment mixes (not approved finals):

- `still-got-me-hook-female-synthetic-vocal.wav`
- `still-got-me-hook-male-synthetic-vocal.wav`

Separate dry and processed vocal stems are also included for each voice. Those stems precede the common final mix gain recorded in `vocal-mix-verification.json`.

The rendering source is `render_vocal_hooks.py`. Processing reference: [PyWORLD's official repository](https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder).
