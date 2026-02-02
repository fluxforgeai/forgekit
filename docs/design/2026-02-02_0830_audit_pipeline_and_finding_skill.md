# Design Analysis: Audit Pipeline and `/finding` Skill

**Date**: 2026-02-02 08:30 UTC
**Analyst**: Claude Code
**Mode**: Tradeoff
**Interactive Checkpoints**: 3 (goal, options, recommendation -- via conversation with user)

---

## Executive Summary

ForgeKit's dual-pipeline architecture has a gap for proactive findings needing corrective action without design decisions. Three options were evaluated: broadening `/incident`, creating a new `/finding` skill, and extending `/analyze`. The recommended approach is a new `/finding` skill that creates a third "audit" pipeline, reusing existing downstream skills (`/investigate`, `/rca-bugfix`, `/design`, `/blueprint`) while producing the documentation artifacts that power the feedback flywheel.

---

## User Context

- **Goal**: Close the taxonomy gap so every change goes through a documented pipeline
- **Constraints**: Must reuse existing skills where possible; must not break existing pipeline flows
- **Priorities**: Institutional memory > Simplicity > Implementation effort

---

## Current State Analysis

### The Gap

```
Reactive:  /watchdog --> /incident --> /investigate --> /rca-bugfix --> /plan
Proactive: /research --> /design --> /blueprint --> /plan
Strategic: /analyze --> feeds into either pipeline (but some findings fit neither)
```

`/analyze` has Design Escalation (routes to `/design`) but no Fix Escalation (no route to corrective action). Findings like "known security bug with known fix" have no entry point.

### What Exists

- Design Escalation in `/analyze`: `DESIGN_ESCALATION.md` -- handles proactive-to-design path
- Shared artifact communication: skills read/write `docs/` directories
- Handoff protocol: all skills suggest next steps at completion
- `/blueprint` skill: bridges design output to implementation prompts

### What's Missing

- No skill for logging proactive findings (proactive equivalent of `/incident`)
- No `docs/findings/` directory in conventions
- No Fix Escalation in `/analyze`
- `/investigate` only accepts incident reports, not findings
- No finding classification taxonomy

---

## External Research (2026 Sources)

Full research documented in: `docs/research/2026-02-02_0725_taxonomy_gap_proactive_findings.md`

Key findings from ITIL, Vulnerability Management Lifecycle, and SonarQube:
- All three frameworks treat proactive findings as a separate category from incidents
- All three require documentation regardless of fix complexity
- Classification by type drives the resolution path

---

## Options Analyzed

### Option A: Broaden `/incident` to Include Findings

**Description**: Add a "finding" mode to `/incident` that uses a different template for proactive discoveries.

**Pros**:
- No new skill (avoids skill sprawl)
- Reuses existing infrastructure

**Cons**:
- Muddles the clean "incident = something broke" definition
- Template fields don't fit (no chronological timeline, no "Reported by", no log evidence)
- Industry precedent (ITIL) deliberately separates incidents from proactive findings
- Confuses users about when to use `/incident`

**Effort**: Low (template change)
**Risk**: Medium -- conceptual confusion

### Option B: New `/finding` Skill (RECOMMENDED)

**Description**: Create a dedicated `/finding` skill as the entry point for the audit pipeline. Routes to existing downstream skills based on finding type.

**Pros**:
- Clean separation of concepts (incident vs finding)
- Purpose-built template for proactive discoveries
- Classification taxonomy drives routing (Fix branch vs Design branch)
- Industry-aligned (ITIL, VML, SonarQube all have dedicated proactive finding categories)
- Reuses existing downstream skills (`/investigate`, `/rca-bugfix`, `/design`, `/blueprint`)

**Cons**:
- Adds one more skill (9 total, up from 8)
- Users must learn when to use `/finding` vs `/incident`

**Effort**: Medium (new SKILL.md + template + minor updates to existing skills)
**Risk**: Low -- additive change, nothing breaks

### Option C: Extend `/analyze` to Produce Finding Artifacts Directly

**Description**: Make `/analyze` write individual finding artifacts to `docs/findings/` as it discovers them, rather than creating a separate skill.

**Pros**:
- No new skill
- Findings are logged as they're discovered (no separate step)

**Cons**:
- Blurs the line between system-level analysis and individual findings
- `/analyze` reports are about the system; findings are about specific issues
- No dedicated handoff protocol for findings
- Classification and routing logic gets buried inside `/analyze`

