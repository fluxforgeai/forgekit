# Design Analysis: ForgeKit Development Environment Strategy

**Date**: 2026-02-11 18:48 UTC
**Analyst**: Claude Code (Session 1)
**Mode**: Tradeoff
**Interactive Checkpoints**: 2 decisions made by user

---

## Executive Summary

ForgeKit needs a standardized development environment that works today (131-line CLI, zero runtime deps) and scales cleanly into Phase 2 (FastAPI MCP server, real dependencies, Docker deployment). After evaluating four approaches against simplicity, reliability, and time-to-setup, **Option A: Single `.venv` + uv dependency groups** is the clear winner. It provides the lowest friction for the current phase while offering a clean upgrade path to uv workspaces when the `server/` package materializes.

---

## User Context

- **Goal**: Standardized development environment for a growing monorepo containing a zero-dep CLI (Phase 1) and a future FastAPI MCP server (Phase 2)
- **Constraints**:
  - CLI must remain zero-dependency (NFR-006: stdlib only, always)
  - Symlink-based bidirectional editing must work (core distribution mechanism)
  - Phase 2 MCP server is high certainty (FastAPI + MCP SDK + auth + metering)
  - Single developer now, potential contributors later
- **Priorities**: Simplicity (5) > Reliability (4) > Time (3) > Performance (2) > Cost (1)

---

## Current State Analysis

### Codebase Profile

| Aspect | Current (Phase 1) | Phase 2 (Planned) |
|--------|-------------------|-------------------|
| Packages | 1 (`forgekit` CLI) | 2 (`forgekit` CLI + `forgekit-server`) |
| Python source | 131 lines (`cli.py` + `__init__.py`) | ~1000+ lines (FastAPI server, 7 modules) |
| Runtime deps | 0 (stdlib only) | FastAPI, MCP SDK, uvicorn, Moesif SDK |
| Skill content | 5,600+ lines Markdown | Same, served via MCP protocol |
| Build backend | hatchling | hatchling (both packages) |
| Entry points | `forgekit` CLI | CLI + `uvicorn forgekit_server.main:app` |
| Deployment | `uv tool install -e .` on user's machine | Docker -> Fly.io/Railway |
| Test framework | pytest installed, no tests written | pytest + pytest-asyncio + httpx |

### What Exists Today

- `pyproject.toml` with `[dependency-groups]` for `dev` (ruff, mypy, pre-commit) and `test` (pytest, pytest-cov)
- `.venv/` created with `uv venv --prompt forgekit`
- `uv.lock` generated (120.6 KB, 23 packages resolved)
- `.gitignore` covers `.venv/`, `__pycache__/`, `dist/`, `build/`
- No `.pre-commit-config.yaml`, no CI/CD, no tests, no Makefile/justfile

### What's Missing

- No pre-commit hooks configured (package installed but no `.pre-commit-config.yaml`)
- No test suite (pytest installed but zero test files)
- No CI/CD pipeline (GitHub Actions)
- No `.python-version` file
- No task runner (Makefile/justfile)
- No workspace configuration for Phase 2 multi-package support

### Key Architectural Constraint: Symlinks

ForgeKit's distribution model creates symlinks from user projects into the ForgeKit repo:

```
project/.claude/skills/ -> ~/Projects/forgekit/skills/
project/.claude/commands/ -> ~/Projects/forgekit/commands/
```

The CLI resolves its install path via `Path(__file__).resolve().parent.parent.parent`. This is a filesystem-native operation. Any development environment must preserve native filesystem access and symlink resolution.

---

## External Research (2026 Sources)

### 1. uv Workspaces for Python Monorepos

**Finding**: uv workspaces are production-proven at scale. Apache Airflow ships 120+ distributions from a single repo using uv workspaces (FOSDEM 2026). LiveKit Agents manages 46 workspace members.

**Configuration**:
```toml
# Root pyproject.toml
[tool.uv.workspace]
members = ["server"]

# server/pyproject.toml references CLI as workspace dep (if needed)
[tool.uv.sources]
forgekit = { workspace = true }
```

