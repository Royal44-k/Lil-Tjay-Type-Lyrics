# SECOND LIFE — Suno 手动导入说明

沿用用户自行操作 Suno 的方式。本包没有连接账户，也没有提交生成任务。

## 每首歌怎么导入

1. 在自定义创作界面分别创建四首。标题对应文件夹名。
2. 将对应 STYLE.txt 放入风格 / 制作描述字段；LYRICS.txt 放入自定义歌词字段。歌词文件已展开全部 Hook，不需要自己复制副歌。
3. 如果界面提供 Exclude，把 EXCLUDE.txt 放进去。不要把研究说明、中文编曲笔记或文件名粘进歌词栏。
4. 使用可用的稳定模型先试完整歌曲。无需为了本方案额外开启最高成本选项。
5. 一次只改一个主要问题。先选 Hook、发音与人物情绪，再修结构和细节；保留满意的版本。

自定义歌词与排除项的产品依据：[Suno 自定义模式](https://help.suno.com/en/articles/2415873)、[Exclude](https://help.suno.com/en/articles/3161921)。具体字段以账户当前界面为准。

## 数值与可控范围

BPM、调性、小节数、声部、配器与停顿均是创作目标，不是文本生成的硬保证。方括号标签也不保证逐条执行。四首 MIDI 记录首个 Hook 的具体音符；它们供 DAW / 歌手参考，不要把 MIDI 当作已经支持的 Suno 输入格式。

如果界面提供创造性与风格遵循程度控制，第一轮取偏保守的创造性、偏高的风格遵循。避免一开始同时极端化多个参数。男 / 女主唱选择是全局倾向，并不能可靠锁定每句声部。

当前没有交付完整主唱音频，不能声称已试听过 Suno 成曲或保证效果。

## 同一母句如何真正复用

本项目需要区分三件事：相似声线、相同旋律、同一次表演。

单独生成四首，再在每首提示词里写同一句话，只能要求一种相似意图。要实现这里设计的 voice reuse，应先录制 V01 的原始女声 take，再将同一 WAV 切片、拉伸或变调，放进四首工程。角色与声音模板也不能替代对同一段录音的复用。

在 Suno 先得到四首独立草样是可行的创作步骤；随后在支持音频编辑的工具里完成统一的母句、转场与混音。若使用 Suno 当前界面里的音频参考或编辑功能，也应检查实际输出是否保留了原 take，而不是重新唱了一遍。

## 有针对性的修改提示

### 01 — 主唱被伴奏盖住

Keep the hook melody and lyric wording. Make the verses drier and less dense. Shorten the guitar tails under the lead, reduce synth activity during lines, and leave a clear gap after each punchline. Keep the 808 weight and half-time groove. The lead should sound controlled and understandable, not screamed.

### 01 — 听成摇滚或 EDM

Keep the trap rhythm and rapped verses central. Treat the guitar as short sampled fragments, not a continuous rock performance. Use a compact chant hook, dry snare and mono 808. Make the section change with a brief silence rather than an EDM riser.

### 02 — Hook 不够洗脑

Keep the exact chorus lyrics. Give each "Fast-forward" the same three-note melodic cell. Make the three "wait" notes descend and separate them clearly. Leave one full beat of silence at the end of chorus lines one and three. Simplify the surrounding instruments so the title phrase is unmistakable.

### 02 — 太幼稚或效果太多

Keep the bright instrumental palette but return the male lead to a natural adult register. Use vocal chops only between lead phrases. Remove most glitch effects from verses and the final chorus. Bring forward the anxious, conversational meaning of the lyrics.

### 03 — 变成普通大抒情歌

Keep the song small and close. Use conversational singing rap in the verses, one lyric line per bar, and a low female register. Remove belting, orchestral swells and excessive runs. Let "quiet, quiet" descend gently, with audible breath and room around the last word.

### 03 — 词太挤

Preserve the lyric wording. Use light rhythmic speech on the long verse lines, with short unstressed syllables and clear sentence accents. Reserve sustained notes for the chorus. Leave a breath between thoughts; do not stretch every word into a ballad phrase.

### 04 — 情绪像广告口号

Keep the performance grounded and specific. Let the verses sound like someone telling a true-to-life neighborhood story, with relaxed timing and little vocal polish. Use small string answers and a tactile piano texture. Let the final chorus feel like several people in a room, not a stadium anthem.

### 04 — 男女人声分工不清

Keep the male singer on the verses and the first three chorus lines. In the fourth chorus line, let the male sing "Not brand new" and the female answer "There's still life in me." Leave space between them. If the voices cannot be separated clearly, prioritize a coherent male lead and reserve the female phrase for later audio editing.

## 第一轮挑选标准

每首听完先关掉播放，试着哼标题动机。记不住就先修 Hook。检查重音是否压在 receipt、forward、quiet、heartbeat 等词的自然音节上。随后检查是否能听清叙事、突变是否服务歌词、不同曲目是否真的有不同距离感。

最值得保留的是“一个清楚的 Hook + 自然人声 + 对的情绪”。与文字一致的配器名称和复杂效果数量，不应比这三项更重要。
