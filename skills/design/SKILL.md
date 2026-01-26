# Design Skill

**Trigger**: `/design {mode} {topic}`

**Purpose**: Research-driven, interactive design analysis for architectural decisions. Combines codebase analysis, documentation review, external research (2026 sources), and impact assessment to provide evidence-based recommendations.

---

## Modes

```
/design tradeoff {topic}     # Compare approaches (default, most common)
/design pattern {name}       # Explain pattern and assess applicability
/design migrate {from} {to}  # Plan migration between approaches
/design validate {proposal}  # Review a proposed design
/design impact {change}      # Assess impact of a specific change
```

---

## Design Principles

1. **Research-First**: Never recommend without understanding current state AND external best practices
2. **Current-Year Sources**: Always search for 2026 documentation, patterns, and practices
3. **Impact-Aware**: Every design decision includes concrete impact assessment
4. **Interactive**: User validates assumptions, priorities, and findings at checkpoints
5. **Evidence-Based**: Recommendations backed by code analysis AND external sources
6. **Actionable Output**: Ends with clear next steps, not just analysis

---

## Research Framework

### Layer 1: Codebase Analysis

Before any design work, understand the current state:

```
1. Target Component(s)
   - Read all source files (use Read tool)
   - Count lines, functions, classes
   - Identify patterns in use
   - Map error handling approach

2. Dependencies (Inward)
   - What does this component import?
   - External libraries used
   - Internal modules depended on

3. Dependencies (Outward)
   - What imports this component? (use Grep)
   - How many callers?
   - What would break if interface changes?

4. Related Code
   - Similar patterns elsewhere in codebase
   - Previous attempts at solving this problem
   - Comments indicating tech debt or TODOs
```

### Layer 2: Documentation Analysis

Read internal docs for context:

```
Priority order:
1. CLAUDE.md              # Project context, decisions
2. ARCHITECTURE.md        # System design
3. README.md              # Project overview
4. docs/RCAs/*.md         # Past failures
5. docs/incidents/*.md    # Related incidents
6. docs/plans/*.md        # Previous design decisions
7. docs/research/*.md     # Prior research
```

### Layer 3: External Research (2026 Sources)

**CRITICAL**: Always include current year (2026) in searches.

```
Use WebSearch for:
- "{topic} best practices 2026"
- "{library} {pattern} 2026"
- "{problem} solutions comparison 2026"
- "how {company} handles {problem} 2026"

Use WebFetch for:
- Official API documentation
- Library documentation
- Relevant blog posts/case studies
```

### Layer 4: Impact Assessment

For every design option, assess:

```
1. CODE CHANGES
   - Files to modify (with estimates)
   - Files to create
   - Files to delete
   - Interfaces changing

2. TEST CHANGES
   - Tests to update
   - New tests needed
   - Test infrastructure changes

3. CONFIGURATION
   - Environment variables
   - Config files
   - Feature flags

4. DEPLOYMENT
   - Database migrations?
   - Breaking changes?
   - Rollback complexity
   - Downtime required?

5. OPERATIONAL
   - Monitoring changes
   - Logging changes
   - Runbook updates

6. DEPENDENCIES
   - New dependencies
   - Dependency updates
   - Removed dependencies

7. RISKS
   - What could go wrong
   - Blast radius
   - Detection strategy
   - Recovery plan
```

---

## Mode: Tradeoff Analysis (`/design tradeoff {topic}`)

The most common mode - comparing approaches for a design decision.

### Workflow

**CHECKPOINT 1: Understand Goal**
```
Use AskUserQuestion:
"What's the design goal for: {topic}?"

Options:
- Improve reliability (reduce failures, better recovery)
- Improve performance (speed, throughput, latency)
- Reduce complexity (easier to maintain, debug)
- Add new capability
- Let me describe the goal...
```

**CHECKPOINT 2: Constraints**
```
Use AskUserQuestion:
"What constraints should I consider?"

Options (multiSelect: true):
- Must maintain backward compatibility
- Cannot change external API contracts
- Limited time/resources for implementation
- Must work with existing infrastructure
- No constraints - open to any approach
- Let me specify constraints...
```

**CHECKPOINT 3: Priorities**
```
Use AskUserQuestion:
"What matters most for this decision?"

Options:
- Reliability > Performance > Simplicity > Cost > Time (Recommended)
- Performance > Reliability > Time > Simplicity > Cost
- Simplicity > Time > Reliability > Performance > Cost
- Time > Simplicity > Reliability > Performance > Cost
- Let me specify my own ranking...
```

**PHASE 1: Codebase Research** (Automatic)
- Read target component source
- Analyze dependencies (in and out)
- Find related patterns in codebase
- Review related incidents/RCAs

