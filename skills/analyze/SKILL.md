# Systems Analyst Skill

**Trigger**: `/analyze {mode} [scope]`

**Purpose**: Strategic-level system analysis that goes beyond reactive incident response to provide **proactive system health assessment, pattern recognition across incidents, architectural insight, and risk prioritization**.

---

## Modes

```
/analyze health                    # Full system health assessment
/analyze patterns [time-period]    # Pattern recognition (default: last-7-days)
/analyze component [scope]         # Deep dive on specific component
/analyze risk [scope]              # Risk assessment with prioritization
/analyze architecture              # Architectural review + doc sync
/analyze discover                  # Build/refresh System Map only
```

---

## Design Principles

1. **Discovery-Based Scoping**: No hard-coded component names. The skill discovers what exists.
2. **Fully Interactive**: ALL modes use AskUserQuestion at key decision points.
3. **Artifact-Driven**: System Map persists across analyses.
4. **No File Edits Without Confirmation**: Architecture mode previews changes before applying.
5. **Design Escalation**: When findings suggest redesign, offer to explore alternatives.

---

## Step 0: Load or Create System Map

Before any analysis, check for existing System Map:

```
IF docs/analysis/system-map.md exists AND is <24h old:
    Load it (skip discovery)
ELSE:
    Run discovery (Step 1)
```

---

## Step 1: System Discovery

When System Map doesn't exist or is stale, discover the system:

### 1.1 Read Project Context
```
Priority order:
1. CLAUDE.md           # Project instructions
2. ARCHITECTURE.md     # Architecture documentation
3. README.md           # Project overview
4. docker-compose.yml  # Service definitions
5. pyproject.toml / package.json  # Dependencies
```

### 1.2 Scan Directory Structure
```
Look for:
- backend/app/services/    # Python service layer
- backend/app/api/         # API routers
- backend/app/models/      # Data models
- src/                     # Generic source
- frontend/                # Frontend code
- lib/ or packages/        # Libraries
```

### 1.3 Analyze Code Metrics
For each discovered module:
- Line count (complexity indicator)
- Import count (coupling indicator)
- Class/function count (scope indicator)

### 1.4 Build System Map
Write to: `docs/analysis/system-map.md`

```markdown
# System Map: {Project Name}

**Generated**: {YYYY-MM-DD HH:MM} UTC
**Generator**: /analyze discover

---

## Components Discovered

### Services
| ID | Name | Path | LOC | Imports | Description |
|----|------|------|-----|---------|-------------|
| svc-1 | {name} | {path} | {loc} | {imports} | {inferred desc} |

### API Layer
| ID | Name | Path | Endpoints |
|----|------|------|-----------|

### Models
| ID | Name | Path | Fields |
|----|------|------|--------|

---

## Dependency Graph
{Component relationships discovered from imports}

---

## Risk Hotspots (Auto-Detected)
- High coupling: {components imported by many others}
- High complexity: {large LOC or many imports}

---

## Documentation Status
| Doc | Exists | Last Updated |
|-----|--------|--------------|
```

---

## Mode: Discover (`/analyze discover`)

**Purpose**: Build or refresh the System Map without full analysis.

### Workflow

1. **Checkpoint 1** (Scope Confirmation):
   ```
   Use AskUserQuestion:
   "I'll scan the project to build a System Map. What should I include?"

   Options (multiSelect: true):
   - Backend services (Recommended)
   - API layer
   - Data models
   - Frontend components
   - Configuration files
   - All of the above
   ```

2. **Checkpoint 2** (Exclusions):
   ```
   Use AskUserQuestion:
   "Any directories or patterns to exclude from scanning?"

   Options:
   - No exclusions (scan everything) (Recommended)
   - Exclude tests/
   - Exclude vendor/node_modules
   - Let me specify...
   ```

3. **Run Discovery** (as specified in Step 1)

