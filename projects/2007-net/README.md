# 2007.net

七首原创英文歌曲 · 2026-09-29 · composition-v1.0

**Some files open a whole room. / 有些文件，打开的是一整个房间。**

从 SYSTEM SEOUL 的 SS-POP 系列与《너》开展可追溯研究，形成一张用当代声音回望 2007 年的概念专辑。人物、歌词、Hook 动机和素材母旋律为本项目新写，前两张 SECOND LIFE 项目保持不动。

## 目录

1. [参考研究](01-SYSTEM-SEOUL-RESEARCH.md)：版本日期、署名、采样线索的证据范围。
2. [专辑完整叙事](02-ALBUM-STORY.md)：中英文介绍、人物时间线、七首的意义与听觉位置。
3. [完整英文歌词本](03-SONGBOOK.md)：七首全文，重复段落已展开。
4. [旋律与编曲总说明](04-PRODUCTION-BIBLE.md)：速度、调性、和弦、Flow、韵脚、声部分工和段落。
5. [Sampling 与 voice reuse](05-SAMPLING-AND-VOICE-REUSE.md)：四组原创有谱素材与另录清单。
6. [Suno 逐曲输入](06-SUNO-IMPORT.md)：七首 Title / Style / Exclude / Lyrics 全文。
7. [研究积累与听检](07-LEARNING-AND-REVIEW.md)：年代依据、创作假设、候选验收与下一轮复盘。
8. [概念宣传](08-CAMPAIGN.md)：双语简介、单曲卡片、视觉与预告方向。

## 曲序

| # | 曲目 | 风格 | BPM / 调性 | 计划时长 |
|---|---|---|---|---|
| 01 | SCREEN NAME | melodic trap / dream R&B | 142 / F# minor | 3:43 |
| 02 | TOP EIGHT | digicore / rage | 156 / B minor | 3:05 |
| 03 | LOW-RES KISS | psychedelic R&B / singing rap | 94 / D major | 2:23 |
| 04 | POP-UP HEAVEN | hyperpop / underground rap | 160 / C# minor | 2:36 |
| 05 | DRAFTS AT 3:17 | underground hip-hop / R&B | 78 / E minor | 3:17 |
| 06 | BURN THIS SUMMER | two-step / melodic rap | 132 / A major | 3:53 |
| 07 | 2007.NET | alternative hip-hop / soulful R&B | 86 / F# minor → A major chorus | 3:10 |

计划总长约 22:06。逐曲显示值四舍五入，实际生成时长尚未测量。

## 文件与制作状态

tracks/ 的每首都有 LYRICS.txt、STYLE.txt、EXCLUDE.txt、TITLE.txt、SUNO-CARD.md、SONG-NOTES.md、ARRANGEMENT.csv、HOOK-MOTIF.mid、HOOK-NOTES.csv。

sources/ 的 VQ01、VA01、K01、S01 各有原创母动机 MIDI、逐音表、英文录制方向和状态说明。共 11 个 MIDI：7 个核心 Hook 动机、4 个素材母动机。它们不是完整歌曲伴奏或歌手音频。

BUILD-CHECK.json 记录构建检查，FINAL-AUDIT.json 记录逐曲完整性、段落与 MIDI 读回核验；MANIFEST.json 提供文件哈希。音乐质量仍需实际演唱与试听判断。

当前完成的是歌词、核心旋律动机与制作设计。尚未录制/生成演唱、渲染伴奏、完成混音母带或发布；没有登录 Suno 或消费额度。GENERATION-LOG.csv 为待填写表，不含虚构试听结果。采样链未确认之处保留在研究稿中，不宣称取得了参考作品的使用许可。

project_spec.py 保存本项目原创音乐决策；build_album.py 使用 Python 标准库重建歌词本、制作总稿、Suno 卡片、MIDI、索引与 ZIP。重建不会清空已有生成日志。修改歌词或音乐决策后需重新核对段落行数、人称与实际演唱，再重建。

2007.net 仅为专辑名称。这里的文件没有注册域名、创建网站或推送 GitHub。
