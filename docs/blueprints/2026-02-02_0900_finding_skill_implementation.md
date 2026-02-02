# Blueprint: `/finding` Skill and Audit Pipeline Implementation

**Date**: 2026-02-02
**Design Reference**: `docs/design/2026-02-02_0830_audit_pipeline_and_finding_skill.md`
**Research Reference**: `docs/research/2026-02-02_0725_taxonomy_gap_proactive_findings.md`

## Objective

Implement the `/finding` skill and integrate it into ForgeKit as the entry point for the audit pipeline. This closes the taxonomy gap where proactive findings with known causes had no documented pipeline.

## Requirements

1. Create `skills/finding/SKILL.md` with finding report template and classification taxonomy
2. Add Fix Escalation checkpoint to `skills/analyze/SKILL.md` (all modes)
3. Add confirmation mode to `skills/investigate/SKILL.md` for finding reports
4. Update `skills/rca-bugfix/SKILL.md` to accept finding-originated investigations
5. Add `docs/findings/` reading to skills that should check past findings

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Separate skill vs broadening `/incident` | Separate `/finding` skill | ITIL precedent; different templates; conceptual clarity |
| Finding types | Defect, Vulnerability, Debt, Gap, Drift | Covers all identified outliers; maps to SonarQube-style taxonomy |
| Branch routing | Type determines Fix vs Design branch | Defect/Vulnerability -> Fix; Debt/Gap/Drift -> Design |
| Investigation mode | Confirmation mode (abbreviated) | Known causes don't need full investigation; still confirms scope |

## Scope

### In Scope
- `skills/finding/SKILL.md` (new)
- Fix Escalation in `skills/analyze/SKILL.md` (modification)
- Confirmation mode in `skills/investigate/SKILL.md` (modification)
- Finding report acceptance in `skills/rca-bugfix/SKILL.md` (modification)
- Cross-skill reading of `docs/findings/` (modification to investigate, analyze, rca-bugfix, research)

### Out of Scope
- Automated skill chaining (Claude Code limitation -- skills require user invocation)
- `/finding` frontmatter configuration (defer until `context: fork` works via Skill tool)
- Changes to `/watchdog`, `/incident`, `/design`, `/blueprint`, `/research` core logic

## Files to Create

### `skills/finding/SKILL.md` (~120 lines)

Structure:
```
# Finding Report Skill

**Trigger**: /finding {description}
**Purpose**: Log a proactive discovery. The proactive equivalent of /incident.

## Instructions
1. Classify the finding (Type + Severity)
2. Write finding report to docs/findings/{date}_{name}.md
3. STOP and suggest next steps based on type

## Classification Taxonomy
- Defect: Code that doesn't work as intended -> Fix branch
- Vulnerability: Security weakness -> Fix branch
- Debt: Maintainability/quality issue -> Design branch
- Gap: Missing expected capability -> Design branch
- Drift: Divergence from intended state -> Either branch

## Finding Report Template
(See research report for full template)

## Handoff Protocol
- For Defect/Vulnerability: suggest /investigate or /rca-bugfix
- For Debt/Gap/Drift: suggest /design {mode}
- Always suggest /investigate for scope confirmation
```

## Files to Modify

### `skills/analyze/SKILL.md`

**Location**: All escalation checkpoints in all modes (health, patterns, component, risk, architecture)

**Change**: Add "Corrective fix" option alongside Design Escalation:

```markdown
## Escalation Checkpoint (Updated)

"Finding: {description}

What type of action does this need?"

Options:
- Design exploration (suggests /design)        -- existing
- Corrective fix (suggests /finding)           -- NEW
- Just note it in the report                   -- existing
- Known accepted limitation                    -- existing
```

### `skills/investigate/SKILL.md`

**Change**: Accept finding reports as input alongside incident reports.

Add near the top of Instructions:

```markdown
## Input Type

Determine the input type:
- If the input references `docs/incidents/*.md` -> Full investigation mode
- If the input references `docs/findings/*.md` -> Confirmation mode

### Confirmation Mode (for findings with known causes)
When investigating a finding (not an incident):
1. Read the finding report from docs/findings/
2. Confirm the finding is real (not a false positive)
3. Determine full scope (how many files/functions affected?)
4. Document evidence (show the affected code)
5. Assess impact (blast radius)
6. Write investigation report (abbreviated -- skip external research, skip hypothesis testing)
```

### `skills/rca-bugfix/SKILL.md`

**Change**: Accept investigations that originated from findings (not just incidents).

Add to the RCA process:

```markdown
## Input Sources

Check for upstream artifacts in this order:
1. docs/investigations/*.md (from /investigate)
2. docs/findings/*.md (from /finding, if /investigate was skipped)
3. User-provided description (direct invocation)

When a finding report exists, the "Root Cause" section may be shorter
(cause is already identified in the finding). Still produce the full
RCA artifact and prompt for /plan mode.
```

### Cross-Skill Reading Updates

Add "Check existing findings" step to:

| Skill | Where to Add | What to Read |
|-------|-------------|-------------|
| `/investigate` | Step 6 (Review Past RCAs) | `docs/findings/*.md` -- related findings |
| `/analyze` (all modes) | Step: Collect Data | `docs/findings/*.md` -- past findings for context |
| `/rca-bugfix` | Before RCA | `docs/findings/*.md` -- related findings |
| `/research` | Step 4 (Check Existing Knowledge) | `docs/findings/*.md` -- related findings |

## Implementation Sequence

1. **Create `skills/finding/SKILL.md`** -- the new skill (no dependencies)
2. **Update `skills/analyze/SKILL.md`** -- add Fix Escalation (depends on step 1 existing)
3. **Update `skills/investigate/SKILL.md`** -- add confirmation mode (depends on step 1 template)
4. **Update `skills/rca-bugfix/SKILL.md`** -- accept finding input (depends on step 1 template)
5. **Add cross-skill reading** -- update investigate, analyze, rca-bugfix, research (depends on steps 1-4)
6. **Validate** -- read-through test of artifact chain (depends on all above)

## Dependencies & Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `/finding` template doesn't fit real-world findings | Low | Medium | Template designed from real test case (Invoicer authorization gap); iterate based on usage |
| `/investigate` confirmation mode too abbreviated | Medium | Low | Users can always choose full investigation; confirmation is the default for findings, not mandatory |
| Existing skills don't find `docs/findings/` on first use | Low | Low | Directory is created by first `/finding` invocation; other skills gracefully handle missing directory |

## Acceptance Criteria

- [ ] `skills/finding/SKILL.md` exists with complete template and classification taxonomy
- [ ] `/analyze` all modes have Fix Escalation option alongside Design Escalation
- [ ] `/investigate` accepts finding reports with abbreviated confirmation mode
- [ ] `/rca-bugfix` accepts finding-originated investigations
- [ ] `/investigate`, `/analyze`, `/rca-bugfix`, `/research` check `docs/findings/` for context
- [ ] README.md documents three pipelines with artifact flows (DONE)
- [ ] ARCHITECTURE.md shows updated skills layer diagram (DONE)
- [ ] CONVENTIONS.md includes `docs/findings/` (DONE)
- [ ] PRD.md includes SK-020 and INT-006/INT-007 (DONE)

## Constraints

- Skills cannot invoke other skills programmatically (Claude Code limitation)
- All skill chaining is user-mediated via handoff suggestions
- `context: fork` frontmatter not yet honored via Skill tool (GitHub #17283)
