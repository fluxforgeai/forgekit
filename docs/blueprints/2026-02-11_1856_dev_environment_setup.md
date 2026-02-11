# Blueprint: ForgeKit Development Environment Setup

**Date**: 2026-02-11
**Design Reference**: docs/design/2026-02-11_1848_dev_environment_strategy.md
**Finding Reference**: docs/findings/2026-02-11_1837_missing_dev_environment_infrastructure.md (F1)

## Objective

Complete the ForgeKit development environment by implementing the remaining infrastructure from the design analysis: pre-commit hooks, tool configuration, initial test suite, CI/CD pipeline, and .gitignore hardening. The foundation (.venv, dependency groups, uv.lock) is already in place.

## Requirements

1. **Pre-commit hooks** — ruff (lint + format), uv-lock sync check, mypy type checking
2. **Tool configuration** — ruff, mypy, and pytest settings in pyproject.toml
3. **Initial test suite** — tests for CLI entry point and core commands (init, status, uninstall)
4. **CI/CD pipeline** — GitHub Actions running lint + test across Python 3.10-3.13
5. **.gitignore hardening** — cover all tool caches, macOS artifacts, coverage output
6. **Commit dev environment** — uv.lock + pyproject.toml changes committed to git

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Single .venv + uv groups | Chosen (score 97/105) | Simplicity, Phase 2 workspace readiness, symlink compatibility |
| ruff for lint AND format | ruff replaces flake8+isort+black | Single tool, Rust-fast, uv ecosystem alignment |
| Local mypy hook | Run from venv, not pre-commit's isolated env | Needs project context and type stubs |
| pytest with coverage | pytest-cov plugin | Standard, already installed |
| GitHub Actions | uv-native CI | `astral-sh/setup-uv@v5` action, `--frozen` for reproducibility |

## Scope

### In Scope
- `.pre-commit-config.yaml` with ruff, uv-lock, and mypy hooks
- `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]` sections in pyproject.toml
- `tests/test_cli.py` covering core CLI functionality
- `.github/workflows/ci.yml` with lint and test jobs
- `.gitignore` additions for tool caches and macOS artifacts
- Git commit of all dev environment changes (pyproject.toml, uv.lock)

### Out of Scope
- Phase 2 workspace config (`[tool.uv.workspace]`) — not needed until server/ exists
- Makefile/justfile task runner — uv run is sufficient for now
- `.python-version` file — pyproject.toml `requires-python` is sufficient
- README update for contributor dev setup — separate concern
- Server package tests — no server package exists yet

## Files to Create

### 1. `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.9.24
    hooks:
      - id: uv-lock

  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run mypy
        language: system
        types: [python]
        pass_filenames: false
        args: [src/]
```

**Notes**:
- ruff and ruff-format use the pre-commit repo (Rust binary, no Python needed, fast)
- uv-lock ensures `uv.lock` stays in sync with pyproject.toml
- mypy uses a `local` hook running `uv run mypy` so it uses the venv's installed packages and type stubs — pre-commit's isolated environments can't see project dependencies

### 2. `tests/__init__.py`

Empty file. Required for Python test package.

### 3. `tests/test_cli.py`

```python
"""Tests for ForgeKit CLI."""
import subprocess
from pathlib import Path

import pytest

from forgekit.cli import get_forgekit_root


def test_get_forgekit_root():
    """get_forgekit_root() returns the repo root (contains pyproject.toml)."""
    root = get_forgekit_root()
    assert root.is_dir()
    assert (root / "pyproject.toml").exists()
    assert (root / "skills").is_dir()
    assert (root / "commands").is_dir()


