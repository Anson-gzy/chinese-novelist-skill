---
name: chinese-novelist
description: |
  中文长篇小说创作、续写、批量分章节写作和终稿审查 skill。适用于写小说、创作故事、分章节剧情、规划长篇、续写章节、修复时间线、维护人物一致性、生成 chapter notes、审查终稿。默认节省 token：先规划，再按“写一章正文 -> 写本章 notes -> 同步 canon”的循环推进；写作期只读规划包和 notes，终审期才读章节原文。用户明确要求自动跑完整流程或使用 subagent 时，减少中途确认并按可并行的文件范围分工。
metadata:
  trigger: 创作中文小说、写小说、分章节故事、长篇小说创作、小说续写、章节 notes、小说终稿审查、novel writing, write a novel
  source: merged local Chinese novelist skill repositories
---

# Chinese Novelist

## Operating Contract

- **Single entry**: `SKILL.md` is the workflow. Do not depend on external phase-flow files.
- **Plan before prose**: no chapter drafting until the planning pack exists and is usable.
- **Draft before notes**: each chapter loop is `chapter-xx.md` first, then `chapter-xx-notes.md`.
- **Notes-first drafting**: while writing the next chapter, read the planning pack and prior notes; do not reread previous prose unless notes are missing, thin, or contradictory.
- **Raw-text final review**: after all chapters are complete, read chapter prose in order and reconcile all canon files.
- **Autonomy**: if the user asks to “自动走完 / 全流程 / 不要一步一停”, treat intake and planning confirmations as pre-authorized. Continue through all safe stages after brief status notes. Stop only for missing critical intent, ambiguous project choice, destructive rewrites, or large final-review prose rewrites.
- **Subagents**: use parallel/subagents only when the user explicitly asks or the runtime request says to do so. Assign disjoint write scopes.
- **Prompt-faithful conflict**: do not soften the user's conflict words. If the prompt says a character hurts someone, fights, lies, freezes someone out, or stays cruel, write that behavior at the stated intensity instead of making it safer, more mature, or quickly reconciled.

## Token Budget

- Load only files needed for the current stage.
- Prefer summaries in chat; write full artifacts to project files.
- During drafting, never bulk-read all old chapters. Use `chapter-xx-notes.md` as the continuity surface.
- If context grows large, keep only: planning pack, last 1-3 notes, active timeline locks, unresolved hooks, and current chapter plan.
- Use templates as structure references, not content to paste back to the user.
- Do not spend tokens on default psychology. Use interiority only when the prompt, POV, or scene pressure makes it necessary.

## Resources

- **Planning default**: `references/outline-template.md`, `references/character-template.md`, `references/timeline-template.md`, `references/global-notes-template.md`
- **Planning on demand**: `references/plot-structures.md`
- **Drafting default**: `references/chapter-template.md`, `references/chapter-notes-template.md`
- **Drafting on demand**: `references/chapter-guide.md`, `references/dialogue-writing.md`, `references/hook-techniques.md`
- **Repair/QA on demand**: `references/content-expansion.md`, `references/consistency.md`, `references/quality-checklist.md`
- **Wordcount**: `python scripts/check_chapter_wordcount.py <chapter_file_path>`
- **Preferences**: skill root `user-preferences.json`, loaded lazily

## Canon Files

Use these names for new and migrated projects:

- `00-outline.md`
- `01-characters.md`
- `02-timeline.md`
- `03-global-notes.md`
- `chapter-xx.md`
- `chapter-xx-notes.md`

Legacy files are input only: `00-大纲.md`, `01-人物档案.md`, `03-写作计划.json`. Normalize their content into the numbered pack.

Canon priority when files disagree:

1. Completed chapter prose
2. `chapter-xx-notes.md`
3. `02-timeline.md`
4. `01-characters.md`
5. `03-global-notes.md`
6. `00-outline.md`

## Craft Guardrails

These rules override any tendency to make scenes smoother, safer, or more "literary" than requested.

- **Conflict fidelity**: preserve the user's conflict type and severity. "伤人" is not "温和误解"; "冷战" is not "快速反省"; "fight" is not "light disagreement" unless the user changes it.
- **No automatic moral cleanup**: do not protect a character's image by making them unusually mature, gentle, apologetic, or self-aware when the prompt asks for uglier behavior.
- **Interiority budget**: do not attach a paragraph of explanation to every action. If a character would not think deeply in that moment, show the action, silence, dodge, insult, hesitation, or consequence instead.
- **No purple prose**: avoid decorative abstractions that sound profound but do not change the scene, such as "the silence became a language." Prefer concrete pressure: what is withheld, what is said badly, what cannot be taken back.
- **Dialogue with rough edges**: conflict dialogue should have misses, interruptions, evasions, bad timing, incomplete sentences, and actual barbs. Do not make everyone speak like they prepared a clean classroom answer.
- **Detailed tension**: when a scene's tension is the point, do not summarize it away. Track beats: trigger, escalation, physical blocking, status shift, who notices, what is threatened, and what remains unresolved.