4. **Checkpoint 3** (Validation):
   ```
   Use AskUserQuestion:
   "I found {N} components. Quick review:"

   {Show summary table}

   "Does this look correct?"
   Options:
   - Yes, save the System Map
   - Remove some components
   - Add missing components
   - Rescan with different options
   ```

5. **Save System Map** to `docs/analysis/system-map.md`

6. **STOP** and present summary. Await instructions.

---

## Mode: System Health (`/analyze health`)

**Purpose**: Overall system reliability assessment.

### Workflow

1. **Load System Map** (create if missing)

2. **Checkpoint 1** (Focus Areas):
   ```
   Use AskUserQuestion:
   "What aspects of system health matter most right now?"

   Options (multiSelect: true):
   - Reliability (incidents, failures, recovery) (Recommended)
   - Performance (speed, throughput, latency)
   - Maintainability (code quality, complexity)
   - Observability (monitoring, logging, alerts)
   - All dimensions equally
   ```

3. **Checkpoint 2** (Known Context):
   ```
   Use AskUserQuestion:
   "Any known issues or recent changes I should account for?"

   Options:
   - No, analyze with fresh eyes (Recommended)
   - Yes, there are known issues (let me describe)
   - Recent deployment may affect results
   - We're in incident recovery mode
   ```

4. **Collect Data**:
   - Read all `docs/RCAs/*.md`
   - Read all `docs/incidents/*.md`
   - Read all `docs/investigations/*.md`
   - Search logs for error patterns (last 7 days)

5. **Analyze**:
   - Count incidents by component
   - Calculate incident frequency trends
   - Identify recurring failure modes
   - Assess monitoring coverage

6. **Score Each Dimension** (0-10):
   - **Reliability**: Success rate, MTTR, incident frequency
   - **Performance**: Throughput, latency (if data available)
   - **Maintainability**: Code complexity, test coverage
   - **Observability**: Monitoring coverage, alert quality

7. **Checkpoint 3** (Validate Scores):
   ```
   Use AskUserQuestion:
   "Here are the preliminary scores:

   | Dimension | Score | Notes |
   |-----------|-------|-------|
   | Reliability | X/10 | {brief note} |
   | Performance | X/10 | {brief note} |
   | Maintainability | X/10 | {brief note} |
   | Observability | X/10 | {brief note} |

   Do these match your experience?"

   Options:
   - Yes, these look accurate
   - Reliability score seems off
   - Performance score seems off
   - Maintainability score seems off
   - Observability score seems off
   - Let me provide context
   ```

8. **Design Escalation Check**:
   If any finding suggests redesign opportunity → trigger escalation checkpoint
   (See DESIGN_ESCALATION.md)

9. **Generate Report**: Write to `docs/analysis/{YYYY-MM-DD_HHMM}_health.md`

10. **STOP** and present summary. Await instructions.

---

## Mode: Pattern Recognition (`/analyze patterns [time-period]`)

**Purpose**: Identify recurring issues across incidents.

### Workflow

1. **Checkpoint 1** (Time Period):
   ```
   Use AskUserQuestion:
   "What time period should I analyze for patterns?"

   Options:
   - Last 7 days (Recommended)
   - Last 30 days
   - Last 90 days
   - Since last deploy
   - Custom range (let me specify)
   ```

2. **Checkpoint 2** (Pattern Focus):
   ```
   Use AskUserQuestion:
   "What types of patterns are you most interested in?"

   Options (multiSelect: true):
   - Temporal patterns (time-of-day, day-of-week clustering) (Recommended)
   - Causal patterns (same root cause recurring)
   - Structural patterns (same components failing together)
   - Cascade patterns (A fails → B fails → C fails)
   - All pattern types
   ```

3. **Collect Data**:
   - All RCAs and incidents in time range
   - Error logs in time range

4. **Pattern Types to Look For**:
   - **Temporal**: Same time of day? Same day of week?
   - **Causal**: Same root cause appearing repeatedly?
   - **Structural**: Same components failing together?
   - **Cascade**: A fails -> B fails -> C fails?

