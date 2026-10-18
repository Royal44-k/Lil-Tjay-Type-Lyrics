# 2007.net — 编曲、旋律与演唱制作总谱说明

这是可进入 demo 制作的文字与动机谱。七首都有完整歌词、和声方案、精确核心 Hook 动机与段落计划；主歌全旋律、完整伴奏和最终演唱仍需编曲/录音实现。MIDI 用通用钢琴事件表示音符，不是人声录音。

所有拍号为 4/4。BPM 指四分音符；半拍感不改变小节计算。CSV 的 start_beat 从 0 开始。休止已保留在 MIDI 总长度中；Hook MIDI 只涵盖下文列明的标题动机，后续句子的方向另列。

数字感主要作用于背景素材和角色分身，主体歌词保持可懂。每首一次只突出一件标志性音色，让鼓、低频、主唱与采样各有空间。

## 01 — SCREEN NAME

melodic trap / dream R&B · 142 BPM · F# minor · 132 小节 · 计划 3:43

### 人物、演唱与 Flow

成年男声，轻微颗粒的中高音；女声仅作开场、尾奏与稀疏回答。男主句末保持真声，少量高音轻混声。

Verse 每行两小节。前八行较整齐，后八行将关键词提前半拍；Pre 每行一小节；Hook 每行两小节，name / slow / glow 留长元音。

### 韵脚与句法

sink/lip 为短 i 近韵；day/say、line/time 是完整落点。unfinished/in it 以内部近韵推进，take/fake 把情节收拢。Hook 主元音为 /oʊ/，screen name 是独立标题口号。

### 和声与编排

Verse: F#m9 | Dmaj9 | Aadd9 | E6. Chorus: F#m9 | Dmaj9 | Amaj9 | Eadd9; one chord per two bars.

一个细亮 FM pluck，短而有音高的 808，拍三军鼓与少量提前的小 hi-hat。吉他弦噪是原创录音计划。Verse 2 开头撤掉 pluck，听清现实房间的细节。

### 原创 Hook 动机

文本：Say my screen name Say it real slow

音高：C#4 – E4 – F#4 – A4 – G#4 – F#4 – E4 – C#4

长度：4 小节。逐音节拍与时值见 HOOK-NOTES.csv，MIDI 包含句尾休止。

前两行的四小节动机在第 5–6 行原样回归。第 3–4 行降到 F#4–E4–C#4 的窄音域，第 7–8 行从 E4 上行到 G#4 后落 F#4，保持每个字可懂。

### 段落表

段落 | 起始小节 | 小节数 | 歌词行数 | 每行占用小节
|---|---:|---:|---:|---|
|Intro - female voice, close and dry|1|4|2|2 2|
|Chorus - male melodic lead|5|16|8|2 2 2 2 2 2 2 2|
|Verse 1 - male, conversational rap|21|32|16|2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2|
|Pre-Chorus|53|4|4|1 1 1 1|
|Chorus|57|16|8|2 2 2 2 2 2 2 2|
|Verse 2 - male, more rhythmically open|73|32|16|2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2|
|Bridge - half-sung|105|8|4|2 2 2 2|
|Final Chorus|113|16|8|2 2 2 2 2 2 2 2|
|Outro - female, unprocessed|129|4|2|2 2|
## 02 — TOP EIGHT

digicore / rage / melodic rap · 156 BPM · B minor · 120 小节 · 计划 3:05

### 人物、演唱与 Flow

男声第一段急于争辩；女声第二段低一点、咬字更干、更直接。第一遍男主 Hook，第二遍女主 Hook，最后共唱。Bridge 逐行男/女交替。

Verse 每行两小节，第一小节可用十六分音符连击，第二小节空出后半拍。四行 Hook 各两小节；最后八行 Hook 共十六小节。Bridge 八行各一小节。

### 韵脚与句法

bus/us、checked/contact 是带口语落点的近韵；name/entertained、shoes/news、feet/seat 保持连贯。女段 coat/wrote、week/speak、shot/not 成对回应。Hook eight/day/page/face 围绕 /eɪ/。

### 和声与编排

Bm(add9) | Gmaj7 | Dadd9 | A(add9), one chord per two bars in the hook; use B/F# pedals under dense rap.

明亮失谐 saw 只占高频，808 单声道短滑音，切碎的自录无词喊声取代拥挤 lead。Break 切四个两小节鼓模块，第三模块留空一拍；恢复时先让女声进。

### 原创 Hook 动机