**CHECKPOINT 4: Validate Current State**
```
Use AskUserQuestion:
"Here's my understanding of the current implementation:

{Summary}

Files involved: {list}
Pattern used: {identified pattern}
Known issues: {from RCAs}

Is this accurate?"

Options:
- Yes, that's correct
- Mostly correct, minor clarification needed
- Missing important context
- That's not quite right
```

**PHASE 2: External Research** (Automatic)
- WebSearch: "{topic} best practices 2026"
- WebSearch: "{library} {pattern} 2026"
- WebSearch: "{problem} solutions comparison 2026"
- WebFetch: Official documentation as needed

**CHECKPOINT 5: Validate Research Sources**
```
Use AskUserQuestion:
"I found these relevant sources:

1. {source 1} - {what it covers}
2. {source 2} - {what it covers}
3. {source 3} - {what it covers}

Any other sources I should check?"

Options:
- These look good, proceed
- Also check {specific doc/source}
- Focus more on {specific aspect}
- Skip external research, just use codebase
```

**PHASE 3: Identify Options** (Automatic)
- Based on research, identify 3-5 viable approaches
- Always include current approach as baseline

**CHECKPOINT 6: Validate Options**
```
Use AskUserQuestion:
"I've identified these approaches to evaluate:

1. {Option A}: {brief description}
2. {Option B}: {brief description}
3. {Option C}: {brief description}
4. Current approach (baseline)

Should I evaluate all of these?"

Options:
- Yes, evaluate all
- Remove an option (explain why)
- Add another option
- Just compare specific options
```

**PHASE 4: Deep Analysis** (Automatic)
For each option:
- How it works (detailed explanation)
- Implementation approach
- Pros and cons
- Impact assessment (using framework)
- Effort estimate
- Risk level

**CHECKPOINT 7: Validate Impact Assessment**
```
Use AskUserQuestion:
"Here's the impact assessment for {recommended option}:

Files to change: {N} files (~{X} lines)
Tests to update: {N} test files
New dependencies: {list or 'none'}
Breaking changes: {yes/no}
Estimated effort: {X hours/days}

Does this match your expectations?"

Options:
- Yes, that seems reasonable
- Effort seems underestimated
- Effort seems overestimated
- Missing some affected areas
- Let me provide more context
```

**PHASE 5: Scoring & Comparison** (Automatic)
- Score each option against user's priorities
- Calculate weighted totals
- Generate trade-off matrix

**CHECKPOINT 8: Review Recommendation**
```
Use AskUserQuestion:
"Based on your priorities, I recommend: {Option}

Summary:
✓ {Primary benefit aligned with top priority}
✓ {Secondary benefit}
✗ {Main trade-off}

Key trade-off: {what you gain} vs {what you lose}

Do you want to proceed with this recommendation?"

Options:
- Yes, create the design document
- I prefer a different option (explain)
- Need more analysis on specific aspect
- Let me think - just save the analysis
```

**PHASE 6: Generate Report** (Automatic)
Write to: `docs/design/{YYYY-MM-DD_HHMM}_{topic_slug}.md`

**CHECKPOINT 9: Next Steps**
```
Use AskUserQuestion:
"Design analysis complete: {filename}

What would you like to do next?"

Options:
- Create implementation plan (EnterPlanMode)
- Start implementing now
- Share with team for review first
- Save for later - just the analysis for now
```

**STOP** and await user decision.

---

## Mode: Pattern Analysis (`/design pattern {name}`)

Explain a design pattern and assess its applicability.

### Workflow

**CHECKPOINT 1: Context**
```
Use AskUserQuestion:
"What's the context for exploring the {pattern} pattern?"

Options:
- Considering adoption in this project
- Debugging existing implementation of it
- Comparing with alternative patterns
- Educational - want to understand it better
```

**PHASE 1: Research** (Automatic)
- WebSearch: "{pattern} implementation 2026"
- WebSearch: "{pattern} pros cons 2026"
- WebSearch: "{pattern} {language} example 2026"
- Scan codebase for existing pattern usage

**CHECKPOINT 2: Variation Selection**
```
Use AskUserQuestion:
"I found these variations of {pattern}:

1. {Variation A}: {brief description}
2. {Variation B}: {brief description}
3. {Variation C}: {brief description}

Which interests you most?"

Options:
- {Variation A}
- {Variation B}
- Compare all variations
- General overview of the pattern
```

**PHASE 2: Analysis** (Automatic)
- Pattern explanation (what, why, when)
- Applicability to this codebase
- Where it could be applied
- Implementation approach
- Pros/cons in this context

**CHECKPOINT 3: Validate Applicability**
```
Use AskUserQuestion:
"Based on analysis, {pattern} would fit well in:

- {Location 1}: {why}
- {Location 2}: {why}

And would NOT fit well in:
- {Location 3}: {why not}

Does this match your intuition?"

Options:
- Yes, that's helpful
- Surprised about {location} - explain more
- What about {other location}?
- I was thinking of a different use case
```

