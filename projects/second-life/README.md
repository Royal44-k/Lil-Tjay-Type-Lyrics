# SECOND LIFE — Creative Pack

四首原创英文歌曲的词曲、编曲方案与 Suno 手动生成材料。研究参考：Sik-K & Lil Moshpit《K-FLIP+》的素材重组方法。

## 先看这三个文件

- **ALBUM-BLUEPRINT.md**：主题、四曲区别、和声、flow、押韵、配器和 voice reuse 的完整制作说明。
- **SECOND-LIFE-SONGBOOK.md**：四首完整歌词，一次阅读。
- **SUNO-IMPORT-GUIDE.md**：导入流程、控制范围和针对性修订提示。

## 每首歌的文件夹

- LYRICS.txt：完整歌词，含展开的重复段落，可放入自定义歌词栏。
- STYLE.txt：英文风格提示，单份控制在 1000 字符以内，便于编辑。
- EXCLUDE.txt：避免的声音方向。
- HOOK-GUIDE.mid：首个八小节 Hook 的音高、节奏、参考和声与 Bass；不是全曲伴奏，也没有人声音频。
- HOOK-NOTES.csv：每个音节对应的音符、开始位置、持续时间；以 C4 = MIDI 60 记谱。
- ARRANGEMENT.csv：全曲段落、小节与计划时间。

00-ORIGINAL-SAMPLE 保存原创母句的单小节 MIDI 和音节表，待歌手录制。此目录不包含真实采样录音。

K-FLIP-RESEARCH.md 为一手资料研究；DELIVERY-MANIFEST.json 记录节奏、文件及结构检查；build_melody_guides.py 可用 Python 标准库重新生成 MIDI、CSV、歌词册和压缩包。

## 使用边界

这是可进入演唱与制作的创作第一版。未生成完整音频，未完成真实人声录制、混音、母带或试听验收。四首标题与所有歌词、旋律骨架为本项目新写；没有放入参考艺人的录音、歌词或克隆声音。

文本提示不能保证精确音符和跨曲同一录音。正式 voice reuse 请录制原创母句一次，再从同一 WAV 派生四曲处理版本。