## Stage 0: Route the Work

Run before questions or writing.

1. Load `user-preferences.json` only for new projects, style-choice requests, "remember my preference" requests, or when project notes lack needed preference context. Treat it as soft guidance; current user instructions win.
2. Extract any intent already present in the user request: premise, genre, protagonist, conflict, tone, chapter count, stop point, automation level.
3. Locate the target project. Prefer a named folder; otherwise scan the workspace for a clear matching project.
4. Classify:
   - **New**: no planning pack -> Stage 1.
   - **Planning Ready**: pack exists, no prose -> summarize and proceed from Stage 2/3 boundary.
   - **Drafting**: pack plus some chapters/notes -> resume Stage 3.
   - **Review Ready**: all planned chapters complete -> Stage 4.
   - **Broken**: missing/stale planning, prose, or notes -> minimal repair before progress.
5. Repair lightly:
   - Prose without notes: create usable notes before advancing.
   - Notes without prose: chapter is incomplete.
   - Missing planning file: reconstruct from existing pack, notes, and prose.
   - Old and new filenames coexist: normalize to numbered pack.
6. Brief the user in 3-6 lines for non-new projects. Healthy existing planning packs are already confirmed; do not ask users to reconfirm them. In autonomous mode, continue after the brief unless a high-risk choice is required.

## Stage 1: Capture Intent

Use only for new projects or missing critical intent. Prefer one compact intake pass: ask at most 3 bundled questions that cover all missing essentials. If more than 3 fields are missing, group them into 2-3 broad questions instead of running a long menu. If the user wants full autonomy and gave enough direction, infer reasonable defaults and record them in `03-global-notes.md`.

Fast path for planning-only requests:

- If the user explicitly wants planning only, no prose yet, and has already supplied a usable broad frame (genre/premise + rough length + basic tone or relationship shape), do not block on intake.
- Build a **v1 planning pack with stated assumptions**. Mark every inferred default in `03-global-notes.md` and in the planning summary.
- Ask follow-up questions only for missing facts that would materially change the outline structure, timeline logic, or ending type.

Collect:

- Language and style baseline. For non-Chinese prose, request a sample only when style matching matters.
- Genre/premise.
- Protagonist setup, key relationships, profession/identity, and core personality.
- Core conflict and inner driver.
- Required conflict intensity, including any words the user used that must not be softened.
- World/background rules when relevant.
- POV, tone, theme, target reader, optional style references.
- Chapter count, target wordcount, stop point, must-include scenes, absolute exclusions.

For Chinese novels, favor a richer intake if needed: premise -> protagonist network -> conflict -> world -> POV/tone -> theme/reader -> scale/constraints. Mark preference-backed options, but do not override the user.

Show one compact configuration summary, then proceed. In autonomous mode, do not ask for a second confirmation unless the summary exposes a real ambiguity.

## Stage 2: Build the Planning Pack

Create or repair `novels/[Novel Name]/`.

1. `00-outline.md`
   - Use `references/outline-template.md`.
   - Read `references/plot-structures.md` only if structure selection is unclear.
   - Include every planned chapter: title, status, estimated words, POV, core events, psychological shift, foreshadowing, hook, planned time node.

2. `01-characters.md`
   - Use `references/character-template.md`.
   - Include protagonist, antagonist, key supporting cast, voice, boundaries, base routine, independent life, and rotating idle-action pool.

3. `02-timeline.md`
   - Use `references/timeline-template.md`.
   - Include D+N timeline, chapter duration, fixed schedules, planning locks, conflict log.
   - Resolve planning-level time contradictions before drafting.

4. `03-global-notes.md`
   - Use `references/global-notes-template.md`.
   - Include user preferences, style rules, taboos, lore limits, side-character activity tracker, repeated-behavior bans, long foreshadowing, conflict intensity locks, and interiority limits.
   - Copy any named character anti-tic reminders from user input or preferences, such as avoiding overuse of phone-checking or another repeated gesture.

5. `Generation Limit`
   - Record all chapters, chapter X, or the chapter containing the requested plot point.

Planning gate:

- Standard mode: show a compact plan summary and ask before drafting.
- Autonomous mode: show the summary and continue unless critical intent is missing or the user requested approval gates.
- Planning-only mode: show the compact plan summary, mark assumptions clearly, and stop after the planning pack as requested.

## Stage 3: Draft Chapters

Draft sequentially until `Generation Limit`.

### Next Chapter

1. Read `00-outline.md` status and planned order.
2. List existing `chapter-xx.md` and `chapter-xx-notes.md`.
3. A chapter is draft-complete only when prose exists and notes are usable.
4. Repair unusable notes before writing the next chapter.
5. Draft the earliest incomplete planned chapter.

### Pre-Flight

Read only:

