# Research: How Industry Frameworks Handle Proactive Findings vs Reactive Incidents

**Date**: 2026-02-02
**Researcher**: Claude Code
**Status**: Complete

---

## Question

ForgeKit's dual-pipeline architecture has a gap for proactive findings that need corrective action without design decisions. How do established industry frameworks (ITIL, security, static analysis) handle this category of finding?

---

## TL;DR

All three frameworks agree: proactive findings are NOT incidents and should NOT be forced through incident workflows. ITIL has Proactive Problem Management (separate from Incident Management). Security has the Vulnerability Management Lifecycle (separate from Incident Response). SonarQube classifies all findings by type (Bug/Vulnerability/Code Smell) with no incident concept at all. The consistent pattern: proactive findings need their own entry point, their own classification, and their own resolution path -- while still producing documentation that feeds back into the system.

---

## Official Documentation

### ITIL: Proactive Problem Management

ITIL separates "Incident Management" (reactive) from "Problem Management" (proactive):

> "Proactive Problem Management is an ongoing activity that tries to identify issues to prevent resulting Incidents from happening."

ITIL's flow for proactive findings:
1. **Proactive Problem** identified (via analysis, trend monitoring, etc.)
2. **Known Error Record** created (documents cause and workaround)
3. **Request for Change (RFC)** generated (the fix)
4. **Change Management** implements the fix

ITIL does NOT force proactive findings through the incident pipeline. They have their own process that still produces documentation feeding back into the Known Error Database.

### Key Points from ITIL
- Proactive findings are "Problems", not "Incidents"
- Problems have their own lifecycle separate from incidents
- The Known Error Record is the institutional memory artifact
- Change Requests bridge from problem identification to implementation

### Security: Vulnerability Management Lifecycle

Security frameworks treat proactive vulnerability discovery as its own lifecycle:

> "Rather than reacting to incidents, organizations adopt a proactive stance, addressing weaknesses before they become active threats."

The Vulnerability Management Lifecycle:
1. **Discover** -- identify vulnerabilities (scanning, code review, analysis)
2. **Assess** -- evaluate severity and impact
3. **Prioritize** -- rank by risk
4. **Remediate** -- fix, mitigate, or accept
5. **Verify** -- confirm the fix works
6. **Monitor** -- watch for recurrence

If a vulnerability becomes an active threat, it ESCALATES to incident response. But the normal path is proactive: find -> assess -> fix -> verify.

### SonarQube: Finding Classification Taxonomy

SonarQube classifies proactive findings by type and severity:

| Type | Definition | Example |
|------|-----------|---------|
| **Bug** | Code that is broken or will break | Null dereference |
| **Vulnerability** | Security weakness | SQL injection |
| **Code Smell** | Maintainability issue | Long method, duplication |
| **Security Hotspot** | Needs manual review | Hardcoded credential pattern |

Severity levels: Blocker, Critical, Major, Minor, Info.

SonarQube's taxonomy is entirely proactive. Nothing is an "incident." Everything is a "finding" with a type and severity. The classification determines the remediation workflow.

---

## Community Knowledge

### Synthesis: What All Three Frameworks Agree On

1. **Proactive findings are NOT incidents** -- they have their own entry point and lifecycle
2. **Proactive findings still need full documentation** -- the audit trail matters
3. **Classification drives the remediation path** -- different finding types get different workflows
4. **The documentation feeds back** -- ITIL's Known Error DB, SonarQube's issue history, VML's remediation records all enable pattern detection and institutional memory

