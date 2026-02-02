# Finding: ForgeKit Taxonomy Gap -- No Pipeline for Proactive Findings Without Design Decisions

**Date**: 2026-02-02
**Discovered by**: `/analyze architecture` (manual, applied to ForgeKit itself during Invoicer session)
**Type**: Gap
**Severity**: High
**Status**: Open

---

## What Was Found

ForgeKit's dual-pipeline architecture (reactive + proactive) has a taxonomy gap. Proactive findings that need corrective action but no design decision have no clean entry point into either pipeline.

The reactive pipeline requires an incident (something broke). The proactive pipeline requires a design decision (architectural choice). A proactive finding with a known cause and known fix -- such as a security vulnerability found by `/analyze` -- fits neither.

This gap means that `/analyze` can route findings to `/design` (via Design Escalation) but cannot route findings to the reactive pipeline for corrective fixes (no Fix Escalation exists).

---

## Affected Components

- `skills/analyze/SKILL.md`: Only has Design Escalation, no Fix Escalation
- `skills/analyze/DESIGN_ESCALATION.md`: One-directional (to `/design` only)
- `skills/investigate/SKILL.md`: Only accepts incident reports, not proactive findings
- `skills/rca-bugfix/SKILL.md`: Positioned after `/investigate` in reactive pipeline only
- `README.md`: Documents only two pipelines
- `ARCHITECTURE.md`: Skills layer diagram shows only two pipelines
- `PRD.md`: Key Differentiator #1 says "Dual pipelines"
- `CONVENTIONS.md`: No `docs/findings/` directory

---

## Evidence

### Test Case: Three Invoicer Priorities

Applied ForgeKit's taxonomy to three real priorities from the Invoicer project:

| Priority | Reactive Pipeline? | Proactive Pipeline? | Result |
|----------|-------------------|--------------------|---------|
| Authorization gap (known security bug) | No -- nothing broke | No -- no design decision | **OUTLIER** |
| Email service split (refactor) | No -- nothing broke | Yes -- `/design migrate` | Fits |
| Error handling (convention) | No -- nothing broke | Yes -- `/design tradeoff` | Fits |

The authorization gap has a known cause (missing `companyId` in WHERE clauses) and a known fix (add it). It's not an incident, not a design question, not a research topic. Yet ForgeKit's philosophy demands it go through a documented pipeline.

### Broader Outlier Categories

The authorization gap is not unique. These proactive finding types all fall through the same gap:

- Known bugs found by analysis
- Deprecated dependencies
- Configuration drift
- Dead code
- Test coverage gaps
- Documentation drift
- Security vulnerabilities with known fixes

---

## Preliminary Assessment

**Likely cause**: The original architecture was designed around two scenarios (something broke vs building something new). The third scenario (proactive finding needing corrective action) was not considered.

**Likely scope**: Affects the core pipeline architecture, all analysis modes, and cross-skill handoff protocols. High scope but low implementation complexity -- the fix reuses existing downstream skills.

**Likely impact**: Without this fix, proactive findings from `/analyze` either get forced through an ill-fitting pipeline (losing template fidelity) or skip the pipeline entirely (breaking the flywheel). Either way, institutional memory is degraded.

---

## Classification Rationale

**Type: Gap** -- ForgeKit is missing an expected capability. The dual-pipeline architecture was intentionally designed but the third scenario was not anticipated.

**Severity: High** -- This affects ForgeKit's core value proposition (institutional memory via documented pipelines). Every proactive finding that skips the pipeline is a lost artifact that can't feed future analysis.

---

**Finding Logged**: 2026-02-02 08:00 UTC
