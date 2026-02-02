# Proactive Finding Skill

**Trigger**: Use `/finding {description}` to log a proactive discovery -- something found by analysis, review, or inspection that needs attention.

**Purpose**: Create a factual record of WHAT was found. Not FIX it -- that's for downstream skills.

**Examples**:
- `/finding Missing companyId filter in invoice WHERE clauses -- authorization gap`
- `/finding Deprecated bcrypt v2.1 in auth service -- known CVE`
- `/finding Config drift: staging environment has debug logging enabled in production`

---

## Instructions

1. Gather facts from analysis output, code inspection, or user description
2. Classify the finding by type and severity
3. Write a finding report to `docs/findings/{YYYY-MM-DD_HHMM}_{name}.md`
4. Create or update the Findings Tracker (see **Findings Tracker Protocol** below)
5. Suggest the appropriate next step based on classification
6. **STOP** and await further instructions

**Do NOT** proceed with fixes, investigations, or design work -- that is the job of downstream skills.

---

## Finding Report Rules

- **Factual only** -- describe what you observed, not what you assume
- **Neutral language** -- no blame, no speculation, no opinions
- **Specific** -- exact file paths, exact code patterns, exact scope
- **Classified** -- every finding gets a type and severity

**DO**: "WHERE clause in `invoices.py:47` filters by `user_id` but not `company_id`"
**DON'T**: "Authorization is broken" or "Security is poor"

---

## Classification Taxonomy

### Finding Types

| Type | Description | Resolution Branch |
|------|-------------|-------------------|
| **Defect** | Known bug found proactively (not via incident) | `/investigate` then `/rca-bugfix` |
| **Vulnerability** | Security issue with known exposure | `/investigate` then `/rca-bugfix` |
| **Debt** | Technical debt requiring remediation | `/design {mode}` |
| **Gap** | Missing expected capability or coverage | `/design {mode}` |
| **Drift** | Configuration, documentation, or code divergence from intent | `/design {mode}` or `/rca-bugfix` |

### Severity Levels

| Severity | Criteria |
|----------|----------|
| **Critical** | Active security exposure, data loss risk, or production breakage imminent |
| **High** | Significant impact on reliability, security, or core functionality |
| **Medium** | Moderate impact, workaround exists, not immediately dangerous |
| **Low** | Minor issue, cosmetic, or optimization opportunity |

---

## Report Template

Write to: `docs/findings/{YYYY-MM-DD_HHMM}_{name}.md`

Example: `docs/findings/2026-02-02_0800_taxonomy_gap_proactive_findings.md`

```markdown
# Finding: {Brief Title}

**Date**: {YYYY-MM-DD}
**Discovered by**: {Skill or method that found this, e.g., `/analyze architecture`}
**Type**: {Defect | Vulnerability | Debt | Gap | Drift}
**Severity**: {Critical | High | Medium | Low}
**Status**: Open

---

## What Was Found

{Factual description of the finding. What exists or is missing, where, and what it affects.}

---

## Affected Components

- {File, module, or system 1}
- {File, module, or system 2}

---

## Evidence

{Code snippets, configuration excerpts, test results, or analysis output that demonstrates the finding.}

---

## Preliminary Assessment

**Likely cause**: {Brief factual assessment of why this exists}

**Likely scope**: {How widespread is this -- isolated or systemic?}

**Likely impact**: {What happens if this is not addressed?}

---

## Classification Rationale

**Type: {Type}** -- {Why this type was chosen over alternatives}

**Severity: {Severity}** -- {What criteria drove the severity rating}

---

**Finding Logged**: {YYYY-MM-DD HH:MM} UTC
```

---

## Findings Tracker Protocol

After writing the individual finding report(s), create or update a Findings Tracker. Each **group of related findings** gets its own named tracker. Multiple trackers can coexist in `docs/findings/` — one per investigation, analysis, or problem domain.

**Naming convention**: `docs/findings/{YYYY-MM-DD_HHMM}_{findings_name}_FINDINGS_TRACKER.md`

The `{findings_name}` is a concise snake_case descriptor of what the findings are about.

**Examples**:
- `2026-02-02_1639_iterable_extraction_pipeline_FINDINGS_TRACKER.md`
- `2026-03-15_0900_auth_authorization_gaps_FINDINGS_TRACKER.md`
- `2026-04-01_1400_api_rate_limiting_FINDINGS_TRACKER.md`

### Decision: Create vs Update

1. Check `docs/findings/` for existing `*_FINDINGS_TRACKER.md` files
2. If findings are **clearly related** to an existing tracker's scope (same system, same root analysis, same problem domain) → **UPDATE** that tracker by adding the new finding(s)
3. If findings are a **new topic**, or no tracker exists, or scope is unclear → **CREATE** a new tracker with a descriptive `{findings_name}`

**When in doubt, create a new tracker.** It is better to have two focused trackers than one bloated tracker mixing unrelated concerns.

### Finding Numbering

