# ForgeKit - Architecture Document

**Version**: 0.1.0
**Author**: Johan Genis (FluxForge AI)
**Created**: 2026-01-26
**Last Updated**: 2026-01-26

---

## System Overview

ForgeKit operates in two modes: **local development** (Phase 1, current) and **MCP server** (Phase 2, planned). Both modes serve the same skill content but through different distribution mechanisms.

```
┌─────────────────────────────────────────────────────────────┐
│                      ForgeKit System                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐              ┌───────────────────────┐    │
│  │ Skill Source  │              │ Distribution Layer    │    │
│  │              │              │                       │    │
│  │ skills/*.md  │─────────────►│ Mode A: Symlinks      │    │
│  │ commands/*.md│              │ Mode B: MCP Server    │    │
│  └──────────────┘              └───────────────────────┘    │
│                                         │                    │
│                                         ▼                    │
│                              ┌───────────────────────┐      │
│                              │ AI Coding Assistants   │      │
│                              │                       │      │
│                              │ • Claude Code         │      │
│                              │ • Cursor              │      │
│                              │ • Cline               │      │
│                              │ • VS Code Copilot     │      │
│                              └───────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
fluxforgeai/forgekit/
├── ARCHITECTURE.md                     # This document
├── CONVENTIONS.md                      # Expected project directory structure
├── IMPLEMENTATION_PLAN.md              # Phased implementation plan
├── PRD.md                              # Product requirements
├── README.md                           # Setup and usage guide
├── pyproject.toml                      # Python package definition
├── .gitignore
│
├── skills/                             # The 8 operational skills
│   ├── blueprint/SKILL.md            #   Design-to-spec for proactive pipeline
│   ├── incident/SKILL.md              #   Incident documentation
│   ├── investigate/SKILL.md           #   Deep investigation
│   ├── rca-bugfix/SKILL.md            #   Root cause analysis + fix prompts
│   ├── watchdog/SKILL.md              #   Autonomous log monitoring
│   ├── analyze/                       #   Systems analysis (5 modes)
│   │   ├── SKILL.md
│   │   ├── DESIGN_ESCALATION.md       #   Analyze → Design bridge spec
│   │   └── DESIGN_SKILL_SPEC.md       #   Design skill full specification
│   ├── design/SKILL.md               #   Architectural design (5 modes)
│   └── research/SKILL.md             #   Topic research
│
├── commands/                           # Session management commands
│   ├── session-start.md               #   Initialize session with context
│   ├── session-end.md                 #   Create handoff documentation
│   └── verify-session.md             #   Verify handoff correctness
│
├── src/forgekit/                       # CLI tool
│   ├── __init__.py                    #   Version (0.1.0)
│   └── cli.py                        #   7 commands: init/update/status/diff/commit/push/uninstall
│
├── docs/research/                      # Skill design research
│   ├── 2026-01-23_0615_systems_analyst_skill_design.md
│   ├── 2026-01-26_1410_skills_integration_architecture.md
│   └── 2026-01-26_1549_forgekit_monetization_and_distribution_strategy.md
│
└── server/                             # MCP Server (Phase 2 - planned)
    ├── pyproject.toml
    ├── src/forgekit_server/
    │   ├── main.py                    #   MCP server entrypoint
    │   ├── auth.py                    #   API key validation + tier checking
    │   ├── skill_registry.py          #   Load, parse, cache skills from markdown
    │   ├── platform_adapter.py        #   Tool name mapping per client platform
    │   ├── prompts.py                 #   MCP prompt handlers
    │   ├── tools.py                   #   MCP tool handlers (watchdog)
    │   └── resources.py               #   MCP resource handlers (templates)
    └── deploy/
        ├── Dockerfile
        └── fly.toml
```

---

## Component Architecture

### 1. Skills Layer

Skills are markdown files with optional YAML frontmatter. Each skill defines a methodology that the AI assistant follows.

```
┌──────────────────────────────────────────────────────────────────┐
│                        SKILLS LAYER                               │
│                                                                   │
│  Reactive Pipeline:                                               │
│  /watchdog ──► /incident ──► /investigate ──► /rca-bugfix ──┐    │
│       │                                       (fix prompt)   │    │
│       │ (autonomous)                                         │    │
│       ▼                                                      ▼    │
│  Telegram alerts                                        /plan mode│
│                                                              ▲    │
│  Proactive Pipeline:                                         │    │
│  /research ──► /design ──► /blueprint ──────────────────────┘    │
│                              (spec + prompt)                      │
│                                                                   │
│  Strategic: /analyze ──► feeds into either pipeline               │
│                                                                   │
│  Session Management:                                              │
│  /session-start ──► (work) ──► /session-end                       │
│                                  │                                │
│                                  ▼                                │
│                          /verify-session                           │
└──────────────────────────────────────────────────────────────────┘
```

