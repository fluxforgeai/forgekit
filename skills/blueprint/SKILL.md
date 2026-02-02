# Blueprint Procedure

**Trigger**: Use `/blueprint {feature description}` when transforming design and research output into an implementation specification and prompt for `/plan` mode.

**Examples**:
- `/blueprint CSV migration with schema drift detection`
- `/blueprint add real-time WebSocket notifications to the monitoring dashboard`
- `/blueprint migrate authentication from session-based to JWT`

## Instructions

The user has described a feature or change to implement. THINK MAX HARD about how to turn existing design and research artifacts into a concrete implementation specification.

**Feature to blueprint**: The argument passed after `/blueprint`

---

## CRITICAL: File Naming Convention

**ALL files MUST use this exact format**: `{YYYY-MM-DD_HHMM}_{feature_name}.md`

✅ **CORRECT**: `2026-01-27_1200_csv_migration_schema_drift.md`
❌ **WRONG**: `BLUEPRINT_CSV_MIGRATION_2026-01-27.md`
❌ **WRONG**: `PROMPT_CSV_MIGRATION_2026-01-27.md`

- Date comes FIRST (e.g., `2026-01-27_1200`)
- Then underscore
- Then feature name in lowercase with underscores
- NO prefix like `BLUEPRINT_` or `PROMPT_`

---

### Step 1: Initial Context Check

Ask the user to run `/context` and share the output.

Based on the context usage:

#### If context > 80% (not enough room):
1. Perform an **expert-level Blueprint** of the feature
2. Write the blueprint to `docs/blueprints/{YYYY-MM-DD_HHMM}_{feature_name}.md`
   - ✅ Example: `docs/blueprints/2026-01-27_1200_csv_migration_schema_drift.md`
   - ❌ NOT: `docs/blueprints/BLUEPRINT_CSV_MIGRATION_2026-01-27.md`
3. Tell the user: "Context is high. Blueprint saved. Please run `/session-end` then `/verify-session` to start fresh."
4. **STOP** - Do not proceed further

#### If context <= 80% (enough room):
1. Perform an **expert-level Blueprint** of the feature
2. Write the blueprint to `docs/blueprints/{YYYY-MM-DD_HHMM}_{feature_name}.md`
   - ✅ Example: `docs/blueprints/2026-01-27_1200_csv_migration_schema_drift.md`
   - ❌ NOT: `docs/blueprints/BLUEPRINT_CSV_MIGRATION_2026-01-27.md`
3. Using the blueprint, write an **expert-level prompt** for `/plan` mode
4. Write the prompt to `docs/prompts/{YYYY-MM-DD_HHMM}_{feature_name}.md`
   - ✅ Example: `docs/prompts/2026-01-27_1200_csv_migration_schema_drift.md`
   - ❌ NOT: `docs/prompts/PROMPT_CSV_MIGRATION_2026-01-27.md`
5. Proceed to Step 2

### Step 2: Pre-Planning Context Check

Ask the user to run `/context` again and share the output.

Based on the context usage:

#### If context > 85% (not enough room for planning):
1. Tell the user: "Context too high for planning. Please run `/session-end` then `/verify-session`"
2. Tell the user: "In the next session, run `/plan` with the prompt saved at `docs/prompts/{YYYY-MM-DD_HHMM}_{feature_name}.md`" (e.g., `docs/prompts/2026-01-27_1200_csv_migration_schema_drift.md`)
3. **STOP**

#### If context <= 85% (enough room):
1. Tell the user: "Ready for planning. Please run `/plan`"
2. When in plan mode, use the expert-level prompt you wrote to guide the implementation plan

---

## Findings Tracker Update Protocol

At the START of blueprinting, check if this work relates to a tracked finding:

1. If input contains `F{N}` (e.g., "F1", "F3"), search `docs/findings/*_FINDINGS_TRACKER.md` for that finding
2. If input is topic-based, search active trackers for a matching finding title
3. If a match is found:
   a. Read the tracker, finding report, and any linked design analysis
   b. Use these as context for the blueprint

At the END of blueprinting (after writing the blueprint + implementation prompt):

