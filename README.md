# ForgeKit

**AI Engineering Skills Toolkit by FluxForge AI**

ForgeKit gives your AI coding assistant a structured engineering process. Instead of ad-hoc debugging and scattered notes, every incident, investigation, finding, and design decision follows a repeatable workflow — and produces documentation that builds your project's institutional memory over time.

Think of it as an engineering runbook that your AI assistant actually follows.

---

## Quick Start

```bash
# Clone the repo
git clone git@github.com:fluxforgeai/forgekit.git ~/Projects/fluxforgeai/forgekit

# Install CLI globally
cd ~/Projects/fluxforgeai/forgekit
uv tool install -e .

# Initialize in any project
cd ~/your-project
forgekit init
```

That's it. Your AI assistant now has access to all ForgeKit skills via slash commands. Try `/analyze health` to get a health assessment of your codebase, or `/incident API returning 500 errors` when something breaks.

---

## How ForgeKit Thinks

ForgeKit organizes engineering work into three pipelines. Each one starts with a trigger ("something happened" or "I want to build something") and ends with a documented plan ready for implementation.

You don't need to memorize the pipelines. Each skill tells you what to run next. But understanding the flow helps you get the most out of the toolkit.

### The Reactive Pipeline — "Something broke"

When production goes sideways, the reactive pipeline walks you through a structured response:

```
/watchdog  -->  /incident  -->  /investigate  -->  /rca-bugfix  -->  /plan
  (detect)      (document)       (dig in)         (fix + learn)     (implement)
```

Each step reads the output of the previous step and builds on it. By the end, you have a documented incident, a root cause analysis, and a fix prompt ready for implementation. Three months from now, when someone asks "what happened to the API that night?", the answer is in `docs/incidents/`.

### The Proactive Pipeline — "Building something new"

When you're adding a feature, migrating a system, or making an architectural change:

```
/research  -->  /design  -->  /blueprint  -->  /plan
  (learn)       (decide)      (spec it)       (implement)
```

Research gathers context. Design evaluates trade-offs (should you use WebSockets or SSE? Redis or Memcached?). Blueprint turns the chosen design into an implementation spec. Plan mode turns it into code.

### The Audit Pipeline — "Found something that needs attention"

Sometimes you discover issues proactively — through code review, analysis, or just reading logs carefully. The audit pipeline handles these:

```
/analyze  -->  /finding  -->  (routes to Fix or Design branch)
```

The `/finding` skill classifies what you found and tells you where to go next:

- **Defect or Vulnerability?** Route to Fix: `/investigate` then `/rca-bugfix`
- **Technical debt, gap, or drift?** Route to Design: `/design` then `/blueprint`

