# 修仙神通咒词工坊

**描述神通 → 获得20～30个咒词关键词 → 自己挑选、组装。**

这是一个供 **OpenCode、Codex、Claude Code** 使用的 Agent Skill。根据功法属性、作用机制、战斗场景和具体效果，默认生成 **24个独立候选词**。每条都说明对应能力、典故或造词来路、如何转译成神通效果。你选好词以后，再按需编排咏唱节奏或写实战片段。

技能名：`xianxia-jjk-chant-generator`。当前版本：`1.0.0`。

## 输出是什么样

> **无住（无视惯性）**  
> 典故借用，取《金刚经》的无所住之意。在神通中借作“不驻留于既定方向”：上一瞬的冲势解除，下一瞬重新指定去向。动量解释属于小说改写。
>
> **尺木（雷翼＋升空）**  
> 《论衡·龙虚》引述过龙凭尺木升天的说法。本次把“升天凭依”改写成肩胛间的雷翼骨架，雷霆依骨架展开、托起肉身；雷翼解释是创作。
>
> **折断的白驹（极速＋急转）**  
> 原创重构，将白驹过隙的时间意象折成锐角。身形沿折线疾行，已有的随身雷幕随折点闭合，截断身后追来的术法。

完整回复会按能力分组列出24个这样的条目。先让作者选择，不默认替作者定稿，也不以三四组成套咒词代替大量候选。

查看[完整雷翼24词示例](skills/xianxia-jjk-chant-generator/references/thunder-wings.md)。

## 安装

### 方式一：克隆后运行安装脚本

需要 Git，以及 Python 3.9或更高版本。安装脚本只复制本地技能文件，不下载依赖、不调用模型。

```bash
git clone https://github.com/JIAzc-elk/xianxia-jjk-chant-generator.git
cd xianxia-jjk-chant-generator
```

Windows（PowerShell）中，根据使用的工具选择一条：

```powershell
python scripts/install.py --tool codex
python scripts/install.py --tool opencode
python scripts/install.py --tool claude
```

macOS／Linux可将 `python` 换成 `python3`。需要同时安装到三个工具时：

```bash
python scripts/install.py --tool all
```

默认安装到个人目录，各项目均可使用。要只安装到某个写作项目：

```powershell
python scripts/install.py --tool codex --scope project --project "D:\我的小说"
```

将 `codex` 换成 `opencode`、`claude` 或 `all` 即可选择目标。项目目录必须已存在。提前查看安装位置可追加 `--dry-run`。

脚本会比对复制结果；重复安装相同版本显示 `UNCHANGED`。如果同名目录含有改动，脚本会停止并保留原文件；先备份、重命名旧目录，再安装新版。`--home PATH` 可指定独立的便携或测试用户目录。

### 方式二：手动复制，不需要Python

下载仓库ZIP并解压，把 `skills/xianxia-jjk-chant-generator/` **整个文件夹**复制到下面任一目标。目录名须保持不变，`references/` 和 `agents/` 一并保留。

| 工具 | 个人安装目标 | 项目安装目标 |
| --- | --- | --- |
| Codex | `~/.agents/skills/xianxia-jjk-chant-generator/` | `<项目>/.agents/skills/xianxia-jjk-chant-generator/` |
| OpenCode | `~/.config/opencode/skills/xianxia-jjk-chant-generator/` | `<项目>/.opencode/skills/xianxia-jjk-chant-generator/` |
| Claude Code | `~/.claude/skills/xianxia-jjk-chant-generator/` | `<项目>/.claude/skills/xianxia-jjk-chant-generator/` |

`~` 表示用户主目录，Windows通常为 `%USERPROFILE%`。OpenCode也支持发现 `.agents/skills` 和 `.claude/skills` 下的技能；脚本采用各工具自身的目录。多个工具安装的是同一份正文。

安装后开启新会话；如果没有发现技能，检查目标内是否直接存在 `SKILL.md`，以及工具本身是否允许加载本地技能。

路径依据（2026-10-23核对）：[OpenAI官方技能文档](https://learn.chatgpt.com/docs/build-skills)、[OpenCode官方文档](https://opencode.ai/docs/skills/)、[Claude Code官方文档](https://code.claude.com/docs/en/skills)。

## 使用

Codex可显式调用：

```text
$xianxia-jjk-chant-generator
雷属性，背生雷翼；周身雷网阻挡远程术法；短时间高速飞行，
可近乎无视惯性地锐角转向，同时增强自身雷法。
给我24个关键词，每个解释来路和对应效果，先让我自己挑选。
```

Claude Code可使用：

```text
/xianxia-jjk-chant-generator 为雷翼神通生成24个可组装关键词，逐词解释典故与机制。
```

OpenCode可直接要求加载技能：

```text
请使用 xianxia-jjk-chant-generator 技能，按我的神通描述生成24个咒词关键词供我选择。
神通描述：……
```

三者也可用自然语言触发：

```text
帮我做修仙神通的咒词关键词：冰属性，以镜面隔断视线，短时隐藏身形，
但不能无敌。给我30个候选，偏古典诡谲，少用现代术语。
```

选好后继续：

```text
我选第1、7、13、24个词。保留原词，帮我排列成两种节奏，说明各段触发效果。
```

如需正文再说：

```text
用我选定的咒词写一段150～250字战斗片段，低声分段触发，穿插动作。
```

## 方法与编辑边界

- 四步法：拆解机制、五维取词、参差编排、实战植入；默认停在选词阶段。
- 五维词库：佛道哲思、古籍博物、经史律令、科学几何、古典意象重构。
- 典故原义、现代术语、原创重构分别注明；不替自造词编古籍出处。
- 神通解释属于小说创作，保留作者给出的持续时间、消耗、强弱与作用边界。
- 创作词库和示例均可调整；作者的本轮要求优先。

## 仓库结构与检查

```text
skills/xianxia-jjk-chant-generator/
  SKILL.md                      三种工具共用的技能正文
  agents/openai.yaml            Codex界面元数据
  references/lexicon.md         词库、典故来源与改写边界
  references/thunder-wings.md   完整24词样例
scripts/install.py             跨平台本地安装器
tests/test_install.py          隔离安装与冲突保护测试
```

运行安装测试：

```bash
python -m unittest discover -s tests -v
```

这些测试验证文件安装行为；生成质量仍取决于所用模型与具体神通描述。技能本身不要求专用API、外部MCP服务或额外运行库。

## 许可

[MIT](LICENSE)。非官方项目；《咒术回战》仅用于描述创作气质，不代表与作品权利方存在关联。
