# 外部 Agent 深度审计与工程调优任务书 (Audit Briefing)

欢迎来到 **Novel Writer: 小说长篇创作与工程化连贯性系统** 仓库。

本文件旨在为你（外部全套代码、架构与技能审计 Agent）提供完整的系统设计背景、工程精简哲学、实战案例拆解以及可直接派发的标准 Audit Prompt。

---

## 一、系统架构与关键资产索引

### 1. 技能操作契约与执行核心 (`SKILL.md`)
- **定位**：面向各种 Agent（Claude、Gemini/Antigravity、Codex 等）的统一执行规程。
- **核心特色**：彻底剥离传统提示词对修辞手法、文风负面清单和文学技巧的说教，全面聚焦于**长篇创作状态机维护、上下文防爆与信息防穿透**。

### 2. 精简模板库 (`references/`)
- `outline-template.md`：全局大纲、阶段划分、TODO 清单与逐章 Brief
- `character-template.md`：角色档案、致命缺陷、阶段性演进记录（Milestone Evolution）
- `timeline-template.md`：D+N 故事天数、时钟时间与时序约束
- `global-notes-template.md`：既成事实、POV 视角知识隔离墙、配角活跃度羁绊追踪表
- `generation-plan-template.json`：机器可读的章节状态与字数计划元数据
- `chapter-notes-template.md`：章节归档备忘（连贯性硬锚点与下章接力）
- `chapter-template.md`：正文标准结构容器

### 3. 工具与自动化脚本 (`scripts/`)
- `export_epub.py`：支持 `ebooklib` 与 `pandoc` 双通道的桌面 EPUB 导出器。
- `check_chapter_wordcount.py`：汉字与英文词数双模统计工具。

### 4. 实战验证案例
- 本地真实案例存放在 `/Users/guziyang/Projects/Novel/the-transfer-kid`，全书 28 章、超 5 万词，完整验证了多视角（Justin / Marcus / Zack）轮转、Notes-Only 读法、POV 隔离与桌面 EPUB 导出的全套可行性。

---

## 二、核心审计维度与攻坚重点

作为审计 Agent，请着重从以下五个方面进行全方位排查与调优：

1. **工程减负与 Token 损耗控制**
   - 检查现有 Prompt 与模板中是否仍残留任何说教式的文学修辞规则，确保将宝贵的上下文窗口 100% 留给项目事实、时序与伏笔。
   - 评估 Pre-Flight 阶段读取 5 大控制文件的 Token 消耗，提出更紧凑的元数据组织方案。

2. **5 大状态控制文件的数据闭环**
   - 检查 `00-outline.md`、`01-characters.md`、`02-timeline.md`、`03-global-notes.md` 与 `04-generation-plan.json` 之间的状态流转是否严密闭环。
   - 评估当章节重写或剧情重大调整时，如何实现一键级联更新或冲突回滚。

3. **POV 视角隔离墙的防穿透与自动化检测**
   - 检查当前规则对第一人称/受限多视角作品中“上帝视角穿透”（角色知道他不应该知道的秘密）的防范是否足够有效。
   - 探索是否可编写轻量静态自检脚本（或 Prompt 检查指令），在生成 `chapter-xx-notes.md` 时自动对比 `03-global-notes.md` 中的视角盲区。

4. **自动化导出工具链健壮性**
   - 审查 `scripts/export_epub.py` 在不同操作系统、不同 Python 环境（缺包兜底）、特殊字符章节名及大批量章节并发导出时的容错表现。

5. **多 Agent 并行创作的可行性演进**
   - 探索在超长篇（如 50-100 章）场景下，如何在严格遵守 5 大控制文件锁（Lock）的前提下，支持多个子 Agent 安全分工撰写独立章节。

---

## 三、直接可用的审计 Prompt (Turnkey Prompt)

若需直接派发外部 Agent 执行全套审计与优化，可直接复制以下 Prompt：

```text
你是一个资深全栈架构师、Prompt 工程专家与长篇小说工程化系统专家。请对当前 Novel Writer（chinese-novelist-skill）小说创作工程化系统进行深度的代码、结构、模板与连贯性规则审计，并执行自动化重构落地。

【项目背景】
本项目由 PenglongHuang/chinese-novelist-skill 演进而来，经 28 章全本英文写实小说《The Transfer Kid》实战检验。核心指导思想是“彻底减负，减少写作文风等文学创作的说教提示，着重强化 Notes-Only 防爆、5 大状态控制文件对齐、POV 视角信息墙与自动 EPUB 导出等工程约束”。

【执行原则与交付要求】
1. 首先将仓库所有文件（SKILL.md、references/、scripts/、README.md）拉入你的内部上下文与工作空间，并参考 the-transfer-kid 的实战结构进行全局拓扑与执行流分析。
2. 对可以直接安全修改、能进一步提升自动化程度、提升 Token 效率、消除冗余说教并强化 5 文件同步与导出鲁棒性的代码或模板，请直接在代码中完成重构与落地。
3. 对属于较大架构扩展（如多 Agent 并行章节写作分工锁协议、自动视角冲突静态检测器等），请在报告中给出详细的技术分析与实施步骤。
4. 审计与修改完成后，在根目录下生成一份名为《AUDIT_REPORT.md》的综合审计报告，必须严格包含以下五大模块：
   - 一、发现的问题清单（按高危/中危/低危/架构与工程优化分类）
   - 二、你的核心解题思路与重构策略
   - 三、已经直接完成的改动与优化项清单（附具体修改文件与行号）
   - 四、尚未修改/暂缓实施的项及其技术权衡
   - 五、下一步长期迭代建议与实施步骤指引
```