This is where the [Findings Tracker](#the-findings-tracker) comes in — more on that below.

---

## Real-World Scenarios

### Scenario 1: Your API starts throwing errors at 2am

You wake up to alerts. Something's wrong with the payment service.

**Step 1** — Document what you see:
```
/incident Payment API returning 500 errors since 02:15 UTC, affecting checkout flow
```
ForgeKit creates `docs/incidents/2026-02-10_0230_payment_api_500_errors.md` with a structured incident report. No guessing the format — it's standardized.

**Step 2** — Dig into the cause:
```
/investigate docs/incidents/2026-02-10_0230_payment_api_500_errors.md
```
The investigation skill reads your incident report, examines the codebase, checks related past incidents, and produces a detailed investigation with hypotheses and evidence.

**Step 3** — Fix it:
```
/rca-bugfix Connection pool exhaustion causing payment API timeouts
```
Root cause analysis plus a fix prompt. The RCA goes into `docs/RCAs/` (your project's permanent knowledge base), and a ready-to-implement prompt goes into `docs/prompts/`.

**Step 4** — Implement:
Enter `/plan` mode with the generated prompt. Code the fix with full context.

**What you end up with**: An incident record, investigation, RCA, and fix — all linked, all searchable, all available for the next engineer (or AI session) that encounters a similar problem.

### Scenario 2: Adding WebSocket support to your application

You need real-time updates. Time to evaluate your options.

**Step 1** — Research the landscape:
```
/research WebSocket vs SSE vs long-polling for real-time order status updates
```
ForgeKit produces a research document covering each approach, with trade-offs specific to your codebase.

**Step 2** — Make the architectural decision:
```
/design tradeoff real-time communication for order status
```
The design skill reads your research, evaluates each option against your project's constraints, and produces a recommendation with clear rationale.

**Step 3** — Spec the implementation:
```
/blueprint WebSocket integration for order status updates
```
Turns the chosen design into a concrete implementation spec: which files to create, which APIs to define, which tests to write. Also generates a prompt for plan mode.

**Step 4** — Build it:
Enter `/plan` mode. The blueprint gives your AI assistant everything it needs to implement the feature correctly.

### Scenario 3: Your analysis reveals a hidden problem

You run a system health check and something looks off.

**Step 1** — Analyze the system:
```
/analyze health
```
The analysis runs across your codebase and operational history, scoring reliability, performance, maintainability, and observability.

**Step 2** — The analysis flags a concern. Log it as a finding:
```
/finding Stale detection reads DB but extraction writes to filesystem — state desynchronization
```
ForgeKit classifies it (Defect, High severity), writes a finding report, and **automatically creates a Findings Tracker** to track resolution across sessions.

**Step 3** — The finding skill tells you what to do next:
```
This is a corrective fix candidate. Recommended next steps:
1. /investigate stale detection state desynchronization
2. /rca-bugfix stale detection state desynchronization
```

You follow the recommended path. The Findings Tracker tracks your progress.

### Scenario 4: Multiple findings from a single analysis

Your `/analyze` run on the extraction pipeline reveals four related issues — a critical defect, two high-severity gaps, and a medium-severity architectural concern.

```
/finding docs/analysis/2026-02-02_1530_extraction_systems_analysis.md
```

ForgeKit processes the analysis and produces:
- 4 individual finding reports in `docs/findings/`
- 1 named Findings Tracker: `docs/findings/2026-02-02_1600_extraction_pipeline_FINDINGS_TRACKER.md`

The tracker lists all four findings sorted by severity, with auto-generated resolution tasks for each one:

```
| # | Finding                    | Type   | Severity     | Status |
|---|----------------------------|--------|--------------|--------|
| F1 | State desynchronization   | Defect | **Critical** | Open   |
| F3 | Download stall blind spot | Gap    | **High**     | Open   |
| F2 | No external termination   | Gap    | **High**     | Open   |
| F4 | Serial queue blocking     | Gap    | **Medium**   | Open   |
```

Over the next few sessions, you work through the findings. Each `/session-end` updates the tracker. Each `/verify-session` confirms your progress was recorded. The tracker persists until all findings are resolved.

---

## Skills Reference

### Reactive Skills

| Skill | Command | What It Does |
|-------|---------|-------------|
| **watchdog** | `/watchdog {description}` | Monitors application logs in the background. When it spots trouble, it creates a structured JSON incident and (optionally) sends a Telegram alert. Think of it as a tireless intern watching your logs. |
| **incident** | `/incident {description}` | Documents what happened — factual, neutral, timestamped. Can read watchdog JSON for automatic incident creation. Writes to `docs/incidents/`. |
| **investigate** | `/investigate {report}` | Deep investigation into an incident or finding. Reads past incidents, RCAs, and findings to identify patterns. Produces hypotheses backed by evidence. Writes to `docs/investigations/`. |
| **rca-bugfix** | `/rca-bugfix {issue}` | Root cause analysis and fix generation. Reads investigations and incidents, identifies the root cause chain, and produces both an RCA document and a ready-to-use fix prompt. Writes to `docs/RCAs/` and `docs/prompts/`. |

### Proactive Skills

| Skill | Command | What It Does |
|-------|---------|-------------|
| **research** | `/research {question}` | Researches a topic using web search, documentation, and codebase analysis. Produces a structured research document with findings, comparisons, and recommendations. Writes to `docs/research/`. |
| **design** | `/design {mode} {topic}` | Architectural design analysis. Modes: `tradeoff` (compare approaches), `migrate` (plan a migration), `from-scratch` (design a new system). Writes to `docs/design/`. |
| **blueprint** | `/blueprint {feature}` | Transforms research and design documents into a concrete implementation spec — files to create, APIs to define, tests to write. Generates a prompt for plan mode. Writes to `docs/blueprints/` and `docs/prompts/`. |

### Strategic Skills

| Skill | Command | What It Does |
|-------|---------|-------------|
| **analyze** | `/analyze {mode} [scope]` | System-level analysis. Modes include `health`, `risk`, `patterns`, `component`, and more. Reads the entire operational history and codebase to produce assessments. Routes discoveries to the appropriate pipeline. Writes to `docs/analysis/`. |
| **finding** | `/finding {description}` | Logs a proactive discovery — something found through analysis, review, or inspection. Classifies it by type and severity, writes a finding report, and auto-creates or updates a [Findings Tracker](#the-findings-tracker). Writes to `docs/findings/`. |

---

## The Findings Tracker

When you log findings with `/finding`, ForgeKit automatically creates a **Findings Tracker** — a living document that tracks resolution progress across sessions.

### How It Works

1. You run `/finding` (directly, or as part of `/analyze`)
2. ForgeKit writes individual finding reports to `docs/findings/`
3. ForgeKit creates (or updates) a named tracker: `docs/findings/{datetime}_{name}_FINDINGS_TRACKER.md`

Each tracker is scoped to a **group of related findings**. If you analyze your authentication system and find three issues, those go into one tracker. If you later analyze your payment system and find two more, those get their own separate tracker. Multiple trackers coexist — one per problem domain.

### What's Inside a Tracker

- **Overview table** — All findings sorted by severity (Critical first), with status
- **Dependency map** — How findings relate to each other
- **Per-finding sections** — Summary, root cause, resolution tasks (auto-generated), status tracking
- **Changelog** — Every update logged with session number and date

### Resolution Tasks

ForgeKit auto-generates resolution tasks based on the finding type:

**For defects and vulnerabilities** (something's broken):
```
- [ ] F1.1: Confirm root cause and scope
- [ ] F1.2: Implement corrective fix
- [ ] F1.3: Verify fix
```

**For debt, gaps, and drift** (something needs designing):
```
- [ ] F1.1: Design approach (evaluate options)
- [ ] F1.2: Implement chosen approach
- [ ] F1.3: Verify implementation
```

When your finding reports contain specific code locations and root causes, the tasks are customized with those details.

### Cross-Session Persistence

The tracker integrates with ForgeKit's session management:

- **`/session-end`** checks all active trackers and updates any that had work done during the session — checking off completed tasks, updating statuses, adding changelog entries.
- **`/verify-session`** reports on all active trackers — showing finding statuses, completed vs remaining tasks, and whether the tracker was properly updated.

Status progression: `Open` --> `In Progress` --> `Resolved` --> `Verified`

### Naming Convention

Trackers are named by their scope:
```
docs/findings/2026-02-02_1639_iterable_extraction_pipeline_FINDINGS_TRACKER.md
docs/findings/2026-03-15_0900_auth_authorization_gaps_FINDINGS_TRACKER.md
docs/findings/2026-04-01_1400_api_rate_limiting_FINDINGS_TRACKER.md
```

---

## Session Management

ForgeKit includes three session commands that maintain continuity between AI coding sessions.

### `/session-start`

Reads your project's `CLAUDE.md` and the latest session handoff document. Orients the AI assistant with full project context, recent work, and current priorities. No more "where were we?" at the start of each session.

### `/session-end`

Creates all handoff documentation for the next session:

1. Saves any active plan files
2. Creates a new `NEXT_SESSION_PROMPT_{datetime}.md` with current status and priorities
3. Creates a `SESSION_SUMMARY_{datetime}.md` documenting what was accomplished
4. Updates `CLAUDE.md` to point to the new handoff
5. Archives old handoff documents
6. Updates any Findings Trackers that had work done during the session

### `/verify-session`

Runs a health check on your session management:

- Is `CLAUDE.md` pointing to the right handoff file?
- Does that file exist?
- Are old handoffs archived?
- Are Findings Trackers up to date?
- Are key project documents in sync?

Run this after `/session-end` to make sure nothing was missed.

---

## Finding Classification

The `/finding` skill classifies discoveries to determine the resolution path:

| Type | What It Means | Where It Goes |
|------|--------------|---------------|
| **Defect** | Code that doesn't work as intended | Fix Branch: `/investigate` then `/rca-bugfix` |
| **Vulnerability** | Security weakness with known exposure | Fix Branch: `/investigate` then `/rca-bugfix` |
| **Debt** | Technical debt that hurts maintainability | Design Branch: `/design` then `/blueprint` |
| **Gap** | A capability that should exist but doesn't | Design Branch: `/design` then `/blueprint` |
| **Drift** | Something diverged from its intended state | Either branch, depending on scope |

Severity levels: **Critical** > **High** > **Medium** > **Low**

---

## CLI Reference

```bash
forgekit init              # Symlink skills and commands into current project
forgekit update            # Pull latest skills from GitHub
forgekit status            # Show version, repo status, and symlink health
forgekit diff              # Show uncommitted changes made through symlinks
forgekit commit -m "msg"   # Commit changes back to forgekit repo
forgekit push              # Push to GitHub
forgekit uninstall         # Remove symlinks from current project
```

### Keeping Skills Updated

When ForgeKit publishes new skills or updates existing ones:

```bash
forgekit update    # Pulls latest changes
```

Because ForgeKit uses symlinks, the update is instant — your projects immediately see the new skill versions. No reinstall, no copy-paste.

### Contributing Changes Back

If you improve a skill while working in a project, the change flows through the symlink back to the ForgeKit repo:

```bash
forgekit diff               # See what changed
forgekit commit -m "Improve /finding skill with batch support"
forgekit push               # Share with the team
```

Every project using ForgeKit immediately picks up the change.

---

## Under the Hood

ForgeKit installs via symlinks. When you run `forgekit init`, it creates:

```
your-project/.claude/
├── settings.json          <- Your project's config (untouched)
├── skills/                <- Symlink -> forgekit/skills/
│   ├── analyze/
│   ├── blueprint/
│   ├── design/
│   ├── finding/
│   ├── incident/
│   ├── investigate/
│   ├── rca-bugfix/
│   ├── research/
│   └── watchdog/
└── commands/              <- Symlink -> forgekit/commands/
    ├── session-start.md
    ├── session-end.md
    └── verify-session.md
```

Skills live in the ForgeKit repo. Projects reference them through symlinks. Edit a skill in any project, and the change is reflected everywhere — no synchronization needed.

### Institutional Memory

Every skill writes to `docs/`. Over time, your project accumulates:

```
docs/
├── incidents/        # What broke and when
├── findings/         # What was discovered proactively (+ Findings Trackers)
├── investigations/   # Deep dives into problems
├── RCAs/             # Root cause analyses
├── research/         # Technology evaluations
├── design/           # Architectural decisions
├── blueprints/       # Implementation specs
├── analysis/         # System health assessments
├── prompts/          # Ready-to-use implementation prompts
├── plans/            # Implementation plans
└── archive/
    └── sessions/     # Past session handoffs
```

This is your project's engineering logbook. Each document is written by one skill and read by downstream skills, creating a feedback loop. The more you use ForgeKit, the better it understands your project's history and patterns.

### Pipeline Data Flow

Skills communicate through shared documents, not APIs. Here's what each skill reads and writes:

| Artifact | Written By | Read By |
|----------|-----------|---------|
| `docs/incidents/*.md` | `/incident` | `/investigate`, `/analyze` |
| `docs/findings/*.md` | `/finding` | `/investigate`, `/analyze`, `/rca-bugfix`, `/research` |
| `docs/findings/*_FINDINGS_TRACKER.md` | `/finding` | `/session-end`, `/verify-session` |
| `docs/investigations/*.md` | `/investigate` | `/rca-bugfix`, `/analyze` |
| `docs/RCAs/*.md` | `/rca-bugfix` | `/investigate`, `/analyze` |
| `docs/research/*.md` | `/research` | `/investigate`, `/design`, `/blueprint` |
| `docs/analysis/*.md` | `/analyze` | `/design`, `/investigate`, `/finding` |
| `docs/design/*.md` | `/design` | `/blueprint` |
| `docs/blueprints/*.md` | `/blueprint` | `/plan` mode |
| `docs/prompts/*.md` | `/rca-bugfix`, `/blueprint` | `/plan` mode |
| `system-map.md` | `/analyze` | `/analyze` (refreshed each run) |

---

## Project Conventions

See [CONVENTIONS.md](CONVENTIONS.md) for the full directory structure and file naming conventions that ForgeKit skills expect.

---

## License

Proprietary — FluxForge AI. All rights reserved.
