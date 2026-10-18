# SECOND LIFE / SECOND LIFE+ — 叙事、宣传与 Suno 制作套装

2026-09-18 · editorial-suno-v1.0

本包扩展两张既有作品的介绍与制作说明。原版四首、PLUS 八首，共十二个曲目位置；同名曲完全共用，共十一种歌曲版本。原歌词、主 Style、Exclude 和旋律资料原样收录，本轮新写详细叙事、概念宣传和附加制作提示。

## 阅读与使用

1. [SECOND LIFE 详细叙事](01-SECOND-LIFE-NARRATIVE.md)：中英文专辑介绍、四首完整故事、音乐与主题的关系。
2. [SECOND LIFE+ 详细叙事](02-SECOND-LIFE-PLUS-NARRATIVE.md)：三首 remix 的变化、四首新作与保留原曲的意义。
3. [概念宣传套装](03-CAMPAIGN-COPY.md)：双语主张、长短简介、十二张单曲卡片、社交文案、两套 30 秒预告分镜与视觉方向。
4. [原版 Suno 总稿](04-SECOND-LIFE-SUNO.md)：四首逐项输入，完整歌词已展开。
5. [PLUS Suno 总稿](05-SECOND-LIFE-PLUS-SUNO.md)：八首逐项输入，完整歌词已展开。
6. [器乐与人声母句](06-SOURCES-AND-VOICE-REUSE.md)：V01 及两张唱片所需素材的生成/录制方向。
7. [Suno 操作与听检](07-SUNO-WORKFLOW.md)：版本、模型选择、分阶段修正、声部分工与记录。

## 每首的输入文件

`suno/SECOND-LIFE/` 与 `suno/SECOND-LIFE-PLUS/` 分别存放十二张独立 PROMPT-CARD.md，以及 Title、Style、Exclude、Lyrics、人声方向、器乐 Style / Exclude、Hook 修正、编排修正的单独文本。Hook MIDI、逐音 CSV 和段落 CSV 一并收录；PLUS 新写七首另有 MusicXML。

第一轮只需复制 Title / Style / Exclude / Lyrics 四栏。其余提示是遇到具体问题时使用，不要同时全部粘贴。

## 资料与验证

- PROMPT-INDEX.csv：十二个曲目位置与对应版本、速度、调性、段落长度。
- SOURCE-PROVENANCE.json：109 份保留资产的来源和哈希。
- QC-REPORT.json：数量、主输入、保留曲一致性等检查。
- FINAL-AUDIT.json：与当前原文件逐一比对、完整提示词收录、目录链接与日志状态的独立核验。
- DELIVERY-MANIFEST.json：打包清单、文件大小与哈希。
- GENERATION-LOG.csv：待真实生成后填写。
- PUBLICATION-LOG.csv：待正式发布时填写。

`samples/` 收录现有器乐/人声作曲资料，属于谱面与 MIDI，不是采样录音；`references/` 收录 PLUS 的声部、发音和素材登记资料。原版 G01/P01/B01 等仍是待录制作计划，没有在此虚构成录音。

整个包可以独立阅读和使用。`build_delivery.py` 使用 Python 标准库及本地快照重建两个 Suno 总稿、独立卡片、索引、检查与 ZIP；运行时不依赖原项目目录。已有生成与发布日志不会清空。修改保留资产时应另存新版本并更新来源记录，避免混淆原版。

本轮没有生成音乐音频、封面或视频成片，也没有登录 Suno、发布宣传或推送 GitHub。声音描述、分镜与模型指令是制作目标；现有资料支持进入制作，实际演唱与听感仍需验收。