文本：Take me out your top eight

音高：F#4 – F#4 – A4 – F#4 – E4 – B3

长度：2 小节。逐音节拍与时值见 HOOK-NOTES.csv，MIDI 包含句尾休止。

首行两小节六音动机为识别点。Keep me in your day 用 E4–F#4–E4–D4–B3 回答；front page 抬到 A4，最后 face-to-face 回到 F#4–D4–B3。不要把每行都唱成同一重音。

### 段落表

段落 | 起始小节 | 小节数 | 歌词行数 | 每行占用小节
|---|---:|---:|---:|---|
|Intro - male, clipped|1|4|2|2 2|
|Chorus - male chant with female responses|5|8|4|2 2 2 2|
|Verse 1 - male rap|13|32|16|2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2|
|Chorus - female takes the lead|45|8|4|2 2 2 2|
|Verse 2 - female, dry and direct|53|32|16|2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2|
|Break - wordless chopped voices|85|8|0|instrumental|
|Bridge - male and female alternate|93|8|8|1 1 1 1 1 1 1 1|
|Final Chorus - shared|101|16|8|2 2 2 2 2 2 2 2|
|Outro - male|117|4|2|2 2|
## 03 — LOW-RES KISS

psychedelic R&B / singing rap · 94 BPM · D major · 56 小节 · 计划 2:23

### 人物、演唱与 Flow

成年女中音为主，有笑意但不持续气声；成年男声第二段与低声和声。亲密来自距离、换气和回答，不靠大段转音。

Verse 十二行各一小节，采用说话式切分；Pre 两行各两小节；Hook 八行各一小节。kiss / this 长元音，distance 两音节，不硬塞多音转音。

### 韵脚与句法

cup/up、ear/disappear、pose/nose 把镜头逐步拉近。男段 again/friend、shines/lines、key/be 为宽松近韵。Hook kiss/this/distance 与 us/enough 交替，不要求每句尾都同韵。

### 和声与编排

Dmaj9 | A/C# | Bm9 | Gmaj9, one chord per bar. Bridge: Em9 | Gmaj7 | D/F# | Asus4.

原创 K01 电钢琴母旋律，反转只处理尾部；轻 sub、干 rim、偏后的 closed hat。左侧短 tremolo 吉他只在两句之间回答。母句 VQ01 的 A4/C#5 在 D major 中作 5/7，避免连续占主唱音域。

### 原创 Hook 动机

文本：Low res kiss Keep it like this

音高：F#4 – A4 – B4 – A4 – F#4 – E4 – D4

长度：2 小节。逐音节拍与时值见 HOOK-NOTES.csv，MIDI 包含句尾休止。

前两行两小节动机后，第 3–4 行停留 A4–F#4–E4；第 5 行 Leave it blurry 从 B4 回 A4；最终 enough 落 F#4，不用高音堆砌提升。

### 段落表

段落 | 起始小节 | 小节数 | 歌词行数 | 每行占用小节
|---|---:|---:|---:|---|
|Intro - female, smiling|1|4|2|2 2|
|Verse 1 - female singing rap|5|12|12|1 1 1 1 1 1 1 1 1 1 1 1|
|Pre-Chorus - female|17|4|2|2 2|
|Chorus - female lead, male low harmony|21|8|8|1 1 1 1 1 1 1 1|
|Verse 2 - male melodic rap|29|12|12|1 1 1 1 1 1 1 1 1 1 1 1|
|Bridge - duet, intimate|41|4|4|1 1 1 1|
|Chorus - duet|45|8|8|1 1 1 1 1 1 1 1|
|Outro - female|53|4|2|2 2|
## 04 — POP-UP HEAVEN

hyperpop / rage / underground rap · 160 BPM · C# minor · 104 小节 · 计划 2:36

### 人物、演唱与 Flow

男主干而有冲劲，广告声由同一成年主唱另录台词后升 formant。广告声只是角色，不采用品牌或真实人物声纹。最后电话声恢复正常。

Verse 1 每行一小节、短促落拍；Verse 2 每行两小节，长句用十六分音符短冲刺后留空。Hook 八行各两小节，click-click 各一次短音。Bridge 八行各一小节。

### 韵脚与句法

square/fare、jaw/flaws、frame/name 与 chest/rest，先用易辨双行韵建立弹跳，再用 expensive / picture / bigger 等内部辅音提升密度。歌词中的阶级压力先被承认，转折才有重量。

### 和声与编排

