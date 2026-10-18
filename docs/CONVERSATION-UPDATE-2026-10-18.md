# 2026-10-18 对话资产增量归档

仓库在 2026-09-13 已归档《STILL GOT ME》。本次将其后在对话中形成的六套音乐项目资料加入 `projects/`，保留原目录中的音频与失败人声实验，不改写旧文件。新目录承载 **654 个来源文件，约 63.47 MiB**。

| 新目录 | 来源目录／补充包 | 文件数 | 核心内容 |
| --- | --- | ---: | --- |
| [dont-hang-up](../projects/dont-hang-up/) | `outputs/scared-2-be-lonely-2026-09-17/`；`DONT-HANG-UP-SUNO-IMPORT.zip` 的六份文字输入 | 39 | 词曲 v1/v2、全曲 MIDI、伴奏／无主唱旋律指导 WAV、Suno 输入与背景研究 |
| [d1fferent-but-excellent](../projects/d1fferent-but-excellent/) | `outputs/d1fferent-but-excellent-2026-09-18/` | 137 | 七首完整英文歌词、旋律与素材谱、研究及 Suno 资料 |
| [second-life](../projects/second-life/) | `outputs/second-life-ep-2026-09-18/` | 33 | 四首原版歌曲和制作资料 |
| [second-life-plus](../projects/second-life-plus/) | `outputs/second-life-plus-2026-09-18/` | 138 | 三首 remix、四首新作、一首保留原作及制作资料 |
| [second-life-duology](../projects/second-life-duology/) | `outputs/second-life-duology-editorial-suno-2026-09-18/` | 211 | 双专辑叙事、宣传、完整 Suno 输入与原素材快照 |
| [2007-net](../projects/2007-net/) | `outputs/2007-net-2026-09-29/` | 96 | 七首英文歌曲、SYSTEM SEOUL 研究、旋律、原创素材与 Suno 输入 |

六目录中的文件均按原字节复制，附有 [来源路径、大小与 SHA-256](../manifests/conversation-update-2026-10-18.json)。本轮没有再次复制独立 ZIP 下载包；它们的内容已在上述目录中。《DON'T HANG UP》的 Suno 补充包仅将尚未出现的六份文字文件提取到 `suno-import/`，其中重复的 Hook WAV 已与 `v2/` 中的现有文件比对一致。

上传期间，远端另有一笔《DON'T HANG UP》归档提交。本次合并保留其 `v1/` 分目录、`v2/suno-import/`、[资产清单](../projects/dont-hang-up/ASSET-INVENTORY.md)及 `releases/` 中的三个原交付 ZIP。它们属于远端先行归档，不计入上述 654 个本轮来源文件；工程目录与 ZIP 因此会有重复内容。

项目状态以各自 README 与验收文档为准。`DON'T HANG UP` 有无主唱 WAV 草样；其余新增专辑主要是完整歌词、编曲计划、MIDI／MusicXML 和提示词。谱面不等于录音，生成日志的空白也不等于完成试听。参考歌曲的人声或商业录音没有被作为素材上传。

原项目中可能仍有指向 `D:/Codex-chat/outputs/...` 的历史来源路径。这些路径用于记录创作时的本地来源；仓库内阅读从根目录索引进入，重建脚本如需运行，应以对应项目 README 的实际依赖和相对路径为准。
