# SECOND LIFE

Track ID: SLP08 · 144 BPM · A major · 4/4 · 96 bars · 计划 2:40

状态：词曲制作稿；未生成完整音频。风格：melodic rap / soulful trap / breakbeat。


## 叙述者与命题

保留上一版原作：修好旧音箱、共同做音乐、搬迁后重建空间。作为 PLUS 版的结尾，原来的 save a seat 经过七首歌后包含了更多人的位置。


## 版本身份与变化

歌词、STYLE、EXCLUDE、Hook MIDI、Hook CSV 与段落 CSV 六个原文件逐字节复制。维持 144 BPM / A major / 96 小节。仅改变在专辑中的排序，不重写、不另作 remix。


## 情绪推进

保持原有叙事与情绪。其他曲目的新角色为结尾增加上下文，不倒过来修改本曲来解释前文。


## 韵脚

沿用原作 heartbeat/me/seat/me 的 Hook 元音链与叙事近韵。


## 重音与 flow

沿用原作两快小节一行的主歌与男女 Hook 接力。原始 MIDI 的男声 Not brand new 之后由女声母句回答，保持不变。


## 段落编排

原结构：4/8/24/8/24/8/16/4 小节。其干声呼吸结尾保持独立完整，不为了串接其他曲目而截断。


## 采样与配器

V01/G01/P01/B01 的上一版素材方案保留。此前只有词曲与 MIDI，没有已录人声或正式母带；本次保存的是这些已存在资产。将来若已有定稿音频，应直接沿用该文件，重新输入 Suno 无法保证同一录音。


## 第一轮听检重点

最容易把重新生成的一首相似歌曲误称为原版保留。用 PRESERVATION.json 的校验区分保存旧文件与生成新录音。


## 和声与演唱资产

Aadd9 → E/G# → F#m7 → Dmaj9。Hook 每个和声两快拍小节（慢速曲即常规小节）。

HOOK-GUIDE.mid 与 HOOK-NOTES.csv 是 Hook 音高/节奏草案，不是人声录音。主歌逐行进拍见全局 VOCAL-MAP.csv；主歌的完整音高表演需在生成或排练时确定。


## Suno Style

```text
English melodic rap and soulful sample-based trap, with a short self-played breakbeat passage and chamber strings. 144 BPM, A major, warm half-time pocket. Grounded male lead, easy melodic title hook, distinct warm female answers. Open with an original female phrase, "There's still life in me"; let that voice answer the male hook. Scuffed piano sample, rounded 808, dry claps, a small human-sounding drum break, cello pulse and high string replies. Narrative verses about repairing a speaker, losing a neighborhood shop and building a shared music room. Each verse line spans two fast bars. Bridge opens into breakbeat motion without changing tempo. Final chorus brings earlier vocal fragments together, leaves room for the words and feels communal rather than grandiose. Last four bars expose the female source phrase and its breath. Hope with weight, tactile detail, strong bass clarity, no triumphalist wall of sound.
```


## Exclude

```text
cinematic trailer drums, sentimental power ballad, stadium rock, children's choir, relentless brass, excessive gospel runs, generic motivational spoken monologue, long EDM build, muddy strings and bass, imitation of a named artist
```


## 针对性修改提示

```text
Retain the original song and existing approved audio if available. Do not rewrite its lyrics, hook, arrangement or vocal roles for this deluxe edition. If only the composition assets exist, treat a new generation as the first audio realization, not as a byte-identical preserved recording.
```