C#m9 pedal in verses; C#m | Amaj7 | E | B in chorus, one chord per two bars. Break stays on C#.

原创 S01 四音叮当素材被切成不同尾长。宽失真 synth 与干主唱交替，不同时填满中频。Break 的最后一小节完全停鼓；Final Hook 前四行只留主唱+短 kick，后四行归还完整编排。

### 原创 Hook 动机

文本：Pop up hea ven Let me in

音高：G#4 – G#4 – E4 – C#4 – E4 – F#4 – G#4

长度：4 小节。逐音节拍与时值见 HOOK-NOTES.csv，MIDI 包含句尾休止。

Pop-up heaven 四音下行后，let me in 三音回升；第二组 one more window/same old skin 复用节奏并降八度。click-click 不做长音；exit 的第二音节短收后留空半拍。

### 段落表

段落 | 起始小节 | 小节数 | 歌词行数 | 每行占用小节
|---|---:|---:|---:|---|
|Intro - pitched version of the lead voice|1|4|2|2 2|
|Verse 1 - male, clipped rap|5|16|16|1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1|
|Chorus - tight melodic chant|21|16|8|2 2 2 2 2 2 2 2|
|Verse 2 - male, accelerating|37|32|16|2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2|
|Break - instrumental, abrupt silence on the last bar|69|8|0|instrumental|
|Bridge - low, nearly spoken|77|8|8|1 1 1 1 1 1 1 1|
|Final Chorus - first half dry, second half full|85|16|8|2 2 2 2 2 2 2 2|
|Outro - unprocessed|101|4|2|2 2|
## 05 — DRAFTS AT 3:17

underground hip-hop / psychedelic R&B · 78 BPM · E minor · 64 小节 · 计划 3:17

### 人物、演唱与 Flow

成年低男声，像在空房间里反复读草稿。Verse 2 的 I was cruel 用接近说话的音高，拒绝靠和声替人物圆场。最后保留女声母句，其后无回答。

Verse 每行一小节，长句可在小节前半段十六分音符说完，后半段停顿；不要每句都拖字。Hook 八行各一小节，backspace 后短停。Bridge 八行各一小节。

### 韵脚与句法

off/lost、laugh/back、read/repeat 是口语近韵，bear/cared、debt/forget 更紧。Verse 2 用 wrong/on 的直白落句打断工整，以免道歉被韵脚美化。Hook seventeen/breathe/me/mean/screen 统一 /iː/。

### 和声与编排

Em9 | Cmaj7 | Gmaj9 | D6; one chord per bar, omit the third on selected D chords. Bridge stays sparse over E/B.

电钢琴两三个开放音、低音单音、软 kick 与刷感 rim。磁带速度晃动只在背景 return。VQ01 降两半音为 G4/B4，保留女性真人呼吸，不为她新增答复台词。

### 原创 Hook 动机

文本：Three se ven teen Back space breathe

音高：G3 – B3 – D4 – B3 – A3 – G3 – E3

长度：2 小节。逐音节拍与时值见 HOOK-NOTES.csv，MIDI 包含句尾休止。

前两行的 G3–B3–D4–B3 / A3–G3–E3 形成一次起落；All these words 限于 G3–A3–B3，none of me 落 E3。最后 crowded screen 从 B3 向 E3 下行，句后留气口。

### 段落表

段落 | 起始小节 | 小节数 | 歌词行数 | 每行占用小节
|---|---:|---:|---:|---|
|Intro - male, close|1|4|2|2 2|
|Verse 1 - male, measured rap|5|16|16|1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1|
|Chorus - restrained low melody|21|8|8|1 1 1 1 1 1 1 1|
|Verse 2 - male, pauses between thoughts|29|16|16|1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1|
|Bridge - spare spoken melody|45|8|8|1 1 1 1 1 1 1 1|
|Chorus - no ad-libs|53|8|8|1 1 1 1 1 1 1 1|
|Outro - sampled female question, then space|61|4|1|4|
## 06 — BURN THIS SUMMER

two-step / melodic rap / R&B · 132 BPM · A major · 128 小节 · 计划 3:53

### 人物、演唱与 Flow

女主 Hook，男主第一段，女主第二段，最后一起唱。女声有棱角、有笑意；她说自己的工作时保持笃定，不唱成安慰男主。

两段 Verse 每行两小节；句中用切分，别把每个字挤在一个小节。Hook 各行两小节；Post 四行各一小节；Bridge 四行各两小节；最后六行 Hook 共十二小节。

