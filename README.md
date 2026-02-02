# ForgeKit

**AI Engineering Skills Toolkit by FluxForge AI**

ForgeKit is a closed-source, cross-platform AI engineering skills toolkit that provides domain-specific incident response, systems analysis, and architectural design capabilities to AI coding assistants.

## Skills

| Skill | Command | Pipeline | Purpose |
|-------|---------|----------|---------|
| **incident** | `/incident {desc}` | Reactive | Document what happened (factual incident record) |
| **investigate** | `/investigate {report}` | Reactive / Audit | Deep investigation into why it happened |
| **rca-bugfix** | `/rca-bugfix {issue}` | Reactive / Audit | Root cause analysis + fix prompt generation |
| **watchdog** | `/watchdog {desc}` | Reactive | Autonomous background log monitoring |
| **analyze** | `/analyze {mode} [scope]` | Strategic | System analysis -- routes findings to any pipeline |
| **finding** | `/finding {description}` | Audit | Log proactive discoveries (the proactive equivalent of `/incident`) |
| **design** | `/design {mode} {topic}` | Proactive / Audit | Research-driven architectural design analysis |
| **research** | `/research {question}` | Proactive | Topic research with documented findings |
| **blueprint** | `/blueprint {feature}` | Proactive / Audit | Transform design/research into implementation spec + prompt |

## Pipelines

ForgeKit skills are organized into three pipelines that converge at `/plan` mode. Each pipeline produces documentation artifacts that feed back into future skill invocations -- building institutional memory.

### Reactive Pipeline (Something broke)

```
/watchdog --> /incident --> /investigate --> /rca-bugfix --> /plan
```

| Step | Skill | Reads | Writes |
|------|-------|-------|--------|
| 0 | `/watchdog` | application logs (live) | `/tmp/watchdog_*_incidents/*.json` + Telegram alert |
| 1 | `/incident` | watchdog JSON (optional), user description | `docs/incidents/{date}_{name}.md` |
| 2 | `/investigate` | `docs/incidents/` (step 1), `docs/RCAs/`, `docs/findings/` | `docs/investigations/{date}_{name}.md` |
| 3 | `/rca-bugfix` | `docs/investigations/` (step 2), `docs/incidents/` (step 1) | `docs/RCAs/{date}_{name}.md` + `docs/prompts/{date}_{name}.md` |
| 4 | `/plan` | `docs/prompts/` (step 3) | `docs/plans/{date}_{name}.md` |

### Proactive Pipeline (Building something new)

```
/research --> /design --> /blueprint --> /plan
```

| Step | Skill | Reads | Writes |
|------|-------|-------|--------|
| 1 | `/research` | `docs/research/`, `docs/RCAs/`, `docs/findings/` | `docs/research/{date}_{topic}.md` |
| 2 | `/design` | `docs/research/` (step 1), `docs/design/`, `docs/analysis/` | `docs/design/{date}_{topic}.md` |
| 3 | `/blueprint` | `docs/design/` (step 2), `docs/research/` (step 1) | `docs/blueprints/{date}_{feature}.md` + `docs/prompts/{date}_{feature}.md` |
| 4 | `/plan` | `docs/prompts/` (step 3) | `docs/plans/{date}_{feature}.md` |

### Audit Pipeline (Proactive finding needs action)

`/analyze` discovers an issue and routes it through `/finding` to the appropriate resolution path.

**Fix Branch** -- for Defect/Vulnerability findings (cause known, no design needed):

```
/analyze --> /finding --> /investigate --> /rca-bugfix --> /plan
```

| Step | Skill | Reads | Writes |
|------|-------|-------|--------|
| 0 | `/analyze` | `system-map.md`, codebase, `docs/findings/`, `docs/RCAs/` | `docs/analysis/{date}_{mode}.md` |
| 1 | `/finding` | `docs/analysis/` (step 0) | `docs/findings/{date}_{name}.md` |
| 2 | `/investigate` | `docs/findings/` (step 1), `docs/RCAs/`, `docs/investigations/` | `docs/investigations/{date}_{name}.md` |
| 3 | `/rca-bugfix` | `docs/findings/` (step 1), `docs/investigations/` (step 2) | `docs/RCAs/{date}_{name}.md` + `docs/prompts/{date}_{name}.md` |
| 4 | `/plan` | `docs/prompts/` (step 3) | `docs/plans/{date}_{name}.md` |

