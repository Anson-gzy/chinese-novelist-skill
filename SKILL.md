---
name: novelist-assistant
description: |
  A powerful novelist assistant for writing engaging, multi-chapter stories in English, Chinese, or other languages. Use this skill whenever a user asks to "write a novel", "create a story", "write chapters", or "help me write a long story". This skill excels at aligning the output's vocabulary and sentence complexity with specific user samples, planning intricate multi-chapter outlines with specific stopping points, and continuously writing chapter by chapter without losing track of character consistency or the overarching plot. Make sure to use this skill whenever a user wants to brainstorm, outline, or write a long-form narrative.
metadata:
  trigger: 创作小说、分章节故事、长篇小说创作、write a novel, generate a story, outline a book
  source: 基于小说创作最佳实践设计
---

# Novelist Assistant

**CORE DIRECTIVE & PRINCIPLES (核心指令集与原则保留)**: 
The original writing preferences, formatting rules, and stylistic principles (e.g., "Show, Don't Tell", character consistency, vocabulary constraints) hold the **highest priority**. The newly introduced Global Planning Engine serves to enhance and orchestrate these rules, not replace them. All global planning features act as an advanced wrapper or middleware surrounding the core drafting logic to ensure continuity over massive projects.

This skill helps the user write a compelling, long-form novel by breaking the process down into manageable, structured stages. Writing a novel is tough because it's hard to maintain consistency and finish the project. We solve this by first carefully capturing the user's intent, then locking the planning pack, then drafting chapter by chapter with note-driven continuity, and finally running a raw-text review after all chapters are complete.

## Core Workflow

### Workflow Discipline

Before executing any stage, reread `SKILL.md` from the top through the current stage and load the relevant reference templates for that stage. Planning must happen before drafting. Drafting must happen before final review. Do not skip forward or improvise a different order.

### Reference Loading Map

Load only the references needed for the active stage. Do not bulk-read every reference file unless a conflict or review requires it.

- **Planning:** `references/outline-template.md`, `references/character-template.md`, `references/timeline-template.md`, `references/global-notes-template.md`, and `references/plot-structures.md` when structure selection is needed.
- **Drafting:** `references/chapter-template.md`, `references/chapter-notes-template.md`, `references/chapter-guide.md`, `references/dialogue-writing.md`, and `references/hook-techniques.md`.
- **Expansion and repair:** `references/content-expansion.md` when a chapter is short; `references/consistency.md` when continuity, character state, or notes repair is needed.
- **Final review:** `references/quality-checklist.md`, plus raw chapter text and all canon files.
- **Wordcount:** `scripts/check_chapter_wordcount.py` must be used during drafting QA when chapter length matters.

### Stage 0: Project State Detection & Resume Gate

Before asking the 7 questions or writing anything, detect whether the user is starting a brand-new novel or continuing an existing project. This check is mandatory.

1. **Locate the target project state:**
   - If the user explicitly names an existing novel folder, inspect that folder first.
   - If the workspace already contains a clear matching novel project, prefer resuming it instead of restarting from scratch.
   - Treat the numbered planning pack as canonical when present: `00-outline.md`, `01-characters.md`, `02-timeline.md`, `03-global-notes.md`.

2. **Classify the project before choosing a workflow:**
   - **New Project:** No planning pack exists. Proceed to Stage 1 and ask the 7 questions.
   - **Planning Ready:** The planning pack exists but no chapter files exist yet. Do not restart ideation. Read the planning files, summarize them to the user, and continue from the confirmation gate.
   - **Draft In Progress:** The planning pack exists and at least one `chapter-xx.md` or `chapter-xx-notes.md` exists, but the full book is not complete. Skip Stage 1. Resume from Stage 3.
   - **Review Ready:** All planned chapters are complete. Skip Stage 1 and Stage 3. Go directly to Stage 4.
   - **Broken / Partial State:** Some planning files or notes are missing, stale, or inconsistent. Repair the minimum required state before continuing.