**Skill Format**:
```markdown
---
description: "When this skill should be used"
---
# Skill Title

## Instructions
[Methodology the AI follows]

## Output Format
[Template for artifacts produced]
```

**Cross-Skill Communication**: Via shared artifacts on the filesystem:

| Artifact Path | Written By | Read By |
|--------------|-----------|---------|
| `docs/blueprints/*.md` | blueprint | plan mode |
| `docs/RCAs/*.md` | rca-bugfix | investigate, analyze |
| `docs/incidents/*.md` | incident | investigate, analyze |
| `docs/analysis/*.md` | analyze | design |
| `docs/design/*.md` | design | blueprint, (implementation) |
| `docs/research/*.md` | research | investigate, design, blueprint |
| `docs/prompts/*.md` | rca-bugfix, blueprint | plan mode |
| `system-map.md` | analyze | analyze (refreshed each run) |

### 2. CLI Layer

The CLI (`forgekit`) manages installation and development workflow.

```
┌──────────────────────────────────────────┐
│              ForgeKit CLI                  │
│           (src/forgekit/cli.py)           │
├──────────────────────────────────────────┤
│                                           │
│  forgekit init                            │
│  ├── Creates .claude/ directory           │
│  ├── Symlinks .claude/skills/ → skills/   │
│  ├── Symlinks .claude/commands/ → cmds/   │
│  └── Writes .forgekit marker file         │
│                                           │
│  forgekit update                          │
│  └── git pull in forgekit repo            │
│                                           │
│  forgekit status                          │
│  ├── Shows version                        │
│  ├── Shows git status of forgekit repo    │
│  └── Shows symlink status in current dir  │
│                                           │
│  forgekit diff                            │
│  └── git diff in forgekit repo            │
│                                           │
│  forgekit commit -m "msg"                 │
│  └── git add -A && git commit in repo     │
│                                           │
│  forgekit push                            │
│  └── git push in forgekit repo            │
│                                           │
│  forgekit uninstall                       │
│  ├── Removes .claude/skills symlink       │
│  ├── Removes .claude/commands symlink     │
│  └── Removes .forgekit marker             │
└──────────────────────────────────────────┘
```

**Key Design Decisions**:
- Zero external dependencies (stdlib only: argparse, os, subprocess, pathlib)
- Detects forgekit install path from `__file__` location (no config needed)
- Symlinks are bidirectional: edits in any project flow to the forgekit repo
- `.forgekit` marker file tracks version and install path per project

### 3. Distribution Layer (Current: Symlinks)

```
~/Projects/fluxforgeai/forgekit/     ← Single source of truth
├── skills/
└── commands/
         │
         │  Symlinks (created by `forgekit init`)
         │
         ├──► ~/Projects/project-a/.claude/skills/
         ├──► ~/Projects/project-a/.claude/commands/
         ├──► ~/Projects/project-b/.claude/skills/
         └──► ~/Projects/project-b/.claude/commands/
```

### 4. Distribution Layer (Phase 2: MCP Server)

```
┌──────────────────────────────────────────────────────────┐
│                  ForgeKit MCP Server                       │
│                  (Python / FastAPI + MCP SDK)              │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────────┐  │
│  │ Auth     │  │ Metering │  │ Skill Registry        │  │
│  │          │  │          │  │                       │  │
│  │ API key  │  │ Per-call │  │ Loads skills/*.md     │  │
│  │ Tier     │  │ Per-user │  │ Parses frontmatter    │  │
│  │ Rate lim │  │ Analytics│  │ Caches in memory      │  │
│  └──────────┘  └──────────┘  └───────────────────────┘  │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │               MCP Protocol Layer                     │ │
│  │                                                     │ │
│  │  Prompts:  incident_report, investigate, rca_bugfix, │ │
│  │            blueprint, analyze_{health,risk,patterns, │ │
│  │            component,architecture},                  │ │
│  │            design_{tradeoff,validate,migrate,impact, │ │
│  │            pattern}, research,                       │ │
│  │            session_{start,end}, verify_session       │ │
│  │                                                     │ │
│  │  Tools:    watchdog_start, watchdog_status,          │ │
│  │            watchdog_stop                             │ │
│  │                                                     │ │
│  │  Resources: forgekit://conventions                   │ │
│  │             forgekit://templates/*                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Platform Adapter                                    │ │
│  │                                                     │ │
│  │  Detects client type and maps tool references:      │ │
│  │  Claude Code: Read, Grep, Glob, Edit, Bash          │ │
│  │  Cursor:      readFile, searchCode, editFile        │ │
│  │  Copilot:     readFile, searchFiles, runCommand     │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  Transport: Streamable HTTP (remote) / stdio (local)     │
└──────────────────────────────────────────────────────────┘
```