- Findings are numbered **F1, F2, F3...** in creation order
- When updating an existing tracker, determine the next number by finding the highest existing FN and incrementing
- F-numbers are **stable identifiers** -- never renumber existing findings

### Overview Table Ordering

The overview table is **always sorted by severity** (most critical first): Critical → High → Medium → Low. Within the same severity level, maintain creation order. Finding detail sections in the document follow the same order as the table.

### Resolution Tasks by Finding Type

Auto-generate resolution tasks based on the finding's classification:

**Defect or Vulnerability** (Corrective Route):
```
- [ ] **FN.1**: Investigate — confirm root cause and scope (→ /investigate → Stage: Investigating)
- [ ] **FN.2**: RCA + fix design (→ /rca-bugfix → Stage: RCA Complete)
- [ ] **FN.3**: Implementation plan (→ /plan → Stage: Planned)
- [ ] **FN.4**: Implement fix (Stage: Implementing → Resolved)
- [ ] **FN.5**: Verify fix in production/test (Stage: Verified)
```

**Debt, Gap, or Drift** (Design Route):
```
- [ ] **FN.1**: Design approach (→ /design → Stage: Designing)
- [ ] **FN.2**: Blueprint + implementation prompt (→ /blueprint → Stage: Blueprint Ready)
- [ ] **FN.3**: Implementation plan (→ /plan → Stage: Planned)
- [ ] **FN.4**: Implement changes (Stage: Implementing → Resolved)
- [ ] **FN.5**: Verify implementation (Stage: Verified)
```

The recommended downstream skill for each task should be included inline:
- Confirm root cause → `/investigate`
- Implement fix → `/rca-bugfix`
- Design approach → `/design tradeoff` or `/design migrate` or `/design from-scratch`

If the finding report provides enough detail to make tasks more specific (exact file paths, exact code changes), **replace the generic tasks with specific ones**. The templates above are fallbacks.

### CREATE: New Tracker Template

Write to: `docs/findings/{YYYY-MM-DD_HHMM}_{findings_name}_FINDINGS_TRACKER.md`

```markdown
**{YYYY-MM-DD HH:MM} UTC**

# {Findings Name} — Findings Tracker

**Created**: {YYYY-MM-DD HH:MM} UTC
**Last Updated**: {YYYY-MM-DD HH:MM} UTC
**Origin**: {What triggered these findings, e.g., "Systems analysis of inAppDelivery extraction"}
**Session**: {Session number, if known}
**Scope**: {One-line description of what this tracker covers, e.g., "Iterable batch extraction reliability and monitoring"}

---

## Overview

{One sentence describing the scope of tracked findings.}

| # | Finding | Type | Severity | Status | Stage | Report |
|---|---------|------|----------|--------|-------|--------|
| F1 | {Brief title} | {Type} | **{Severity}** | Open | Open | [Report]({relative_path_to_finding_report}) |

**Status legend**: `Open` → `In Progress` → `Resolved` → `Verified`
**Stage legend**: `Open` → `Investigating` / `Designing` → `RCA Complete` / `Blueprint Ready` → `Planned` → `Implementing` → `Resolved` → `Verified`

---

## Dependency Map

```
No dependencies mapped yet. Update as relationships between findings are identified.
```

---

## F1: {Brief Title} ({Severity} {Type})

**Summary**: {One-line factual summary from the finding report's "What Was Found"}

**Root cause**: {From the finding report's Preliminary Assessment — "Likely cause"}

**Resolution tasks**:

{Auto-generated tasks based on finding type — see Resolution Tasks section above}

**Recommended approach**: {Downstream skill from Classification Taxonomy — e.g., `/rca-bugfix` or `/design tradeoff`}

**Status**: Open
**Stage**: Open
**Resolved in session**: —
**Verified in session**: —
**Notes**: —

**Lifecycle**:
| Stage | Timestamp | Session | Artifact |
|-------|-----------|---------|----------|
| Open | {YYYY-MM-DD HH:MM} UTC | {N} | [Finding Report]({relative_path_to_finding_report}) |

---

## Changelog

| Date | Session | Action |
|------|---------|--------|
| {YYYY-MM-DD HH:MM} UTC | {N} | Created tracker. F1 logged ({Severity} {Type}). |

---

## Cross-References

| Document | Description |
|----------|-------------|
| {finding_report_path} | F1 finding report |
```

### UPDATE: Adding to an Existing Tracker

When findings are related to an existing `*_FINDINGS_TRACKER.md`, add them to it:

1. **Assign next F-number**: Find the highest existing FN in the tracker, use N+1
2. **Add row to overview table**: Insert in severity-sorted position (Critical first, Low last)
3. **Add finding detail section**: Insert in the same severity-sorted position (before the Changelog section, after the last finding section of equal or higher severity)
4. **Add changelog entry**: New row with date, session, and `FN logged ({Severity} {Type})`
5. **Add cross-reference entry**: Link to the new finding report
6. **Update `Last Updated`** timestamp at top of tracker