- `00-outline.md`
- `01-characters.md`
- `02-timeline.md`
- `03-global-notes.md`
- relevant prior `chapter-xx-notes.md`

Extract current event, scene goal, POV, required conflict intensity, tension target, psychological shift if needed, previous emotional residue, unresolved hooks, foreshadowing, time window, locks, fixed schedules, and side-character opportunities.

### Side Characters

Blend necessity and distance:

- First ask whether the chapter has a real narrative reason for the character.
- Then check setting, routine, relationship pressure, and chapters since last appearance.
- If absent for 3-4 chapters, actively seek a natural low-intrusion beat.
- Do not force a major scene solely because they are overdue.
- Use brief presence, group chat, secondhand mention, background action, or independent-life detail when appropriate.
- Rotate idle actions. Obey repeated-behavior bans from `03-global-notes.md`.

### Prose

Write `chapter-xx.md` first. It contains only title and narrative prose.

Rules:

- Stay inside the timeline budget.
- Apply the craft capsule: concrete scene, prompt-faithful conflict, character-specific voice, time continuity, hook, no AI-flavored filler.
- Do not downgrade conflict. Keep fights, cruelty, cold wars, injury, betrayal, humiliation, avoidance, or silence at the level requested by the user and canon.
- Do not over-explain emotion. Use interiority sparingly; prefer visible behavior and consequences unless the POV demands direct thought.
- Do not pad with fluff or purple prose. Cut lines that sound deep but do not add pressure, information, choice, or consequence.
- When tension matters, write it in beats instead of summary: trigger, escalation, interruption, status change, damage, aftermath.
- End with a hook.
- Read dialogue/hook/expansion references only when that exact problem appears.
- If short, expand existing scenes; do not add timeline-breaking events.

### Notes and Sync

After prose, write `chapter-xx-notes.md` with:

- core event
- ending state
- time anchor
- appearing/mentioned characters
- relationship changes
- new canon facts
- foreshadowing added/resolved
- unresolved questions
- next-chapter handoff

Then:

1. Run wordcount when required.
2. Read `references/consistency.md` only when a timeline, character, or notes conflict is suspected.
3. Update `00-outline.md`, `02-timeline.md`, `03-global-notes.md`.
4. Update `01-characters.md` only for durable canon.
5. Stop at `Generation Limit`; otherwise continue.

## Parallel/Subagent Mode

Use only if explicitly requested.

Main agent owns shared canon files: `00-outline.md`, `01-characters.md`, `02-timeline.md`, `03-global-notes.md`.

Safe parallel tasks:

- **Planning split**: one worker drafts outline ideas, one drafts character/timeline risks, one drafts global-note constraints. Main agent merges into the four canon files.
- **Drafting support**: parallelize QA, notes repair, continuity checks, expansion suggestions, or independent scene research. Keep the next chapter itself on the critical path unless chapter ranges are truly independent and pre-planned.
- **Chapter writer**: if assigned, gets a disjoint chapter range and writes only those `chapter-xx.md` and `chapter-xx-notes.md` files.
- **Final review split**: workers audit disjoint chapter ranges and report conflicts. Main agent performs canon reconciliation.

Rules:

- Never assign two agents the same chapter.
- Workers must not rewrite shared canon unless explicitly assigned that file.
- Main agent integrates notes, timeline, outline status, and character updates after workers finish.
- If continuity depends on a previous unfinished chapter, keep that chapter on the critical path locally instead of parallelizing it.
- Prefer read-only parallel review over parallel prose generation when sequential continuity is fragile.

## Stage 4: Final Review

Enter only when all planned chapters are complete.

1. Brief: chapter count, known conflicts, files likely to change. In autonomous mode, continue unless raw-prose rewrites are large or destructive.
2. Verify every `chapter-xx.md` and `chapter-xx-notes.md` exists; run wordcount checks when required.
3. Build a conflict ledger, then read chapter prose in batches of 3-5 chapters to avoid context blowups.
4. Audit time continuity, plot causality, character consistency, POV, setup/payoff, side-character activity, repeated tics, AI flavor, prompt-faithful conflict intensity, over-explained psychology, purple prose, and locked constraints.
5. Reconcile only changed sections of `00-outline.md`, `01-characters.md`, `02-timeline.md`, `03-global-notes.md`, and affected chapter notes to match final prose.
6. Fix known timeline, plot, or character-setting conflicts immediately. Do not leave known contradictions unresolved.
7. Update `user-preferences.json` only when the user asked to remember something, or when a preference is stable across projects. Put project-specific reminders in `03-global-notes.md` instead.

## Stage 5: Handoff

When stopping:

- Partial run: report last completed chapter, next chapter, updated files, open hooks/conflicts.
- Full run: report review complete, conflicts fixed, canon files updated, residual risks.
- Blocked run: report current state, blocker, next action, and exact files needed.

Keep the report brief unless the user asks for detail.
