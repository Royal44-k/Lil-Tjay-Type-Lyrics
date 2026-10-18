# 器乐、采样母句与 voice reuse 提示词

这些方向用于单独取得制作素材。现有 `samples/` 内是 MIDI、MusicXML 与 CSV；没有已录制的钢琴、提琴或歌手干声。具体音符以源谱为参考，文本生成不保证精确复现。生成后仍需选取实际可用乐句并记录来源。

## V01｜两张唱片共享的原创女声母句

**Lyrics**

```text
There's still life in me.
```

**Style / recording direction**

```text
One adult female voice singing the exact phrase Theres still life in me in a natural close a cappella take. F-sharp minor, 96 BPM reference pulse. Five clear syllables, a gently descending melodic shape, warm human tone and a complete final breath. Begin promptly, leave a little room before and after the phrase, with a dry small-room character and restrained vibrato. Keep it simple enough to cut into syllables later.
```

**Exclude**

```text
drums, bass, instruments, backing choir, spoken narration, long introduction, vocal runs, heavy reverb
```

作曲音高为 C#5–C#5–A4–F#4–E4；正式录制时参考 `samples/V01/`。如生成结果自带伴奏或长串重复，不能直接登记成满足规格的干声 take。严格复现时，让实际歌手或合适音源实现源谱，再得到可上传的音频。不要把 MIDI 文件当作已确认支持的 Suno 音频输入。

### 取得一条可用原 take 之后

| 目标曲目 | 采用片段与处理意图 |
|---|---|
| 原版 NO RECEIPT | still 短切片，反拍、短包络、受控失真 |
| 原版 FAST FORWARD | life / in / me 尾音，计划升五半音到 B minor 语境，只在句间出现 |
| 原版 ROOM TONE | 恢复自然声，尾奏完整唱句；96 到 92 的适配以实际录音决定 |
| SECOND LIFE，两张专辑共用 | 原五音不变，进入 A major 和声；男声 Not brand new 后女声回答 |
| Split Sheet Remix | still 单片，用量更少，为三人叙述留白 |
| Night Shift Remix | 少量尾音回声；与 D minor 的实际音高配合另行检查 |
| Open Door Remix | 气息或短尾音作过渡；主对话必须清楚 |

新增四曲各有自己的器乐识别点，不要求全部放同一女声句。相似声线、同一旋律、同一段录音分别记录。若模型重新唱了同一句，它就是新 take；严格复用需在可编辑音频的工程中使用同一源 WAV。

## 原版器乐母素材

### G01｜破音吉他源

```text
Instrumental solo electric guitar, F-sharp minor, 154 BPM reference grid. A short original punk-influenced power-chord phrase with sharp muted attacks, small rests and controlled amplifier grit. Clear separate gestures for chopping into a trap beat. Dry close recording, complete releases, no continuous wall of distortion.
```

### P01｜电钢琴源

```text
Instrumental solo electric piano, 92 BPM, F-sharp minor moving through B minor nine, E thirteen and A major nine. A short human-played phrase with open voicings, clear key attacks, gentle sustain and generous gaps. Warm small-room character, restrained bass notes, complete decay.
```

### B01｜自演鼓 break 的备选方向

```text
Instrumental acoustic drum kit only, 144 BPM, a short human-played break with dry kick, snare, soft ghost notes and restrained hi-hat. Clear accents and small timing variations, suitable for chopping and rearranging into a soulful trap bridge. Keep the room compact and the ending complete.
```

G01、P01、B01 在原版中是待录计划，当前没有对应现成录音。将 P01 用于同名曲时选择共享音高的片段并重配和声；若重新演奏 A major 版本，登记为新演奏。B01 若由生成器得到，要写“生成鼓段”，不能登记成真人自演。

## PLUS 新增器乐源

### P01R / STR01R｜Split Sheet Remix

分别制作，得到两条独立素材后再编排。

```text
Solo dry piano, F-sharp minor, 140 BPM, two bars of clipped minor-arpeggio attacks with deliberate gaps. A low-to-middle register phrase, light mechanical detail, short releases and room for a separate bass instrument. Instrumental source material.
```

```text
Solo pizzicato violin, F-sharp minor, 140 BPM, two bars of short bright replies separated by silence. Light plucked attacks, restrained dynamics, dry recording and no sustained string pad. Instrumental source material.
```

### P02｜IVORY HOURS / Night Shift Remix

```text
Solo upright piano, D minor, 88 BPM. An original four-bar motif with a hesitant descending right hand, sparse low notes and small pauses. Natural damper and key detail, human touch, dry intimate room and a complete final decay. Instrumental source material.
```

IVORY HOURS 可先展示完整演奏，再拆成短片；Night Shift Remix 采用音头或短句重排到 138 网格，避免默认整段大幅拉伸。

### V02｜COUNTERSTEP

```text
Solo violin, G minor, a short four-bar waltz phrase in three-quarter time at 108 BPM. Clear short bow attacks, a rising minor arpeggio and a small descending reply. Natural bow changes, dry room, audible triple-meter lilt and a clean phrase ending. Instrumental source material.
```

源四小节约 6.67 秒，等于 144 BPM 四拍的四小节。可以保持音频原速、改用四拍鼓重设重音。`samples/V02/TARGET-144-4-4.mid` 是对齐参考；实际生成如果没遵守三拍，先记作不符合源规格的候选。

### P03 / V03｜SOFT LANDING

```text
Solo soft felt piano, E-flat major, 76 BPM. A sparse four-bar arpeggio with warm extended harmony, gentle attacks, tactile key detail and generous pauses. Intimate dry room, human timing and a complete natural release. Instrumental source material.
```

```text
Solo pizzicato violin, E-flat major, 76 BPM. Very short paired high-note replies separated by long silences across four bars. Delicate plucked attacks, modest dynamics, dry recording and complete note releases. Instrumental source material.
```

### P04 / V04｜LAST TRAIN, FIRST LIGHT

```text
Solo piano, E minor with relative-major warmth, 78 BPM. A rising four-bar ostinato opening into a lyrical answer. Steady human touch, restrained left hand, clear note attacks, natural sustain and a complete ending. Instrumental source material.
```

```text
Solo lyrical violin, E minor, 78 BPM. A four-bar phrase of short melodic answers with natural bow changes and long spaces between gestures. Warm middle register, restrained expression, dry room and full releases. Instrumental source material.
```

源四小节在 156 BPM 网格占八小节，时长仍约 12.31 秒。不要把播放速度翻倍。主唱延长一句时，优先删去该处提琴回答。

## 源素材通用 Exclude

除 V01 使用其专用排除项外，可从下面按需要删减。做 B01 鼓段时不排除 drums。

```text
vocals, spoken words, choir, full-band arrangement, cinematic build, long introduction
```

若制作独奏器乐，另行加 drums 和 bass；不把所有排除词机械堆进每份提示。生活声 F01（衣料、椅子、杯碟、门扣）适合自行录制短素材，当前没有交付，也不要求用音乐生成器代替。

保存原始 take、编辑 take、切片版；每个实际 source 填明录音/生成方式、源文件、采用片段与处理。不要用谱面时间替代实际波形切点。