1. Update the tracker's overview table: set `Stage` to `Blueprint Ready`, set `Status` to `In Progress`
2. Update the per-finding **Lifecycle** table — append row:
   ```
   | Blueprint Ready | {YYYY-MM-DD HH:MM} UTC | {session} | [Blueprint]({blueprint_path}) + [Prompt]({prompt_path}) |
   ```
3. Check the resolution task: `[x] **FN.2**: Blueprint + implementation prompt...`
4. Add changelog entry:
   ```
   | {YYYY-MM-DD HH:MM} UTC | {session} | FN stage → Blueprint Ready. Blueprint: {blueprint_path}, Prompt: {prompt_path} |
   ```
5. Update `Last Updated` timestamp at top of tracker

**HANDOFF UPDATE** — After the standard handoff message to the user, add:

```
Tracker updated: {tracker_path} — FN stage → Blueprint Ready

After /plan completes, update the tracker:
- Stage → Planned
- Lifecycle row: `| Planned | {timestamp} | {session} | [Plan]({plan_path}) |`
- Check task: `[x] **FN.3**: Implementation plan...`
- Changelog: `FN stage → Planned. Plan: {plan_path}`
```

This ensures the tracker gets updated after /plan (which is EnterPlanMode and can't be modified directly).

If no matching finding exists, proceed normally — not all blueprints originate from findings.

---

## Blueprint Analysis Process

When creating the blueprint, follow this process:

1. **Read upstream artifacts**: Check `docs/design/` and `docs/research/` for existing analysis related to the feature
2. **Extract requirements**: Identify what must be built from the design/research outputs (NOT diagnosing a bug — this is greenfield/proactive work)
3. **Define scope**: Clearly separate what's in-scope vs. out-of-scope
4. **Identify affected files**: List all files that will need changes
5. **Determine implementation sequence**: Order the work by dependencies
6. **Surface architecture decisions**: Document decisions already made and any that remain open
7. **Define acceptance criteria**: What does "done" look like?
8. **Identify dependencies and risks**: What could block or complicate implementation?

---

## Blueprint Template

When writing blueprints, use this structure:

```markdown
# Blueprint: {Feature Title}

**Date**: {YYYY-MM-DD}
**Design Reference**: {path to docs/design/*.md, if any}
**Research Reference**: {path to docs/research/*.md, if any}

## Objective
{Clear statement of what will be built and why}

## Requirements
1. {Requirement 1}
2. {Requirement 2}
3. {Requirement 3}

## Architecture Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| {Decision 1} | {Choice} | {Why} |
| {Decision 2} | {Choice} | {Why} |

## Scope

### In Scope
- {Item 1}
- {Item 2}

### Out of Scope
- {Item 1}
- {Item 2}

## Files Likely Affected
- {file1.py} — {what changes}
- {file2.tsx} — {what changes}

## Implementation Sequence
1. {Step 1} — {why this order}
2. {Step 2} — {depends on step 1 because...}
3. {Step 3}

## Dependencies & Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Risk 1} | {H/M/L} | {H/M/L} | {How to handle} |

## Acceptance Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Constraints
- {Constraint 1}
- {Constraint 2}
```

---

## Prompt Template

When writing prompts for `/plan` mode, use this structure:

```markdown
# Implementation Prompt: {Feature Title}

**Blueprint Reference**: docs/blueprints/{YYYY-MM-DD_HHMM}_{feature_name}.md
**Design Reference**: {path to docs/design/*.md, if any}

## Context
{Brief summary of the feature and why it's being built, drawn from the blueprint}

## Goal
{What needs to be implemented}

## Requirements
1. {Requirement 1}
2. {Requirement 2}

## Files Likely Affected
- {file1.py}
- {file2.tsx}

## Implementation Sequence
1. {Step 1}
2. {Step 2}

## Constraints
- {Any constraints or considerations}

## Acceptance Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}

---

## Plan Output Instructions

**IMPORTANT**: When you finish creating the implementation plan, save it to:
`docs/plans/{YYYY-MM-DD_HHMM}_{feature_name}.md`

Example: `docs/plans/2026-01-27_1300_csv_migration_schema_drift.md`

The plan file should include:
- Summary of the approach
- Step-by-step implementation tasks
- Files to modify with specific changes
- Testing strategy
- Rollback plan (if applicable)
```
