# ForgeKit - Implementation Plan

**Version**: 0.1.0
**Author**: Johan Genis (FluxForge AI)
**Created**: 2026-01-26
**Last Updated**: 2026-02-11

---

## Quick Reference

**Current Phase**: Phase 1+ (Dev Infrastructure Complete) / Pre-Phase 2
**Next Task**: Phase 2 planning
**Active Tracker**: `docs/findings/2026-02-11_1837_dev_environment_infrastructure_FINDINGS_TRACKER.md` (F1: Resolved)

---

## Executive Summary

ForgeKit is an AI engineering skills toolkit distributed as an MCP server for closed-source monetization. Development follows four phases: local development (complete), MCP server MVP, marketplace monetization, and platform expansion.

---

## Phase 1: Local Development Environment (COMPLETE)

**Status**: Done (2026-01-26)
**Goal**: Consolidate skills into a private repo with CLI tooling.

### Completed Steps

| Step | Description | Status |
|------|-------------|--------|
| 1.1 | Create repo structure (`skills/`, `commands/`, `src/`, `docs/`) | DONE |
| 1.2 | Copy 7 skills from pilot_connector `.claude/skills/` | DONE |
| 1.3 | Copy 3 session commands from `.claude/commands/` | DONE |
| 1.4 | Copy 3 research documents to `docs/research/` | DONE |
| 1.5 | Genericize project-specific references (absolute paths, container names, project names) | DONE |
| 1.6 | Build CLI tool (`forgekit init/update/status/diff/commit/push/uninstall`) | DONE |
| 1.7 | Create `pyproject.toml` with entry point | DONE |
| 1.8 | Create README.md and CONVENTIONS.md | DONE |
| 1.9 | Initialize git repo, initial commit (21 files) | DONE |
| 1.10 | Replace originals with symlinks, verify skills accessible | DONE |
| 1.11 | Install CLI globally via pip (`forgekit` command available) | DONE |

### Deliverables
- Private git repo at `~/Projects/fluxforgeai/forgekit/`
- 7 skills + 3 commands genericized and portable (8 skills after `/blueprint` added 2026-01-27)
- CLI tool installed and working
- Symlinks verified in pilot_connector project

---

## Phase 2: MCP Server MVP

**Status**: Not Started
**Goal**: Serve skills via MCP protocol for cross-platform, closed-source distribution.

### Steps

| Step | Description | Dependencies |
|------|-------------|-------------|
| 2.1 | Design skill-to-MCP mapping (Prompts, Tools, Resources) | Phase 1 |
| 2.2 | Set up MCP server project (`server/` directory, FastAPI + MCP SDK) | Phase 1 |
| 2.3 | Implement skill registry (load markdown files, parse frontmatter, cache) | 2.2 |
| 2.4 | Implement MCP Prompts handlers (all 8 skills + modes as named prompts) | 2.3 |
| 2.5 | Implement MCP Tools handlers (watchdog start/stop/status) | 2.3 |
| 2.6 | Implement MCP Resources handlers (conventions, templates) | 2.3 |
| 2.7 | Implement authentication layer (API keys, tier checking) | 2.2 |
| 2.8 | Implement platform adaptation layer (Claude/Cursor/Copilot tool name mapping) | 2.4 |
| 2.9 | Add usage metering (per-invocation logging) | 2.7 |
| 2.10 | Containerize (Dockerfile) | 2.4-2.6 |
| 2.11 | Deploy to hosting platform (Fly.io / Railway / Render) | 2.10 |
| 2.12 | Test with Claude Code as MCP client | 2.11 |
| 2.13 | Test with Cursor as MCP client | 2.11 |
| 2.14 | Test with Cline as MCP client | 2.11 |
| 2.15 | Private beta with 3-5 users | 2.12-2.14 |

### Deliverables
- Hosted MCP server at `https://api.forgekit.ai/mcp`
- API key management
- Cross-platform verified (Claude Code, Cursor, Cline)
- Usage metering operational

---

## Phase 3: Marketplace & Monetization

**Status**: Not Started
**Goal**: Generate revenue from ForgeKit skills.

### Steps