def test_cli_help():
    """forgekit --help exits 0 and shows usage."""
    result = subprocess.run(
        ["uv", "run", "forgekit", "--help"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "ForgeKit" in result.stdout


def test_cli_status(capsys):
    """forgekit status runs without error."""
    from forgekit.cli import cmd_status

    class Args:
        pass

    cmd_status(Args())
    captured = capsys.readouterr()
    assert "ForgeKit v" in captured.out


def test_cmd_init_creates_symlinks(tmp_path, monkeypatch):
    """forgekit init creates skills and commands symlinks."""
    monkeypatch.chdir(tmp_path)

    from forgekit.cli import cmd_init

    class Args:
        pass

    cmd_init(Args())

    claude_dir = tmp_path / ".claude"
    assert claude_dir.is_dir()
    assert (claude_dir / "skills").is_symlink()
    assert (claude_dir / "commands").is_symlink()

    # Symlinks point to real directories with content
    assert (claude_dir / "skills").is_dir()
    assert (claude_dir / "commands").is_dir()

    # Marker file created
    marker = tmp_path / ".forgekit"
    assert marker.exists()
    content = marker.read_text()
    assert "version=0.1.0" in content


def test_cmd_uninstall_removes_symlinks(tmp_path, monkeypatch):
    """forgekit uninstall removes symlinks and marker."""
    monkeypatch.chdir(tmp_path)

    from forgekit.cli import cmd_init, cmd_uninstall

    class Args:
        pass

    # First init, then uninstall
    cmd_init(Args())
    cmd_uninstall(Args())

    claude_dir = tmp_path / ".claude"
    assert not (claude_dir / "skills").exists()
    assert not (claude_dir / "commands").exists()
    assert not (tmp_path / ".forgekit").exists()


def test_cmd_init_replaces_existing_symlink(tmp_path, monkeypatch):
    """forgekit init replaces an existing symlink without error."""
    monkeypatch.chdir(tmp_path)

    from forgekit.cli import cmd_init

    class Args:
        pass

    # Init twice — second call should replace symlinks
    cmd_init(Args())
    cmd_init(Args())

    claude_dir = tmp_path / ".claude"
    assert (claude_dir / "skills").is_symlink()
    assert (claude_dir / "commands").is_symlink()
```

**Coverage targets**:
- `get_forgekit_root()` — path resolution
- CLI entry point accessibility (`--help`)
- `cmd_status` — runs without crash
- `cmd_init` — symlink creation, marker file
- `cmd_uninstall` — symlink removal, marker cleanup
- `cmd_init` idempotency — replacing existing symlinks

**Not tested** (deferred):
- `cmd_update/diff/commit/push` — git operations that modify repo state; need mock infrastructure
- Error paths — e.g., existing non-symlink directory blocking init

### 4. `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --frozen --group dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy src/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: uv sync --frozen --group test
      - run: uv run pytest --cov=forgekit --cov-report=term-missing
```

**Key decisions**:
- `--frozen` fails if `uv.lock` is out of sync (catches forgotten lock updates)
- Lint job uses `--group dev` (ruff, mypy); test job uses `--group test` (pytest, pytest-cov)
- Matrix tests Python 3.10 through 3.13 (per `requires-python = ">=3.10"`)
- Coverage report in terminal output (no upload to external service yet)

## Files to Modify

### 5. `pyproject.toml` — Add tool configuration sections

Append after existing content:

```toml
[tool.ruff]
target-version = "py310"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
packages = ["forgekit"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Rationale**:
- `target-version = "py310"` — matches `requires-python`
- `line-length = 120` — modern standard, avoids excessive wrapping
- `select = ["E", "F", "I", "W"]` — errors, pyflakes, isort, warnings (conservative, no opinionated style rules)
- mypy `packages = ["forgekit"]` — scopes type checking to the CLI package
- pytest `testpaths = ["tests"]` — explicit test directory

### 6. `.gitignore` — Add tool cache exclusions

Add these lines:

```
# Tool caches
.mypy_cache/
.pytest_cache/
.ruff_cache/

# Coverage
.coverage
htmlcov/

# macOS
.DS_Store

# Environment
.env
.env.local
```

## Implementation Sequence

1. **Update pyproject.toml** — Add `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]` sections
   - Must come first so ruff/mypy/pytest use correct config when run in later steps

2. **Update .gitignore** — Add tool caches, macOS artifacts, coverage exclusions
   - Before running tools that generate caches

3. **Create .pre-commit-config.yaml** — Hook configuration
   - After tool config exists in pyproject.toml

4. **Run `pre-commit install`** — Activate hooks
   - After config file exists

5. **Create tests/__init__.py and tests/test_cli.py** — Initial test suite
   - After pytest config is in pyproject.toml

6. **Run test suite** — Verify tests pass
   - `uv run pytest --cov=forgekit --cov-report=term-missing`

7. **Run linters** — Verify clean output
   - `uv run ruff check .`
   - `uv run ruff format --check .`
   - `uv run mypy src/`

8. **Create .github/workflows/ci.yml** — CI pipeline
   - After tests and linters verified locally

9. **Commit all changes** — Single commit with all dev environment setup
   - Includes: pyproject.toml, uv.lock, .gitignore, .pre-commit-config.yaml, tests/, .github/workflows/

## Dependencies & Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ruff pre-commit rev doesn't match installed version | Low | Low | Pin to v0.15.0 (matches `uv sync` install) |
| mypy finds type errors in existing CLI code | Medium | Low | Fix errors or add type: ignore where justified |
| CI fails on Python 3.10 due to syntax | Low | Medium | CLI uses only basic stdlib; test locally with 3.10 |
| pre-commit install requires hook directory | Very Low | Very Low | `.git/hooks/` exists since git repo is initialized |

## Acceptance Criteria

- [ ] `uv run ruff check .` exits 0 (no lint errors)
- [ ] `uv run ruff format --check .` exits 0 (code already formatted)
- [ ] `uv run mypy src/` exits 0 (no type errors)
- [ ] `uv run pytest --cov=forgekit` exits 0, all tests pass
- [ ] `pre-commit run --all-files` exits 0 (all hooks pass)
- [ ] `.github/workflows/ci.yml` exists and defines lint + test jobs
- [ ] `uv.lock` is committed to git
- [ ] All tool caches are gitignored

## Constraints

- CLI must remain zero-dependency (NFR-006) — no runtime imports added
- Tests must not modify the actual forgekit repo (use tmp_path fixtures)
- All tool config lives in pyproject.toml (no separate .ruff.toml, mypy.ini, etc.)
- Pre-commit hooks must work with `uv run` (not require separate installs)
