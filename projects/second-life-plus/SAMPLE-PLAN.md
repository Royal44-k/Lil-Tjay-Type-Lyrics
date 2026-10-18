# 乐器采样与素材复用计划

## 当前资产是什么

本包交付原创 MIDI / MusicXML 作曲草案、切片方案与素材账本。**尚未录制钢琴、小提琴或 V01 人声；没有现成的音频采样包。** MIDI 里的 General MIDI 音色仅便于辨认声部，不能代表最终音质、奏法或真人演唱。

演奏录音、授权音色库渲染、Suno 生成的器乐录音是三种不同来源。选用哪一种，就按真实来源登记 performer / source_audio / license_document 等字段；不能把生成的录音写成真人演奏，也不能把只有谱的材料写成已录 take。

## 素材清单

| ID | 名称 / 乐器 | 源速度与长度 | 用途 | 已交付 |
|---|---|---|---|---|
| V01 | There's still life in me / 原创女声旋律 | 96 BPM，4/4，一小节 | 01/03/05 的碎片；08 完整回答 | 上一版 MIDI 与音节表原样保留 |
| P01R | Ledger Keys / 短钢琴 | 140 BPM，4/4，两小节 | NO RECEIPT Remix；ROOM TONE Remix 可重演改和声 | MIDI、MusicXML、CSV |
| STR01R | Margin Notes / 小提琴拨弦 | 140 BPM，4/4，两小节 | NO RECEIPT Remix | MIDI、MusicXML、CSV |
| P02 | Uneven Key / 立式钢琴 | 88 BPM，4/4，四小节，约 10.91 秒 | IVORY HOURS；FAST FORWARD Remix | 双手 MIDI、MusicXML、CSV |
| V02 | Counter Waltz / 独奏小提琴 | 108 BPM，3/4，四小节，约 6.67 秒 | COUNTERSTEP | 源三拍谱、144 四拍对齐 MIDI、CSV |
| P03 | Lamplight Keys / 弱音钢琴 | 76 BPM，4/4，四小节，约 12.63 秒 | SOFT LANDING | 双手 MIDI、MusicXML、CSV |
| V03 | Small Gestures / 小提琴拨弦 | 76 BPM，4/4，四小节 | SOFT LANDING 句间回答 | MIDI、MusicXML、CSV |
| P04 | Platform Window / 钢琴 | 78 BPM，4/4，四小节，约 12.31 秒 | LAST TRAIN, FIRST LIGHT | 双手 MIDI、MusicXML、CSV |
| V04 | Daybreak Answer / 独奏小提琴 | 78 BPM，4/4，四小节 | LAST TRAIN, FIRST LIGHT 句尾回答 | MIDI、MusicXML、CSV |
| G01/P01/B01 | 上一版吉他/钢琴/自演鼓 break 方案 | 依原方案 | SECOND LIFE | 保留制作计划，未冒充已录素材 |

## 先演奏，再切片

钢琴：先保存完整无鼓演奏。踏板与制音器声适量，低音与右手独立导出参考轨；正式 take 仍保留整体手感。录音若存在强底噪，先另存处理版，不覆盖原文件。将衰减交给耳朵判断，不能把每个样本机械切成同长方块。

小提琴：V02 用短弓起音，保留必要的连贯方向；V03 是拨弦，不能把长弓音简单压短就称为同种奏法；V04 用完整乐句与自然换弓。采样库渲染时选择相应奏法、调整连音与力度，而不只更换一个 GM 音色名。

每份音频至少保存 `source dry`、`edited source`、`chop map` 三种状态。不同变调与拉伸版本另存，文件名如 `P02_UnevenKey_take01_dry_native.wav`；实际采样率、位深与演奏者另入账本。

## 分曲处理

**01 NO RECEIPT Remix**：P01R 的琴键起音按短音切割，句内以稀疏重复维持冷感；STR01R 在主唱尾字之后回应。808 进来时移走钢琴最低根音。V01 的 still 只占间隙，不用高音连射掩盖多声部接力。