| Step | Description | Dependencies |
|------|-------------|-------------|
| 3.1 | Define pricing tiers (Free/Pro/Enterprise) | Phase 2 |
| 3.2 | Implement tier-based access control in MCP server | 3.1 |
| 3.3 | Integrate billing provider (Stripe / Paddle) | 3.1 |
| 3.4 | List on MCPize marketplace (70% revenue share) | Phase 2 |
| 3.5 | List on Cline Marketplace | Phase 2 |
| 3.6 | Register on Official MCP Registry | Phase 2 |
| 3.7 | Integrate Moesif for usage analytics and billing | 3.3 |
| 3.8 | Build landing page (forgekit.ai) | 3.1 |
| 3.9 | Create demo videos for each skill | 3.8 |
| 3.10 | Write Terms of Service and Privacy Policy | 3.1 |
| 3.11 | Launch public beta | 3.2-3.10 |
| 3.12 | Iterate on pricing based on usage data | 3.11 |

### Deliverables
- Pricing tiers active
- Listed on 2+ marketplaces
- Landing page live
- Revenue flowing

---

## Phase 4: Platform Expansion

**Status**: Not Started
**Goal**: Maximize reach and feature depth.

### Steps

| Step | Description | Dependencies |
|------|-------------|-------------|
| 4.1 | Build full platform adaptation layer (generic tool references in skills) | Phase 2 |
| 4.2 | Add AGENTS.md export for non-MCP tools | 4.1 |
| 4.3 | Build team/org features (shared artifacts, RBAC) | Phase 3 |
| 4.4 | Add analytics dashboard (skill usage, team insights) | 4.3 |
| 4.5 | Enable custom skill development (Enterprise tier) | 4.3 |
| 4.6 | Explore VS Code extension for enhanced UX | Phase 3 |
| 4.7 | Add new skill domains (security, testing, documentation) | Phase 3 |

### Deliverables
- Full cross-platform support
- Enterprise features
- Growing skill library

---

## Skill Refinement Backlog (Ongoing)

These improvements apply across all phases:

| Item | Description | Priority |
|------|-------------|----------|
| `/blueprint` skill | Design-to-spec bridge for proactive pipeline (DONE -- 2026-01-27) | DONE |
| `/finding` skill | Audit pipeline entry point for proactive discoveries (DONE -- multiple sessions 2026-01-28 to 2026-02-10) | DONE |
| Fix escalation in `/analyze` | Add "Corrective fix" option alongside Design Escalation in all analyze modes | High |
| `/investigate` confirmation mode | Accept finding reports as input with abbreviated investigation for known causes | High |
| Standardize handoff protocol | All 9 skills use consistent end format | High |
| Add context-awareness | analyze/design check context budget before starting | High |
| Finding artifact integration | `/investigate`, `/analyze`, `/rca-bugfix`, `/research` read `docs/findings/` | Medium |
| Watchdog-incident bridge | /incident can parse watchdog JSON files | Medium |
| Research integration | investigate/rca-bugfix check existing research first | Medium |
| Add --quick flag | All skills support abbreviated execution | Medium |
| Generic tool references | Replace Claude-specific tool names with {tool:read_file} placeholders | Phase 2 |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Phase |
|------|------------|--------|------------|-------|
| Data loss (skills only on one laptop) | Was High, now Low | Critical | Phase 1 complete: git repo + GitHub | 1 |
| MCP adoption stalls | Low | High | Maintain CLI fallback | 2 |
| Prompt extraction via MCP | Medium | Medium | ToS + rate limiting + obfuscation | 2-3 |
| Competitor copies methodology | Medium | Medium | First-mover + continuous innovation | 3 |
| EU AI Act compliance | Low | Low | Monitor regulations | 3 |

---

## Dev Environment Infrastructure (Cross-Phase)

**Status**: Complete (Resolved)
**Goal**: Standardized development environment with quality gates, CI/CD, and Phase 2 workspace readiness.
**Tracker**: `docs/findings/2026-02-11_1837_dev_environment_infrastructure_FINDINGS_TRACKER.md`