### 韵脚与句法

sun/one、mix/bit、tees/knees、pass/past、behave/brave 与 pen/then 构成松紧变化。女段讲工作选择时使用 take/break 的近韵保留自然口语，再由 time/rhyme 拉回。Hook track/back、bad/had 简短可合唱。

### 和声与编排

Amaj9 | E/G# | F#m9 | Dmaj9, one chord per two bars in hooks; piano source notes reharmonized over this progression.

K01 原创电钢琴切音头到 132 的 two-step 网格；不用整段机械提速。带音高的弹性 bass、shuffle hat、干 claps，允许原创笑声在 snare 前出现一次。尾奏留 road-noise 录音计划，声音要短且不抢字。

### 原创 Hook 动机

文本：Burn this sum mer Track by track

音高：E4 – F#4 – A4 – A4 – G#4 – F#4 – E4

长度：4 小节。逐音节拍与时值见 HOOK-NOTES.csv，MIDI 包含句尾休止。

burn-this-sum-mer 四音上行趋平，track-by-track 三级下行。If the disc starts skipping 用短音符；back 拉长。最终两行在 A4–G#4–F#4–E4 内下落，收在 A3 或 A4。

### 段落表

段落 | 起始小节 | 小节数 | 歌词行数 | 每行占用小节
|---|---:|---:|---:|---|
|Intro - female, spontaneous|1|4|2|2 2|
|Chorus - female lead, male answer|5|16|8|2 2 2 2 2 2 2 2|
|Verse 1 - male, buoyant melodic rap|21|32|16|2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2|
|Post-Chorus - female and male|53|4|4|1 1 1 1|
|Verse 2 - female, playful then direct|57|32|16|2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2|
|Chorus - shared|89|16|8|2 2 2 2 2 2 2 2|
|Bridge - shared, open space|105|8|4|2 2 2 2|
|Final Chorus - shared|113|12|6|2 2 2 2 2 2|
|Outro - female|125|4|2|2 2|
## 07 — 2007.NET

alternative hip-hop / soulful R&B · 86 BPM · F# minor / A major chorus · 68 小节 · 计划 3:10

### 人物、演唱与 Flow

现在时的成年男声比 01 更低、更松；女声回放保持原 take，桥段男声回答新录。声线变化表达年龄和距离，不合成特定艺人的声音。

Verse 每行一小节，长句用说唱、短句留白；Hook 前八行各一小节；Final 追加 I was here / I'm still here 各两小节。Bridge 八行各一小节。片名开场读 Two thousand seven, dot net。

### 韵脚与句法

keys/CDs、end/them、eyes/night 的近韵像边看照片边说话。Verse 2 did/hid、blur/hurt、bars/far、kind/shrine 渐趋清楚。Hook here/disappear 是核心长元音，end/again 放松收束。

### 和声与编排

Verse: F#m9 | Dmaj9 | Amaj9 | E6. Chorus: Amaj9 | E/G# | F#m9 | Dmaj9. Same pitch collection, changed harmonic center; no tempo change.

复用 K01 的音高片段，在 86 网格重新演奏或编辑；若重新演奏另登记 take。干鼓、软 bass、少量真正弦乐答句可以在最后八小节出现，但不做电影式大结局。尾奏不放品牌关机声。

### 原创 Hook 动机

文本：I was here I was here

音高：F#3 – A3 – C#4 – E4 – C#4 – A3

长度：2 小节。逐音节拍与时值见 HOOK-NOTES.csv，MIDI 包含句尾休止。

两次 I was here 的第二次从更高的位置回落，再由 close the window 接 E4–C#4–B3。最后 moving back again 落 A3。终场新回答 I'm here 用 B3–F#3，听感应像说话后带出的旋律。

### 段落表

段落 | 起始小节 | 小节数 | 歌词行数 | 每行占用小节
|---|---:|---:|---:|---|
|Intro - male, present day|1|4|2|2 2|
|Verse 1 - male, reflective rap|5|16|16|1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1|
|Chorus - male lead, female harmony|21|8|8|1 1 1 1 1 1 1 1|
|Verse 2 - male, natural speech rhythm|29|16|16|1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1|
|Bridge - female archive and present male alternate|45|8|8|1 1 1 1 1 1 1 1|
|Final Chorus - lead and harmony|53|12|10|1 1 1 1 1 1 1 1 2 2|
|Outro - male, dry|65|4|2|2 2|