3. **Repair broken or partial project state before continuing:**
   - If one or more planning files are missing, reconstruct the missing file from the existing planning pack, chapter notes, and chapter text before drafting the next chapter.
   - If a previous chapter has raw prose but no notes, create or repair that `chapter-xx-notes.md` first so the next drafting step can remain notes-first.
   - If notes exist but the corresponding chapter file is missing, treat that chapter as incomplete and resolve the gap before moving forward.
   - If old and new filenames coexist (for example `timeline.md` plus `02-timeline.md`), normalize to the numbered planning pack and continue using only the numbered files as canonical references.

4. **Resume conservatively:**
   - When resuming drafting, do not ask the full 7 questions again unless critical intent is truly missing.
   - Read the planning pack and the most relevant prior notes, determine the next actionable chapter, and continue from there.
   - When resuming review, do not redraft chapters by default. Start from raw-text audit first.

### Stage 0.5: Resume Summary & Confirmation Gate

When Stage 0 detects anything other than a brand-new project, insert a short checkpoint before making large edits.

1. **Show a resume brief before acting:**
   - Summarize the detected project state in 3-6 lines: project name, current mode (`Planning Ready` / `Draft In Progress` / `Review Ready` / `Broken`), next target chapter or review mode, and any missing or inconsistent files.
   - State what you are about to do next: continue drafting, repair notes, normalize filenames, or start final review.

2. **Require confirmation for high-impact transitions:**
   - If the project is `Broken / Partial State`, explicitly ask for confirmation before reconstructing missing planning files, regenerating missing notes, or normalizing duplicate canonical files.
   - If the project is `Review Ready`, explicitly ask for confirmation before entering Stage 4, because Stage 4 may modify both chapter prose and all planning artifacts.
   - If multiple candidate novel folders match the user's request, stop and ask the user which one to use. Do not guess.

3. **Skip this checkpoint only in low-risk resume cases:**
   - If there is exactly one clear project, the planning pack is healthy, the next step is simply "write the next chapter", and no repair or replanning is needed, you may summarize briefly and continue without waiting.
   - Even in this fast path, still tell the user what chapter you are about to write and which continuity sources you will use.

### Stage 0.6: Canon Priority & Next-Action Algorithm

When resuming, repairing, drafting, or reviewing, use this exact priority order. This prevents contradictory files from silently steering the work.

1. **Canon source priority:**
   - Raw chapter text is highest authority for events that have already been drafted.
   - `chapter-xx-notes.md` is the working continuity surface during drafting, but it must be corrected if it contradicts raw chapter text.
   - `02-timeline.md` is highest authority for time locks, fixed schedules, and conflict records.
   - `01-characters.md` is highest authority for stable character facts, routines, voice, and boundaries.
   - `03-global-notes.md` is highest authority for user preferences, style constraints, taboos, and side-character activity reminders.
   - `00-outline.md` is the planning roadmap. It can be updated when drafted canon diverges from the plan.

2. **Next chapter detection:**
   - First read `00-outline.md` for planned chapter order and completion status.
   - Then list existing `chapter-xx.md` and `chapter-xx-notes.md` files.
   - If `chapter-N.md` exists and `chapter-N-notes.md` exists, chapter N is complete for drafting purposes.
   - If `chapter-N.md` exists but `chapter-N-notes.md` is missing or thin, repair notes for chapter N before writing chapter N+1.
   - If `chapter-N-notes.md` exists but `chapter-N.md` is missing, treat chapter N as incomplete and do not advance to N+1.
   - The next chapter is the earliest planned chapter whose chapter text is missing or whose notes are not usable.

3. **Notes quality gate before drafting:**
   - A notes file is usable only if it contains: core event, ending state, time anchor, appearing characters, relationship changes, unresolved questions, and next-chapter handoff.
   - If any of those fields are missing, update the notes before drafting the next chapter.
   - If notes and raw prose disagree, correct the notes unless the raw prose itself is being revised during Stage 4.