**PHASE 3: Generate Report** (Automatic)
Write to: `docs/design/{YYYY-MM-DD_HHMM}_pattern_{name}.md`

**STOP** and await instructions.

---

## Mode: Migration Planning (`/design migrate {from} {to}`)

Plan migration from one approach to another.

### Workflow

**CHECKPOINT 1: Migration Reason**
```
Use AskUserQuestion:
"Why are you migrating from {from} to {to}?"

Options:
- Performance issues with current approach
- Maintainability concerns
- Deprecation of current approach
- New requirements that current can't meet
- Let me explain...
```

**CHECKPOINT 2: Constraints**
```
Use AskUserQuestion:
"What constraints affect this migration?"

Options (multiSelect: true):
- Must maintain backward compatibility during migration
- Cannot have downtime
- Must be reversible (rollback capability)
- Limited time window for migration
- No constraints
- Let me specify...
```

**CHECKPOINT 3: Migration Strategy Preference**
```
Use AskUserQuestion:
"What migration strategy do you prefer?"

Options:
- Big bang (all at once, faster but riskier)
- Strangler fig (gradual replacement)
- Parallel run (both systems, compare results)
- Let me understand options first
```

**PHASE 1: Current State Analysis** (Automatic)
- Deep dive into current implementation
- Map all usages and dependencies
- Identify migration complexity per component

**PHASE 2: Target State Research** (Automatic)
- Research target approach (2026 sources)
- Find migration guides
- Look for similar migration case studies

**CHECKPOINT 4: Validate Understanding**
```
Use AskUserQuestion:
"Migration scope:

Current ({from}):
- {N} files using this approach
- {N} call sites
- Key complexity: {description}

Target ({to}):
- {approach description}
- Key benefit: {description}

Is this accurate?"

Options:
- Yes, proceed with planning
- Current scope is different
- Target understanding needs correction
- Add more context
```

**PHASE 3: Migration Plan** (Automatic)
- Step-by-step migration plan
- Risk assessment per step
- Rollback points
- Testing strategy
- Timeline estimate

**CHECKPOINT 5: Review Plan**
```
Use AskUserQuestion:
"Migration plan summary:

Phase 1: {description} ({effort})
Phase 2: {description} ({effort})
Phase 3: {description} ({effort})

Total effort: {estimate}
Risk level: {assessment}

Does this look feasible?"

Options:
- Yes, create detailed plan
- Timeline is too aggressive
- Missing a phase
- Risk is too high - reconsider
```

**PHASE 4: Generate Report** (Automatic)
Write to: `docs/design/{YYYY-MM-DD_HHMM}_migrate_{from}_to_{to}.md`

**STOP** and await instructions.

---

## Mode: Design Validation (`/design validate {proposal}`)

Review a proposed design before implementation.

### Workflow

**CHECKPOINT 1: Receive Proposal**
```
Use AskUserQuestion:
"How should I receive the design proposal?"

Options:
- Read from file (provide path)
- I'll paste it here
- It's described in the conversation above
- Reference a PR or issue
```

**CHECKPOINT 2: Review Focus**
```
Use AskUserQuestion:
"What aspects should I focus on?"

Options (multiSelect: true):
- Completeness (covers all requirements?)
- Feasibility (can we actually build this?)
- Risk assessment (what could go wrong?)
- Alignment with architecture
- All of the above (Recommended)
```

**PHASE 1: Proposal Analysis** (Automatic)
- Parse and understand the proposal
- Compare to codebase reality
- Identify gaps or conflicts
- Research alternatives for weak points

**CHECKPOINT 3: Clarify Ambiguities**
```
Use AskUserQuestion:
"I have questions about the proposal:

1. {Ambiguity 1}
2. {Ambiguity 2}

Can you clarify?"

Options:
- Let me explain...
- Skip these - not critical
- The proposal should cover this
```

**PHASE 2: Validation** (Automatic)
- Assess each aspect (completeness, feasibility, risk)
- Score the proposal
- Identify improvements

**CHECKPOINT 4: Review Findings**
```
Use AskUserQuestion:
"Validation summary:

✓ {Strength 1}
✓ {Strength 2}
⚠ {Concern 1}
✗ {Gap 1}

Overall: {Ready to implement | Needs revision | Major concerns}

How should I proceed?"

Options:
- Create detailed review document
- Focus on addressing concerns
- Proposal looks good - summarize and done
- Compare with alternative approach
```

**PHASE 3: Generate Report** (Automatic)
Write to: `docs/design/{YYYY-MM-DD_HHMM}_review_{proposal_name}.md`

