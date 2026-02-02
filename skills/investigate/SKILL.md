# Deep Investigation Skill

**Trigger**: Use `/investigate {incident or finding report}` when you need a thorough investigation of an incident, bug, unexpected behavior, or proactive finding.

**Input**: An incident report (from `/incident`) or a finding report (from `/finding`) describing what happened or what was found.

**Examples**:
- `/investigate Extraction hung at 12% - no error in logs, last event was url_refresh_triggered at 07:38 UTC`
- `/investigate Rate limiting errors despite batch processing - 429 responses every 2 seconds starting 14:00 UTC`
- `/investigate Health check showing red but API responding - monitor page shows Backend=red since 09:15 UTC`
- `/investigate Finding: Missing companyId filter in invoice WHERE clauses -- authorization gap`

---

## Instructions

THINK MAX HARD about this incident or finding.

### Input Type Detection

Determine the input type and route accordingly:

```
IF input references a finding report (docs/findings/*.md) OR starts with "Finding:":
    → Confirmation Mode (abbreviated investigation)
ELSE:
    → Full Investigation Mode (standard investigation)
```

### Full Investigation Mode (incidents)

1. **Research online** for relevant documentation and known issues (search as of {current_month_year})
2. **Consult relevant API/library documentation** based on what the incident involves (search as of {current_month_year})
3. **Deeply investigate** the incident provided after `/investigate`
4. **Review past RCAs and Investigations** in `docs/RCAs/` and `docs/investigations/` to avoid repeating errors and recognize patterns
5. **Write detailed Investigation Report** to `docs/investigations/{YYYY-MM-DD_HHMM}_{issue_name}.md`
6. **THEN STOP** and await further instructions

### Confirmation Mode (findings)

When a proactive finding is provided, the cause is often already known. The investigation confirms scope and validates the finding:

1. **Read the finding report** in `docs/findings/` to understand what was found
2. **Confirm the finding is real** -- reproduce or verify the evidence
3. **Determine scope** -- is it isolated or systemic?
4. **Document additional evidence** beyond what the finding captured
5. **Assess impact** -- what is the blast radius if unaddressed?
6. **Write abbreviated Investigation Report** to `docs/investigations/{YYYY-MM-DD_HHMM}_{issue_name}.md`
7. **THEN STOP** and await further instructions

---

## Investigation Process

### Step 1: External Research

**Search online** (use current date context: {current_month_year}):
- Search for known issues, bugs, or limitations related to the problem
- Search for relevant API documentation updates
- Look for community discussions or Stack Overflow answers

**Consult Relevant Documentation**:

First, identify what technology/API/library the incident involves. Then search for documentation specific to that technology.

**EXAMPLES** (use these as a pattern, NOT as default searches):
- If the incident involves **Iterable**: Search "Iterable API {relevant_topic} {current_month_year}"
- If the incident involves **Intercom**: Search "Intercom API {relevant_topic} {current_month_year}"
- If the incident involves **GCS/Google Cloud Storage**: Search "Google Cloud Storage {relevant_topic} {current_month_year}"
- If the incident involves **httpx/requests**: Search "Python httpx {relevant_topic} {current_month_year}"
- If the incident involves **FastAPI**: Search "FastAPI {relevant_topic} {current_month_year}"
- If the incident involves **PostgreSQL**: Search "PostgreSQL {relevant_topic} {current_month_year}"

**IMPORTANT**: Only search documentation relevant to the actual incident. Do NOT default to searching Iterable or Intercom docs unless the incident specifically involves those APIs.

From the documentation, extract:
- Rate limits, timeouts, expected behavior
- Recent API changes or deprecations
- Known limitations or gotchas

### Step 2: Gather Internal Evidence

- Search logs for relevant events
- Read related source code files
- Check recent changes that might be related
- Look for patterns in timing, data, or behavior

### Step 3: Build Timeline

Construct a precise timeline of events:
- When did the incident first appear?
- What happened immediately before?
- What was the system state?

### Step 4: Identify Root Cause

- Distinguish between symptoms and causes
- Identify primary, secondary, and contributing factors
- Trace the code path that led to the incident
- Compare our implementation against official API documentation

### Step 5: Analyze Impact

- What was affected?
- How much data/time was lost?
- What is the blast radius?

### Step 6: Review Past RCAs and Investigations (MANDATORY)

**Before recommending any fixes**, you MUST:

1. **Read all files in `docs/RCAs/`** - Look for:
   - Similar issues that were previously resolved
   - Fixes that were implemented and their effectiveness
   - Patterns that keep recurring

2. **Read all files in `docs/research/`** - Look for:
   - Previous research on related technologies or APIs
   - Best practices and anti-patterns already documented
   - Implementation guidance that applies to this incident

3. **Read all files in `docs/plans/`** - Look for:
   - Implementation plans that addressed similar issues
   - Approaches that were planned but may not have been fully implemented
   - Step-by-step fixes that could be reused or adapted

