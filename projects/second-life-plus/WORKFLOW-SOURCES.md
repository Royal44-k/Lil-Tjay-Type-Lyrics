# 参考工作流与来源记录

检索日期：2026-09-18。外部资料只作为研究依据；未安装插件、执行外部仓库脚本或修改用户的全局工具配置。

## 用户指定的 GitHub 仓库

[bitwize-music-studio/claude-ai-music-skills](https://github.com/bitwize-music-studio/claude-ai-music-skills)

读取的 main 快照：**58f32c25b9fb2dfe569478459b0a591e0dff22e8**。以下链接固定到该提交，以免后续仓库修改影响本次依据。

| 参考文件 | 本项目采用的内容 |
|---|---|
| [album-conceptualizer](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/58f32c25b9fb2dfe569478459b0a591e0dff22e8/skills/album-conceptualizer/SKILL.md) | 曲序、情绪曲线、每首在专辑中的作用 |
| [lyric-writer](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/58f32c25b9fb2dfe569478459b0a591e0dff22e8/skills/lyric-writer/SKILL.md) | 感官细节、主歌推进、韵脚与重音审查 |
| [lyric-reviewer](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/58f32c25b9fb2dfe569478459b0a591e0dff22e8/skills/lyric-reviewer/SKILL.md) | 将主观创作检查与可验证缺陷分开记录 |
| [checklist-reference](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/58f32c25b9fb2dfe569478459b0a591e0dff22e8/skills/lyric-reviewer/checklist-reference.md) | 逐项检查视角、重复、结构、发音、密度 |
| [suno-engineer](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/58f32c25b9fb2dfe569478459b0a591e0dff22e8/skills/suno-engineer/SKILL.md) | 精简风格字段、独立 Exclude、歌词标签与表现方向分开 |
| [track template](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/58f32c25b9fb2dfe569478459b0a591e0dff22e8/templates/track.md) | 每首统一的状态、角色、生成输入、发音与生成日志 |
| [mastering checklist](https://github.com/bitwize-music-studio/claude-ai-music-skills/blob/58f32c25b9fb2dfe569478459b0a591e0dff22e8/reference/mastering/mastering-checklist.md) | 源文件保护、编码预览、跨设备听检、版本交付 |

以上为社区制作工作流，不是统一行业认证。本项目进行了以下判断与调整：

- 不将固定行数、固定词数、固定慢速 Verse 上限当作 rap 通则；根据实际小节份额、句法和演唱负荷检查。
- 自然重音可以落在切分位置；不要求每个强调词都在第一、三拍。
- 已明确的英文句意不需要反复向用户确认同形异音词；先记录读法，实际输出读错后再做最小替换。
- 不把所有 Hook 重复都视为“自押韵错误”；有意重复与无意填充分别判断。
- 不把技能库的一组响度阈值当作全行业母带硬性规范。平台技术判断回到官方资料。
- 本项目已经明确由用户授权写作，采用现有创作方向完成具体稿件；不把通用规划问卷变成创作的前置阻碍。

## Suno 官方产品依据

- [v6 FAQ](https://help.suno.com/en/articles/13924481)：模型定位、音频与局部编辑、Variety、Max Mode。界面和可用模型以实际账户为准。
- [Custom lyrics](https://help.suno.com/en/articles/2415873)：使用自己的歌词。
- [Exclude](https://help.suno.com/en/articles/3161921)：排除项字段。

仅把这些功能当作可用工作方式的依据，不据此承诺模型忠实执行指定音符、固定声部、同一次演唱或精确采样。

## 音频与发行资料的官方依据

- [Spotify loudness normalization](https://support.spotify.com/au/artists/article/loudness-normalization/)：播放归一化及其母带优化建议。
- [Apple Digital Masters 指南](https://www.apple.com/apple-music/apple-digital-masters/docs/apple-digital-masters.pdf)：原生分辨率、编码检查、动态与峰值。
- [IFPI — When to assign](https://isrc.ifpi.org/why-use-isrc/when-to-assign)：新录音与实质改变的版本需独立识别代码。

韩国参考歌曲的具体版本与署名来源独立保存在 RESEARCH-KOREAN-REMIX.md。没有把参考歌曲的实际 BPM、调性、采样处理参数或商业成绩猜成已验证事实。
