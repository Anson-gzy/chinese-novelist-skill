---
name: novel-writer
description: |
  长篇小说分章节创作与工程化连贯性系统（中英文双语支持）。
  以实战项目（如 28 章的 The Transfer Kid）为验证标杆，通过 Notes-Only 前文查阅禁令、5 大状态控制文件全量对齐、POV 视角信息墙与桌面 EPUB 自动导出机制，支持超长篇（20-50+ 章）零遗忘、零冲突、零死板的沉浸式创作。
  当用户提到：写小说、创作故事、分章节写作、长篇小说、小说续写、the-transfer-kid、novel-writer 时使用。
metadata:
  trigger: 创作小说、写小说、分章节故事、长篇小说创作、novel-writer, chinese-novelist
  source: 经 The Transfer Kid 实战沉淀与减负重构的小说工程化系统
---

# Novel Writer: 小说长篇创作与工程化助手

本系统专为超长篇（20–50+ 章）分章节严肃小说创作而设计。基于真实大型连载案例（*The Transfer Kid*, 28 章全本）实战检验，**核心原则是“强工程约束 + 零文风说教”**：

- **现代大模型天生具备顶级文学语感**：彻底剔除传统 Prompt 中对比喻、修辞、对话标点、"展示而非讲述"的泛泛说教与繁琐文风负面清单（如死板禁止“不是……而是……”）。
- **将所有算力集中于模型容易失效的真实痛点**：跨章记忆漂移、时序前后矛盾、多视角秘密穿透、配角无故蒸发、上下文窗口爆炸，以及文件状态失步。

---

## 核心硬规则 (Hard Guardrails)

在创作全生命周期中，必须无条件遵守以下 6 大硬规则：

### 1. 前文查阅禁令 (Notes-Only Policy)
- **绝对红线**：向下推进新章节或查询往期剧情时，**只允许读取 `chapter-xx-notes.md` 与 5 大控制文件**，**严禁加载或读取章节正文全文（`chapter-xx.md`）**。
- **核心目的**：彻底防止上下文窗口被海量历史原文撑爆，杜绝模型在后续创作中产生信息混淆与记忆幻觉。
- *唯一例外*：仅当剧情必须精准确认前文某句特定对话原文或特异道具命名时，方可使用切片查看个别行，查完即关。

### 2. 桌面 EPUB 自动导出规则 (Desktop EPUB Export Policy)
- 每完成一章正文与自检后，必须立即调用导出工具自动将该章转为独立 EPUB 输出至桌面对应的项目文件夹。
- **查找优先级**：先检测 `~/Desktop/` 是否存在同名或大小写/空格变体的文件夹（如 `The Transfer kid` / `the-transfer-kid`）。若存在直接输出；若不存在则自动创建 `~/Desktop/{书名}/`。
- **文件规范**：每章独立命名为 `chapter-01.epub`、`chapter-02.epub` ... `chapter-xx.epub`。使用项目内置的 `scripts/export_epub.py`（自动支持 `ebooklib` 与 `pandoc` 双通道）。

### 3. 语言锁定与字数基线 (Language Lock & Word Count)
- 动笔前读取 `00-outline.md` 与 `04-generation-plan.json` 中的 `language`（`zh` 或 `en`）。一旦确立，全书严格锁定：
  - **中文（zh）**：每章正文 **3000–5000 汉字**。
  - **英文（en）**：每章正文 **1500–2500 词**。
- 绝不偷工减料，不以大段心理总结敷衍字数，字数不达标必须补充扎实的行动节拍与对局拉扯。

### 4. 5 大状态控制文件全量对齐 (5-File Alignment Criteria)
每次写完一章并生成该章 `chapter-xx-notes.md` 后，**必须同拍更新并核验全套 5 个控制文件**，缺一不可：
1. `00-outline.md`：勾选 TODO 清单项 `[x]`，更新完成字数与进度。
2. `01-characters.md`：记录登场新角色、既有角色新性格切面与阶段性演进（如 `Ch.28 Evolution: ...`）。
3. `02-timeline.md`：推进故事时间节点（D+N、星期、具体钟点、持续时长）。
4. `03-global-notes.md`：更新既成事实、核验 POV 信息墙、刷新配角活跃度追踪表。
5. `04-generation-plan.json`：更新该章节状态 `status: "completed"`、字数 `wordCount` 及通过状态。