| Step | Description | Status |
|------|-------------|--------|
| D.1 | Create `.venv` with uv, add dependency groups (dev/test) to pyproject.toml | ✅ DONE |
| D.2 | Generate and commit `uv.lock` | ✅ DONE |
| D.3 | Design tradeoff: single .venv vs multiple vs Docker | ✅ DONE (Option A: single .venv, score 97/105) |
| D.4 | Blueprint: pre-commit, tests, CI, tool config | ✅ DONE |
| D.5 | Add `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]` to pyproject.toml | ✅ DONE |
| D.6 | Create `.pre-commit-config.yaml` (ruff, uv-lock, mypy) | ✅ DONE |
| D.7 | Create initial test suite (`tests/test_cli.py`, 6 tests) | ✅ DONE |
| D.8 | Create `.github/workflows/ci.yml` (lint + test matrix 3.10-3.13) | ✅ DONE |
| D.9 | Harden `.gitignore` (tool caches, macOS, coverage) | ✅ DONE |
| D.10 | Verify all acceptance criteria pass | ✅ DONE |

---

## Session Progress Log

### Session 1: 2026-02-11
**Duration**: ~2.5 hours
**Completed**:
- [x] D.1: Created `.venv` named `forgekit` with `uv venv --prompt forgekit`
- [x] D.2: Added `[dependency-groups]` (dev: ruff, mypy, pre-commit; test: pytest, pytest-cov)
- [x] D.2: Generated `uv.lock` (23 packages, 120.6 KB)
- [x] D.3: Design tradeoff analysis — 4 options, weighted scoring, Option A wins (97/105)
- [x] D.4: Blueprint with exact file specs for 6 files + implementation prompt
- [x] Finding F1 logged, tracker created, lifecycle: Open → Designing → Blueprint Ready

**Key Decisions**:
- Single `.venv` + uv dependency groups over multiple venvs or Docker (design analysis score 97 vs 68 vs 51)
- uv as sole package manager (already in README, community consensus 2026)
- Docker reserved for Phase 2 MCP server deployment only, not development
- uv workspaces for Phase 2 monorepo (add `[tool.uv.workspace]` when `server/` materializes)

**Artifacts Created**:
- `docs/findings/2026-02-11_1837_missing_dev_environment_infrastructure.md` — F1 finding report
- `docs/findings/2026-02-11_1837_dev_environment_infrastructure_FINDINGS_TRACKER.md` — Tracker
- `docs/design/2026-02-11_1848_dev_environment_strategy.md` — Design analysis
- `docs/blueprints/2026-02-11_1856_dev_environment_setup.md` — Blueprint
- `docs/prompts/2026-02-11_1856_dev_environment_setup.md` — Implementation prompt

**Next Session**:
- Run `/plan` with prompt at `docs/prompts/2026-02-11_1856_dev_environment_setup.md`
- Implement D.5-D.9 (tool config, pre-commit, tests, CI, .gitignore)
- Verify acceptance criteria (D.10)
- Commit all dev environment changes

### Session 2: 2026-02-11
**Completed**:
- [x] D.5: Added `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]` to pyproject.toml
- [x] D.6: Created `.pre-commit-config.yaml` (ruff v0.15.0, uv-lock 0.9.24, mypy local hook)
- [x] D.7: Created `tests/test_cli.py` (6 tests, all passing, 69% coverage)
- [x] D.8: Created `.github/workflows/ci.yml` (lint + test matrix Python 3.10-3.13)
- [x] D.9: Hardened `.gitignore` (tool caches, macOS, coverage, environment files)
- [x] D.10: All 8 acceptance criteria verified passing
- [x] Fixed pre-existing lint issues: removed unused `os` and `sys` imports from cli.py, auto-formatted
- [x] Installed pre-commit hooks, verified all 4 hooks pass on all files
- [x] F1 tracker updated: Blueprint Ready → Planned → Implementing → Resolved

**Artifacts Created**:
- `.pre-commit-config.yaml` — Pre-commit hook configuration
- `tests/__init__.py` — Test package marker
- `tests/test_cli.py` — 6 CLI tests
- `.github/workflows/ci.yml` — CI pipeline (lint + test matrix)

**Artifacts Modified**:
- `pyproject.toml` — Tool configuration sections added
- `.gitignore` — Tool caches, macOS, coverage, environment exclusions
- `src/forgekit/cli.py` — Removed unused imports, reformatted
- `src/forgekit/__init__.py` — Reformatted
- `IMPLEMENTATION_PLAN.md` — D.5–D.10 marked DONE, Session 2 log
- F1 Findings Tracker — Resolved

---

**Plan Status**: Phase 1 Complete. Dev infrastructure complete (Resolved). Ready for Phase 2 planning.
