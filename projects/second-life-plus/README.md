# SECOND LIFE+

**交付版本：preproduction-v1.0 · 2026-09-18**

八首英文歌曲：三首实质重写的 remix、四首新增单曲、一首保留原作。当前是供 Suno 制作及后续编曲使用的预制作包，未生成正式音频、未完成混音母带，也未办理发行。

## 从这里开始

1. **ALBUM-DIRECTION.md**：专辑叙事、顺序、三首 remix 的保留与变化。
2. **SONGBOOK.md**：八首完整英文歌词。
3. **SUNO-PASTEBOOK.md**：八首可逐项复制的 Title / Style / Exclude / Lyrics。
4. **SUNO-WORKFLOW.md**：逐首导入、声部处理、采样路径与候选版本选择。
5. **ACCEPTANCE.md**：本阶段已检查的项目、Suno 生成后和发行前应完成的验收。

## 曲目

| # | 名称 | 版本 | 风格 |
|---|---|---|---|
| 01 | NO RECEIPT | Split Sheet Remix | Drill / underground hip-hop |
| 02 | IVORY HOURS | 新作 | Piano-sample underground hip-hop / jazz rap |
| 03 | FAST FORWARD | Night Shift Remix | Melodic trap / R&B |
| 04 | COUNTERSTEP | 新作 | Violin-sample drill / melodic rap |
| 05 | ROOM TONE | Open Door Remix | Singing rap / alternative R&B / UK garage |
| 06 | SOFT LANDING | 新作 | R&B / trap-soul |
| 07 | LAST TRAIN, FIRST LIGHT | 新作 | Piano trap / melodic rap |
| 08 | SECOND LIFE | 原作保留 | Melodic rap / soulful trap / breakbeat |

计划总长约 **21:21**，来自小节与速度计算，实际音频时长待生成后记录。

## 每首歌的交付

`tracks/` 内各目录包含：完整带标签歌词、无标签歌词、发行歌词草稿、英文风格提示、排除项、针对性修改提示、制作说明、段落 CSV、Hook MIDI 与逐音 CSV。新写七首另有 Hook 主旋律 MusicXML。

MIDI 的通用音色只是音符试听标记，不是钢琴、小提琴或真人歌手的实际录音。MusicXML 的音符门限量化到十六分音符便于编辑；MIDI 保留更细的发音时值，二者不能当作完全一致的演奏记录。主歌已逐行安排小节与角色，完整主歌音高表演待生成/演唱阶段定稿。

`samples/` 内包括八段原创器乐素材的 MIDI、MusicXML 与逐音 CSV，以及沿用的原创 V01 人声母句 MIDI。COUNTERSTEP 的提琴素材另附 144 BPM 四拍对齐 MIDI。它们是采样前的作曲素材，录音、切片和音频处理尚待执行。

## 管理与验收文件

- `VOCAL-MAP.csv`：每行歌词的角色、起始小节、占用小节与计划时间。
- `TRACK-METADATA.csv`：曲目版本、速度、调性、词数等；真实艺人、署名、ISRC 等留待实际确定。
- `SAMPLE-REGISTER.csv` / `SAMPLE-PLAN.md`：素材来源、状态与切片方案。
- `GENERATION-LOG.csv`：真实生成后填写候选版本和决定，当前没有虚构记录。
- `CREDITS-AND-SPLITS.csv`：署名及分成登记表，当前未假填人员或比例。
- `AUDIO-QC.csv`：音频生成后的实测与听检表。
- `QC-REPORT.json`：文件和结构检查结果；音频项目明确标为 pending。
- `PRESERVATION.json`：SECOND LIFE 六个原文件的 SHA-256 一致性证据。
- `DELIVERY-MANIFEST.json`：交付清单、大小与哈希。

## 研究与可复现性

`RESEARCH-KOREAN-REMIX.md` 记录三个韩国 remix 的一手来源；`WORKFLOW-SOURCES.md` 记录对指定 GitHub 技能库及平台官方文档的采用与判断。

`album.json`、`track_notes.json`、`score_material.py` 是可编辑内容源。当前压缩包可独立使用；若运行 `build_pack.py` 重新构建，需要相邻的上一版 `second-life-ep-2026-09-18` 目录。脚本会从上一版重新复制 SECOND LIFE 的六个保留文件，请勿把尚未另存的改版放进其保留目录。生成日志、人员表和音频 QC 表若已存在不会被清空；曲目表的人工署名/发行字段、采样表的录音来源字段也会保留。衍生的制作状态仍标示本脚本能验证的预制作范围，音频是否合格以单独的听检与测量记录为准。

本包没有参考艺人的录音、原曲歌词或克隆声线；没有安装所参考仓库的插件，也没有调用 Suno 账户。
