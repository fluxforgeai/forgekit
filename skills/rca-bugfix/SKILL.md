# RCA Bug Fix Procedure

**Trigger**: Use `/rca-bugfix {issue description}` when investigating and fixing bugs that require root cause analysis.

**Examples**:
- `/rca-bugfix health check timeout causing gray indicators on monitor page`
- `/rca-bugfix rate limiting still happening despite batch processing implementation`
- `/rca-bugfix extractions stuck at 0 records during streaming`

## Instructions

The user has provided an issue to investigate. THINK MAX HARD about this issue.

**Issue to investigate**: The argument passed after `/rca-bugfix`

---

## Input Sources

Before starting the RCA, check for upstream artifacts that provide context:

1. **`docs/investigations/*.md`** (from `/investigate`) -- If an investigation exists for this issue, read it first. It contains root cause analysis, evidence, and recommended fixes.
2. **`docs/findings/*.md`** (from `/finding`) -- If a proactive finding exists for this issue (and investigation was skipped), read it first. It contains classification, evidence, and preliminary assessment.
3. **User-provided description** (direct invocation) -- If no upstream artifacts exist, work from the description provided after `/rca-bugfix`.

**Note**: When a finding report exists with a known cause, the Root Cause section of the RCA may be shorter since the cause is already documented. Focus the RCA on confirming the cause, defining the fix, and writing the implementation prompt.

---

## CRITICAL: File Naming Convention

**ALL files MUST use this exact format**: `{YYYY-MM-DD_HHMM}_{issue_name}.md`

✅ **CORRECT**: `2026-01-22_1700_stream_download_timeout.md`
❌ **WRONG**: `RCA_STREAM_DOWNLOAD_TIMEOUT_2026-01-22.md`
❌ **WRONG**: `PROMPT_ADD_RETRY_2026-01-22.md`

- Date comes FIRST (e.g., `2026-01-22_1700`)
- Then underscore
- Then issue name in lowercase with underscores
- NO prefix like `RCA_` or `PROMPT_`

---

### Step 1: Initial Context Check

Ask the user to run `/context` and share the output.

Based on the context usage:

#### If context > 80% (not enough room):
1. Perform an **expert-level Root Cause Analysis (RCA)** on the issue
2. Write the RCA to `docs/RCAs/{YYYY-MM-DD_HHMM}_{issue_name}.md`
   - ✅ Example: `docs/RCAs/2026-01-22_1700_stream_download_timeout.md`
   - ❌ NOT: `docs/RCAs/RCA_STREAM_DOWNLOAD_TIMEOUT_2026-01-22.md`
3. Tell the user: "Context is high. RCA saved. Please run `/session-end` then `/verify-session` to start fresh."
4. **STOP** - Do not proceed further

#### If context <= 80% (enough room):
1. Perform an **expert-level Root Cause Analysis (RCA)** on the issue
2. Write the RCA to `docs/RCAs/{YYYY-MM-DD_HHMM}_{issue_name}.md`
   - ✅ Example: `docs/RCAs/2026-01-22_1700_stream_download_timeout.md`
   - ❌ NOT: `docs/RCAs/RCA_STREAM_DOWNLOAD_TIMEOUT_2026-01-22.md`
3. Using the RCA findings, write an **expert-level prompt** for `/plan` mode
4. Write the prompt to `docs/prompts/{YYYY-MM-DD_HHMM}_{issue_name}.md`
   - ✅ Example: `docs/prompts/2026-01-22_1700_stream_download_timeout.md`
   - ❌ NOT: `docs/prompts/PROMPT_ADD_RETRY_2026-01-22.md`
5. Proceed to Step 2

### Step 2: Pre-Planning Context Check

Ask the user to run `/context` again and share the output.

Based on the context usage:

