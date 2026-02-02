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
4. Suggest the appropriate next step based on classification
5. **STOP** and await further instructions

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

## Handoff Protocol

After writing the finding report, suggest the next step based on the finding type:

### Defect or Vulnerability
```
Finding logged: docs/findings/{YYYY-MM-DD_HHMM}_{name}.md

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

Summary: {One-line factual summary}
Type: {Debt | Gap | Drift} | Severity: {level}

This needs a design decision. Recommended next steps:
1. /design tradeoff {topic} -- if multiple approaches exist
2. /design migrate {topic} -- if moving between implementations
3. /design from-scratch {topic} -- if building a new capability

Awaiting your instructions.
```

**Do NOT continue.** Wait for the user to decide how to proceed.
