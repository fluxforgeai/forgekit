# Finding: No Standardized Development Environment — Missing .venv, Dependency Groups, and Lockfile

**Date**: 2026-02-11
**Discovered by**: Manual review during first ForgeKit development session
**Type**: Gap
**Severity**: Medium
**Status**: Open

---

## What Was Found

ForgeKit has no local development environment infrastructure. The project has a `pyproject.toml` with zero runtime dependencies and a CLI entry point, but no provisions for development or testing tooling:

1. **No virtual environment** — No `.venv` directory, no documented setup process for contributors
2. **No dependency groups** — `pyproject.toml` has no `[dependency-groups]` section for dev tools (linter, type checker, formatter) or test tools (pytest, coverage)
3. **No lockfile** — No `uv.lock` for deterministic dependency resolution across environments
4. **No dev workflow documentation** — README covers end-user installation (`uv tool install -e .`) but not contributor development setup
5. **No environment strategy** — No documented approach for how dev, test (CI), and production environments relate to each other

The CLI itself is correctly designed with zero runtime dependencies (stdlib only, per NFR-006). The gap is in the surrounding development infrastructure.

---

## Affected Components

- `pyproject.toml` — missing `[dependency-groups]` section
- Project root — no `.venv/` directory
- Project root — no `uv.lock` file
- `README.md` — documents end-user install only, not contributor dev setup
- `.gitignore` — already includes `.venv/` (foresight, but no venv existed to ignore)

---

## Evidence

### pyproject.toml (before)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "forgekit"
version = "0.1.0"
description = "ForgeKit - AI Engineering Skills Toolkit by FluxForge AI"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "Proprietary"}
authors = [{name = "Johan Genis"}]

[project.scripts]
forgekit = "forgekit.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/forgekit"]
```

No `[dependency-groups]`, no `[tool.ruff]`, no `[tool.pytest.ini_options]`, no `[tool.mypy]` — no development tooling configuration of any kind.

### Architecture context

`ARCHITECTURE.md` documents a planned Phase 2 MCP server (`server/` directory with its own `pyproject.toml` and dependencies: FastAPI, MCP SDK, uvicorn, etc.). The monorepo will contain two distinct Python packages with different dependency profiles. Without a workspace-aware development environment, Phase 2 development will require ad-hoc environment management.

---

## Preliminary Assessment

**Likely cause**: Phase 1 focused on skill content and CLI functionality. The CLI has zero runtime dependencies, so a development environment wasn't strictly necessary to build and test the 131-line CLI. Development infrastructure was deferred.

**Likely scope**: Isolated to project infrastructure. Does not affect skill content, CLI functionality, or end-user installation. Becomes critical when Phase 2 introduces real dependencies (FastAPI, MCP SDK) and the repo grows to support multiple contributors.

**Likely impact**: Without standardized dev infrastructure:
- No linting, formatting, or type checking enforced
- No test framework available
- No reproducible builds (no lockfile)
- Phase 2 server development would require improvised environment setup
- Contributors would each configure their own tooling inconsistently

---

## Classification Rationale

**Type: Gap** — The development environment is a missing expected capability. Every Python project of ForgeKit's ambition (monorepo, MCP server, marketplace distribution) needs standardized dev tooling. This is infrastructure that should exist but doesn't.

**Severity: Medium** — The project functions correctly without it today (Phase 1 is complete, CLI works). But it blocks quality assurance (no tests, no linting) and will become a higher-severity gap when Phase 2 begins. Not critical because no production system is affected.

---

**Finding Logged**: 2026-02-11 18:37 UTC
