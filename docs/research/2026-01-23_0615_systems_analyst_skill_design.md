# Systems Analyst Skill: Design Research & Specification

**Date**: 2026-01-23
**Author**: Claude Code (Session 77)
**Purpose**: Deep research and design for an AI-powered Systems Analyst skill

---

## Executive Summary

This document presents comprehensive research on designing a **Systems Analyst** skill for Claude Code—an AI-powered capability that goes beyond reactive incident response to provide **proactive system health analysis, pattern recognition across incidents, architectural insight, and strategic recommendations**.

The Systems Analyst skill represents the evolution from **task-specific tools** (incident, investigate, rca-bugfix, watchdog) to a **holistic analytical framework** that reasons about the entire system as an interconnected whole.

---

## Table of Contents

1. [The 2026 Landscape](#1-the-2026-landscape)
2. [Gap Analysis: What's Missing](#2-gap-analysis-whats-missing)
3. [Systems Thinking Framework](#3-systems-thinking-framework)
4. [Skill Design: The Systems Analyst](#4-skill-design-the-systems-analyst)
   - 4.1 Core Purpose
   - 4.2 Design Principle: Portability Through Discovery
   - 4.3 Trigger and Usage
   - 4.4 Scope Resolution Strategy
   - 4.5 Discovery Mechanism
   - 4.6 Skill Modes (Updated)
   - 4.7 Optional Project Configuration
   - 4.8 Portability Verification
5. [Implementation Patterns](#5-implementation-patterns)
6. [Integration with Existing Skills](#6-integration-with-existing-skills)
7. [Prompt Engineering Principles](#7-prompt-engineering-principles)
8. [Real-World Applications](#8-real-world-applications)
9. [Risk Assessment](#9-risk-assessment)
10. [Recommended Implementation](#10-recommended-implementation)
    - 10.1 Skill File Structure
    - 10.2 Implementation Priority
    - 10.3 Success Criteria
    - 10.4 Portability Testing Checklist
    - 10.5 Anti-Patterns to Avoid
11. [Interactive Design Patterns](#11-interactive-design-patterns) *(NEW)*
    - 11.1 The Problem with Batch-Only Skills
    - 11.2 Interactive Skill Architecture
    - 11.3 Checkpoint Definitions by Mode
    - 11.4 Risk Mode: Interactive Example
    - 11.5 Architecture Mode: Discrepancy Resolution
    - 11.6 Mode Flags
    - 11.7 Benefits of Interactive Design
12. [Artifact-Driven Architecture](#12-artifact-driven-architecture) *(NEW)*
    - 12.1 The Problem: Repeated Discovery
    - 12.2 Solution: System Map as Shared Artifact
    - 12.3 System Map Structure
    - 12.4 Refresh Strategy
    - 12.5 Benefits of Artifact Sharing

---

## 1. The 2026 Landscape

### 1.1 Industry State of AI-Powered Analysis

The AI systems analysis landscape in 2026 is characterized by several key trends:

**Autonomous IT Operations**
- Just 4% of organizations have reached full operational maturity with AI across IT operations
- 12% are using AI to automate root cause analysis and remediation
- 49% are still piloting or experimenting with AI in limited environments
- The goal is shifting from reactive alerting to **predictive prevention and autonomous remediation**

Source: [LogicMonitor - 5 Observability & AI Trends 2026](https://www.logicmonitor.com/blog/observability-ai-trends-2026)

**AI SRE Copilots**
- AI agents now perform initial triage and troubleshooting autonomously
- Multi-agent systems investigate different hypotheses simultaneously
- Working in parallel, they build a complete picture 3.5x faster than human on-call teams
- Tools like Datadog's Bits AI SRE work completely autonomously without initial prompting

Source: [Grafana Labs - AI Assistant Found Root Cause 3.5x Faster](https://grafana.com/blog/a-tale-of-two-incident-responses-how-our-ai-assist-helped-us-find-the-cause-3-5x-faster/)

**Convergence of Disciplines**
- AI engineering, cloud engineering, SRE, and security are converging into a shared operating model
- Common pipelines, shared SLOs, and unified accountability for AI-enabled services
- Telemetry engineering treats signals as first-class artifacts designed and governed like code

Source: [IBM - Observability Trends 2026](https://www.ibm.com/think/insights/observability-trends)

### 1.2 Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| MTTR reduction with AI | 17.8% average, 30-70% for leaders | [incident.io](https://incident.io/blog/5-best-ai-powered-incident-management-platforms-2026) |
| AIOps market growth | $11-16B (2025) → $30B+ (2030) | [Middleware.io](https://middleware.io/blog/observability-predictions/) |
| Developers with systematic debugging | 40-60% faster resolution | [WeAreBrain](https://wearebrain.com/blog/10-effective-debugging-techniques-for-developers/) |
| Organizations deploying anomaly detection | 60%+ | [LogicMonitor](https://www.logicmonitor.com/resources/2026-observability-ai-trends-outlook) |

### 1.3 The Shift in Human Roles

> "Instead of focusing solely on manual tasks and scripting, SREs can become trainers and strategists for AI systems, teaching AI to recognize patterns, filter out noise and avoid costly errors. This shift will elevate the SRE function from a task-oriented role to a strategic discipline centered on managing intelligent automation systems."

Source: [Dynatrace - Six Observability Predictions 2026](https://www.dynatrace.com/news/blog/six-observability-predictions-for-2026/)

---

## 2. Gap Analysis: What's Missing

### 2.1 Current Skill Landscape

Your existing skills form a **reactive incident response pipeline**:

```
[Watchdog] → [Incident] → [Investigate] → [RCA-Bugfix] → [Plan]
   ↓            ↓             ↓               ↓            ↓
 Detect      Document       Analyze        Diagnose     Implement
```

Each skill excels at its specific task:

| Skill | Purpose | Scope |
|-------|---------|-------|
| `/watchdog` | Passive monitoring, error detection | Real-time, event-driven |
| `/incident` | Document WHAT happened | Single incident, factual |
| `/investigate` | Analyze WHY it happened | Single incident, causal |
| `/rca-bugfix` | Root cause + fix prompt | Single issue, solution |
| `/plan` | Implementation planning | Single fix, execution |

### 2.2 The Missing Layer: Systems Thinking

What's missing is a **meta-analytical layer** that:

1. **Sees patterns across multiple incidents** - Not just "this failed" but "this is the third timeout failure this week"
2. **Understands system topology** - How components interact and affect each other
3. **Predicts future issues** - Based on trends and weak signals
4. **Recommends architectural changes** - Beyond point fixes to systemic improvements
5. **Learns from history** - Builds institutional memory across sessions
6. **Provides strategic guidance** - Trade-off analysis, prioritization, risk assessment

### 2.3 The Systems Analyst Gap

```
                                    ┌─────────────────────┐
                                    │  SYSTEMS ANALYST    │  ← MISSING
                                    │  (Strategic Layer)  │
                                    └─────────────────────┘
                                             │
              ┌──────────────────────────────┼──────────────────────────────┐
              │                              │                              │
              ▼                              ▼                              ▼
    ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
    │  Pattern        │          │  System Health  │          │  Architecture   │
    │  Recognition    │          │  Assessment     │          │  Recommendations│
    └─────────────────┘          └─────────────────┘          └─────────────────┘
              │                              │                              │
              └──────────────────────────────┼──────────────────────────────┘
                                             │
                                             ▼
    ┌──────────────────────────────────────────────────────────────────────────┐
    │  Existing Skills: watchdog → incident → investigate → rca-bugfix → plan  │
    │  (Tactical Layer)                                                        │
    └──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Systems Thinking Framework

### 3.1 What is Systems Thinking?

Systems thinking is an analytical approach that views software as an **interconnected whole** rather than isolated components. It helps identify:

- **Feedback loops** - Where outputs become inputs (positive or negative)
- **Emergent behavior** - System properties that arise from component interactions
- **Leverage points** - Small changes that produce large effects
- **Root causes vs symptoms** - Distinguishing underlying issues from surface manifestations

Source: [daily.dev - Systems Thinking in Software Development](https://daily.dev/blog/systems-thinking-in-software-development-guide)

### 3.2 The Seven Principles (Adapted from Springer Research)

1. **Trust = Speed** - Higher trust in the system enables faster decision-making
2. **Interconnection over isolation** - Components affect each other
3. **Patterns over events** - Look for recurring structures, not just incidents
4. **Structure influences behavior** - System design determines outcomes
5. **Feedback loops drive dynamics** - Identify reinforcing and balancing loops
6. **Delays cause oscillations** - Timing mismatches create instability
7. **Mental models matter** - How we think about the system affects how we fix it

Source: [Springer - Seven Principles of Systems Thinking](https://link.springer.com/chapter/10.1007/978-3-319-54087-0_4)

### 3.3 Traditional Analysis Methodologies

**5 Whys**
- Iterative questioning to drill down to root cause
- Best for single-cause problems
- Weakness: Can miss complex multi-factor issues

**Fishbone (Ishikawa) Diagram**
- Categorizes potential causes into branches
- Best for problems with multiple contributing factors
- Categories: People, Process, Technology, Environment, Data, External

**Fault Tree Analysis**
- Top-down deductive analysis
- Maps all possible paths to failure
- Best for safety-critical systems

**FMEA (Failure Mode and Effects Analysis)**
- Systematic identification of potential failures
- Risk prioritization using severity, occurrence, detection scores
- Best for proactive prevention

Source: [ComplianceQuest - Pros and Cons of RCA Techniques](https://www.compliancequest.com/blog/pros-cons-of-5why-pareto-fishbone-diagram/)

### 3.4 AI-Enhanced Analysis

Modern AI brings new capabilities to these traditional methods:

| Traditional | AI-Enhanced |
|-------------|-------------|
| Manual 5 Whys questioning | Automated causal chain discovery from logs |
| Static fishbone diagrams | Dynamic cause categorization with ML |
| Human pattern recognition | Cross-incident pattern detection |
| Periodic health checks | Continuous anomaly detection |
| Tribal knowledge | Searchable institutional memory |

---

## 4. Skill Design: The Systems Analyst

### 4.1 Core Purpose

The Systems Analyst skill provides **strategic-level system understanding** by:

1. Analyzing the system as a whole, not just individual incidents
2. Recognizing patterns across time and components
3. Assessing overall system health and risk posture
4. Recommending architectural improvements
5. Prioritizing issues based on systemic impact

### 4.2 Design Principle: Portability Through Discovery

**Critical Design Constraint**: The skill must be **portable across any project** without requiring project-specific configuration.

This means:
- NO hard-coded component names (e.g., `batch_client`)
- NO project-specific subsystem names (e.g., `extraction-pipeline`)
- NO assumptions about architecture (e.g., `iterable-connector`)

Instead, the skill uses **discovery-based scoping** to automatically understand any system it's applied to.

### 4.3 Trigger and Usage

```
/analyze {mode} [scope]

# Modes with generic/discoverable scopes:
/analyze system health              # No scope needed - analyzes everything
/analyze patterns last-7-days       # Time-based scope (generic)
/analyze component                  # AUTO-DISCOVER components, present options
/analyze component "API clients"    # Natural language scope
/analyze component backend/services # Path-based scope
/analyze risk                       # AUTO-DISCOVER subsystems
/analyze risk "external integrations" # Natural language scope
/analyze architecture               # Full architectural review
/analyze architecture "data flow"   # Focused architectural review
```

### 4.4 Scope Resolution Strategy

The skill resolves scopes using this priority order:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCOPE RESOLUTION FLOW                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. NO SCOPE PROVIDED?                                           │
│    → Run discovery, present options to user                     │
│    → Example: /analyze component → "Found 8 components..."      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. PATH PROVIDED? (contains / or file extension)                │
│    → Use path directly                                          │
│    → Example: /analyze component backend/app/services/          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. NATURAL LANGUAGE PROVIDED?                                   │
│    → Use LLM reasoning to find matching code/components         │
│    → Example: /analyze component "the retry logic"              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. PROJECT ALIAS PROVIDED? (from optional config)               │
│    → Map to actual component using project configuration        │
│    → Example: /analyze component api-client → batch_client.py   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.5 Discovery Mechanism

When no scope is provided, or when the skill needs to understand the system, it runs **automatic discovery**:

#### Step 1: Read Project Context Files
```
Sources (in priority order):
├── CLAUDE.md           # Project instructions, often contains architecture
├── ARCHITECTURE.md     # Explicit architecture documentation
├── README.md           # Project overview
├── docker-compose.yml  # Service definitions
├── package.json        # Frontend dependencies and scripts
├── requirements.txt    # Backend dependencies
└── pyproject.toml      # Python project metadata
```

#### Step 2: Scan Directory Structure
```
Analysis targets:
├── backend/app/services/    # Service layer modules
├── backend/app/api/         # API routers
├── backend/app/models/      # Data models
├── frontend/app/            # Frontend pages/components
├── frontend/components/     # Reusable components
└── src/                     # Alternative source layout
```

#### Step 3: Analyze Code Dependencies
```
Techniques:
├── Import graph analysis    # Find highly-imported modules (core components)
├── Class/function counting  # Identify large, complex modules
├── Cross-file references    # Map component relationships
└── Test file mapping        # tests/test_X.py → X is important
```

#### Step 4: Build System Map
```
Output: Discovered System Structure

Services (backend/app/services/):
├── iterable/
│   ├── batch_client.py      # 1,200 lines, 45 imports
│   ├── extraction_service.py # 2,500 lines, 38 imports
│   └── client.py            # 400 lines, 12 imports
├── intercom/
│   ├── contacts_service.py  # 800 lines
│   └── ...
└── workflow_scheduler.py    # 1,800 lines, 52 imports

API Layer (backend/app/api/):
├── extractions.py
├── workflows.py
└── schedules.py

Models (backend/app/models/):
├── extraction.py
├── workflow.py
└── schedule.py
```

#### Step 5: Present Options to User
```
/analyze component

> Discovered 12 components in this project:
>
> Services:
>   1. iterable/batch_client     - Batch export operations (1,200 LOC)
>   2. iterable/extraction       - Core extraction logic (2,500 LOC)
>   3. workflow_scheduler        - FSM and scheduling (1,800 LOC)
>   4. gcs_upload_service        - GCS integration (600 LOC)
>
> API Layer:
>   5. api/extractions           - Extraction endpoints
>   6. api/workflows             - Workflow endpoints
>
> Which would you like to analyze? (Enter number, path, or description)
```

### 4.6 Skill Modes (Updated)

The Systems Analyst operates in five modes, all using discovery-based scoping:

#### Mode 1: System Health Assessment
```
/analyze system health
```
- **Scope**: Entire system (no discovery needed)
- Scans all recent incidents, RCAs, and investigations
- Identifies recurring issues and trends
- Assesses overall reliability posture
- Provides health score and recommendations

#### Mode 2: Pattern Recognition
```
/analyze patterns {time-period}
```
- **Scope**: Time-based (generic: last-7-days, last-month, since-deploy)
- Analyzes incidents/errors over specified period
- Identifies recurring failure modes
- Detects correlation between events
- Flags emerging issues

#### Mode 3: Component Deep Dive
```
/analyze component                      # Discovery mode
/analyze component "the API client"     # Natural language
/analyze component backend/services/x/  # Path-based
```
- **Scope**: Auto-discovered, natural language, or path
- Focused analysis on specific component
- Maps upstream/downstream dependencies
- Identifies component-specific failure modes
- Recommends component-level improvements

#### Mode 4: Risk Assessment
```
/analyze risk                           # Discovery mode
/analyze risk "external integrations"   # Natural language
/analyze risk backend/app/services/     # Path-based
```
- **Scope**: Auto-discovered subsystems or described area
- Evaluates risk posture of subsystem
- Identifies single points of failure
- Assesses blast radius of potential failures
- Prioritizes risks by likelihood and impact

#### Mode 5: Architectural Review
```
/analyze architecture                   # Full system
/analyze architecture "data flow"       # Focused review
/analyze architecture "API design"      # Focused review
```
- **Scope**: Full system or natural language focus area
- Reviews architectural patterns in use
- Identifies anti-patterns and technical debt
- Recommends architectural improvements
- Considers scalability, reliability, maintainability

### 4.7 Optional Project Configuration

Projects can **optionally** define component aliases in CLAUDE.md for convenience:

```markdown
<!-- SYSTEMS_ANALYST_CONFIG_START -->
## System Components (for /analyze)

| Alias | Path | Description |
|-------|------|-------------|
| batch-client | backend/app/services/iterable/batch_client.py | Iterable API client |
| extractor | backend/app/services/iterable/extraction_service.py | Core extraction |
| scheduler | backend/app/services/workflow_scheduler.py | FSM and retries |
<!-- SYSTEMS_ANALYST_CONFIG_END -->
```

**Important**: This configuration is **entirely optional**. The skill works without it via discovery.

### 4.8 Portability Verification

The skill is portable when it passes this test:

```
✅ Works on project A (Python/FastAPI backend)
✅ Works on project B (Node.js/Express backend)
✅ Works on project C (Microservices architecture)
✅ Works on project D (Monolithic Rails app)
✅ Works on project E (Frontend-only React app)

For each project:
- /analyze system health     → Works without configuration
- /analyze component         → Discovers components automatically
- /analyze risk              → Identifies subsystems automatically
- /analyze architecture      → Reviews whatever architecture exists
```

### 4.4 Output Structure

All analyses produce a standardized report:

```markdown
# Systems Analysis: {Scope}

**Date**: {YYYY-MM-DD HH:MM} UTC
**Analyst**: Claude Code (Session {N})
**Mode**: {Health | Patterns | Component | Risk | Architecture}

---

## Executive Summary
{2-3 sentence overview of findings}

---

## Scope & Methodology
- **Analyzed**: {What was examined}
- **Period**: {Time range}
- **Data Sources**: {Logs, RCAs, code, etc.}

---

## Key Findings

### Finding 1: {Title}
**Severity**: {Critical | High | Medium | Low}
**Category**: {Reliability | Performance | Security | Architecture}
{Description with evidence}

### Finding 2: {Title}
...

---

## Pattern Analysis
{Recurring themes, correlations, trends}

---

## Risk Matrix

| Risk | Likelihood | Impact | Score | Mitigation |
|------|------------|--------|-------|------------|
| ... | ... | ... | ... | ... |

---

## System Health Score

| Dimension | Score | Notes |
|-----------|-------|-------|
| Reliability | X/10 | ... |
| Performance | X/10 | ... |
| Maintainability | X/10 | ... |
| Observability | X/10 | ... |
| **Overall** | **X/10** | ... |

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
- {Links to relevant RCAs, investigations, plans}

---

**Analysis Complete**: {YYYY-MM-DD HH:MM} UTC
```

---

## 5. Implementation Patterns

### 5.1 Multi-Step Analysis Workflow

The Systems Analyst follows a structured workflow with **discovery-first scoping**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEMS ANALYST WORKFLOW                     │
│                  (Discovery-Based Scoping)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 0: SYSTEM DISCOVERY (if scope not provided)                │
│ - Read CLAUDE.md, ARCHITECTURE.md, README.md                    │
│ - Scan directory structure for components                       │
│ - Analyze import graphs for core modules                        │
│ - Build system map                                              │
│ - Present options to user OR proceed with natural language      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: SCOPE DEFINITION                                        │
│ - Parse user request for analysis scope                         │
│ - Determine analysis mode (health, patterns, component, etc.)   │
│ - Resolve scope (discovery, natural language, or path)          │
│ - Define time boundaries and data sources                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: DATA COLLECTION                                         │
│ - Read all docs/RCAs/*.md                                       │
│ - Read all docs/investigations/*.md                             │
│ - Read all docs/incidents/*.md                                  │
│ - Search logs for relevant events                               │
│ - Read relevant source code                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: PATTERN RECOGNITION                                     │
│ - Identify recurring failure modes                              │
│ - Detect temporal patterns (time of day, frequency)             │
│ - Find correlation between incidents                            │
│ - Map causal chains across components                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: SYSTEMS MODELING                                        │
│ - Build mental model of system architecture                     │
│ - Identify feedback loops                                       │
│ - Map dependencies and coupling                                 │
│ - Locate leverage points for improvement                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: RISK ASSESSMENT                                         │
│ - Calculate likelihood × impact for identified issues          │
│ - Assess blast radius of potential failures                     │
│ - Identify single points of failure                             │
│ - Prioritize by risk score                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: RECOMMENDATION SYNTHESIS                                │
│ - Generate immediate tactical fixes                             │
│ - Propose short-term improvements                               │
│ - Recommend strategic architectural changes                     │
│ - Consider trade-offs and constraints                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 7: REPORT GENERATION                                       │
│ - Write analysis to docs/analysis/YYYY-MM-DD_HHMM_{scope}.md   │
│ - Present findings with evidence                                │
│ - STOP and await user instructions                              │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Data Collection Strategy

The analyst uses **discovery-based data collection** that adapts to any project structure:

```python
# Pseudo-code for discovery-based data collection
def discover_data_sources(project_root):
    sources = {}

    # 1. Documentation (standard locations)
    doc_patterns = [
        "docs/RCAs/*.md",
        "docs/investigations/*.md",
        "docs/incidents/*.md",
        "docs/plans/*.md",
        "docs/research/*.md",
        "docs/**/*.md",           # Catch-all for other docs
    ]
    sources["documentation"] = find_files(doc_patterns)

    # 2. Project context files
    context_files = [
        "CLAUDE.md",
        "ARCHITECTURE.md",
        "README.md",
        "CONTRIBUTING.md",
    ]
    sources["context"] = find_existing(context_files)

    # 3. Configuration files (discover project type)
    config_patterns = {
        "python": ["pyproject.toml", "requirements.txt", "setup.py"],
        "node": ["package.json", "tsconfig.json"],
        "docker": ["docker-compose.yml", "Dockerfile"],
        "kubernetes": ["k8s/*.yaml", "helm/**/*.yaml"],
    }
    sources["config"] = discover_configs(config_patterns)

    # 4. Source code (discover based on project type)
    code_patterns = discover_source_layout(project_root)
    # Might return: backend/app/services/, src/, lib/, etc.
    sources["code"] = code_patterns

    # 5. Logs (discover running services)
    sources["logs"] = discover_log_sources()
    # Might return: docker containers, log files, systemd journals

    return sources

def discover_source_layout(root):
    """Discover source code layout regardless of project type."""
    layouts = [
        # Python patterns
        ("backend/app/", "Python backend"),
        ("src/", "Generic source"),
        ("app/", "Application code"),
        ("lib/", "Library code"),
        # Node patterns
        ("src/", "TypeScript/JavaScript source"),
        ("pages/", "Next.js pages"),
        ("components/", "React components"),
        # Generic patterns
        ("services/", "Service layer"),
        ("api/", "API layer"),
        ("models/", "Data models"),
    ]
    return find_existing_layouts(root, layouts)
```

**Key Principle**: The data collection adapts to the project rather than assuming a specific structure.

### 5.3 Pattern Recognition Algorithms

The analyst looks for these pattern types:

**Temporal Patterns**
- Time-of-day clustering (failures at specific hours)
- Day-of-week patterns (weekend vs weekday)
- Frequency analysis (increasing failure rate)

**Causal Patterns**
- Repeated root causes across incidents
- Cascade failures (A fails → B fails → C fails)
- Circular dependencies

**Structural Patterns**
- Common components in failures
- Shared dependencies
- Coupling hotspots

### 5.4 Scoring Methodology

**Risk Score Calculation**
```
Risk Score = Likelihood (1-5) × Impact (1-5)

Likelihood Scale:
1 = Rare (< 1% chance)
2 = Unlikely (1-10%)
3 = Possible (10-50%)
4 = Likely (50-90%)
5 = Almost Certain (> 90%)

Impact Scale:
1 = Negligible (< 1% data affected)
2 = Minor (1-10% data affected)
3 = Moderate (10-25% data affected)
4 = Major (25-50% data affected)
5 = Critical (> 50% data affected)

Risk Categories:
1-5: Low (green)
6-12: Medium (yellow)
13-19: High (orange)
20-25: Critical (red)
```

**Health Score Calculation**
```
Health Score = Average of dimension scores (0-10)

Dimensions:
- Reliability: Success rate, MTTR, incident frequency
- Performance: Latency, throughput, resource utilization
- Maintainability: Code quality, test coverage, documentation
- Observability: Monitoring coverage, alert accuracy, log quality

Interpretation:
9-10: Excellent
7-8: Good
5-6: Fair
3-4: Poor
1-2: Critical
```

---

## 6. Integration with Existing Skills

### 6.1 Skill Hierarchy

```
                    ┌─────────────────────┐
                    │  /analyze           │  Strategic (new)
                    │  Systems Analyst    │
                    └─────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  /watchdog  │  │  /research  │  │  /plan      │   Operational
    │  Monitor    │  │  Explore    │  │  Execute    │
    └─────────────┘  └─────────────┘  └─────────────┘
              │               │
              ▼               ▼
    ┌─────────────┐  ┌─────────────┐
    │  /incident  │  │  /investigate│                    Tactical
    │  Document   │  │  Analyze    │
    └─────────────┘  └─────────────┘
                          │
                          ▼
                ┌─────────────────┐
                │  /rca-bugfix    │
                │  Diagnose & Fix │
                └─────────────────┘
```

### 6.2 When to Use Which Skill

| Situation | Skill | Why |
|-----------|-------|-----|
| Error just detected | `/incident` | Document what happened |
| Need to understand why | `/investigate` | Deep dive on single incident |
| Ready to fix | `/rca-bugfix` | Create RCA and fix prompt |
| Need to implement | `/plan` | Create implementation plan |
| Continuous monitoring | `/watchdog` | Passive error detection |
| Multiple incidents, need overview | `/analyze` | **Systems-level patterns** |
| Architecture concerns | `/analyze architecture` | **Structural review** |
| Risk assessment needed | `/analyze risk` | **Risk prioritization** |

### 6.3 Handoff Protocols

**From Systems Analyst to Other Skills**

```
/analyze → identifies issue → recommends → /investigate {issue}
/analyze → finds pattern → recommends → /rca-bugfix {pattern}
/analyze → architectural concern → recommends → /plan {improvement}
```

**From Other Skills to Systems Analyst**

```
/investigate → completed → user decides → /analyze patterns
/rca-bugfix → fix deployed → user wants → /analyze system health
Multiple /incidents → user wants overview → /analyze patterns last-7-days
```

---

## 7. Prompt Engineering Principles

### 7.1 2026 Prompt Engineering Best Practices

Based on current research, effective AI analysis skills should follow these principles:

**Workflow Design Over Word Engineering**
> "The focus shifts from perfecting individual prompts to architecting entire AI-powered processes."

Source: [IBM - The 2026 Guide to Prompt Engineering](https://www.ibm.com/think/prompt-engineering)

**Agentic Workflow Principles**
1. Plan tasks thoroughly to ensure complete resolution
2. Provide clear preambles for major tool usage decisions
3. Use structured tracking (TODO tools) for workflow progress
4. Decompose into sub-tasks and reflect after each step

Source: [OpenAI - Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

**Context Engineering**
- Provide rich context about system architecture
- Include relevant history (past incidents, decisions)
- Specify constraints and requirements clearly
- Define output format precisely

### 7.2 Skill Prompt Structure

The Systems Analyst skill prompt should include:

```markdown
# Systems Analyst Skill

**Trigger**: `/analyze {scope}`

## Context You Have
- Access to all docs/RCAs/, docs/investigations/, docs/incidents/
- Ability to read source code
- Ability to search logs
- Knowledge of system architecture from CLAUDE.md

## Your Role
You are a senior systems analyst with expertise in:
- Site Reliability Engineering (SRE)
- Root cause analysis
- Systems thinking
- Risk assessment
- Architectural patterns

## Analysis Methodology

THINK MAX HARD about the system as a whole.

### Step 1: Scope Definition
[Parse request, determine mode, set boundaries]

### Step 2: Data Collection
[Systematic gathering from all sources]

### Step 3: Pattern Recognition
[Temporal, causal, structural patterns]

### Step 4: Systems Modeling
[Architecture, dependencies, feedback loops]

### Step 5: Risk Assessment
[Likelihood × Impact scoring]

### Step 6: Recommendation Synthesis
[Immediate, short-term, strategic]

### Step 7: Report Generation
[Standardized output format]

## Output Format
[Detailed template]

## After Analysis
STOP and present findings. Await user instructions.
```

---

## 8. Real-World Applications

### 8.1 Application to Kuda Data Connector

Based on the current project state, here's how the Systems Analyst would help:

**Current Pain Points** (from session history):
1. Repeated network timeout failures (ConnectTimeout, ReadTimeout, RemoteProtocolError)
2. URL expiration issues during long downloads
3. Extraction hangs requiring manual intervention
4. FSM retry storms creating new export jobs

**Systems Analysis Would Reveal**:

```
Pattern: Network Resilience Gap
├── ConnectTimeout in initiate_export (Jan 21, 22)
├── ConnectTimeout in URL refresh (Jan 22)
├── ReadTimeout in stream download (Jan 22)
├── RemoteProtocolError in stream download (Jan 23)
└── Root Pattern: httpx client has no transport-level retry

Recommendation: Implement HTTPTransport(retries=3) across all clients
Impact: Would prevent 80% of observed failures
```

```
Pattern: Long-Running Operation Vulnerability
├── URL expiration after 30 minutes
├── Downloads taking 40+ minutes for large files
├── No proactive refresh before expiration
└── Root Pattern: Time-bounded resources without lifecycle management

Recommendation: Implement proactive URL refresh at 20-minute mark
Impact: Eliminate URL expiration failures entirely
```

### 8.2 Example Analysis Output

```markdown
# Systems Analysis: Iterable Connector Reliability

**Date**: 2026-01-23 06:15 UTC
**Analyst**: Claude Code (Session 77)
**Mode**: System Health Assessment

---

## Executive Summary

The Iterable connector exhibits a recurring pattern of network-related failures
during batch export operations. Analysis of 12 incidents over 3 days reveals
a systematic gap in retry logic at the HTTP transport layer, causing cascading
failures that trigger FSM retry storms and waste API quota.

---

## Key Findings

### Finding 1: Missing Transport-Level Retries
**Severity**: Critical
**Category**: Reliability

The httpx AsyncClient is configured without transport retries:
- `ConnectTimeout` failures are not retried at transport level
- `RemoteProtocolError` (connection drops) trigger full extraction restart
- Each retry creates new Iterable export job (API quota waste)

Evidence: 5 incidents in 72 hours with same root cause.

### Finding 2: Time-Bounded Resource Mismanagement
**Severity**: High
**Category**: Architecture

Iterable download URLs expire after 30 minutes, but:
- No proactive refresh before expiration
- URL refresh is reactive (triggered when URLs are already old)
- Refresh failures cause silent continuation with stale URLs

Evidence: 2 incidents where extractions hung after URL expiration.

---

## Risk Matrix

| Risk | Likelihood | Impact | Score | Mitigation |
|------|------------|--------|-------|------------|
| Network timeout during download | 4 | 4 | 16 (High) | Add transport retries |
| URL expiration mid-download | 3 | 5 | 15 (High) | Proactive refresh |
| FSM retry storm | 3 | 3 | 9 (Medium) | Rate limit retries |
| Telegram notification gaps | 2 | 2 | 4 (Low) | Fixed in Session 77 |

---

## System Health Score

| Dimension | Score | Notes |
|-----------|-------|-------|
| Reliability | 4/10 | Frequent failures, poor retry logic |
| Performance | 7/10 | Good throughput when working |
| Maintainability | 6/10 | Good code structure, some complexity |
| Observability | 8/10 | Excellent logging, good monitoring |
| **Overall** | **6.25/10** | **Fair - reliability issues dominate** |

---

## Recommendations

### Immediate (This Week)
1. Add `httpx.AsyncHTTPTransport(retries=3)` to batch_client.py
2. Add `RemoteProtocolError` to retryable exceptions in stream_download

### Short-term (This Month)
1. Implement proactive URL refresh at 20-minute mark
2. Add circuit breaker for repeated failures
3. Rate limit FSM retries to prevent storm

### Strategic (This Quarter)
1. Consider chunked downloads with resume capability
2. Implement download checkpointing to GCS
3. Add predictive health monitoring for Iterable API
```

---

## 9. Risk Assessment

### 9.1 Risks of Implementing Systems Analyst Skill

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Context exhaustion (large analysis) | High | Medium | Implement incremental analysis mode |
| Analysis paralysis (too much data) | Medium | Medium | Define clear scope boundaries |
| Stale recommendations | Medium | Low | Include freshness indicators |
| Over-reliance on AI judgment | Low | High | Always require human approval |

### 9.2 Benefits vs Costs

**Benefits**:
- Proactive issue identification
- Pattern recognition across incidents
- Consistent analytical methodology
- Institutional memory building
- Strategic vs tactical focus

**Costs**:
- Significant context usage per analysis
- Requires comprehensive data collection
- May surface overwhelming number of issues
- Learning curve for effective usage

---

## 10. Recommended Implementation

### 10.1 Skill File Structure

```
.claude/skills/analyze/
├── SKILL.md              # Main skill definition with discovery logic
├── discovery/
│   ├── project_scanner.md    # How to scan project structure
│   ├── component_finder.md   # How to identify components
│   └── scope_resolver.md     # How to resolve natural language scopes
├── templates/
│   ├── health.md         # Health assessment template
│   ├── patterns.md       # Pattern analysis template
│   ├── component.md      # Component deep dive template
│   ├── risk.md           # Risk assessment template
│   └── architecture.md   # Architecture review template
└── examples/
    ├── python_fastapi.md     # Example for Python/FastAPI project
    ├── node_express.md       # Example for Node/Express project
    └── microservices.md      # Example for microservices
```

### 10.2 Implementation Priority

1. **Phase 1**: Discovery Mechanism (foundation for all modes)
   - Project structure scanning
   - Component identification
   - Natural language scope resolution

2. **Phase 2**: System Health Assessment mode (most valuable, no scope needed)

3. **Phase 3**: Pattern Recognition mode (time-based scope, generic)

4. **Phase 4**: Component Deep Dive mode (requires discovery)

5. **Phase 5**: Risk Assessment mode (requires discovery)

6. **Phase 6**: Architectural Review mode (most complex)

### 10.3 Success Criteria

The Systems Analyst skill is successful when it:

**Functional Criteria**:
- Identifies issues before they cause incidents (proactive)
- Reduces MTTR by providing pre-analyzed context
- Surfaces patterns that individual incident analysis misses
- Provides actionable, prioritized recommendations
- Builds institutional memory that persists across sessions

**Portability Criteria** (NEW):
- Works on any project without configuration
- Discovers components automatically via scanning
- Accepts natural language scopes ("the API client")
- Falls back gracefully when discovery finds nothing
- Produces useful output even on unfamiliar codebases

### 10.4 Portability Testing Checklist

Before considering the skill complete, test on diverse project types:

```
□ Python/FastAPI backend (like this project)
□ Node.js/Express backend
□ React/Next.js frontend
□ Monolithic application
□ Microservices architecture
□ Library/package (no services)
□ Empty/new project (graceful handling)
```

For each test:
- `/analyze system health` produces meaningful output
- `/analyze component` discovers something useful
- `/analyze risk` identifies relevant concerns
- Natural language scopes resolve correctly

### 10.5 Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| Hard-coded component names | Not portable | Discovery-based |
| Project-specific paths | Not portable | Pattern-based scanning |
| Assuming specific frameworks | Limits applicability | Framework detection |
| Requiring configuration | Friction to adoption | Optional config, works without |
| Single output format | Doesn't fit all projects | Adaptive templates |

---

## Sources

1. [BigPanda - AI-Powered IT Root Cause Analysis](https://www.bigpanda.io/our-product/root-cause-analysis/)
2. [incident.io - 5 Best AI-Powered Incident Management Platforms 2026](https://incident.io/blog/5-best-ai-powered-incident-management-platforms-2026)
3. [Grafana Labs - AI Assistant Found Root Cause 3.5x Faster](https://grafana.com/blog/a-tale-of-two-incident-responses-how-our-ai-assist-helped-us-find-the-cause-3-5x-faster/)
4. [Xurrent - How AI Is Transforming Observability 2026](https://www.xurrent.com/blog/ai-incident-management-observability-trends)
5. [DevActivity - AI-Powered RCA: Slash MTTR by 50%](https://devactivity.com/posts/trends-news-insights/cut-mttr-by-50-how-ai-powered-root-cause-analysis-is-revolutionizing-incident-response/)
6. [Dash0 - 7 Best AI SRE Tools 2026](https://www.dash0.com/comparisons/best-ai-sre-tools)
7. [LogicMonitor - Observability & AI Trends 2026](https://www.logicmonitor.com/resources/2026-observability-ai-trends-outlook)
8. [IBM - Observability Trends 2026](https://www.ibm.com/think/insights/observability-trends)
9. [Dynatrace - Six Observability Predictions 2026](https://www.dynatrace.com/news/blog/six-observability-predictions-for-2026/)
10. [Middleware.io - Observability Predictions 2026](https://middleware.io/blog/observability-predictions/)
11. [Claude Blog - Eight Trends Defining Software 2026](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026)
12. [Claude Docs - Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
13. [Claude Blog - Introducing Agent Skills](https://claude.com/blog/skills)
14. [Lee Han Chung - Claude Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
15. [daily.dev - Systems Thinking in Software Development](https://daily.dev/blog/systems-thinking-in-software-development-guide)
16. [Springer - Seven Principles of Systems Thinking](https://link.springer.com/chapter/10.1007/978-3-319-54087-0_4)
17. [WeAreBrain - 10 Debugging Techniques 2026](https://wearebrain.com/blog/10-effective-debugging-techniques-for-developers/)
18. [ComplianceQuest - 5 Whys vs Fishbone vs Pareto](https://www.compliancequest.com/blog/pros-cons-of-5why-pareto-fishbone-diagram/)
19. [Rootly - Automated Postmortem Tools for SRE](https://rootly.com/sre/drive-learning-automated-postmortem-tools-for-sre-teams)
20. [Atlassian - How to Run a Blameless Postmortem](https://www.atlassian.com/incident-management/postmortem/blameless)
21. [IBM - The 2026 Guide to Prompt Engineering](https://www.ibm.com/think/prompt-engineering)
22. [OpenAI - Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
23. [Nucamp - Incident Response 2026 Playbook](https://www.nucamp.co/blog/incident-response-in-2026-a-step-by-step-playbook-with-checklists)
24. [PagerDuty - AI-Powered Incident Playbook](https://www.pagerduty.com/blog/ai/ai-agents-incident-response-automate-vs-escalate/)

---

**Research Complete**: 2026-01-23 06:15 UTC
**Updated**: 2026-01-23 06:45 UTC - Added discovery-based scoping for portability
**Updated**: 2026-01-23 07:15 UTC - Added interactive design patterns and artifact sharing
**Ready for**: Skill Implementation

---

## 11. Interactive Design Patterns

### 11.1 The Problem with Batch-Only Skills

Traditional skill design:
```
User triggers → Skill runs to completion → Output report → Stop
```

This is **one-way communication**. The skill can't:
- Understand business context
- Know which risks matter most to the user
- Confirm assumptions before acting
- Distinguish "documentation is wrong" from "code is wrong"

### 11.2 Interactive Skill Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 INTERACTIVE SYSTEMS ANALYST                     │
└─────────────────────────────────────────────────────────────────┘

                    /analyze {mode}
                          │
                          ▼
              ┌───────────────────────┐
              │  PHASE 1: DISCOVERY   │  Automatic
              │  (Build System Map)   │
              └───────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  CHECKPOINT 1:        │  ← User Input
              │  Scope & Context      │     (AskUserQuestion)
              └───────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  PHASE 2: ANALYSIS    │  Automatic
              │  (Uses user context)  │
              └───────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  CHECKPOINT 2:        │  ← User Input
              │  Validate Findings    │     (AskUserQuestion)
              └───────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  PHASE 3: REPORT      │  Automatic
              │  (Draft with context) │
              └───────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
         No file edits           File edits needed
              │                       │
              ▼                       ▼
    ┌─────────────────┐    ┌───────────────────────┐
    │  OUTPUT REPORT  │    │  CHECKPOINT 3:        │  ← User Input
    │  (Final)        │    │  Preview & Confirm    │     (REQUIRED)
    └─────────────────┘    │  Changes              │
                           └───────────────────────┘
                                      │
                                      ▼
                           ┌─────────────────┐
                           │  APPLY CHANGES  │
                           │  (Only if yes)  │
                           └─────────────────┘
```

### 11.3 Checkpoint Definitions by Mode

| Mode | Checkpoint 1 | Checkpoint 2 | Checkpoint 3 | Modifies Files? |
|------|--------------|--------------|--------------|-----------------|
| `system health` | None (analyzes all) | Validate findings | None | No |
| `patterns` | Time period confirm | None | Validate patterns | No |
| `component` | Component selection | Context gathering | Validate findings | No |
| `risk` | Scope + risk tolerance | Validate each risk | None | No |
| `architecture` | None (analyzes all) | **Resolve discrepancies** | **Preview & confirm** | **Yes** |

### 11.4 Risk Mode: Interactive Example

```
/analyze risk

┌─────────────────────────────────────────────────────────────────┐
│ CHECKPOINT 1: SCOPE & CONTEXT                                   │
│                                                                 │
│ "I found 12 components. Which should I assess for risk?"        │
│                                                                 │
│ ○ All components (comprehensive)                                │
│ ○ External integrations only                                    │
│ ○ Data pipeline only                                           │
│ ○ Let me specify...                                            │
│                                                                 │
│ "What's your risk tolerance?"                                   │
│                                                                 │
│ ○ Conservative - flag everything suspicious                    │
│ ○ Moderate - flag likely issues                                │
│ ○ Aggressive - critical issues only                            │
│                                                                 │
│ "Any known issues I should be aware of?" [text input]          │
└─────────────────────────────────────────────────────────────────┘
                              │
                        User answers
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECKPOINT 2: FINDING VALIDATION                                │
│                                                                 │
│ "I found 5 risks. Let me validate each:"                       │
│                                                                 │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ RISK 1: ConnectTimeout in batch_client (no retry)              │
│ Severity: HIGH                                                  │
│                                                                 │
│ Is this a known issue?                                         │
│ ○ Known - actively being fixed                                 │
│ ○ Known - accepted risk                                        │
│ ○ New finding - investigate                                    │
│ ○ Not a real risk - explain why                                │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ RISK 2: URL expiration during long downloads                   │
│ ... (repeat for each HIGH severity finding)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                        User validates each
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FINAL REPORT                                                    │
│ (Incorporates user context and validation)                      │
│                                                                 │
│ - Known issues marked as "Being Fixed" or "Accepted"           │
│ - New findings highlighted for investigation                    │
│ - False positives excluded                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 11.5 Architecture Mode: Discrepancy Resolution

This mode is **critical** because it may modify `ARCHITECTURE.md`.

```
/analyze architecture

┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: DISCOVERY (automatic)                                  │
│ - Read ARCHITECTURE.md                                          │
│ - Scan actual codebase                                          │
│ - Compare and identify discrepancies                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECKPOINT 2: DISCREPANCY RESOLUTION                            │
│                                                                 │
│ Found 4 discrepancies between ARCHITECTURE.md and code:         │
│                                                                 │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ DISCREPANCY 1:                                                  │
│ Doc says: "3 backend services"                                  │
│ Reality:  5 services found                                      │
│                                                                 │
│ What should I do?                                               │
│ ○ Update ARCHITECTURE.md (doc is outdated)                     │
│ ○ Flag as tech debt (extra services shouldn't exist)           │
│ ○ Ignore (intentional difference)                              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ DISCREPANCY 2:                                                  │
│ Doc says: "REST API only"                                       │
│ Reality:  GraphQL endpoint also found                           │
│                                                                 │
│ What should I do?                                               │
│ ○ Update ARCHITECTURE.md (doc is outdated)                     │
│ ○ Flag as tech debt (GraphQL should be removed)                │
│ ○ Ignore (intentional, don't document)                         │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
└─────────────────────────────────────────────────────────────────┘
                              │
                        User resolves each
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECKPOINT 3: PREVIEW & CONFIRM CHANGES                         │
│                                                                 │
│ Based on your input, I will make these changes:                 │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ARCHITECTURE.md                                             │ │
│ │                                                             │ │
│ │ @@ -15,7 +15,9 @@                                          │ │
│ │  ## Backend Services                                       │ │
│ │ -The backend consists of 3 services:                       │ │
│ │ +The backend consists of 5 services:                       │ │
│ │  - batch_client: Iterable API integration                  │ │
│ │  - extraction_service: Core extraction logic               │ │
│ │ +- workflow_scheduler: FSM and retry logic                 │ │
│ │ +- gcs_upload_service: GCS integration                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Apply these changes?                                            │
│ ○ Yes, apply all changes                                       │
│ ○ Let me review each change individually                       │
│ ○ No, cancel (just output the report)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                        User confirms
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ APPLY CHANGES (only after explicit confirmation)                │
└─────────────────────────────────────────────────────────────────┘
```

### 11.6 Mode Flags

```
/analyze risk                    # Default: interactive
/analyze risk --batch            # Skip questions, use defaults
/analyze risk --interactive      # Explicit interactive (same as default)

/analyze architecture            # Default: interactive (REQUIRED)
/analyze architecture --dry-run  # Show discrepancies, don't offer to fix
/analyze architecture --batch    # ERROR: Cannot modify files without confirmation
```

**Key Rule**: Any mode that **modifies files** MUST be interactive. No `--batch` for destructive operations.

### 11.7 Benefits of Interactive Design

| Aspect | Batch Mode | Interactive Mode |
|--------|------------|------------------|
| Context | Generic assumptions | User-provided context |
| Relevance | May flag irrelevant issues | Focused on what matters |
| Accuracy | May misinterpret intent | Clarifies before acting |
| Trust | "AI decided this" | "AI asked, I confirmed" |
| File safety | Risk of wrong edits | Changes previewed & confirmed |
| Learning | One-shot analysis | Dialogue improves understanding |

---

## 12. Artifact-Driven Architecture

### 12.1 The Problem: Repeated Discovery

Without shared artifacts, each mode rediscovers the system independently:
- Wasteful (repeated work)
- Inconsistent (different discoveries)
- No institutional memory

### 12.2 Solution: System Map as Shared Artifact

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARTIFACT FLOW                                │
└─────────────────────────────────────────────────────────────────┘

     /analyze discover
            │
            ▼
    ┌───────────────────┐
    │   SYSTEM MAP      │  ← Persisted artifact
    │   (system-map.md) │    docs/analysis/system-map.md
    └───────────────────┘
            │
    ┌───────┴───────┬───────────────┬───────────────┐
    │               │               │               │
    ▼               ▼               ▼               ▼
/analyze       /analyze       /analyze       /analyze
component      risk           architecture   patterns
    │               │               │               │
    │ Reads         │ Reads         │ Reads         │ Reads
    │ system map    │ system map    │ system map    │ system map
    ▼               ▼               ▼               ▼
Component      Risk            Architecture   Pattern
Report         Report          Report         Report
    │               │               │               │
    └───────────────┴───────┬───────┴───────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   ANALYSIS HISTORY      │  ← Accumulated Knowledge
              │   docs/analysis/*.md    │    (institutional memory)
              └─────────────────────────┘
```

### 12.3 System Map Structure

**Location**: `docs/analysis/system-map.md`

```markdown
# System Map: {Project Name}

**Generated**: 2026-01-23 07:00 UTC
**Generator**: /analyze discover
**Project Type**: Python/FastAPI

---

## Components Discovered

### Services (backend/app/services/)

| ID | Name | Path | LOC | Imports | Description |
|----|------|------|-----|---------|-------------|
| svc-1 | batch_client | iterable/batch_client.py | 1,200 | 45 | Iterable API |
| svc-2 | extraction_service | iterable/extraction_service.py | 2,500 | 38 | Core extraction |
| svc-3 | workflow_scheduler | workflow_scheduler.py | 1,800 | 52 | FSM and retries |

### API Layer (backend/app/api/)

| ID | Name | Path | Endpoints |
|----|------|------|-----------|
| api-1 | extractions | extractions.py | 8 |
| api-2 | workflows | workflows.py | 12 |

### Models (backend/app/models/)

| ID | Name | Path | Fields |
|----|------|------|--------|
| mdl-1 | Extraction | extraction.py | 15 |
| mdl-2 | Workflow | workflow.py | 20 |

---

## Dependency Graph

```
svc-2 (extraction_service) ──depends──> svc-1 (batch_client)
svc-3 (workflow_scheduler) ──depends──> svc-2 (extraction_service)
api-1 (extractions) ──calls──> svc-2 (extraction_service)
```

---

## Pre-Identified Risk Hotspots

- **svc-1**: High coupling (imported by 5 modules)
- **svc-3**: High complexity (1,800 LOC, 52 imports)

---

## Documentation Status

| Doc | Exists | Last Updated | Sync Status |
|-----|--------|--------------|-------------|
| ARCHITECTURE.md | Yes | 2026-01-20 | Outdated (3 discrepancies) |
| README.md | Yes | 2026-01-15 | Unknown |
| API docs | No | - | Missing |
```

### 12.4 Refresh Strategy

```
/analyze discover                    # Create or refresh system map
/analyze discover --if-stale         # Refresh only if >24h old
/analyze component                   # Auto-create map if missing, else use cached
/analyze component --refresh         # Refresh map first, then analyze
```

### 12.5 Benefits of Artifact Sharing

| Without Artifacts | With Artifacts |
|-------------------|----------------|
| Each mode rediscovers | Discover once, use everywhere |
| Inconsistent component lists | Single source of truth |
| No history | Analysis history persisted |
| Session-bound knowledge | Cross-session memory |
| Can't track changes over time | Can diff system maps |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-23 06:15 | Initial research document |
| 2026-01-23 06:45 | Major update: Discovery-based scoping for portability |
| 2026-01-23 07:15 | Major update: Interactive design patterns and artifact sharing |

### Key Changes in 07:15 Update:
- Section 11: Added Interactive Design Patterns
  - 11.1: Problem with batch-only skills
  - 11.2: Interactive skill architecture diagram
  - 11.3: Checkpoint definitions by mode
  - 11.4: Risk mode interactive example
  - 11.5: Architecture mode discrepancy resolution
  - 11.6: Mode flags (--batch, --interactive, --dry-run)
  - 11.7: Benefits comparison table
- Section 12: Added Artifact-Driven Architecture
  - 12.1: Problem of repeated discovery
  - 12.2: System Map as shared artifact
  - 12.3: System Map structure/template
  - 12.4: Refresh strategy
  - 12.5: Benefits of artifact sharing
