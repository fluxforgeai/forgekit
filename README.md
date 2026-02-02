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

Each downstream skill automatically updates the [Findings Tracker](#the-findings-tracker) with its stage transition:

```
Fix route:    /finding → /investigate → /rca-bugfix → /plan → implement → verify
               Open    Investigating  RCA Complete  Planned  Resolved   Verified

Design route: /finding → /design   → /blueprint     → /plan → implement → verify
               Open     Designing  Blueprint Ready  Planned  Resolved   Verified
```

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

**Step 4** — Investigate. You can invoke the next skill two ways:

```
# Option A: Pass the artifact path (explicit — the skill reads it directly)
/investigate docs/findings/2026-02-10_0800_state_desynchronization.md

# Option B: Reference the finding number (tracker-aware — the skill looks up F1 in the tracker)
/investigate F1
```

Both work. Option A is explicit: the skill reads the file you point it to. Option B uses the lifecycle tracking protocol: the skill searches `docs/findings/*_FINDINGS_TRACKER.md` for F1, finds the linked finding report and any prior artifacts, and uses all of them as context.

The investigation produces a report in `docs/investigations/`. The tracker is automatically updated: F1 Stage → `Investigating`.

**Step 5** — Fix it. Same pattern — pass the investigation report or reference the finding:

```
# Option A: Pass the investigation report
/rca-bugfix docs/investigations/2026-02-10_0830_state_desynchronization.md

# Option B: Reference the finding (skill finds the tracker, finding report, AND investigation)
/rca-bugfix F1
```

The RCA skill reads upstream artifacts in order: investigations first, then findings. When you pass `F1`, it resolves the full chain — tracker → finding report → investigation — and uses all of them as context for the root cause analysis.

**Step 6** — Plan and implement:
Enter `/plan` mode with the generated prompt. The tracker is updated at each step: `RCA Complete` → `Planned` → `Resolved` → `Verified`.

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
| # | Finding                    | Type   | Severity     | Status | Stage |
|---|----------------------------|--------|--------------|--------|-------|
| F1 | State desynchronization   | Defect | **Critical** | Open   | Open  |
| F3 | Download stall blind spot | Gap    | **High**     | Open   | Open  |
| F2 | No external termination   | Gap    | **High**     | Open   | Open  |
| F4 | Serial queue blocking     | Gap    | **Medium**   | Open   | Open  |
```

Over the next few sessions, you work through the findings. Every downstream skill automatically updates the tracker as it processes a finding. You invoke each skill with the F-number — the skill resolves the full artifact chain (tracker → finding report → investigation → RCA) from that single identifier:

```
Session 1: /finding discovers F1, F2, F3, F4 → tracker created (all Stage: Open)

Session 2: /investigate F1
             → tracker: F1 Stage → Investigating, lifecycle row added
           /rca-bugfix F1
             → tracker: F1 Stage → RCA Complete, lifecycle row added

Session 3: /plan (with F1 prompt)
             → tracker: F1 Stage → Planned, lifecycle row added
           Implement fix
             → tracker: F1 Stage → Resolved

Session 4: Verify fix in production
             → tracker: F1 Stage → Verified ✓
```

Each `/session-end` reconciles the tracker with reality — if an artifact exists but the tracker wasn't updated (e.g., the skill ran before lifecycle tracking was added), session-end backfills the missing stages. Each `/verify-session` confirms everything is consistent.

---

## Skills Reference

### Reactive Skills

| Skill | Command | What It Does | Tracker-Aware |
|-------|---------|-------------|:---:|
| **watchdog** | `/watchdog {description}` | Monitors application logs in the background. When it spots trouble, it creates a structured JSON incident and (optionally) sends a Telegram alert. Think of it as a tireless intern watching your logs. | — |
| **incident** | `/incident {description}` | Documents what happened — factual, neutral, timestamped. Can read watchdog JSON for automatic incident creation. Writes to `docs/incidents/`. | — |
| **investigate** | `/investigate {report}` | Deep investigation into an incident or finding. Reads past incidents, RCAs, and findings to identify patterns. Produces hypotheses backed by evidence. Writes to `docs/investigations/`. | ✓ → `Investigating` |
| **rca-bugfix** | `/rca-bugfix {issue}` | Root cause analysis and fix generation. Reads investigations and incidents, identifies the root cause chain, and produces both an RCA document and a ready-to-use fix prompt. Writes to `docs/RCAs/` and `docs/prompts/`. | ✓ → `RCA Complete` |

### Proactive Skills

| Skill | Command | What It Does | Tracker-Aware |
|-------|---------|-------------|:---:|
| **research** | `/research {question}` | Researches a topic using web search, documentation, and codebase analysis. Produces a structured research document with findings, comparisons, and recommendations. Writes to `docs/research/`. | — |
| **design** | `/design {mode} {topic}` | Architectural design analysis. Modes: `tradeoff` (compare approaches), `migrate` (plan a migration), `from-scratch` (design a new system). Writes to `docs/design/`. | ✓ → `Designing` |
| **blueprint** | `/blueprint {feature}` | Transforms research and design documents into a concrete implementation spec — files to create, APIs to define, tests to write. Generates a prompt for plan mode. Writes to `docs/blueprints/` and `docs/prompts/`. | ✓ → `Blueprint Ready` |

### Strategic Skills

| Skill | Command | What It Does | Tracker-Aware |
|-------|---------|-------------|:---:|
| **analyze** | `/analyze {mode} [scope]` | System-level analysis. Modes include `health`, `risk`, `patterns`, `component`, and more. Reads the entire operational history and codebase to produce assessments. Routes discoveries to the appropriate pipeline. Writes to `docs/analysis/`. | — |
| **finding** | `/finding {description}` | Logs a proactive discovery — something found through analysis, review, or inspection. Classifies it by type and severity, writes a finding report, and auto-creates or updates a [Findings Tracker](#the-findings-tracker). Writes to `docs/findings/`. | ✓ Creates tracker |

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

### Lifecycle Tracking

Every finding is tracked from discovery through resolution. The tracker maintains two levels of granularity:

- **Status** (coarse, 4 values): `Open` → `In Progress` → `Resolved` → `Verified`
- **Stage** (fine-grained, 7 values): tracks exactly where in the pipeline a finding sits

There are two stage progressions depending on the finding type:

**Corrective Route** (Defect / Vulnerability — something's broken):
```
Open → Investigating → RCA Complete → Planned → Implementing → Resolved → Verified
         /investigate    /rca-bugfix    /plan      (code work)   session-end  session-end
```

**Design Route** (Debt / Gap / Drift — something needs designing):
```
Open → Designing → Blueprint Ready → Planned → Implementing → Resolved → Verified
        /design      /blueprint       /plan      (code work)   session-end  session-end
```

Every downstream skill that processes a finding **automatically updates the tracker** — setting the Stage, appending a lifecycle row, checking the resolution task, and adding a changelog entry. You don't need to update the tracker manually.

Each finding's detail section includes a **Lifecycle table** that grows as the finding progresses:

```
| Stage          | Timestamp             | Session | Artifact                              |
|----------------|-----------------------|---------|---------------------------------------|
| Open           | 2026-02-02 16:00 UTC  | 119     | [Finding Report](docs/findings/...)   |
| Investigating  | 2026-02-03 09:00 UTC  | 120     | [Investigation](docs/investigations/) |
| RCA Complete   | 2026-02-03 11:00 UTC  | 120     | [RCA](docs/RCAs/) + [Prompt](docs/prompts/) |
| Planned        | 2026-02-03 14:00 UTC  | 120     | [Plan](docs/plans/...)                |
| Resolved       | 2026-02-04 10:00 UTC  | 121     | Commit abc123                         |
| Verified       | 2026-02-04 15:00 UTC  | 121     | Production validation                 |
```

### Cross-Session Persistence

The tracker integrates with ForgeKit's session management:

- **`/session-end`** checks all active trackers and updates any that had work done during the session — checking off completed tasks, updating statuses and stages, backfilling any missed lifecycle rows, and adding changelog entries.
- **`/verify-session`** reports on all active trackers — showing finding statuses and stages, verifying stage consistency against existing artifacts, and flagging any lifecycle gaps.

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
| `docs/findings/*_FINDINGS_TRACKER.md` | `/finding` | `/investigate`, `/rca-bugfix`, `/design`, `/blueprint`, `/session-end`, `/verify-session` |
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
