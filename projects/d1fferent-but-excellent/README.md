# D1fferent but Excellent

2026-09-18 · preproduction-v1.0 · 七首原创英文歌曲。

**D1fferent 按 different 演唱；1 代表 chosen one。** 全碟把“我被选中，所以必须证明”逐渐推进为“我可以选择怎样使用自己的独特之处”。完整歌词、Hook 音符、配器素材与 Suno 输入已经交付。演唱、器乐录音、完整伴奏、混音与母带尚未生成。

## 使用顺序

1. `ALBUM-DIRECTION.md`：人物、曲序、七首的意义与声音。
2. `SONGBOOK.md`：七首完整英文歌词。
3. `SUNO-PASTEBOOK.md`：逐项复制 Title / Style / Exclude / Lyrics。
4. `SUNO-WORKFLOW.md`：生成顺序、音频参考、候选版本与声部修正。
5. `ACCEPTANCE.md`：预制作、草样、混音及发行资料各阶段如何验收。

## 交付内容

每首目录内有 12 类资料：带标签歌词、纯歌词、发行歌词草稿、Style、Exclude、针对性修改提示、制作说明、段落 CSV、Hook MIDI、Hook 逐音 CSV、Hook MusicXML、八小节鼓型 CSV。实际文件项数以清单为准；不能把 MusicXML 或 MIDI 当作录音。

`samples/` 含 9 个原创作曲源：吉他、钢琴、电钢琴、短弓提琴、提琴回答、合成器及三音人声动机。每个源包含 MIDI / MusicXML / 逐音 CSV。音频录制或音源渲染后才成为可切片的录音素材。

根目录管理资料包括：曲目元数据、320 行的声部/小节分配、首尾动机比较、素材账本、待填的真实生成日志、学习记录、署名分成和音频 QC 表。`QC-REPORT.json`、`DELIVERY-MANIFEST.json` 记录结构校验与文件完整性。

`RESEARCH-DESTINED-2-WIN.md` 为带来源的背景与文本研究；`PRODUCER-NOTEBOOK.md` 将本轮决定接入前几轮的制作经验。研究没有冒充原专辑的实际试听或音频测量。

## 曲目与计划时长

| # | 曲名 | 方向 | 计划 |
|---|---|---|---|
| 01 | ONE OF ONE | Guitar melodic trap | 2:44 |
| 02 | AFTER THE FLASH | Ambient melodic trap / R&B | 2:40 |
| 03 | DON'T MAKE IT COOL | R&B / singing rap | 2:09 |
| 04 | SIDE DOOR | Melodic drill | 2:29 |
| 05 | WEAR IT OUT | Soulful piano trap | 2:51 |
| 06 | GOOD ON ME | Melodic rage / synth trap | 2:25 |
| 07 | D1FFERENT BUT EXCELLENT | Soulful melodic rap | 2:45 |

总长按小节计算约 **18:04**。计划秒数与真实输出分开记录，不能把表中数字当成已测时长。

## 重建与编辑

本包可独立使用，重建只需 Python 标准库。修改 `album_data.py`、`score_material.py` 或各曲 `LYRICS.txt`，然后运行 `python build_pack.py`。`music_io.py` 是本地复用的文件工具，不依赖之前的专辑目录。

重建会覆盖衍生歌词册、乐谱与制作表格。已有生成日志、学习记录、署名分成和音频 QC 不会被清空；曲目表的人工署名/发行字段、素材表的真实录音来源字段也会保留。衍生状态仍代表脚本能验证的预制作范围。

未登录或操作 Suno，未生成声线克隆，未使用参考曲录音或歌词，未向 GitHub 推送。本包没有虚构艺人署名、分成、发行代码或测量值。