5. **Checkpoint 3** (Validate Top Patterns):
   ```
   For each significant pattern found (top 3):

   Use AskUserQuestion:
   "Pattern Found: {description}

   Occurrences: {N} times in {period}
   Components: {list}

   Is this pattern..."

   Options:
   - New insight - investigate further
   - Known issue - being addressed
   - Known issue - accepted/deprioritized
   - False positive - explain why
   ```

6. **Design Escalation Check**:
   If any pattern suggests redesign opportunity → trigger escalation checkpoint
   (See DESIGN_ESCALATION.md)

7. **Generate Report**: Write to `docs/analysis/{YYYY-MM-DD_HHMM}_patterns.md`

8. **STOP** and present findings. Await instructions.

---

## Mode: Component Deep Dive (`/analyze component [scope]`)

**Purpose**: Focused analysis on a specific component.

### Workflow

1. **Scope Resolution**:
   ```
   IF no scope provided:
       Present discovered components from System Map
       Use AskUserQuestion: "Which component?"
   ELSE IF scope is a path:
       Use path directly
   ELSE:
       Use natural language matching to find component
   ```

2. **Checkpoint 1** (Component Selection):
   ```
   Use AskUserQuestion:
   "Which component would you like to analyze?"

   Options:
   - {Component 1 from System Map}
   - {Component 2 from System Map}
   - {Component 3 from System Map}
   - Let me specify by path or description
   ```

3. **Checkpoint 2** (Analysis Depth):
   ```
   Use AskUserQuestion:
   "How deep should the analysis go?"

   Options:
   - Quick overview (dependencies, recent incidents) (Recommended)
   - Standard analysis (+ code patterns, error handling)
   - Deep dive (+ test coverage, all historical incidents)
   ```

4. **Checkpoint 3** (Context):
   ```
   Use AskUserQuestion:
   "Any specific concerns about this component?"

   Options:
   - No specific concerns - general analysis (Recommended)
   - Recent failures - focus on reliability
   - Performance issues - focus on efficiency
   - Planning changes - assess impact
   - Let me describe...
   ```

5. **Analyze Component**:
   - Read all source files
   - Map dependencies (what it imports, what imports it)
   - Find related incidents/RCAs
   - Identify error handling patterns
   - Assess test coverage (if requested)

6. **Design Escalation Check**:
   If findings suggest redesign opportunity → trigger escalation checkpoint
   (See DESIGN_ESCALATION.md)

7. **Generate Report**: Write to `docs/analysis/{YYYY-MM-DD_HHMM}_component_{name}.md`

8. **STOP** and present findings. Await instructions.

---

## Mode: Risk Assessment (`/analyze risk [scope]`)

**Purpose**: Prioritized risk matrix with likelihood and impact scoring.

### Workflow

1. **Checkpoint 1** (Scope):
   ```
   Use AskUserQuestion:
   "What scope should I assess for risks?"

   Options:
   - All components (comprehensive)
   - External integrations only (Recommended)
   - Data pipeline only
   - Recently changed components
   - Let me specify...
   ```

2. **Checkpoint 2** (Risk Tolerance):
   ```
   Use AskUserQuestion:
   "What's your risk tolerance for this assessment?"

   Options:
   - Conservative - flag everything suspicious (Recommended)
   - Moderate - flag likely issues only
   - Aggressive - critical risks only
   ```

3. **Checkpoint 3** (Business Context):
   ```
   Use AskUserQuestion:
   "Any business context that affects risk prioritization?"

   Options:
   - No special context (Recommended)
   - Preparing for high-traffic event
   - In stabilization period (minimize changes)
   - Aggressive timeline (speed > perfection)
   - Let me describe...
   ```

4. **Identify Risks**:
   - Single points of failure
   - Missing error handling
   - No retry logic for network calls
   - Hardcoded timeouts
   - Missing monitoring
   - Stale dependencies