**STOP** and await instructions.

---

## Mode: Impact Analysis (`/design impact {change}`)

Assess impact of a specific change before making it.

### Workflow

**CHECKPOINT 1: Describe Change**
```
Use AskUserQuestion:
"Describe the change you're considering:"

Options:
- Point to specific code/file to change
- Describe in natural language
- Reference a ticket or issue
- It's in the conversation above
```

**CHECKPOINT 2: Change Scope**
```
Use AskUserQuestion:
"What type of change is this?"

Options:
- Interface change (method signatures, contracts)
- Implementation change (internal only)
- Dependency change (add/remove/update)
- Configuration change
- Let me describe...
```

**PHASE 1: Impact Discovery** (Automatic)
- Find all usages of affected code (Grep)
- Map dependencies
- Identify affected tests
- Check related configurations

**CHECKPOINT 3: Validate Scope**
```
Use AskUserQuestion:
"Here's what I found would be affected:

Code:
- {file 1}: {how affected}
- {file 2}: {how affected}

Tests:
- {test file 1}
- {test file 2}

Config:
- {config if any}

Anything I'm missing?"

Options:
- No, this covers it
- Also affects {additional area}
- {File} isn't actually affected
- Need to check {specific area}
```

**PHASE 2: Risk Assessment** (Automatic)
- Full impact assessment using framework
- Risk scoring
- Mitigation suggestions

**CHECKPOINT 4: Review Assessment**
```
Use AskUserQuestion:
"Impact assessment:

Effort: {estimate}
Risk: {Low/Medium/High}
Breaking changes: {yes/no}

Top risk: {description}
Mitigation: {suggestion}

Does this help with your decision?"

Options:
- Yes, proceed with the change
- Yes, but need to mitigate risks first
- Risk is too high - reconsider
- Need more detail on {aspect}
```

**PHASE 3: Generate Report** (Automatic)
Write to: `docs/design/{YYYY-MM-DD_HHMM}_impact_{change_slug}.md`

**STOP** and await instructions.

---

## Report Template

All modes generate reports with this structure:

```markdown
# Design Analysis: {Topic}

**Date**: {YYYY-MM-DD HH:MM} UTC
**Analyst**: Claude Code (Session {N})
**Mode**: {Tradeoff | Pattern | Migrate | Validate | Impact}
**Interactive Checkpoints**: {N} decisions made by user

---

## Executive Summary
{2-3 sentences}

---

## User Context
- **Goal**: {from checkpoint}
- **Constraints**: {from checkpoint}
- **Priorities**: {weighted list from checkpoint}

---

## Current State Analysis
{Codebase findings}

---

## External Research (2026 Sources)
{Research findings with source links}

---

## {Mode-Specific Analysis}
{Options / Pattern / Migration Plan / Validation / Impact}

---

## Trade-Off Matrix (if applicable)
| Criterion | Weight | Option 1 | Option 2 | Current |
|-----------|--------|----------|----------|---------|

---

## Recommendation
{With rationale and key trade-off}

---

## Impact Assessment
{Full 7-section framework}

---

## Risks & Mitigations
| Risk | L | I | Mitigation |

---

## Next Steps
- [ ] {Action items}

---

## Sources
- {URLs and file references}

---

**Analysis Complete**: {timestamp}
```

---

## Flags

```
--quick         Reduce to 3 checkpoints (goal, options, recommendation)
--deep          More thorough research (5+ external sources)
--no-external   Skip external research (codebase only)
--compare-only  Don't recommend, just compare options
```

---

## After Design Analysis

**ALWAYS STOP** after generating the report.

Output format:
```
Design analysis complete: docs/design/{filename}.md

Mode: {mode}
Interactive checkpoints: {N}
Research sources: {N} internal, {N} external

Recommendation: {one-line summary}
Key trade-off: {what you gain} vs {what you lose}

Estimated effort: {if applicable}
Risk level: {if applicable}

Next steps options provided at final checkpoint.

Awaiting your instructions.
```

**Do NOT** proceed with implementation without explicit user direction.

---

## Integration

### From /analyze
When `/analyze` escalates with "deep dive" option:
```
User runs: /design tradeoff "{topic from escalation}"
```

### To Implementation
When user selects "Create implementation plan":
```
Use EnterPlanMode to create detailed implementation plan
```

---

## Examples

```
/design tradeoff "retry strategy for API calls"
→ Full interactive comparison of retry approaches

/design pattern "circuit breaker"
→ Pattern explanation + applicability assessment

/design migrate "scattered retries" "centralized middleware"
→ Migration plan with phases and rollback points

/design validate "the proposed caching layer"
→ Review of design proposal with gaps identified

/design impact "changing batch_client timeout from 30s to 60s"
→ Impact assessment of specific change
```