### Batch Findings

When a single `/finding` invocation produces multiple findings (e.g., from a comprehensive analysis):

- Assign F-numbers sequentially (F1, F2, F3...)
- Add ALL findings to the tracker in one pass
- Sort the overview table by severity after all are added
- Changelog gets ONE entry: `Created tracker. F1-FN logged from {source}.` (for creation) or `FN-FM added from {source}.` (for update)

---

## Lifecycle Tracking Protocol

Every downstream skill that processes a finding MUST update the Findings Tracker. This ensures the tracker reflects the true state of each finding at all times.

### How It Works

- Each finding has a **Status** (coarse: Open → In Progress → Resolved → Verified) and a **Stage** (fine-grained pipeline position)
- When a downstream skill processes a finding, it updates: Stage column, lifecycle table row, resolution task checkbox, and changelog entry
- The F-number (`F1`, `F2`, etc.) is the stable identifier used across all skills. Downstream skills accept `F{N}` as input to identify the finding

### Stage Progression

**Corrective Route** (Defect / Vulnerability):
```
Open → Investigating → RCA Complete → Planned → Implementing → Resolved → Verified
         /investigate    /rca-bugfix    /plan      (code work)   session-end  session-end
```

**Design Route** (Debt / Gap / Drift):
```
Open → Designing → Blueprint Ready → Planned → Implementing → Resolved → Verified
        /design      /blueprint       /plan      (code work)   session-end  session-end
```

### Stage ↔ Status Mapping

| Stage | Status |
|-------|--------|
| Open | Open |
| Investigating / Designing | In Progress |
| RCA Complete / Blueprint Ready | In Progress |
| Planned | In Progress |
| Implementing | In Progress |
| Resolved | Resolved |
| Verified | Verified |

Status is the coarse view (4 states) — preserved for backward compatibility.
Stage is the fine-grained view (7 states) — tracks pipeline position.

### What Each Downstream Skill Updates

| Skill | Sets Stage To | Checks Task | Lifecycle Row Artifact |
|-------|--------------|-------------|----------------------|
| `/investigate` | Investigating | FN.1 | Investigation report |
| `/rca-bugfix` | RCA Complete | FN.2 | RCA + Prompt |
| `/design` | Designing | FN.1 (design route) | Design analysis |
| `/blueprint` | Blueprint Ready | FN.2 (design route) | Blueprint + Prompt |
| `/plan` (via handoff) | Planned | FN.3 | Plan |
| code implementation | Implementing → Resolved | FN.4 | Commit/PR |
| verification | Verified | FN.5 | Test/validation |

### Update Checklist (for downstream skills)

When a downstream skill processes a tracked finding, it MUST:
1. Update the overview table: set `Stage` column to the new stage
2. Update the overview table: set `Status` column per the Stage ↔ Status mapping
3. Append a row to the per-finding **Lifecycle** table
4. Check the corresponding resolution task checkbox (`[x]`)
5. Add a changelog entry: `| {date} | {session} | FN stage → {Stage}. {Artifact}: {path} |`
6. Update `Last Updated` timestamp at top of tracker

---

## Handoff Protocol

After writing the finding report, suggest the next step based on the finding type:

### Defect or Vulnerability
```
Finding logged: docs/findings/{YYYY-MM-DD_HHMM}_{name}.md
Tracker updated: docs/findings/{YYYY-MM-DD_HHMM}_{findings_name}_FINDINGS_TRACKER.md (FN)

Summary: {One-line factual summary}
Type: {Defect | Vulnerability} | Severity: {level}

This is a corrective fix candidate. Recommended next steps:
1. /investigate {one-line summary} -- to confirm scope and impact
2. /rca-bugfix {one-line summary} -- if cause is already clear

Awaiting your instructions.
```

### Debt, Gap, or Drift
```
Finding logged: docs/findings/{YYYY-MM-DD_HHMM}_{name}.md
Tracker updated: docs/findings/{YYYY-MM-DD_HHMM}_{findings_name}_FINDINGS_TRACKER.md (FN)

Summary: {One-line factual summary}
Type: {Debt | Gap | Drift} | Severity: {level}

This needs a design decision. Recommended next steps:
1. /design tradeoff {topic} -- if multiple approaches exist
2. /design migrate {topic} -- if moving between implementations
3. /design from-scratch {topic} -- if building a new capability

Awaiting your instructions.
```

### Batch Findings (multiple from one analysis)
```
Findings logged:
  F1: docs/findings/{YYYY-MM-DD_HHMM}_{name1}.md — {Severity} {Type}
  F2: docs/findings/{YYYY-MM-DD_HHMM}_{name2}.md — {Severity} {Type}
  ...

Tracker: docs/findings/{YYYY-MM-DD_HHMM}_{findings_name}_FINDINGS_TRACKER.md

{For each finding, list its one-line summary and recommended next step}

Awaiting your instructions.
```

**Do NOT continue.** Wait for the user to decide how to proceed.