5. **Score Each Risk**:
   ```
   Likelihood (1-5): How likely to occur?
   Impact (1-5): How severe if it does?
   Risk Score = Likelihood x Impact

   1-5: Low (green)
   6-12: Medium (yellow)
   13-19: High (orange)
   20-25: Critical (red)
   ```

6. **Checkpoint 4** (Validate HIGH/CRITICAL findings):
   ```
   For each HIGH or CRITICAL risk:

   Use AskUserQuestion:
   "Risk: {description}
   Score: {X} ({severity})

   Is this..."

   Options:
   - New finding - needs attention
   - Known - actively being fixed
   - Known - accepted risk
   - Not a real risk (explain)
   ```

7. **Design Escalation Check**:
   If any risk suggests redesign opportunity → trigger escalation checkpoint
   (See DESIGN_ESCALATION.md)

8. **Generate Report**: Write to `docs/analysis/{YYYY-MM-DD_HHMM}_risk.md`

9. **STOP** and present findings. Await instructions.

---

## Mode: Architecture Review (`/analyze architecture`)

**Purpose**: Review architecture, identify discrepancies between docs and code.

**WARNING**: This mode may modify ARCHITECTURE.md. Interactive confirmation REQUIRED.

### Workflow

1. **Checkpoint 1** (Scope):
   ```
   Use AskUserQuestion:
   "What should the architecture review focus on?"

   Options:
   - Full system architecture (Recommended)
   - Backend services only
   - Data flow and pipelines
   - API design
   - Let me specify...
   ```

2. **Checkpoint 2** (Documentation Intent):
   ```
   Use AskUserQuestion:
   "How should I handle discrepancies between docs and code?"

   Options:
   - Assume code is truth, docs are outdated (Recommended)
   - Assume docs are truth, code has drifted
   - Ask me for each discrepancy
   - Just report discrepancies, don't suggest fixes
   ```

3. **Discover Actual Architecture**:
   - Scan codebase for services, APIs, models
   - Build dependency graph
   - Identify patterns in use (Repository, Service, Factory, etc.)

4. **Compare to Documentation**:
   - Read ARCHITECTURE.md (if exists)
   - Identify discrepancies:
     - Components in code but not in docs
     - Components in docs but not in code
     - Incorrect relationships
     - Outdated descriptions

5. **Checkpoint 3** (For EACH discrepancy - if "ask me" selected):
   ```
   Use AskUserQuestion:
   "Discrepancy: Doc says '{X}', code shows '{Y}'"

   Options:
   - Update ARCHITECTURE.md (doc is outdated)
   - Flag as tech debt (code should change)
   - Ignore (intentional difference)
   ```

6. **Checkpoint 4** (If any doc updates):
   ```
   REQUIRED before any file edits.

   Show diff preview:
   "I will make these changes to ARCHITECTURE.md:

   {diff preview}

   Apply changes?"

   Options:
   - Yes, apply all changes
   - Let me review each change individually
   - No, cancel (just output the report)
   ```

7. **Design Escalation Check**:
   If architectural issues suggest redesign → trigger escalation checkpoint
   (See DESIGN_ESCALATION.md)

8. **Generate Report**: Write to `docs/analysis/{YYYY-MM-DD_HHMM}_architecture.md`

9. **Apply Changes** (only if confirmed in Checkpoint 4)

10. **STOP** and present findings. Await instructions.

---

## Design Escalation

When any mode detects a finding that suggests **architectural redesign** rather than a point fix, trigger an escalation checkpoint.

### Escalation Triggers
- Same logic duplicated in 3+ files
- Technology choice conflicts with requirements
- Approach won't scale to 10x
- Same component in 3+ incidents
- High coupling hotspot

### Escalation Checkpoint
```
Use AskUserQuestion:
"Finding: {description}

This suggests a design consideration rather than a point fix.
Would you like to explore design alternatives?"

Options:
- Yes, explore inline (quick trade-off analysis)
- Yes, deep dive (recommend /design skill)
- No, just note it in the report
- No, this is a known accepted limitation
```

