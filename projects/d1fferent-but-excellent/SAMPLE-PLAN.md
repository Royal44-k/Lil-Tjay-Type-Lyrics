# 原创素材与取样方案

当前九项是新作的 MIDI / MusicXML 作曲资料，不是钢琴、提琴、吉他或人声的录音。源谱中 MIDI 音色用于辨认声部，不能代表实际奏法和音质。采样应在真实录制、授权音源渲染或生成器乐之后执行。

| ID | 名称 / 乐器 | 源设置 | 目标用途 |
|---|---|---|---|
| G01 | Crooked Cuff / 干净电吉他 | 73 BPM，4/4，4 小节 | 01 的 146 网格 8 小节，原速放置 |
| P02 | Empty Hall / felt piano | 66 BPM，4/4，4 小节 | 02 的 132 网格 8 小节，保留完整衰减 |
| EP03 | Eighty Percent / electric piano | 104 BPM，4/4，4 小节 | 03 的短和弦起音重排与空拍 |
| V04 | Latch / 短弓小提琴 | 142 BPM，4/4，2 小节 | 04 的干燥切片和节奏性回答 |
| P05 | Worn Sleeve / 立式钢琴 | 84 BPM，4/4，4 小节 | 05 的自然演奏切片，留旧琴触感 |
| V05 | Loose Thread / 小提琴回答 | 84 BPM，4/4，4 小节 | 05 句间回答；实际主唱占位时删去当次回答 |
| SYN06 | Lime Lining / saw synth | 152 BPM，4/4，2 小节 | 06 音头 gate、八度位移与 stop-start |
| P07 | Blue Ink / 温暖钢琴 | 70 BPM，4/4，4 小节 | 07 的 140 网格 8 小节，完整指触与自然尾音 |
| VC01 | One of one / 人声作曲动机 | 146 BPM，3 音，一小节容器 | 01 的开头；07 改写中音后重唱 |

## 制作路径

先录制无鼓的完整乐句，保存原始 WAV，再另存编辑版。真人演奏、采样库渲染和 AI 生成素材按真实来源登记；不要把生成或 MIDI 渲染写成真人演奏。钢琴保留适量踏板与击键细节；吉他滑弦不是每个空隙都要出现；V04 的短弓与 V05 的连贯回答需使用对应奏法。

G01/P02/P07 的源速度是目标一半，源四小节时长等于目标八小节。不要因数字翻倍就把音频加速两倍。切点以实际音头和尾音为准；当前 CSV 的秒数只描述谱面，不能作为真实波形的测量结果。

01：G01 第一遍保持较完整，在主歌只抽两个音头做回答，给 dense rhyme block 留空间。

02：P02 的向前起音为主体；只复制衰减做少量 reverse swell，别把每个句首都吸满。早餐段减少反向处理，保留同一琴的较近距离。

03：EP03 音头可交替保留/删除；别把乐器的切分复制成每一句主唱的切分，两个声部要能对话。

04：V04 以弓头和短音作为节奏材料；同一录音的小片段换顺序比一层持续弦乐更能兑现 sampling。808 占最低频，小提琴不额外叠低根音。

05：P05 的自然衰减不必切齐固定网格；先保护主唱的话，再安排 V05。桥段可只保留琴凳与手指离键的真实余声，前提是录音里确实存在，不能假称已录 foley。

06：SYN06 是原创合成器序列，不是外来唱片样本。主唱进入时缩减 saw 的音数或音区，再用均衡器处理遮挡。

07：P07 与和声转位一起建立较温暖的结尾。VC01 的中音从 B3 到 C4；两端为等音同高。末音门限为新句缩短，这是 variation，若实际另唱就登记新的 take。

## 取得纯器乐备选的文字提示

用于 Suno 或其他实际可用生成器的探索，不能保证复现 MIDI。需要精确音符时先用合适音源渲染或请演奏者录制，再将音频作为参考。

```text
Solo clean picked electric guitar, C-sharp minor, 73 BPM, a short four-bar phrase with separated attacks, a small rising answer and room for natural string decay. Dry intimate recording, instrumental source material.
```

```text
Solo felt piano, F-sharp minor, 66 BPM, a four-bar descending phrase with sparse left-hand roots, soft natural attacks and long clear pauses. Complete decay, small dry room, instrumental source material.
```

```text
Solo electric piano, A major, 104 BPM, syncopated short arpeggios and warm extended harmony, a four-bar phrase with open space after each gesture. Dry, playful, instrumental source material.
```

```text
Solo violin, D minor, 142 BPM, two bars of short detached bow attacks, a minor arpeggio and a brief descending answer. Dry close recording, clear natural bow changes, instrumental source material.
```

```text
Solo upright piano, G minor, 84 BPM, a four-bar soulful motif, gentle uneven human touch, sparse left hand, clear damper detail and a complete final decay. Instrumental source material.
```

```text
Solo violin, G minor, 84 BPM, short lyrical answers separated by long rests, restrained dynamics and natural bow changes. A four-bar phrase, dry recording, instrumental source material.
```

```text
A short gated saw-synth sequence, E minor with bright major-color harmony, 152 BPM, bouncy two-bar motif, separated attacks and sudden rests, clean low end, instrumental source material.
```

```text
Solo warm piano, D-flat major, 70 BPM, a four-bar phrase with gentle gospel-colored inversions, lyrical right hand, sparse bass and complete natural releases. Intimate and human, instrumental source material.
```

VC01 更适合由实际主唱唱出 One of one 后保留干声。没有必要为了做一个三音 tag 强行制造另一位歌手身份。
