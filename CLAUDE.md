# ForgeKit — Project Context

**Project**: ForgeKit - AI Engineering Skills Toolkit by FluxForge AI
**Owner**: Johan Genis
**Repo**: ~/Projects/forgekit

---

## Key Documents

- `README.md` — Full product documentation and usage guide
- `ARCHITECTURE.md` — System design, Phase 1 + Phase 2 architecture
- `IMPLEMENTATION_PLAN.md` — Phased roadmap with session progress log
- `PRD.md` — Product requirements
- `CONVENTIONS.md` — Directory structure and file naming conventions

---

## Development Environment

- **Package manager**: uv (v0.9.24+)
- **Virtual environment**: `.venv` named `forgekit` (single venv, uv dependency groups)
- **Setup**: `uv venv .venv --prompt forgekit && uv sync --group dev --group test`
- **Design decision**: `docs/design/2026-02-11_1848_dev_environment_strategy.md`

---

## Active Findings Trackers

- `docs/findings/2026-02-11_1837_dev_environment_infrastructure_FINDINGS_TRACKER.md` — F1: Blueprint Ready

---

<!-- SESSION_CONFIG_START -->
user_name: Johan
project_name: ForgeKit
timezone: SAST (UTC+2)
session_docs:
  - IMPLEMENTATION_PLAN.md
  - ARCHITECTURE.md
<!-- SESSION_CONFIG_END -->

<!-- SESSION_HANDOFF_START -->
@NEXT_SESSION_PROMPT_2026-02-11_1929.md
<!-- SESSION_HANDOFF_END -->

---

**Last Updated**: 2026-02-11
**Last Session**: Session 1 (2026-02-11) — Dev environment bootstrap, design analysis, blueprint