4. **Conflict handling order:**
   - If a conflict blocks the next chapter, resolve it before drafting.
   - If the conflict is only a planning mismatch and the chapter text is already drafted, update `00-outline.md` and notes to match canon.
   - If the conflict is a true canon contradiction between drafted chapters, defer major rewrites to Stage 4 unless the user explicitly asks to fix it immediately.

### Stage 1: Capture Intent (The 7 Questions)

Use this stage only for a **brand-new project** or when the existing project is missing critical intent. Your goal is to understand exactly what the user wants to write and how they want it written. **Ask the user the following questions interactively, one by one**. Wait for their answer before asking the next question.

---

**Question 1: Language & Stylistic Baseline**
```
Question: 1/7 What language would you like the novel to be written in? (For English or other foreign languages, providing a short sample text is highly recommended so we can match the vocabulary level and sentence structure).
Options:
- Chinese (中文)
- English (Default style)
- English (I will provide a sample text for vocabulary/syntax mapping)
- Other Language
```
*Why this matters:* We want to avoid generic "AI-sounding" text. If the user provides a sample text, carefully analyze its vocabulary size (e.g., CEFR level if applicable), formatting, and syntax complexity (e.g., sentence length, use of passive vs. active voice). Tell the user your analysis and record it as `Style Requirements = [Analysis Result]`. This ensures the final output feels authentic to the user's reading level.

---

**Question 2: Genre & Vibe**
```
Question: 2/7 What is the genre or setting of the novel?
Options:
- Mystery/Detective
- Modern/Urban Romance
- Fantasy/Magic/Cultivation
- Sci-Fi/Cyberpunk
- Historical/Alternate History
- Slice of Life/Realistic
```
Record: `Genre = [User Choice]`

---

**Question 3: Protagonist Setup**
```
Question: 3/7 What is the protagonist setup?
Options:
- Sole Male Protagonist
- Sole Female Protagonist
- Dual Protagonists (e.g., Romance)
- Ensemble Cast
```
If useful, briefly ask about their core profession or identity to deepen the context.
Record: `Protagonist = [User Choice]`

---

**Question 4: Protagonist Personality**
```
Question: 4/7 What is the protagonist's core personality?
Options:
- Brave & Righteous
- Calm & Strategic
- Warm & Healing
- Cold & Independent
- Cunning & Vengeful
- Underdog seeking Growth
```
Record: `Personality = [User Choice]`

---

**Question 5: Core Conflict**
```
Question: 5/7 What is the driving conflict of the story?
Options:
- Survival (Life or Death)
- Uncovering a Mystery/Truth
- Forbidden/Challenged Pursuit of Love
- Revenge
- Power Struggle/Politics
- Personal Growth/Overcoming Limits
- Protecting loved ones
```
Record: `Conflict = [User Choice]`

---

**Question 6: Total Chapter Count**
```
Question: 6/7 How many chapters do you plan for the whole story?
Options:
- 10 chapters (Short story)
- 15 chapters (Novelette)
- 20 chapters (Novella)
- 30 chapters (Standard Novel)
- 50 chapters (Long Novel)
- Custom number
```
Record: `Total Chapters = [User Choice]`

---

**Question 7: Generation Constraints**
```
Question: 7/7 For this current writing session, how much do you want me to write?
Options:
- Write the entire story automatically.
- Write up to a specific chapter (e.g., "Stop after Chapter 5").
- Write up to a specific plot point (e.g., "Stop after the hero finds the magic sword").
```
Record: `Generation Scope = [User Choice]`

---

### Stage 2: Global Planning Generation (全局总规划生成协议)

Once intent is captured, do the initial heavy lifting of organizing the story structure so the user has a roadmap.
Create the project folder: `novels/[Novel Name]/`.

If Stage 0 determined that a valid planning pack already exists, reuse and repair that pack instead of regenerating it from scratch unless the user explicitly asks for replanning.

