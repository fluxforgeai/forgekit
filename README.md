# ForgeKit

**AI Engineering Skills Toolkit by FluxForge AI**

ForgeKit is a closed-source, cross-platform AI engineering skills toolkit that provides domain-specific incident response, systems analysis, and architectural design capabilities to AI coding assistants.

## Skills

| Skill | Command | Pipeline | Purpose |
|-------|---------|----------|---------|
| **incident** | `/incident {desc}` | Reactive | Document what happened (factual incident record) |
| **investigate** | `/investigate {report}` | Reactive | Deep investigation into why it happened |
| **rca-bugfix** | `/rca-bugfix {issue}` | Reactive | Root cause analysis + fix prompt generation |
| **watchdog** | `/watchdog {desc}` | Reactive | Autonomous background log monitoring |
| **analyze** | `/analyze {mode} [scope]` | Either | Strategic system analysis (health, risk, patterns, component, architecture) |
| **design** | `/design {mode} {topic}` | Either | Research-driven architectural design analysis |
| **research** | `/research {question}` | Proactive | Topic research with documented findings |
| **blueprint** | `/blueprint {feature}` | Proactive | Transform design/research into implementation spec + prompt |

## Pipelines

ForgeKit skills are organized into two pipelines that converge at `/plan` mode:

### Reactive Pipeline (Something broke)

```
/watchdog → /incident → /investigate → /rca-bugfix → /plan
```

| Step | Skill | Artifact |
|------|-------|----------|
| 1 | `/watchdog` | Telegram alert (auto-detected issue) |
| 2 | `/incident` | `docs/incidents/*.md` |
| 3 | `/investigate` | `docs/investigations/*.md` |
| 4 | `/rca-bugfix` | `docs/RCAs/*.md` + `docs/prompts/*.md` |
| 5 | `/plan` | `docs/plans/*.md` (implementation plan) |

### Proactive Pipeline (Building something new)

```
/research → /design → /blueprint → /plan
```

| Step | Skill | Artifact |
|------|-------|----------|
| 1 | `/research` | `docs/research/*.md` |
| 2 | `/design` | `docs/design/*.md` |
| 3 | `/blueprint` | `docs/blueprints/*.md` + `docs/prompts/*.md` |
| 4 | `/plan` | `docs/plans/*.md` (implementation plan) |

### Convergence Points

Both pipelines produce a `docs/prompts/*.md` file that feeds into `/plan` mode. The reactive pipeline generates a fix prompt (from `/rca-bugfix`), while the proactive pipeline generates a feature prompt (from `/blueprint`).

`/analyze` is a strategic skill that feeds into either pipeline — its findings can trigger `/design` (proactive) or `/investigate` (reactive) depending on what's discovered.

### When to Use Which Pipeline

| Situation | Pipeline | Start With |
|-----------|----------|------------|
| Production incident or bug | Reactive | `/incident` or `/watchdog` |
| New feature or migration | Proactive | `/research` |
| Performance investigation | Reactive | `/investigate` |
| Architecture change | Proactive | `/research` or `/design` |
| Unknown system state | Either | `/analyze` |

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
├── settings.json          ← Your project (unchanged)
├── skills/                ← Symlink → forgekit/skills/
│   ├── blueprint/
│   ├── incident/
│   ├── investigate/
│   ├── rca-bugfix/
│   ├── watchdog/
│   ├── analyze/
│   ├── design/
│   └── research/
└── commands/              ← Symlink → forgekit/commands/
    ├── session-start.md
    ├── session-end.md
    └── verify-session.md
```

Edits to skills in any project flow through the symlink to the forgekit repo. Use `forgekit commit` and `forgekit push` to save changes.

## Project Conventions

See [CONVENTIONS.md](CONVENTIONS.md) for the expected directory structure that ForgeKit skills use.

## License

Proprietary - FluxForge AI. All rights reserved.