### 5. 视角信息墙与知识边界隔离 (POV Knowledge Boundaries)
- **第一人称或受限多视角核心铁律**：每一个 POV 角色**只能使用其亲眼所见、亲耳所闻的信息**。
- 严禁上帝视角信息穿透（例如在 *The Transfer Kid* 中：Justin 绝不能提前知道 Marcus 是电话号码中间人；Marcus 被出拳后绝不能提前洞悉 Justin 误会他是伴侣；Zack 的私人过往绝不能在 Justin 章节中无端被引用）。
- 每次写前必须在 `03-global-notes.md` 中核对当前视角的知识盲区。

### 6. 配角活跃度羁绊追踪 (Side Character Activity Tracker)
- 在 `03-global-notes.md` 中维护配角出场追踪表（配角姓名、上次出场章节、出场形式：在场/线上/被提及）。
- 超过 3–5 章未露面的重点配角会自动触发活跃度预警。写作时必须寻找自然切口，以走廊偶遇、群聊消息、背景动作、被他人提起等轻量低侵入形式保持其存在感，严禁人物断崖式蒸发。

---

## 5 大核心控制文件体系

项目根目录下严格维护以下 5 个控制文件（模板详见 `references/`）：

```text
novel-project/
├── 00-outline.md             # 全书总大纲、TODO 检查清单、阶段划分与逐章详细 Brief
├── 01-characters.md          # 角色档案库（核心价值观、缺陷、阶段弧光进化、语言特征、MBTI）
├── 02-timeline.md            # 严格时序表（D+N、绝对时间、时序约束、冲突检测）
├── 03-global-notes.md        # 既成事实基石、POV 知识边界隔离表、配角活跃度追踪表
├── 04-generation-plan.json   # 机器可读的章节元数据与进度计划
├── chapter-01.md             # 正文（标题 + *(POV: 角色名)* + 正文）
├── chapter-01-notes.md       # 本章连贯性速览（核心事件、新确立事实、伏笔、下章接力）
├── ...
└── chapter-xx.md
```

---

## 极简执行工作流 (Four-Phase Lifecycle)

### Phase 0: 路由与断点识别
- 检查当前项目目录是否存在 5 大控制文件。
- 若为已有项目（如包含前 10 章正文及 notes），直接读取 `04-generation-plan.json` 与最后一章的 `notes.md`，完成断点无缝续写。
- 绝不要求用户重新确认已有健康文件的设定。

### Phase 1: 极简需求收集 (Lean Intake)
- 严禁对用户进行冗长繁琐的 20 个文学问题盘问。
- 仅聚焦核心要素：**题材设定、主线核心冲突、POV 视角规则、语言（zh/en）、目标篇幅**。
- 若用户已提供现成大纲或素材包，自动提炼填充，直接进入规划。

### Phase 2: 建立 5 大控制基石
- 基于 `references/` 下的模板，快速生成项目的全套 5 大控制文件：
  `00-outline.md`、`01-characters.md`、`02-timeline.md`、`03-global-notes.md`、`04-generation-plan.json`。
- 向用户输出核心大纲与视角规则摘要，确认后立即进入自动化连续创作。

### Phase 3: 连续分章创作循环 (Autonomous Loop)
进入本阶段后，AI 自主推进，无需每章停下打扰用户。每章执行标准的四步流水线：

```text
[Step 1: Pre-Flight 写前自检]
 └── 读 00-outline 章节 Brief + 读上一章 notes.md + 查 03-global-notes (POV 边界 & 配角预警)
      ↓
[Step 2: 正文 Drafting]
 └── 严格按锁定语言写满字数底线（中文 3000-5000 / 英文 1500-2500），严守 POV 边界
      ↓
[Step 3: 生成 Notes]
 └── 提炼该章 chapter-xx-notes.md（核心事实、新确立秘密、下章接力点、时间锚点）
      ↓
[Step 4: 5 文件全量同步与 EPUB 导出]
 └── 同步 00/01/02/03/04 五大文件状态
 └── 执行 python3 scripts/export_epub.py chapter-xx.md --desktop
      ↓
[自动进入下一章，循环推进]
```

### Phase 4: 终审交付与全本归档
- 汇总全书字数与章节完成度。
- 调用 `export_epub.py` 生成全本整合 EPUB 文件，向用户汇报终审成果。
