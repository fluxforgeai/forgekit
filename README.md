# ForgeKit

**AI Engineering Skills Toolkit by FluxForge AI**

ForgeKit is a closed-source, cross-platform AI engineering skills toolkit that provides domain-specific incident response, systems analysis, and architectural design capabilities to AI coding assistants.

## Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| **incident** | `/incident {desc}` | Document what happened (factual incident record) |
| **investigate** | `/investigate {report}` | Deep investigation into why it happened |
| **rca-bugfix** | `/rca-bugfix {issue}` | Root cause analysis + fix prompt generation |
| **watchdog** | `/watchdog {desc}` | Autonomous background log monitoring |
| **analyze** | `/analyze {mode} [scope]` | Strategic system analysis (health, risk, patterns, component, architecture) |
| **design** | `/design {mode} {topic}` | Research-driven architectural design analysis |
| **research** | `/research {question}` | Topic research with documented findings |

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
