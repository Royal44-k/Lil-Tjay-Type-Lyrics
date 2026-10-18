# DON'T HANG UP — Suno 手动创作提示词包

适用：用户自行在浏览器操作 Suno。整理日期：2026-09-17。本包不连接账户，也不提交生成。

## 推荐填入方式

使用 Custom / Advanced 中的自定义歌词方式，把 STYLE.txt、LYRICS.txt、EXCLUDE.txt 分别粘贴到对应输入框。标题为 DON'T HANG UP，Instrumental 关闭。不要把中文制作解析一起塞进歌词框。章节方括号是演唱与编排提示，不是歌词；它们不能保证被逐项执行。

官方说明：[输入自己的歌词](https://help.suno.com/en/articles/2415873)、[Exclude](https://help.suno.com/en/articles/3161921)、[Vocal Gender](https://help.suno.com/en/articles/10153473)。

## 主题、人物和氛围

主题是“从需要别人陪伴，到学会陪伴别人”。主角是正在上升的音乐人：能让观众唱出他的歌词，却不习惯对亲近的人说自己累了。故事的终点是一件很小的事：他终于能关掉电视睡觉。

听感从深夜酒店的冷光，走向清晨厨房的暖光。男声近、干、带呼吸；背景深、宽、留空间。Verse 中的情绪通过擦掉短信、未拆膜的沙发、站着吃饭和电话那头的椅子声逐渐显现。结尾保留一点未解决的生活压力，声音里多一些信任。

## 两个人声的角色

男声是叙述者。明亮、略有颗粒感的男高音，以美式英语自然连读；Verse 保持 rap 的节奏主动性，Hook 才拉长元音。修音让旋律稳定，但希望仍能听见重音、气息和句尾力度变化。

女声是简短的陪伴与回应。完整母句：
If your words run out / I'll be listening.

这里的“采样”是希望生成一条原创女声，并形成切片式的听感；文本提示本身不代表已经导入了真实采样录音。开头、Bridge 给完整句；男声 Hook 的停顿放短回答。女声不要从头到尾盖住主唱，也不要接管整段 Verse。

## 旋律与演唱

主 Hook 的起始动机为 G3-C4-Eb4 / G3-Bb3-C4。DON'T / HANG / UP 是三个清楚的重音，前两词短、UP 长。第二次标题在结尾回落，既重复又有一点变化。最终 Hook 改成 I WON'T HANG UP，I 可作弱起，保持 WON'T / HANG / UP 的强拍识别。

Verse 建议在 G3-Eb4 附近展开，主要使用重复音、小幅级进与节奏切分；四行一组时，在第 4 行末尾留下换气位置。Hook 可上到 G4；女声母句位于 G4-Eb5。音域和逐音符要求用于描述写作方向，Suno 可能重新演绎。若旋律保留是首要目标，使用自有旋律参考音频比只输入音名更明确，但仍需试听核对。

## 韵脚与叙事节奏

- Verse 1 第一组：light / flight / lines / mine，围绕 /aɪ/，从碎片式观察转到“台上会表达，电话里语塞”。
- 第二组：hearts / part，her / hurt；先是转账和删消息，再跨行写母亲的劳累。
- 第三组：black / back / bad / cracks，/æ/ 连续近韵；加入对方的直接引语与反问，让叙述者承担责任。
- 第四组：head / yet / breath / said，/ɛ/ 韵；准备好的解释被一句日常关心打断。
- Verse 2 第一组：plastic / habits / fabric / standin'，用 /æ/、/ɪ/ 近韵与生活物件制造画面。
- 第二组：straight / playin' / place / safe，/eɪ/ 韵；新住处与旧焦虑并置。
- 第三组：three / me / breathe / speak，/iː/ 韵；把“我成长了”写成真正等对方开口的动作。
- Hook：up / stuck / shut / fuck up / rush，共同的 /ʌ/ 元音有利于反复与拖音。近韵依靠重读元音成立，无须每一组都做成完全韵。

## Beat 和编排

148 BPM，按 74 BPM 半拍感演唱，C minor。Cm9-Abmaj7-Ebmaj7-G7sus4/G7 的和声给标题保留回到 C 的落点。柔和键盘和少量拨弦作为高频记忆；808 温暖、集中，滑音只在转折处出现。军鼓使用半拍重心；hat 轻而有切分，滚奏放在句尾。

曲式目标：Intro 4 / Hook 16 / Verse 1 16 / Pre 4 / Hook 16 / Verse 2 16 / Bridge 8 / Final Hook 16 / Outro 4。按 148 BPM 约 2:42，加尾音。Suno 输出不一定严格遵循小节或时间；先保证段落和表演完整。

- Intro：女声母句、键盘，短开场。
- 首 Hook：尽早进入主唱，鼓与低音确立节奏，标题容易听清。
- Verse 1：减少装饰，句式可密可疏；母亲段落收低力度。
- 第二次 Hook：保持核心旋律，添加少量真正复唱式的厚度。
- Verse 2：前四行减少 hat，让画面靠近；听对方说话时旋律稍打开。
- Bridge：撤鼓，女声完整回来；男声唱 Call me tomorrow / Even if you're alright。
- Final Hook：稍加宽度、和声和复唱，核心变化是从请求到承诺。
- Outro：Listening / Yeah, I'm here，留短尾音。

## 设置起点

Title: DON'T HANG UP
Mode: Custom / Advanced with your own lyrics
Instrumental: Off
Preferred model: v6 if available; otherwise the model included in your plan
Variety: 0 for the first pass, if shown
Vocal Gender: Male for the primary lead; female refrain is specified in Styles and Lyrics
If the interface supports leaving Vocal Gender unselected, compare that setting if the female part disappears
Weirdness: 35% only if this control is present (creative starting point, not an official preset)
Style Influence: 70% only if this control is present (creative starting point, not an official preset)
Audio Influence: leave unused without an audio reference
Max Mode: optional for a later refinement, not necessary for the first exploration
Length target: about 2:40-3:10, expressed as a creative target rather than a guaranteed duration

Variety 设为 0 用于保留手写风格标签，依据当前官方 v6 说明。35% Weirdness 和 70% Style Influence 是本作品的试验起点，未在本项目生成中验证；若你的界面没有这些控件，直接跳过，不能将旧教程的界面当作当前必选项。

Vocal Gender 只帮助引导主要声线，不能可靠锁定每个段落的男女声。优先用清楚的角色说明和歌词段落标记表达分工。

官方来源：[v6 FAQ](https://help.suno.com/en/articles/13924481)、[Creative Sliders](https://help.suno.com/en/articles/6141377)。

## 可选：使用已有旋律导唱作参考

上级目录中有 32 秒的 DONT-HANG-UP-v2-HOOK-PREVIEW-NO-VOCALS.wav。它是自有创作的乐器导唱：电钢琴代表男声旋律，较高的铃音代表女声母句，文件本身没有演唱。

如采用音频参考，附加说明见 REFINEMENT-PROMPTS.md。首轮也可以只用文字与歌词，让 Suno 提出自己的演唱旋律。不要将乐器导唱的合成音色误当成想保留的人声质感。[音频上传官方说明](https://help.suno.com/en/articles/6141569)

## 试听时如何选版本

先听标题是否一遍就能记住，再听 Verse 里 Mom、I'm tired、stepped back、TV 等词是否自然清楚。检查女声是否主要出现在主唱空隙、两段 Verse 是否都完整唱出、最终 Hook 是否确实改成 I won't。最后再评估低音与高频是否舒适。

每轮只改一个主要问题。针对性修订提示见 REFINEMENT-PROMPTS.md；修订后仍需复听，生成式编辑不保证其余部分完全不变。
