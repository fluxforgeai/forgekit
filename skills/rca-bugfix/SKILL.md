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
