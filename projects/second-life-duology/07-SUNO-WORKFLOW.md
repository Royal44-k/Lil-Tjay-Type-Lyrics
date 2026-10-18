# 两张专辑的 Suno 制作流程

本轮提供完整文本输入、原有旋律资料和制作辅助方向，由用户自行在浏览器中操作。没有调用账户、消费 credits 或提交生成。

## 先选正确版本

| 想制作的作品 | 输入总稿 | 数量 |
|---|---|---|
| SECOND LIFE 原版 | 04-SECOND-LIFE-SUNO.md | 4 首 |
| SECOND LIFE+ | 05-SECOND-LIFE-PLUS-SUNO.md | 8 首 |

两张共 12 个曲目位置、11 个不同歌曲版本。同名曲 SECOND LIFE 共用同一份原作，不加 Remix 后缀。PLUS 的另外三个旧标题必须带完整版本名，避免将原版歌词与 remix 声部设置混用。

## 第一轮：只用四栏

进入账户实际可用的自定义创作流程，把 Title、Style、Exclude、Lyrics 分别复制到对应字段。歌词已经展开完整重复段落，不需要自行补“副歌同上”。中文说明、宣传简介、角色代号和技术表格不粘到歌词框里。操作依据：[Custom lyrics](https://help.suno.com/en/articles/2415873)、[Exclude](https://help.suno.com/en/articles/3161921)。

2026-09-18 核查的 [v6 FAQ](https://help.suno.com/en/articles/13924481) 将 v6 用于较明确目标，v6-wild 用于探索；可用模型依账户方案而定。若界面有 Variety，可设为 0 来减少 Style 被改写。Max Mode 是会增加额度消耗的可选项，先比较普通候选再决定是否需要。此处不假设用户已开通某种方案。

一次生成一首。专辑介绍帮助理解方向，不作为“一次生成整张专辑”的超长提示。每首的主 Style 已包含其主要风格与编排，不再同时叠上整张专辑所有流派。

## 建议制作顺序

**原版**：先试 FAST FORWARD 的标题与停顿，再试 ROOM TONE 的自然低女声。找到可用声线后制作 V01 母句，再完成 NO RECEIPT 与同名曲的素材联系。

**PLUS**：先试 COUNTERSTEP 的提琴律动、Night Shift Remix 的女主 Hook 与双声部，再试 SOFT LANDING 的亲密尺度。随后做叙事密度更高的 Split Sheet Remix / IVORY HOURS，并完成另外两首。原同名曲已有选定音频时直接沿用。

这些是制作优先级，不改变专辑曲序，也不是已经完成的 A/B 听测。

## 其他提示词什么时候用

| 文件 | 用途 | 如何使用 |
|---|---|---|
| VOCAL-DIRECTION.txt | 角色、声区、咬字或表演不对 | 对已有候选做局部修正，或作为实际录音指导 |
| INSTRUMENTAL-STYLE.txt | 单独探索伴奏 | 使用账户支持的器乐创作方式；不放入完整歌曲歌词 |
| INSTRUMENTAL-EXCLUDE.txt | 防止纯伴奏出现人声 | 和器乐 Style 配套使用 |
| HOOK-REPAIR.txt | 标题不清楚、不易记、动机丢失 | 优先修副歌，保留已经满意的段落 |
| ARRANGEMENT-REPAIR.txt | 乐器、段落或密度偏离 | 一次处理一个主要问题 |

不要一次把这些文字全部塞入 Style。修人声时先处理人声，修节奏时保持歌词与声线不变，才能比较原因。

## 旋律与采样的控制范围

方括号、BPM、调性、小节数、男女标签是方向，不能保证逐条执行。Hook MIDI 和 MusicXML 用于演奏或 DAW 参考；本包没有假定 Suno 可以直接读取它们。需要音频输入时，先录制或用合适音源渲染成实际音频。

v6 官方说明支持音频参考、局部修改与采样工作流，但结果仍须与源音频比对。模型若重新唱同一句，记为新 take。真正的同一人声复用，要在支持音频编辑的工程中使用同一 WAV。参照 06-SOURCES-AND-VOICE-REUSE.md 完成素材登记。

同名曲六个原文件已经验证在两张中的内容完全一致。如果此前还没有选定录音，第一次生成是首次音频实现；重新生成不能据此声称保留了同一母带。

## 三首 remix 的声部检查

- Split Sheet Remix：男艺人 → 低男声制作伙伴 → 女工程师，三段不能被同一个角色的语气抹平。
- Night Shift Remix：女声拥有 Hook 和较长第二段；Bridge 男/女/男/女。不要让男声在最后夺回主导。
- Open Door Remix：男 Verse 1、女 Verse 2；Bridge 女/男/女/男；Outro 女。两步鼓型可以轻盈，对话仍需有重量。

标签若未执行，选出最好的段落后局部编辑，必要时分段制作再组装。参考 references/PLUS-VOCAL-MAP.csv，不靠增加真实艺人的名字来解决声部问题。

## 听检与记录

第一遍不看歌词，关闭播放后尝试复唱标题；第二遍逐句对照，检查漏词、错重音与串位；第三遍只听低频、人声与器乐是否争位。比较候选时尽量匹配感知响度。为每个候选记真实 URL、模型、输入版本、问题和留用理由。

优先听清的词：receipt 重读第二音节；quiet 两音节；Ivory 本稿按三音节演唱；Counterstep 重读首音节；LAST TRAIN / FIRST LIGHT 四个标题词各有明确落点。完整发音补充见 references/PLUS-PRONUNCIATION.md。

计划时长约 10:41 与 21:21。实际生成变长、变短或移调时，记录实际值，不能用目标数代替测量。结构、咬字与情绪通过后，再进入正式混音、母带和发行资料阶段。宣传文案中的声音描述也应在成曲后核对一次。