Single `uv.lock` for the entire workspace. `uv run --package forgekit-server` targets a specific member.

**Sources**: [uv Workspaces Docs](https://docs.astral.sh/uv/concepts/projects/workspaces/), [FOSDEM 2026: Modern Python Monorepo](https://fosdem.org/2026/schedule/event/WE7NHM-modern-python-monorepo-apache-airflow/)

### 2. Dependency Groups (PEP 735)

**Finding**: Dependency groups are dev-time only, never published to PyPI. The `dev` group is special in uv: `uv run` installs it automatically. Use `include-group` to compose groups.

**Best practice**: Use `optional-dependencies` for end-user features, `dependency-groups` for all dev/test tooling.

**Sources**: [uv Dependencies Docs](https://docs.astral.sh/uv/concepts/projects/dependencies/), [Simon Willison: Dependency groups and uv run](https://til.simonwillison.net/uv/dependency-groups)

### 3. venv vs Docker for Development

**Finding**: The 2026 consensus is "both, for different purposes." Use venv for local dev (fast iteration), Docker for production deployment. Use a venv *inside* Docker containers too (Hynek Schlawack's recommendation — isolates app deps from system Python).

**Sources**: [Hynek: Production-ready Docker with uv](https://hynek.me/articles/docker-uv/), [Hynek: Why I Still Use venvs in Docker](https://hynek.me/articles/docker-virtualenv/)

### 4. Lockfile Management

**Finding**: Commit `uv.lock` to git. Use `uv sync --frozen` in CI to fail if lockfile is out of date. Use the `uv-lock` pre-commit hook to keep it in sync.

**Sources**: [uv Locking and Syncing](https://docs.astral.sh/uv/concepts/projects/sync/), [GitHub Issue #9797](https://github.com/astral-sh/uv/issues/9797)

### 5. Single vs Multiple Virtual Environments

**Finding**: Universal recommendation is one venv per project. In a monorepo with uv workspaces, you get a single venv for the workspace with all members sharing it — managed by uv's resolver to ensure compatibility.

**Sources**: [Python venv Docs](https://docs.python.org/3/library/venv.html), [InfoWorld: venv Dos and Don'ts](https://www.infoworld.com/article/2257028/python-virtualenv-and-venv-dos-and-donts.html)

---

## Options Evaluated

### Baseline: No Formal Environment (Pre-Session State)

**How it works**: CLI installed globally via `uv tool install -e .`. No local `.venv`, no dependency groups, no lockfile. Dev tools (if any) installed ad-hoc.

**Pros**:
- Zero setup time
- Works for 131-line stdlib CLI

**Cons**:
- No linting, formatting, or type checking
- No test framework available
- No reproducible builds
- No CI/CD possible
- Phase 2 would require starting from scratch
- Contributors would each configure their own tooling

**Impact assessment**:
- Files to change: 0
- Effort: 0
- Risk: High — accumulates tech debt, no quality gates

### Option A: Single `.venv` + uv Dependency Groups

**How it works**: One `.venv` at the project root, named `forgekit`. Dependency groups in `pyproject.toml` separate dev/test tooling from runtime. `uv.lock` pins all versions. When Phase 2 arrives, add `[tool.uv.workspace]` to root `pyproject.toml` and create `server/pyproject.toml` — the same `.venv` expands to serve both packages.

**Setup**:
```bash
uv venv .venv --prompt forgekit
uv sync --group dev --group test
```

**Phase 2 evolution**:
```toml
# Add to root pyproject.toml
[tool.uv.workspace]
members = ["server"]
```
```bash
uv sync --group dev --group test  # Now installs both packages
```

**Pros**:
- One activation, everything available (CLI, server, dev tools, test tools)
- `uv.lock` provides deterministic builds across all environments
- Dependency groups keep concerns separated without environment proliferation
- Natural evolution to workspaces — add 3 lines to `pyproject.toml`
- Matches 2026 Python community consensus (FOSDEM, uv docs, Hynek)
- Symlinks work natively (no container boundary)
- `uv run` auto-installs `dev` group — zero friction for daily work
- CI uses same toolchain: `uv sync --frozen --group test && uv run pytest`

**Cons**:
- CLI and server share a venv, so server deps are available when working on CLI (minor — no conflict risk since CLI has zero deps)
- Cannot test CLI in a truly pristine zero-dep environment locally (CI can do this)
- Workspace config is forward-looking — not needed until Phase 2

**Impact assessment**:
- Files to change: 1 (`pyproject.toml` — already done)
- Files to create: 0 (`.venv` and `uv.lock` already generated)
- Effort: Already complete for Phase 1. Phase 2 adds 3 lines.
- Risk: Very low — standard toolchain, proven at scale
- Breaking changes: None

### Option B: Multiple `.venv`s (One Per Package)

**How it works**: Each package gets its own `.venv`. For Phase 1, one `.venv` for the CLI. For Phase 2, a second `.venv` for the server. Dev tools duplicated in each, or a third `.venv` for shared tooling.

**Setup**:
```bash
# Phase 1
uv venv .venv --prompt forgekit-cli
uv sync --group dev --group test

# Phase 2 (additional)
cd server/
uv venv .venv --prompt forgekit-server
uv sync --group dev --group test
```

**Pros**:
- Complete isolation between CLI and server environments
- Can verify CLI truly has zero runtime deps locally
- Each package's venv is minimal (only its deps)

**Cons**:
- Switching between venvs constantly during development
- Dev tools (ruff, mypy, pytest) installed twice
- No unified lockfile — dependency versions can drift between packages
- Pre-commit hooks need to know which venv to use
- IDE must be configured for multiple interpreters
- `pytest` runs in one venv can't test cross-package interactions
- More disk space (minor but real — duplicated ruff, mypy, etc.)
- Fights against uv's design — uv workspaces exist precisely to avoid this

**Impact assessment**:
- Files to change: 1 (`pyproject.toml` per package)
- Additional complexity: Shell aliases or direnv for auto-switching
- Effort: Medium setup, ongoing friction
- Risk: Low technical risk, high ergonomic cost
- Breaking changes: None, but workflow changes significantly

### Option C: Docker-First Development

**How it works**: All development happens inside Docker containers. A `docker-compose.yml` defines a `cli` service and (later) a `server` service. Source code is volume-mounted. Dev tools run inside the container.

**Setup**:
```yaml
# docker-compose.yml
services:
  dev:
    build: .
    volumes:
      - .:/app
      - .venv:/app/.venv  # persist venv across restarts
    command: bash
```

**Pros**:
- Identical environment across all machines
- Phase 2 server + external services (if any) managed by compose
- Production parity — same base image for dev and deploy
- No Python version management on host

**Cons**:
- **Breaks symlinks**: ForgeKit's core distribution model creates symlinks from user projects to the repo. Container filesystem isolation breaks cross-host symlink resolution. `Path(__file__).resolve()` inside a container resolves to container paths, not host paths.
- **Cannot run `forgekit init` from inside container**: The CLI creates symlinks in the user's project directory, which may not be mounted.
- Rebuild or restart friction on every dependency change
- Volume mount performance on macOS (historically slow, improved but still measurable)
- Docker Desktop license cost for commercial use
- Overkill for 131-line stdlib CLI
- Dev tools (ruff, mypy) run slower through container indirection
- Hot reload requires additional configuration
- Every developer needs Docker installed and running

**Impact assessment**:
- Files to create: `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- Effort: High initial setup, ongoing maintenance
- Risk: **High** — breaks symlink resolution, the core architectural mechanism
- Breaking changes: CLI workflow fundamentally changes

---

## Trade-Off Matrix

Scoring: 1 (worst) to 5 (best) per criterion. Weights from user priorities.

| Criterion | Weight | Baseline | A: Single .venv | B: Multiple .venvs | C: Docker Dev |
|-----------|--------|----------|-----------------|---------------------|---------------|
| **Simplicity** | 5 | 3 | **5** | 2 | 1 |
| **Reliability** | 4 | 1 | **4** | 4 | 5 |
| **Time to setup** | 3 | 5 | **4** | 3 | 1 |
| **Phase 2 readiness** | 3 | 1 | **5** | 3 | 4 |
| **Symlink compat** | 4 | 5 | **5** | 5 | 1 |
| **CI/CD alignment** | 2 | 1 | **5** | 3 | 4 |
| | | | | | |
| **Weighted Total** | | **49** | ****97**** | **68** | **51** |

### Scoring Rationale

**Simplicity** (weight 5):
- Baseline: 3 — trivial but no tooling
- A: 5 — one venv, one activation, everything works, natural workspace evolution
- B: 2 — constant venv switching, duplicate tools, IDE confusion
- C: 1 — Docker overhead for a 131-line CLI, compose config, volume mounts

**Reliability** (weight 4):
- Baseline: 1 — no lockfile, no reproducibility, no quality gates
- A: 4 — `uv.lock` deterministic builds, single source of truth, `--frozen` in CI
- B: 4 — each venv is deterministic but versions can drift across packages
- C: 5 — container images are immutable snapshots, highest reproducibility

**Time to setup** (weight 3):
- Baseline: 5 — zero setup
- A: 4 — `uv venv && uv sync` (already done, 2 seconds)
- B: 3 — setup per package, configure switching, IDE config
- C: 1 — Dockerfile, compose, .dockerignore, volume config, debugging mount issues

**Phase 2 readiness** (weight 3):
- Baseline: 1 — start from scratch when server arrives
- A: 5 — add 3 lines for workspace config, `uv sync` handles both packages
- B: 3 — already separated but no unified resolution
- C: 4 — compose naturally handles multi-service, but symlink issue remains

**Symlink compatibility** (weight 4):
- Baseline: 5 — native filesystem, no indirection
- A: 5 — native filesystem, no indirection
- B: 5 — native filesystem, no indirection
- C: 1 — container boundary breaks symlink resolution, `forgekit init` fails

**CI/CD alignment** (weight 2):
- Baseline: 1 — nothing to align with
- A: 5 — CI runs `uv sync --frozen --group test && uv run pytest`, identical toolchain
- B: 3 — CI needs to know which package to test, multiple sync steps
- C: 4 — CI can use same Docker image, but adds image build step

---

## Recommendation

**Option A: Single `.venv` + uv dependency groups.**

Weighted score: **97** (next closest: B at 68, then C at 51, Baseline at 49).

### Why Option A Wins

1. **Simplicity dominance**: One venv, one activation, one lockfile. `uv sync --group dev --group test` and you're done. No switching, no Docker, no compose.

2. **Seamless Phase 2 path**: When the `server/` package materializes, add `[tool.uv.workspace]` (3 lines) to root `pyproject.toml`. Same `.venv` expands. Same `uv sync`. Same `uv run`. This is proven at scale (Apache Airflow: 120+ distributions, FOSDEM 2026).

3. **Symlink preservation**: Native filesystem access. `Path(__file__).resolve()` works. `forgekit init` creates symlinks. Bidirectional editing flows naturally.

4. **2026 community consensus**: uv + venv + lockfile is the standard Python development model. Docker is for deployment. Every major reference (Hynek Schlawack, uv docs, FOSDEM talks) confirms this.

### Key Trade-Off

**What you gain**: Maximum simplicity, fastest iteration, clean growth path.

**What you give up**: Server deps are present in venv when working on CLI. This is a non-issue in practice — the CLI has zero deps, so there's nothing to conflict with. If you ever need to verify the CLI runs with zero deps, CI can do that in an isolated environment.

---

## Impact Assessment

### Code Changes
- `pyproject.toml`: Already updated with `[dependency-groups]`
- No other code changes required for Phase 1
- Phase 2: Add `[tool.uv.workspace]` section (3 lines)

### Files Created
- `.venv/`: Already created
- `uv.lock`: Already generated (commit to git)

### Configuration
- No environment variables needed
- No config files beyond `pyproject.toml`
- `.pre-commit-config.yaml` recommended (separate concern)

### Deployment
- No deployment impact — this is dev environment only
- Production deployment (Phase 2) uses Docker independently

### Operational
- Developer runs `source .venv/bin/activate` once per terminal session
- `uv sync` after any `pyproject.toml` change
- `uv run pytest` / `uv run ruff check .` / `uv run mypy src/` for quality gates

### Dependencies
- `uv` (already installed: v0.9.24)
- Python 3.10+ (already available: 3.13.7 system, 3.12.12 in venv)

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| uv breaks backward compat | Very Low | Medium | `uv.lock` pins uv version, update deliberately |
| Server deps conflict with CLI | None | N/A | CLI has zero deps — nothing to conflict |
| Workspace config complexity in Phase 2 | Low | Low | Well-documented, proven at scale (Airflow, LiveKit) |
| Developer forgets to activate venv | Low | Low | `uv run` works without activation; add shell prompt |

---

## Phase 2 Evolution Playbook

When the `server/` directory is ready:

**Step 1**: Create `server/pyproject.toml`:
```toml
[project]
name = "forgekit-server"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "mcp>=1.0.0",
]
```

**Step 2**: Add workspace config to root `pyproject.toml`:
```toml
[tool.uv.workspace]
members = ["server"]
```

**Step 3**: Re-sync:
```bash
uv sync --group dev --group test
```

The `.venv` now contains both packages. `uv run forgekit status` runs the CLI. `uv run uvicorn forgekit_server.main:app --reload` runs the server. Same venv, same lockfile, zero friction.

**Step 4**: Create `server/deploy/Dockerfile` for production (separate concern from dev environment).

---

## Next Steps

- [x] Create `.venv` with `uv venv --prompt forgekit`
- [x] Add `[dependency-groups]` to `pyproject.toml`
- [x] Run `uv sync --group dev --group test`
- [x] Generate `uv.lock`
- [ ] Commit `uv.lock` to git
- [ ] Configure `.pre-commit-config.yaml` (ruff, mypy, uv-lock hook)
- [ ] Create initial test suite (`tests/test_cli.py`)
- [ ] Set up GitHub Actions CI (`.github/workflows/ci.yml`)
- [ ] Add `[tool.ruff]` and `[tool.mypy]` config to `pyproject.toml`

---

## Sources

### Internal
- `pyproject.toml` — Package definition and dependency groups
- `src/forgekit/cli.py` — CLI source (131 lines, stdlib only)
- `ARCHITECTURE.md` — Phase 2 MCP server design, technology stack
- `IMPLEMENTATION_PLAN.md` — Phased roadmap, server dependencies
- `PRD.md` — NFR-006 (zero CLI deps), success metrics
- `.gitignore` — Existing exclusions

### External (2026)
- [uv Workspaces Documentation](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- [FOSDEM 2026: Modern Python Monorepo with uv (Apache Airflow)](https://fosdem.org/2026/schedule/event/WE7NHM-modern-python-monorepo-apache-airflow/)
- [uv: Managing Dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [Simon Willison: Dependency groups and uv run](https://til.simonwillison.net/uv/dependency-groups)
- [Hynek Schlawack: Production-ready Python Docker Containers with uv](https://hynek.me/articles/docker-uv/)
- [Hynek Schlawack: Why I Still Use Python Virtual Environments in Docker](https://hynek.me/articles/docker-virtualenv/)
- [uv: Locking and Syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv: Using uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/)
- [LiveKit Agents: Package Management with uv](https://deepwiki.com/livekit/agents/9.2-package-management-with-uv)

---

**Analysis Complete**: 2026-02-11 18:48 UTC
