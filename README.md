# English Hip-Hop Songwriting & Production Archive

本仓库按项目归档对话中的原创英文 hip-hop 词曲、研究、旋律动机、编曲方案、Suno 输入和可用制作素材。最初的《STILL GOT ME》资料保留在原目录；后续作品集中放在 [projects/](projects/)。参考艺人未参与这些原创项目。

## 后续作品

| 项目 | 内容 | 制作状态 |
| --- | --- | --- |
| [DON'T HANG UP](projects/dont-hang-up/README.md) | 受《Scared 2 Be Lonely》研究启发的原创 melodic trap；[v2 词曲与伴奏](projects/dont-hang-up/v2/README.md)、[Suno 输入](projects/dont-hang-up/suno-import/README.md) | 词曲与三段无主唱 WAV 草样；尚无完成的人声演唱 |
| [D1fferent but Excellent](projects/d1fferent-but-excellent/README.md) | 七首英文歌曲、原创 Hook 与采样母动机 | 预制作资料；未生成全曲音频 |
| [SECOND LIFE](projects/second-life/README.md) | 原版四首，含完整歌词、编曲与 Hook 引导 | 预制作资料 |
| [SECOND LIFE+](projects/second-life-plus/README.md) | 三首 remix、四首新作、一首保留原曲 | 预制作资料 |
| [两张唱片的叙事与宣传制作包](projects/second-life-duology/README.md) | 详细叙事、概念宣传和 12 个曲目位置的 Suno 输入 | 文本与谱面制作包 |
| [2007.net](projects/2007-net/README.md) | 七首英文歌曲；早期互联网主题、完整歌词、Hook 和原创素材动机 | 预制作资料；未生成演唱音频 |

[制作知识索引](docs/PRODUCER-KNOWLEDGE-INDEX.md)串联各轮研究与待验证判断；[本次增量归档说明](docs/CONVERSATION-UPDATE-2026-10-18.md)记录文件范围与去重规则；[新增文件哈希清单](manifests/conversation-update-2026-10-18.json)可用于核对字节。

## STILL GOT ME · 2026-09-13 初次归档

这首歌以 Lil Tjay《Born 2 Be Great》为研究起点，保留歌词、美国 hip-hop 文化与制作研究、Hook 旋律、伴奏草图、可编辑 MIDI、人声实验和制作脚本。

**当前状态：完整英文歌词已写出；音频仅完成约 29 秒的 Hook 草图；两版合成人声已被用户否定；真实演唱版本尚未完成。** 仓库名描述研究方向，不代表 Lil Tjay 或 Halsey 参与了本项目。

## STILL GOT ME 文件导航

| 内容 | 文件 | 状态 |
| --- | --- | --- |
| 完整英文歌词、主题、押韵与唱法 | [STILL-GOT-ME.md](lyrics/STILL-GOT-ME.md) | 当前保留稿 |
| Hook 旋律 + beat | [WAV](audio/instrumental/still-got-me-hook-demo.wav?raw=1) | 合成乐器导唱，无人声 |
| Hook 纯伴奏 | [WAV](audio/instrumental/still-got-me-hook-backing.wav?raw=1) | 制作草图 |
| 可编辑 MIDI | [MIDI](midi/still-got-me-hook.mid) | 6 轨，含旋律、和声、低音、鼓 |
| 逐音节音符与时间 | [CSV](scores/still-got-me-hook-notes.csv) | 68 个音节事件 |
| 原曲背景与解释 | [研究笔记](research/background-research.md) | 事实与解读分开记录 |
| 美国 hip-hop / trap 文化 | [文化研究](research/american-hiphop-culture-research.md) | 含来源链接 |
| Melodic trap 制作与英文写作 | [制作研究](research/melodic-trap-production-research.md) | 含来源及阅读限制 |

主题是一个虚构的新兴说唱歌手在追求经济安全、认可与成功时，面对家庭责任、攀比、忠诚和自我价值的矛盾。Hook 用 “Still got me” 串起身份与自我接纳；歌词采用英文直接创作。

## 音乐规格

- 风格：American hip-hop / melodic trap。
- 工程速度：144 BPM；半拍体感：72 BPM；4/4 拍。
- 调性：F♯ minor；和声：Dmaj7 / Aadd9 / F♯m9 / Esus2。
- Hook：144 BPM 网格上的 16 小节；音乐段约 26.67 秒，含尾音约 28.67 秒。
- WAV：44.1 kHz、16-bit PCM；混音与伴奏为立体声。原始语音素材为单声道。
- 完整歌曲的 128 小节结构、约 3:33 时长是制作建议，尚无对应的全曲演唱录音。

## 保留的人声实验

**以下版本仅作失败实验归档，不作为成品推荐。** 两者使用 HeyGen 公共库存语音（Aria / Shaun），经 WORLD 调整音高和时长，再加入叠唱、和声、混响、延迟。用户听后认为效果糟糕，项目随后转向寻找真实演唱素材。

| 实验 | 试听文件 | 音域 |
| --- | --- | --- |
| 女声 | [MP3](audio/vocal-experiments/rejected/mixes/still-got-me-hook-female-synthetic-vocal.mp3?raw=1) · [WAV](audio/vocal-experiments/rejected/mixes/still-got-me-hook-female-synthetic-vocal.wav?raw=1) | C♯4–C♯5 |
| 男声 | [MP3](audio/vocal-experiments/rejected/mixes/still-got-me-hook-male-synthetic-vocal.mp3?raw=1) · [WAV](audio/vocal-experiments/rejected/mixes/still-got-me-hook-male-synthetic-vocal.wav?raw=1) | C♯3–C♯4 |

还保留了两版的 [干声与湿声分轨](audio/vocal-experiments/rejected/stems)、[原始合成语音](audio/vocal-experiments/rejected/sources)、[逐词对齐数据](data/vocals) 和 [制作说明](docs/VOCAL-EXPERIMENT.md)。没有收录 Lil Tjay / Halsey 的原唱录音、MV 或人声模型。

## 目录

```text
lyrics/                         完整英文歌词及创作说明
research/                       原曲背景、文化、制作研究
audio/instrumental/             Hook 伴奏与旋律导唱草图
audio/vocal-experiments/rejected/
  mixes/                        被否定的男女声混音
  stems/                        干声、湿声分轨
  sources/                      公共库存语音原文件及 PCM 解码
midi/                           可编辑多轨 MIDI
scores/                         音节—音高—时值 CSV
data/vocals/                    时间戳、音色来源、对齐记录
data/verification/              原制作环节的参数检查记录
scripts/original/               对话中使用的原始制作脚本
scripts/reproduce.py            在缓存目录离线复现草图
scripts/verify_archive.py       校验归档内容与校验和
docs/                           项目记录、索引、来源与复现指南
manifests/                      文件清单、SHA-256、排除项
```

## 归档说明

共保留 **31 个既有资产文件**，约 **47.6 MB**；新增文档、复现入口和校验工具另计。媒体文件保持原始字节；服务商临时音频链接从元数据移除，改为仓库内文件路径。两个源语音文件实际是 MP3，已修正扩展名，内容未变。

约 254 MB 的第三方依赖与可再生分析缓存未上传。此前依用户要求删除的中文歌曲资产没有恢复。具体去向及修改记录见 [资产索引](docs/ASSET-INVENTORY.md) 和 [机器可读清单](manifests/assets.json)。

- [项目需求与过程记录](docs/PROJECT-HISTORY.md)
- [资料来源](docs/REFERENCES.md)
- [复现与验证](docs/REPRODUCING.md)
- [材料来源说明](docs/PROVENANCE.md)

归档日期：2026-09-13。SHA-256 校验可用 `python scripts/verify_archive.py` 运行；音频参数检查可加 `--audio`。