#### If context > 85% (not enough room for planning):
1. Tell the user: "Context too high for planning. Please run `/session-end` then `/verify-session`"
2. Tell the user: "In the next session, run `/plan` with the prompt saved at `docs/prompts/{YYYY-MM-DD_HHMM}_{issue_name}.md`" (e.g., `docs/prompts/2026-01-22_1700_stream_download_timeout.md`)
3. **STOP**

#### If context <= 85% (enough room):
1. Tell the user: "Ready for planning. Please run `/plan`"
2. When in plan mode, use the expert-level prompt you wrote to guide the implementation plan

---

## Findings Tracker Update Protocol

At the START of RCA, check if this work relates to a tracked finding:

1. If input contains `F{N}` (e.g., "F1", "F3"), search `docs/findings/*_FINDINGS_TRACKER.md` for that finding
2. If input is topic-based, search active trackers for a matching finding title
3. If a match is found:
   a. Read the tracker, finding report, and any linked investigation report
   b. Use these as context for the RCA

At the END of RCA (after writing the RCA + implementation prompt):

1. Update the tracker's overview table: set `Stage` to `RCA Complete`, set `Status` to `In Progress`
2. Update the per-finding **Lifecycle** table — append row:
   ```
   | RCA Complete | {YYYY-MM-DD HH:MM} UTC | {session} | [RCA]({rca_path}) + [Prompt]({prompt_path}) |
   ```
3. Check the resolution task: `[x] **FN.2**: RCA + fix design...`
4. Add changelog entry:
   ```
   | {YYYY-MM-DD HH:MM} UTC | {session} | FN stage → RCA Complete. RCA: {rca_path}, Prompt: {prompt_path} |
   ```
5. Update `Last Updated` timestamp at top of tracker

**HANDOFF UPDATE** — After the standard handoff message to the user, add:

```
Tracker updated: {tracker_path} — FN stage → RCA Complete

After /plan completes, update the tracker:
- Stage → Planned
- Lifecycle row: `| Planned | {timestamp} | {session} | [Plan]({plan_path}) |`
- Check task: `[x] **FN.3**: Implementation plan...`
- Changelog: `FN stage → Planned. Plan: {plan_path}`
```

This ensures the tracker gets updated after /plan (which is EnterPlanMode and can't be modified directly).

If no matching finding exists, proceed normally — not all RCAs originate from findings.

---

## RCA Template

When writing RCAs, use this structure:

```markdown
# Root Cause Analysis: {Issue Title}

**Date**: {YYYY-MM-DD}
**Severity**: {Critical/High/Medium/Low}
**Status**: {Investigating/Identified/Resolved}

## Problem Statement
{Clear description of the issue}

## Symptoms
- {Observable symptom 1}
- {Observable symptom 2}

## Root Cause
{The actual underlying cause}

## Evidence
{Code snippets, logs, or data supporting the root cause}

## Impact
{What was affected and how}

## Resolution
{How to fix it}

## Prevention
{How to prevent this in the future}
```

---

## Prompt Template

When writing prompts for `/plan` mode, use this structure:

```markdown
# Implementation Prompt: {Issue Title}

**RCA Reference**: docs/RCAs/{YYYY-MM-DD_HHMM}_{issue_name}.md

## Context
{Brief summary of the root cause}

## Goal
{What needs to be implemented/fixed}

## Requirements
1. {Requirement 1}
2. {Requirement 2}

## Files Likely Affected
- {file1.py}
- {file2.tsx}

## Constraints
- {Any constraints or considerations}

## Acceptance Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}

---

## Plan Output Instructions

**IMPORTANT**: When you finish creating the implementation plan, save it to:
`docs/plans/{YYYY-MM-DD_HHMM}_{issue_name}.md`

Example: `docs/plans/2026-01-22_1800_stream_download_timeout.md`

The plan file should include:
- Summary of the approach
- Step-by-step implementation tasks
- Files to modify with specific changes
- Testing strategy
- Rollback plan (if applicable)
```
