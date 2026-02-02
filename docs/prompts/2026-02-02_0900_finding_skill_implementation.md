# Implementation Prompt: `/finding` Skill and Audit Pipeline

**Blueprint Reference**: `docs/blueprints/2026-02-02_0900_finding_skill_implementation.md`
**Design Reference**: `docs/design/2026-02-02_0830_audit_pipeline_and_finding_skill.md`
**Finding Reference**: `docs/findings/2026-02-02_0800_taxonomy_gap_proactive_findings.md`

## Context

ForgeKit's dual-pipeline architecture has a taxonomy gap: proactive findings that need corrective action but no design decision have no clean entry point. A new `/finding` skill closes this gap by serving as the audit pipeline's entry point, routing to existing downstream skills based on finding type.

## Goal

Create the `/finding` skill (SKILL.md) and update existing skills to support the audit pipeline.

## Requirements

1. Create `skills/finding/SKILL.md` with:
   - Finding report template (What Was Found, Affected Components, Evidence, Preliminary Assessment)
   - Classification taxonomy: Defect, Vulnerability, Debt, Gap, Drift
   - Severity levels: Critical, High, Medium, Low
   - Handoff protocol that suggests next steps based on finding type
   - Type-to-branch routing (Defect/Vulnerability -> Fix, Debt/Gap/Drift -> Design)

2. Update `skills/analyze/SKILL.md`:
   - Add "Corrective fix (suggests /finding)" to all escalation checkpoints
   - Existing Design Escalation options remain unchanged

3. Update `skills/investigate/SKILL.md`:
   - Add input type detection (incident report vs finding report)
   - Add confirmation mode for findings with known causes (abbreviated: confirm scope, document evidence, assess impact)
   - Full investigation mode remains the default for incident reports

4. Update `skills/rca-bugfix/SKILL.md`:
   - Accept investigations that originated from findings
   - Check `docs/findings/` for related findings before RCA

5. Add `docs/findings/*.md` reading to: `/investigate`, `/analyze`, `/rca-bugfix`, `/research`

## Files Likely Affected

- `skills/finding/SKILL.md` (NEW)
- `skills/analyze/SKILL.md` (modify escalation checkpoints)
- `skills/investigate/SKILL.md` (add confirmation mode)
- `skills/rca-bugfix/SKILL.md` (accept finding input)
- `skills/research/SKILL.md` (add findings check)

## Implementation Sequence

1. Create `skills/finding/SKILL.md`
2. Update `skills/analyze/SKILL.md` -- Fix Escalation
3. Update `skills/investigate/SKILL.md` -- confirmation mode
4. Update `skills/rca-bugfix/SKILL.md` -- finding input
5. Add cross-skill `docs/findings/` reading
6. Validate artifact chain (read-through test)

## Constraints

- Follow existing skill conventions (trigger format, template structure, handoff protocol)
- Finding report template must match fields defined in research report
- Classification taxonomy: exactly 5 types (Defect, Vulnerability, Debt, Gap, Drift)
- Must not break existing pipeline flows (additive change only)

## Acceptance Criteria

- [ ] `skills/finding/SKILL.md` exists with complete template and taxonomy
- [ ] `/analyze` all modes have Fix Escalation alongside Design Escalation
- [ ] `/investigate` accepts finding reports with confirmation mode
- [ ] `/rca-bugfix` accepts finding-originated investigations
- [ ] Cross-skill reading of `docs/findings/` added to 4 skills
- [ ] All existing skills continue to work unchanged

---

## Plan Output Instructions

**IMPORTANT**: When you finish creating the implementation plan, save it to:
`docs/plans/2026-02-02_0915_finding_skill_implementation.md`

The plan file should include:
- Summary of the approach
- Step-by-step implementation tasks
- Files to modify with specific changes
- Testing strategy (read-through test of artifact chain)
- Rollback plan (revert SKILL.md and skill modifications)