See `DESIGN_ESCALATION.md` for full specification.

---

## Report Template (All Modes)

```markdown
# Systems Analysis: {Mode} - {Scope}

**Date**: {YYYY-MM-DD HH:MM} UTC
**Analyst**: Claude Code (Session {N})
**Mode**: {Health | Patterns | Component | Risk | Architecture}
**Interactive Checkpoints**: {N} decisions made by user

---

## Executive Summary
{2-3 sentences: What was analyzed, key finding, main recommendation}

---

## User Context
{Captured from checkpoints: focus areas, known issues, risk tolerance, etc.}

---

## Scope & Methodology
- **Analyzed**: {What was examined}
- **Period**: {Time range if applicable}
- **Data Sources**: {RCAs, incidents, logs, code}

---

## Key Findings

### Finding 1: {Title}
**Severity**: {Critical | High | Medium | Low}
**Category**: {Reliability | Performance | Security | Architecture}
**User Validation**: {New finding | Known-fixing | Known-accepted | N/A}
{Description with evidence}

---

## {Mode-Specific Section}
{Health: Scores | Patterns: Pattern list | Risk: Risk matrix | Architecture: Discrepancies}

---

## Design Considerations
{Any findings that triggered design escalation, with user's decision}

---

## Recommendations

### Immediate (This Week)
1. {High-priority action}

### Short-term (This Month)
1. {Medium-priority action}

### Strategic (This Quarter)
1. {Long-term improvement}

---

## Related Documents
- {Links to relevant RCAs, incidents}

---

**Analysis Complete**: {YYYY-MM-DD HH:MM} UTC
```

---

## Flags

```
--batch         Skip interactive checkpoints (use defaults)
                NOT allowed for architecture mode
--dry-run       Show findings without creating reports
--refresh       Force refresh System Map before analysis
--verbose       Show all findings, not just significant ones
```

**Note**: `--batch` is NOT allowed for architecture mode (file edits require confirmation).

---

## After Analysis

**ALWAYS STOP** after generating the report.

Output format:
```
Analysis complete: docs/analysis/{filename}.md

Interactive decisions: {N} checkpoints
User context applied: {summary of user inputs}

Key Finding: {One-line summary of most important finding}

{Mode-specific metrics}
Health Score: {X}/10 (if health mode)
Risks Found: {N} critical, {N} high (if risk mode)
Patterns Found: {N} recurring issues (if patterns mode)

Design Considerations: {N} escalation opportunities identified

Recommended next steps:
- {Specific recommendation based on findings}

Awaiting your instructions.
```

**Do NOT** proceed with fixes or implementations without user direction.

---

## Integration with Other Skills

| After Analysis... | Consider... |
|-------------------|-------------|
| Found specific incident pattern | `/investigate {pattern}` |
| Identified root cause | `/rca-bugfix {cause}` |
| Design escalation selected "deep dive" | `/design tradeoff {topic}` |
| Need implementation plan | Use EnterPlanMode |
| Need ongoing monitoring | `/watchdog {component}` |

---

## Example Usage

```
User: /analyze discover
→ Interactive: confirms scope, exclusions, validates findings

User: /analyze health
→ Interactive: focus areas, known context, validates scores

User: /analyze patterns
→ Interactive: time period, pattern types, validates top patterns

User: /analyze patterns last-30-days
→ Skips time period question, still asks pattern types

User: /analyze component
→ Interactive: component selection, depth, concerns

User: /analyze component "the batch client"
→ Skips selection, still asks depth and concerns

User: /analyze risk
→ Interactive: scope, tolerance, business context, validates findings

User: /analyze architecture
→ Interactive: focus, discrepancy handling, change confirmation

User: /analyze health --batch
→ Uses defaults for all checkpoints, still generates report
```
