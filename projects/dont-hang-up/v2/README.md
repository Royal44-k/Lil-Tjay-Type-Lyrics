# DON'T HANG UP v2

当前交付：修订歌词、主题与韵脚设计、全曲逐音节旋律 MIDI、原创伴奏 WAV、乐器音色导唱 WAV。暂无人声演唱音频。

## 试听

- `DONT-HANG-UP-v2-HOOK-PREVIEW-NO-VOCALS.wav`：32 秒开场与 Hook；电钢琴代表男声旋律，铃音代表女声采样母句。
- `DONT-HANG-UP-v2-MELODY-GUIDE-NO-VOCALS.wav`：完整旋律导唱，约 2:45，含尾音。
- `DONT-HANG-UP-v2-INSTRUMENTAL.wav`：完整原创伴奏。

音频均为 44.1 kHz、16-bit、立体声。乐器导唱只用于核对旋律、节奏与编排；不是最终演唱或母带。

## 词曲与工程

- `LYRICS.txt`：v2 歌词，保留段落演唱提示。
- `CREATIVE-DIRECTION.md`：主题氛围、叙事、韵链、旋律与制作安排。
- `DONT-HANG-UP-v2-full-topline.mid`：全曲七轨 MIDI，包含两段 Verse、Pre、Bridge、三个 Hook 和女声母句的建议旋律。
- `TOPLINE-SCORE.csv`：574 个人声指南音节事件，含拍点、时值与音高。
- `composition-v2.json`：可编辑音符与段落数据。
- `build_demo.py`：导出脚本，需要 Python 与 NumPy；读取本目录的 `source-v1-composition.json`（第一版的 Hook 与和声写作底稿）。
- `VERIFICATION.json`：音频与旋律数据检查结果。

## 演唱生成进度

用户已选择 Suno。已在应用右侧打开 Suno 的登录窗口，等待用户登录；尚未提交生成任务。`SUNO-LYRICS.txt` 与 `SUNO-STYLE.txt` 已分开准备，登录后用于创作页。生成器可能重新演绎旋律，产出后须与歌词和结构核对。

此前 Runway 调用因免费方案不支持音乐生成而返回 `paid_plan_required`，没有创建歌曲任务。`GENERATION-PROMPT.txt` 保留该完整制作提示，便于追溯。

研究依据与编辑复核见上级目录 `verified-background.md` 和 `CRAFT-REVIEW-v2.md`。没有从参考歌曲中复制录音或旋律。