**Design Branch** -- for Debt/Gap/Drift findings (architectural decision needed):

```
/analyze --> /finding --> /design --> /blueprint --> /plan
```

| Step | Skill | Reads | Writes |
|------|-------|-------|--------|
| 0 | `/analyze` | `system-map.md`, codebase, `docs/findings/`, `docs/RCAs/` | `docs/analysis/{date}_{mode}.md` |
| 1 | `/finding` | `docs/analysis/` (step 0) | `docs/findings/{date}_{name}.md` |
| 2 | `/design` | `docs/findings/` (step 1), `docs/research/`, `docs/design/` | `docs/design/{date}_{topic}.md` |
| 3 | `/blueprint` | `docs/findings/` (step 1), `docs/design/` (step 2) | `docs/blueprints/{date}_{feature}.md` + `docs/prompts/{date}_{feature}.md` |
| 4 | `/plan` | `docs/prompts/` (step 3) | `docs/plans/{date}_{feature}.md` |

### Convergence Points

All three pipelines produce a `docs/prompts/*.md` file that feeds into `/plan` mode:

- **Reactive**: `/rca-bugfix` generates a fix prompt
- **Proactive**: `/blueprint` generates a feature prompt
- **Audit (Fix)**: `/rca-bugfix` generates a fix prompt (same as reactive)
- **Audit (Design)**: `/blueprint` generates a feature prompt (same as proactive)

`/analyze` is the strategic coordinator that routes findings to the right pipeline via escalation checkpoints.

### Finding Classification

The `/finding` skill classifies discoveries to determine which branch to take:

| Type | Definition | Resolution Branch |
|------|-----------|-------------------|
| **Defect** | Code that doesn't work as intended | Fix: `/investigate` -> `/rca-bugfix` |
| **Vulnerability** | Security weakness | Fix: `/investigate` -> `/rca-bugfix` |
| **Debt** | Maintainability / quality issue | Design: `/design` -> `/blueprint` |
| **Gap** | Missing expected capability | Design: `/design` -> `/blueprint` |
| **Drift** | Divergence from intended state | Either, depending on scope |

### When to Use Which Pipeline

| Situation | Pipeline | Start With |
|-----------|----------|------------|
| Production incident or bug | Reactive | `/incident` or `/watchdog` |
| New feature or migration | Proactive | `/research` |
| Performance investigation | Reactive | `/investigate` |
| Architecture change | Proactive | `/research` or `/design` |
| Known bug found by analysis | Audit (Fix) | `/analyze` -> `/finding` |
| Code quality issue found | Audit (Design) | `/analyze` -> `/finding` |
| Unknown system state | Any | `/analyze` |

## Session Management Commands

| Command | Purpose |
|---------|---------|
| `/session-start` | Initialize session with full project context |
| `/session-end` | Create handoff documentation for next session |
| `/verify-session` | Verify session handoff files are correct |

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

## CLI Commands

```bash
forgekit init        # Create .claude/skills and .claude/commands symlinks
forgekit update      # Pull latest from GitHub
forgekit status      # Show version, repo status, symlink status
forgekit diff        # Show uncommitted changes in skills/commands
forgekit commit -m "msg"  # Commit changes made through symlinks
forgekit push        # Push to GitHub
forgekit uninstall   # Remove symlinks from current project
```

## How It Works

ForgeKit installs via symlinks. When you run `forgekit init`, it creates:

```
your-project/.claude/
├── settings.json          <- Your project (unchanged)
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

Edits to skills in any project flow through the symlink to the forgekit repo. Use `forgekit commit` and `forgekit push` to save changes.

## Project Conventions

See [CONVENTIONS.md](CONVENTIONS.md) for the expected directory structure that ForgeKit skills use.

## License

Proprietary - FluxForge AI. All rights reserved.