**MCP Primitive Mapping**:

| MCP Primitive | Control | ForgeKit Usage |
|---------------|---------|---------------|
| **Prompts** | User-controlled | Skill instructions (methodology, templates, output formats) |
| **Tools** | Model-controlled | Watchdog operations (start/stop/status) |
| **Resources** | App-controlled | Conventions doc, report templates |

---

## Security Architecture

### IP Protection (Trade Secret Model)

```
┌─────────────────────────────────────────────┐
│            Protection Layers                  │
├─────────────────────────────────────────────┤
│                                              │
│  Layer 1: Technical                          │
│  ├── MCP server: prompts in-memory only      │
│  ├── Never written to user's filesystem      │
│  ├── API key required for every request      │
│  └── Rate limiting prevents bulk extraction  │
│                                              │
│  Layer 2: Legal                              │
│  ├── Trade secret protection (automatic)     │
│  ├── Copyright (human-authored content)      │
│  ├── Terms of Service (no reverse eng.)      │
│  └── API key agreement                       │
│                                              │
│  Layer 3: Operational                        │
│  ├── Private GitHub repo (Phase 1)           │
│  ├── Usage logging (detect anomalies)        │
│  └── Tier-based access control               │
└─────────────────────────────────────────────┘
```

### Authentication Flow (Phase 2)

```
User Request
     │
     ▼
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Validate │────►│ Check    │────►│ Serve    │
│ API Key  │     │ Tier     │     │ Prompt   │
└──────────┘     └──────────┘     └──────────┘
     │                │                │
     ▼                ▼                ▼
  401 if          403 if           200 + prompt
  invalid        wrong tier        content
```

---

## Technology Stack

### Current (Phase 1)

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Skills | Markdown + YAML frontmatter | Claude Code native format |
| CLI | Python 3.10+ (stdlib only) | Zero dependencies, works everywhere |
| Package | pyproject.toml + hatchling | Modern Python packaging |
| VCS | Git | Standard |
| Install | pip / uv | Python ecosystem |

### Planned (Phase 2+)

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| MCP Server | Python + FastAPI + MCP SDK | Python ecosystem, async support |
| Auth | API keys (self-managed) | Simple, no OAuth complexity needed initially |
| Metering | Moesif | Purpose-built for API/MCP metering |
| Billing | Stripe / Paddle | Industry standard |
| Hosting | Fly.io / Railway | Simple deployment, global edge |
| Containerization | Docker | Standard |

---

## Data Flow

### Local Mode (Phase 1)

```
User invokes /analyze risk
         │
         ▼
Claude Code loads .claude/skills/analyze/SKILL.md
         │ (via symlink → forgekit/skills/analyze/SKILL.md)
         ▼
Claude follows methodology:
  1. Reads codebase (Read, Grep, Glob tools)
  2. Asks user at checkpoints (AskUserQuestion)
  3. Writes report to docs/analysis/*.md
  4. Suggests next skill (/design or /investigate)
```

### MCP Mode (Phase 2)

```
User intent: "analyze the risk of our API layer"
         │
         ▼
AI Tool sends: get_prompt("analyze_risk", {scope: "API"})
         │ (MCP JSON-RPC over Streamable HTTP)
         ▼
ForgeKit Server:
  1. Validates API key
  2. Checks tier (Pro required)
  3. Meters invocation
  4. Loads analyze/SKILL.md (cached)
  5. Extracts risk mode instructions
  6. Adapts tool names for client platform
  7. Returns prompt content
         │
         ▼
AI Tool follows methodology (same as local, tool names adapted)
```

---

## Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Repo name | `forgekit` | `claude-skills`, `skillforge` | No trademark risk ("Claude"), brandable, product-ready |
| Distribution (Phase 1) | Symlinks | Copy, git submodule | Bidirectional edits, single source of truth |
| Distribution (Phase 2) | MCP server | CLI download, npm package | Cross-platform + closed-source + monetizable |
| CLI dependencies | Zero (stdlib) | Click, Typer, Rich | Minimal install, no dependency conflicts |
| Skill format | Markdown + YAML frontmatter | JSON, YAML, custom DSL | Claude Code native, human-readable, portable |
| IP protection | Trade secret + MCP | Open source, encryption | MCP keeps prompts server-side; trade secret is strongest legal protection for prompts |
| Cross-platform | MCP protocol | AGENTS.md, rulesync | MCP is the emerging industry standard (Linux Foundation) |
| Session commands | Included in ForgeKit | Separate repo (claude-session-kit) | Unified toolkit, single install command |

---

**Architecture Status**: Phase 1 implemented and operational. Phase 2 (MCP server) is designed but not built.