**02 IVORY HOURS**：先展示 P02 的 A-B-C-D 四个一小节区域。主歌将区域继续拆成两拍或一拍碎片，采用 C-A-B 的不完整顺序；Hook 恢复较长片段。最后保留衰减，让记忆里的缺口能够被听见。精确切点以实际 take 为准，当前秒数不是已测波形标记。

**03 FAST FORWARD Remix**：P02 的 D minor 身份保留，按音头重排到 138 网格。不要默认把 88 的整段直接拉到 138；选择短句、留出残响，可以降低大幅时间处理的伪影。需要女声 Hook 空间时，让琴声停一下。

**04 COUNTERSTEP**：108 BPM 的三拍源一小节与 144 BPM 的四拍目标一小节，都是 1.667 秒。四小节总时长一致；本包 `TARGET-144-4-4.mid` 以 4/3 的拍位映射证明这种关系。实际音频可以原速放置；这是重设重拍关系，不是把录音快放。Bridge 暂时减少四拍鼓，让听众听出原来的摆动。

**05 ROOM TONE Remix**：若复用 P01R 的真实录音，须在 A major / F#m9 等和声中选择合适音片，不能整个和弦片无判断照搬。需要的不同转位可另录并登记为 P01R-A；气息采样在句间即可，避免把两人的交谈切碎。

**06 SOFT LANDING**：P03 的短琶音作为柔软循环，V03 在第 2.5、3 拍等预留位置回答。人声若延长，就让提琴退后或删掉该次回答。两种乐器的自然高频胜过持续铺满的亮垫。

**07 LAST TRAIN, FIRST LIGHT**：78 BPM 源四小节与 156 BPM 目标八小节时长一致。原速素材能维持演奏者的手感，鼓用双倍网格；无需为了匹配数字将录音加速一倍。V04 仅在尾句空隙和桥段出现，最终 Hook 可增加一个真正的对位，不把主唱旋律再抄一遍。

**08 SECOND LIFE**：按上一版方案。新作里出现更多钢琴或提琴，不构成修改这首保留曲的理由。

## 在 Suno 中取得备选器乐素材

如果先做纯 Suno 路线，可用下列方向生成无主唱的器乐片段，再选择完整乐句。**这会产生备选新演奏，不能保证与 MIDI 一致。** 记录实际音高和时长后再切；需要严格复现谱面时，应将 MIDI 交给演奏者或合适音源渲染。

P02：
```text
Solo upright piano, D minor, 88 BPM, intimate four-bar motif with a hesitant descending right hand and sparse low notes. Natural felt and damper detail, human timing, clear pauses and a complete final decay. Instrumental source material, small dry room.
```

V02：
```text
Solo violin, G minor, a short four-bar waltz phrase in three-quarter time at 108 BPM. Clear short bow attacks, a rising minor arpeggio followed by a small descending answer, natural bow changes, dry room. Expose the triple-meter lilt and finish the phrase cleanly.
```

P03 / V03 分开生成或录制：
```text
Solo soft felt piano, E-flat major, 76 BPM, sparse four-bar arpeggio with warm extended harmony and generous pauses. Intimate, tactile, gentle attack and natural decay. Instrumental.
```
```text
Solo pizzicato violin, E-flat major, 76 BPM, very short paired high-note replies separated by long silences. A few delicate gestures in four bars, dry and clear. Instrumental.
```

P04 / V04 分开生成或录制：
```text
Solo piano, E minor with relative-major warmth, 78 BPM, a rising four-bar ostinato that opens into a lyrical answer. Steady human touch, restrained left hand, natural sustain, complete phrase ending. Instrumental.
```
```text
Solo lyrical violin, E minor, 78 BPM, short phrase-ending answers with natural bow changes and long spaces between them. Warm middle register, restrained expression, dry room, complete releases. Instrumental.
```

生成结果若带鼓、带歌声、不是所需拍号，先将它记作不符合该 source 规格的候选。不要为了保留一次生成而篡改原方案的验收记录。