**Effort**: Medium (significant changes to `/analyze`)
**Risk**: Medium -- complicates an already complex skill (765 lines)

### Option D: Do Nothing (Baseline)

**Description**: Accept the gap. Route proactive findings through whichever pipeline is closest.

**Pros**: Zero effort

**Cons**:
- Template fields don't fit (lose fidelity)
- No finding artifacts for the flywheel (lose institutional memory)
- `/analyze` has no clean routing for corrective fixes
- Goes against ForgeKit's core philosophy (every change documented)

---

## Trade-Off Matrix

| Criterion | Weight | A: Broaden /incident | B: New /finding | C: Extend /analyze | D: Do Nothing |
|-----------|--------|---------------------|-----------------|-------------------|---------------|
| Institutional Memory | 5 | 3 | 5 | 4 | 1 |
| Conceptual Clarity | 4 | 2 | 5 | 3 | 2 |
| Implementation Effort | 2 | 4 | 3 | 3 | 5 |
| Industry Alignment | 3 | 2 | 5 | 3 | 1 |
| Reuse of Existing Skills | 3 | 4 | 5 | 3 | 5 |
| **Weighted Total** | | **47** | **80** | **55** | **37** |

Scoring: 1 = Poor, 5 = Excellent

---

## Recommendation

**Recommended Option**: B -- New `/finding` skill

**Rationale**: `/finding` provides the cleanest separation of concepts while maximizing institutional memory. It's the proactive equivalent of `/incident` -- same role (documentation entry point), different context (proactive vs reactive). The finding classification taxonomy (Defect/Vulnerability/Debt/Gap/Drift) naturally drives routing to the correct resolution path:

- Defect/Vulnerability -> Fix branch: `/investigate` -> `/rca-bugfix` -> `/plan`
- Debt/Gap/Drift -> Design branch: `/design` -> `/blueprint` -> `/plan`

**Key Trade-off**: One more skill to learn vs. complete pipeline coverage for all finding types.

---

## Impact Assessment

### Code Changes
- New file: `skills/finding/SKILL.md` (~100 lines)
- Modified: `skills/analyze/SKILL.md` (add Fix Escalation checkpoint)
- Modified: `skills/investigate/SKILL.md` (accept finding reports as input)
- Modified: `skills/rca-bugfix/SKILL.md` (accept findings from investigate)

### Documentation Changes (already applied)
- Modified: `README.md` (three pipelines with artifact flows)
- Modified: `ARCHITECTURE.md` (updated skills diagram and artifact table)
- Modified: `CONVENTIONS.md` (added `docs/findings/` directory)
- Modified: `PRD.md` (SK-020, INT-006, INT-007, updated differentiator)
- Modified: `IMPLEMENTATION_PLAN.md` (added backlog items)

### New Directories
- `docs/findings/` (added to project conventions)

### Breaking Changes
- None. Additive change. Existing pipelines work unchanged.

---

## Risks & Mitigations

| Risk | L | I | Mitigation |
|------|---|---|------------|
| Skill sprawl (too many skills) | Low | Medium | `/finding` is lightweight, reuses existing downstream skills |
| User friction (extra step) | Medium | Low | The step produces documentation value; "When to Use" table in README clarifies |
| Template overlap with `/incident` | Low | Low | Templates are deliberately different (proactive vs reactive fields) |
| `/investigate` confusion | Medium | Medium | Clear "Input Type" selector; abbreviated confirmation mode |

---

## Next Steps

- [x] Create design document (this file)
- [ ] Create blueprint with implementation spec
- [ ] Create `skills/finding/SKILL.md`
- [ ] Update `skills/analyze/SKILL.md` with Fix Escalation
- [ ] Update `skills/investigate/SKILL.md` with confirmation mode
- [ ] Validate artifact chain integrity (read-through test)

---

## Sources

- Finding: `docs/findings/2026-02-02_0800_taxonomy_gap_proactive_findings.md`
- Research: `docs/research/2026-02-02_0725_taxonomy_gap_proactive_findings.md`
- Industry Research: `docs/research/2026-01-26_1410_skills_integration_architecture.md`
- Design Escalation Spec: `skills/analyze/DESIGN_ESCALATION.md`

---

**Analysis Complete**: 2026-02-02 08:30 UTC