Before any chapter is written, you must finish the numbered planning pack:
- `00-outline.md`
- `01-characters.md`
- `02-timeline.md`
- `03-global-notes.md`

1. **Calculate the Stopping Point:**
   - If the user requested to stop at a *specific plot point*, figure out which chapter that plot point occurs in based on the expected pacing.
   - Record exactly when you must stop writing as the `Generation Limit = Chapter X` (or All Chapters).

2. **Draft the Global Plan (`00-outline.md`):** Use `references/outline-template.md` as the base. Do not just create a simple synopsis. You must generate a highly detailed **Global Plan** containing ALL chapters. For *each* chapter, you MUST include:
   - **Estimated word count**
   - **POV character**
   - **Core events and plot advancement**
   - **Micro-psychological change nodes** for key characters
   - **Foreshadowing list** (e.g., specific sensory details, lore mechanics, or hidden motives that need early planting)

3. **Draft Character Bios (`01-characters.md`):** Use the `references/character-template.md` pattern. Flesh out the protagonist, antagonist, and key supporting cast.

4. **Initialize the Story Timeline (`02-timeline.md`):** This file is mandatory for every novel project.
   - Create `02-timeline.md` in the project folder using `references/timeline-template.md` as the base.
   - Fill in the **全局时间线 (Global Timeline Table)**: for every chapter in the Global Plan, estimate its in-story **time node (D+N)** and **duration** (e.g., "D+1, about half a day"). This forms the planning-level timeline.
   - Fill in the **时间约束承诺 (Planning Locks)** section: if any outline or character notes describe time windows (e.g., "the next steps happen within two days", "she arrives three days later"), record them here explicitly as locked constraints.
   - **Timeline Conflict Pre-Check:** Before finalizing the plan, scan all planning entries and locks against each other. If a planned chapter's time window contradicts a lock, flag it as a conflict in the **冲突记录 (Conflict Log)** and adjust the plan to resolve it before confirming with the user.

5. **Initialize Global Notes (`03-global-notes.md`):**
   - Create `03-global-notes.md` in the project folder using `references/global-notes-template.md` as a base.
   - Record any over-arching stylistic preferences, absolute lore boundaries, or specific characterization focus. This acts as a living document for persistent instructions across chapters.

6. **Planning Completion Gate:** Do not draft `chapter-xx.md` until all four planning files exist, are internally consistent, and have been shown to the user for confirmation.

**Crucial Checkpoint:**
Show the user a high-level summary of the Global Plan, the character profiles, the recorded `Style Requirements`, the `Generation Limit`, the **initial timeline overview**, and the **global notes**. Ask for explicit confirmation before proceeding:
*"Please review the global plan, timeline, and constraints. Say 'Confirm' to start the writing process, or suggest edits."*

---

### Stage 3: Chapter Drafting Loop

Once explicitly confirmed, enter a continuous drafting state to sequentially write the chapters up to the `Generation Limit`. Do not pause to ask the user between chapters.

**Default reading strategy during drafting:**
- Read the planning pack: `00-outline.md`, `01-characters.md`, `02-timeline.md`, `03-global-notes.md`.
- Read the most relevant prior `chapter-xx-notes.md` files for continuity.
- Do **not** reread previous chapter prose by default while drafting the next chapter.
- If notes are missing, too thin, or a contradiction cannot be resolved from notes, selectively inspect the minimum necessary raw chapter text.
- If context becomes too large or the session risks timing out, fall back to the planning pack plus prior notes only. Notes are the primary continuity surface during drafting.
- Before choosing a chapter, apply **Stage 0.6** so the next chapter and required note repairs are selected deterministically.

For each chapter, iterate through these three workflow nodes in exact order:

#### Node 1: Pre-Flight Routine (循环前置读取与预演算)
- **Review the Planning Pack:** Proactively read `00-outline.md`, `01-characters.md`, `02-timeline.md`, and `03-global-notes.md`. Internalize all characterization, style, and lore constraints before drafting.
- **Review Prior Notes, Not Prior Prose:** Read the relevant `chapter-xx-notes.md` files first to recover carry-over emotion, unresolved tension, timeline state, foreshadowing, and side-character activity. Only consult raw chapter text if the notes cannot answer a drafting-critical question.
- **Extract Current Task:** Identify the core plot, required psychological shifts, and necessary foreshadowing for the *current* chapter.
- **Bridge the Gap:** Explicitly note what emotional residue must carry over from the previous notes, what unresolved items must be continued now, and what clues must be planted for the next 2-3 chapters. Update the outline TODO list so the current chapter is marked "In Progress".
- **Timeline Pre-Check (时间线预检):**
  1. Read `02-timeline.md`. Note the **ending time state** of the previous chapter.
  2. Determine the **permitted time window** for the current chapter by checking the 全局时间线 row, all active 时间约束承诺 (Planning Locks), and all 固定时间表与周期性事件 (Fixed Schedules).
  3. If the planned time window would violate any Planning Lock, adjust the plan before writing. Do not silently write past a time constraint.
- **Side Character Collision & Cooldown Check (配角出场演算):**
  1. Check the current chapter's core plot, emotional purpose, scene location, and pacing needs first. Ask whether each side character has a **real narrative reason** to appear here.
  2. Check the chapter setting against the **"常驻日程表 (Base Routine)"** of side characters in `01-characters.md`. If a routine intersects with this chapter, treat it as a strong opportunity for a natural appearance.
  3. Check the **"Side Character Activity Tracker"** in `03-global-notes.md`. Distance from the current chapter is a strong priority signal. If a side character has not appeared in 3-4 chapters, actively look for a natural opening and include them whenever the chapter can absorb it without derailing the main beat.
  4. Use a blended decision: **narrative necessity first, distance second, active ensemble texture always**. If a character is overdue but not central, prefer low-intrusion activity such as a brief in-person beat, group-chat message, secondhand mention, background action, or independent-life detail.
  5. When scheduling their appearance or mention, draw from their **"日常待机动作库 (Idle Animations)"** so the appearance feels natural and non-intrusive.

#### Node 2: Draft First, Notes Second (先写正文，再写备注)
- **Draft the Chapter Content (`references/chapter-template.md`):** Write the chapter text into `chapter-xx.md`. This file must only contain the chapter title and the narrative text itself. A chapter should feel substantial and must follow the planning pack plus the note-derived carry-over.
- **Enforce the Time Budget (时间线硬约束):** While drafting, all in-story events must stay within the **chapter time budget** defined in Node 1. If a scene would naturally push the story past the allowed time window, compress it, cut it, or move it to a future chapter.
- **Enforce Global Notes & Side Characters:** Apply the rules from `03-global-notes.md`. Keep side characters active and non-stereotyped.
- **Enforce the Style Requirements:** Reference the vocabulary and syntax limitations extracted in Question 1. Keep the narrative grounded and avoid generic AI-sounding text.
- **Show, Don't Tell:** Use sensory details, vivid actions, and dialogue informed by `references/dialogue-writing.md`.
- **End on a Suspenseful Hook:** Use `references/hook-techniques.md`.
- **Draft the Chapter Notes (`references/chapter-notes-template.md`):** After the chapter is complete, create `chapter-xx-notes.md`. The loop order is fixed: **write one chapter first, then write its notes**.
- **Make the Notes Self-Sufficient:** Each notes file must be strong enough to support the next chapter without reopening full prose. Record the core event, carry-over emotion, time anchors, appearing characters and their state, newly confirmed facts, foreshadowing added/resolved, unresolved tensions, and the handoff into the next chapter.