4. **Read all files in `docs/investigations/`** - Look for:
   - Related incidents
   - Root causes that might apply here
   - Recommended fixes that were or weren't implemented

5. **Read all files in `docs/findings/`** - Look for:
   - Related proactive findings
   - Known issues that may connect to this incident
   - Evidence or assessments that apply here

3. **Document patterns found**:
   - Has this exact issue occurred before?
   - Has a similar issue occurred before?
   - Did a previous fix inadvertently cause this issue?
   - Is this a regression of a previously fixed bug?

**This step ensures we**:
- Don't repeat mistakes
- Learn from past incidents
- Recognize recurring patterns
- Build on previous solutions rather than reinventing them
- Leverage existing research on related technologies

---

## Investigation Report Template

Write the report to: `docs/investigations/{YYYY-MM-DD_HHMM}_{issue_name}.md`

Example: `docs/investigations/2026-01-22_1645_url_refresh_timeout.md`

Use this structure:

```markdown
# Investigation: {Issue Title}

**Date**: {YYYY-MM-DD}
**Investigator**: Claude Code (Session {number})
**Severity**: {Critical/High/Medium/Low}
**Status**: Investigation Complete

---

## Executive Summary

{2-3 sentences describing what happened and the impact}

---

## External Research Findings

### Official Documentation Consulted
- {Technology/API name}: {Link to relevant docs}
- {Key findings from docs}

### Known Issues / Community Reports
- {Any relevant issues found online}
- {Stack Overflow, GitHub issues, forum posts}

### API/Library Behavior Notes
- {Documented rate limits, timeouts, etc.}
- {Any undocumented behavior discovered}

---

## Learnings from Previous RCAs/Investigations/Research

### Related Past Incidents
- {List any related RCAs, investigations, or research found}
- {What was learned from them}

### Patterns Identified
- {Is this a recurring issue?}
- {Has a similar fix been attempted before?}

### Applicable Previous Solutions
- {Solutions from past incidents that might apply here}

---

## Timeline of Events

| Time (UTC) | Event | Details |
|------------|-------|---------|
| HH:MM:SS | Event name | Description |

---

## Root Cause Analysis

### Primary Cause
{The main reason this happened}

### Secondary Cause
{Contributing factor}

### Tertiary Cause (if applicable)
{Additional contributing factor}

---

## Contributing Factors

### 1. {Factor Name}
{Description with code evidence}

### 2. {Factor Name}
{Description with code evidence}

---

## Evidence

### Log Evidence
```json
{Relevant log entries}
```

### Code Evidence
```python
# file.py:line_number
{Relevant code snippet}
```

---

## Impact Assessment

| Metric | Value |
|--------|-------|
| Records affected | X |
| Data loss | X% |
| Downtime | X minutes |

---

## Recommended Fixes

### Fix 1: {Title} (HIGH/MEDIUM/LOW PRIORITY)
{Description with code example}

**Informed by**: {Reference to past RCA/investigation if applicable, or "New approach"}

### Fix 2: {Title} (HIGH/MEDIUM/LOW PRIORITY)
{Description with code example}

**Informed by**: {Reference to past RCA/investigation if applicable, or "New approach"}

---

## Upstream/Downstream Impact Analysis

### Upstream (Callers)
{What calls the affected code}

### Downstream (Called Methods)
{What the affected code calls}

---

## Verification Plan

1. {How to verify fix 1 works}
2. {How to verify fix 2 works}

---

**Investigation Complete**: {YYYY-MM-DD HH:MM} UTC
**Ready for**: {RCA Document / Implementation Plan / Fix}
```

---

## After Writing the Report

### Full Investigation Mode Output

**STOP** and tell the user:

```
Investigation complete.

Report saved to: docs/investigations/{YYYY-MM-DD_HHMM}_{issue_name}.md

Summary: {1-2 sentence summary}

Sources consulted:
- {List of documentation/URLs researched}

Past RCAs/Investigations/Research reviewed:
- {List of related past documents consulted}

Awaiting your instructions. Options:
1. Run `/rca-bugfix` to create RCA and implementation prompt
2. Run `/plan` to start planning the fix
3. Ask me to investigate further
```

### Confirmation Mode Output

**STOP** and tell the user:

```
Finding confirmed.

Report saved to: docs/investigations/{YYYY-MM-DD_HHMM}_{issue_name}.md

Finding: {reference to original finding report}
Scope: {isolated | systemic | broader than expected}
Confirmed: {Yes -- real issue | Partially -- narrower than reported | No -- false positive}

Awaiting your instructions. Options:
1. Run `/rca-bugfix` to fix the confirmed issue (cause is known)
2. Run `/plan` to start planning the fix
3. Ask me to investigate further
```

Do NOT proceed with fixes or additional work until the user responds.
