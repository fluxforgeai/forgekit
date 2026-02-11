# Implementation Prompt: ForgeKit Development Environment Setup

**Blueprint Reference**: docs/blueprints/2026-02-11_1856_dev_environment_setup.md
**Design Reference**: docs/design/2026-02-11_1848_dev_environment_strategy.md

## Context

ForgeKit's development environment foundation is in place (.venv named "forgekit", uv dependency groups for dev/test, uv.lock generated). This prompt completes the remaining infrastructure: pre-commit hooks, tool configuration, initial test suite, and CI/CD pipeline.

This is a Gap finding (F1) in the dev environment infrastructure tracker. The design analysis chose Option A (single .venv + uv dependency groups, score 97/105) over multiple venvs and Docker-first development.

## Goal

Implement the 5 remaining items from the design analysis to complete the ForgeKit dev environment:
1. Tool configuration (ruff, mypy, pytest) in pyproject.toml
2. .gitignore hardening
3. Pre-commit hooks
4. Initial test suite
5. GitHub Actions CI pipeline

## Requirements

1. All tool config must live in `pyproject.toml` (no separate config files)
2. Pre-commit hooks: ruff lint+format, uv-lock sync, mypy (local hook using `uv run`)
3. Tests must use `tmp_path` and `monkeypatch` — never modify the actual repo
4. CI must test Python 3.10-3.13 with `--frozen` lockfile enforcement
5. CLI must remain zero-dependency (NFR-006) — no runtime imports added

## Files to Create

1. **`.pre-commit-config.yaml`** — ruff (v0.15.0), uv-lock (0.9.24), mypy (local hook via `uv run mypy`)
2. **`tests/__init__.py`** — empty file
3. **`tests/test_cli.py`** — 6 tests: get_forgekit_root, cli_help, cmd_status, cmd_init, cmd_uninstall, init_idempotency
4. **`.github/workflows/ci.yml`** — lint job (ruff, mypy) + test matrix (3.10-3.13 with coverage)

## Files to Modify

5. **`pyproject.toml`** — append `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.mypy]`, `[tool.pytest.ini_options]`
6. **`.gitignore`** — add `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/`, `.DS_Store`, `.env`

## Implementation Sequence

1. Update `pyproject.toml` with tool config sections
2. Update `.gitignore` with tool caches and macOS artifacts
3. Create `.pre-commit-config.yaml`
4. Run `pre-commit install` to activate hooks
5. Create `tests/__init__.py` and `tests/test_cli.py`
6. Run `uv run pytest --cov=forgekit --cov-report=term-missing` — verify all tests pass
7. Run `uv run ruff check .` and `uv run ruff format --check .` — verify clean
8. Run `uv run mypy src/` — verify no type errors (fix any found)
9. Create `.github/workflows/ci.yml`
10. Run `pre-commit run --all-files` — verify all hooks pass

## Exact File Contents

Refer to the blueprint at `docs/blueprints/2026-02-11_1856_dev_environment_setup.md` for the exact contents of each file. The blueprint contains copy-ready code for all 6 files.

## Constraints

- CLI (`src/forgekit/cli.py`) must NOT gain any new imports or runtime dependencies
- Tests use pytest fixtures (`tmp_path`, `monkeypatch`, `capsys`) — no external test utilities
- If mypy finds type errors in existing CLI code, fix them (don't suppress with `# type: ignore` unless genuinely necessary)
- If ruff finds formatting issues, let `ruff format` fix them (don't fight the formatter)

## Acceptance Criteria

- [ ] `uv run ruff check .` exits 0
- [ ] `uv run ruff format --check .` exits 0
- [ ] `uv run mypy src/` exits 0
- [ ] `uv run pytest --cov=forgekit` exits 0, all 6 tests pass
- [ ] `pre-commit run --all-files` exits 0
- [ ] `.github/workflows/ci.yml` defines lint + test jobs
- [ ] `uv.lock` committed to git
- [ ] All tool caches gitignored

---

## Plan Output Instructions

**IMPORTANT**: When you finish creating the implementation plan, save it to:
`docs/plans/2026-02-11_HHMM_dev_environment_setup.md`

The plan file should include:
- Summary of the approach
- Step-by-step implementation tasks
- Files to modify with specific changes
- Testing strategy
- Verification checklist