### Common Pitfalls Mentioned
- Forcing proactive findings through incident workflows loses template fidelity (fields don't fit)
- Skipping documentation for "trivial" fixes breaks the feedback loop
- Not classifying finding types leads to uniform (wrong) remediation approaches

---

## Best Practices

Based on research:

1. **Separate entry points for reactive vs proactive**: Don't merge incidents and findings into one concept. Their templates, fields, and workflows are fundamentally different.
2. **Classify findings by type**: The type determines the resolution path. Defects get fixed directly. Structural issues get designed first. This is the branching logic.
3. **Every finding produces an artifact**: Even trivial fixes should create a finding record. The artifact is what feeds the flywheel -- not the fix itself.

---

## Relevance to ForgeKit

ForgeKit's dual-pipeline architecture maps to the reactive/proactive split but misses the audit/corrective category. The gap aligns exactly with what all three frameworks independently solved.

### Files That May Be Affected
- `skills/analyze/SKILL.md` -- needs Fix Escalation alongside Design Escalation
- `skills/analyze/DESIGN_ESCALATION.md` -- needs broadening or a sibling `FIX_ESCALATION.md`
- `skills/investigate/SKILL.md` -- needs to accept finding reports (not just incidents)
- `skills/rca-bugfix/SKILL.md` -- needs to accept findings from investigate (not just incidents)
- `README.md` -- needs three pipelines documented
- `ARCHITECTURE.md` -- needs updated skills layer diagram
- `CONVENTIONS.md` -- needs `docs/findings/` directory
- `PRD.md` -- needs `/finding` skill entry and updated differentiator

---

## Implementation Analysis

### Already Implemented
- Design Escalation in `/analyze`: `skills/analyze/DESIGN_ESCALATION.md` -- handles the proactive-to-design path
- Shared artifact communication: `CONVENTIONS.md` -- skills already read/write shared docs
- Handoff protocol: all skills suggest next steps at completion

### Should Implement
1. **New `/finding` skill**
   - Why: Provides the missing entry point for proactive findings (equivalent of `/incident` for reactive)
   - Where: `skills/finding/SKILL.md`
   - How: Finding report template with type classification (Defect/Vulnerability/Debt/Gap/Drift)

2. **Fix Escalation in `/analyze`**
   - Why: `/analyze` can escalate to `/design` but not to corrective fix. Needs both paths.
   - Where: `skills/analyze/SKILL.md` escalation checkpoints
   - How: Add "Corrective fix (suggests /finding)" option alongside Design Escalation

3. **Investigation confirmation mode**
   - Why: `/investigate` expects incidents with unknown causes. Findings with known causes need abbreviated investigation (confirm scope, document evidence).
   - Where: `skills/investigate/SKILL.md`
   - How: Input type selector (incident vs finding) with adjusted depth

### Should NOT Implement
1. **Broadening `/incident` to include findings**
   - Why not: `/incident` has a specific, clean definition ("factual record of WHAT happened"). Its template fields (chronological timeline, "Reported by: User/System/Monitoring", raw log evidence) don't apply to proactive findings. Broadening it would muddle both concepts.
   - Source: ITIL precedent -- incidents and problems are deliberately separate processes.

2. **Skipping documentation for "trivial" fixes**
   - Why not: Breaks the flywheel. The documentation IS the product value. "Trivial" fixes accumulate into patterns that only `/analyze patterns` can detect if the artifacts exist.
   - Source: All three frameworks require documentation regardless of fix complexity.

---

## Sources

1. [Atlassian - Problem Management in ITIL](https://www.atlassian.com/itsm/problem-management) -- Proactive vs reactive problem management
2. [Rezolve.ai - Incident vs Problem vs Change Management](https://www.rezolve.ai/blog/incident-management-vs-problem-management-vs-change-management) -- ITIL process relationships
3. [IBM - Vulnerability Management Lifecycle](https://www.ibm.com/think/topics/vulnerability-management-lifecycle) -- VML phases and proactive approach
4. [Red Canary - Vulnerability Management Lifecycle](https://redcanary.com/cybersecurity-101/security-operations/vulnerability-management-lifecycle/) -- Discovery-to-remediation workflow
5. [SentinelOne - Vulnerability Management Lifecycle](https://www.sentinelone.com/cybersecurity-101/cybersecurity/vulnerability-management-lifecycle/) -- Proactive stance vs reactive approach
6. [Sonar - How to Identify and Prioritize Critical Code Issues](https://www.sonarsource.com/resources/library/critical-code-issues/) -- SonarQube finding taxonomy
7. [Hyperproof - How to Remediate Your Audit Findings](https://hyperproof.io/resource/audit-findings-remediation-efforts/) -- Audit finding remediation workflow
8. [Dawgen Global - From Findings to Fixes](https://www.dawgen.global/from-findings-to-fixes-the-dawgen-method-for-remediation-that-actually-sticks/) -- Structured remediation methodology

---

## Related Documents

- Finding: `docs/findings/2026-02-02_0800_taxonomy_gap_proactive_findings.md`
- Design: `docs/design/2026-02-02_0830_audit_pipeline_and_finding_skill.md`
- Blueprint: `docs/blueprints/2026-02-02_0900_finding_skill_implementation.md`
- Prompt: `docs/prompts/2026-02-02_0900_finding_skill_implementation.md`
- Skills Integration Research: `docs/research/2026-01-26_1410_skills_integration_architecture.md`
- Invoicer Research (discovery context): Invoicer `docs/research/2026-02-02_0725_forgekit_taxonomy_gap_proactive_findings.md`

---

**Research Complete**: 2026-02-02 07:25 UTC