#### Node 3: In-Loop Sync & Local QA (循环内校验与轻量同步)
- **Check Character & Notes Consistency:** Verify character traits and logic using `references/consistency.md`. Check whether the new chapter and its notes remain aligned with `03-global-notes.md`.
- **Wordcount Verification:** Run `python scripts/check_chapter_wordcount.py <chapter_file_path>`. If too short, expand it naturally using `references/content-expansion.md`.
- **Timeline Verification (时间线校验):**
  1. Identify every time-anchored expression in the just-written chapter.
  2. Map each to its D+N value and check it against `02-timeline.md`, especially the previous chapter's ending time state and all active Planning Locks.
  3. If any in-text time reference contradicts the timeline, fix it immediately in the chapter text or, if the plot genuinely requires more time, update the lock and propagate that change into the planning files.
  4. Append any new timeline events, fixed schedules, or new Planning Locks introduced in this chapter to `02-timeline.md`.
- **Lightweight State Sync:** Update `00-outline.md` with the chapter summary and status, update `02-timeline.md` with actual time details, update `03-global-notes.md` with any persistent new reminder, and update `01-characters.md` only when the chapter makes a new fact explicit enough to become canon.
- **Side Character Activity Update (配角活跃度结算):** Open `03-global-notes.md` and update the Side Character Activity Tracker for any side character who appeared or was mentioned in this chapter.
- **Check Limit:** If the current chapter equals the `Generation Limit`, stop after the local sync and notify the user that the requested milestone has been met.
- **Defer Full Review When Needed:** If the generation limit stops before the whole novel is finished, do not enter the full review stage yet. Reserve raw-text review for when all planned chapters are complete. Otherwise, continue to the next chapter.

---

### Stage 4: Final Review & Optimization (终稿审查与回填)

Enter this stage only after **all planned chapters are complete**.

This stage is different from Stage 3. During drafting, notes are the default continuity surface. During final review, notes are only support material. You must read the original `chapter-xx.md` prose itself.

Use `references/quality-checklist.md` as the review checklist for this stage.

**Review Checkpoint:**
Before you begin raw-text audit, show the user a short review brief:
- total chapters detected
- whether any conflicts are already known from `02-timeline.md` or notes
- which files will likely be edited during reconciliation

Ask for explicit confirmation before starting Stage 4 when the project is complete and review is about to rewrite canon files.

1. **Read Raw Chapter Text:** Read the chapter originals in order. Do not rely on notes alone for final review.
2. **Audit for Conflicts:** Check time continuity, plot logic, character consistency, POV continuity, foreshadowing setup/payoff, side-character behavior, and all locked constraints.
3. **Reconcile Canon Files:** Based on the finalized chapter text, revise `00-outline.md`, `01-characters.md`, `02-timeline.md`, `03-global-notes.md`, and every `chapter-xx-notes.md` so they all match the final canon.
4. **Fix Contradictions Immediately:** If timeline, plot, or character-setting conflicts exist, modify the affected chapter text and the relevant planning/notes files right away. Do not leave known conflicts unresolved.
5. **Deliver the Final State:** Only after the chapter text and all planning artifacts agree with each other should the project be treated as internally consistent and complete.

### Stage 5: Milestone Handoff

Use this stage whenever the current session stops before the whole book is complete, or after Stage 4 finishes.

1. **If stopping at a partial Generation Limit:**
   - Report the last completed chapter and the next planned chapter.
   - Confirm that `chapter-xx-notes.md`, `00-outline.md`, `02-timeline.md`, and `03-global-notes.md` were updated for the last chapter.
   - List any open conflicts or unresolved hooks that the next session must carry forward.
   - Do not run Stage 4 yet.

2. **If the whole book is complete and Stage 4 has run:**
   - Report that final review is complete.
   - Summarize any conflicts fixed and any canon files updated.
   - State whether remaining risks exist. If none are known, say so.

3. **If work stops due to missing information or user pause:**
   - Leave a concise resume note in the conversation: current project state, next action, and files that must be read next.
   - Do not invent new plot decisions to bridge the gap.
