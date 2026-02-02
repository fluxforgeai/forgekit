# ForgeKit Project Conventions

ForgeKit skills expect projects to follow these directory conventions. Create directories as needed.

## Expected Directory Structure

```
your-project/
├── CLAUDE.md                      # Project context (auto-loaded by Claude Code)
├── docs/
│   ├── incidents/                 # /incident writes here
│   ├── findings/                  # /finding writes here (proactive discoveries)
│   ├── investigations/            # /investigate writes here
│   ├── blueprints/                # /blueprint writes implementation specs here
│   ├── RCAs/                      # /rca-bugfix writes RCA reports here
│   ├── prompts/                   # /rca-bugfix and /blueprint write prompts here
│   ├── analysis/                  # /analyze writes reports here
│   ├── design/                    # /design writes reports here
│   ├── research/                  # /research writes findings here
│   ├── monitoring/                # /watchdog writes monitoring reports here
│   ├── plans/                     # Implementation plans
│   └── archive/
│       └── sessions/              # Archived session handoffs
├── NEXT_SESSION_PROMPT_*.md       # Current session handoff (root)
├── SESSION_SUMMARY_*.md           # Current session summary (root)
└── system-map.md                  # /analyze shared artifact (auto-created)
```

## File Naming Convention

All ForgeKit artifacts use this format:

```
{YYYY-MM-DD_HHMM}_{description}.md
```

Examples:
- `2026-01-22_1700_stream_download_timeout.md`
- `2026-01-26_1410_skills_integration_architecture.md`

## Shared Artifacts

Skills communicate through shared documents. Each artifact is written by one skill and read by downstream skills, creating a feedback loop (institutional memory).

| Artifact | Written By | Read By |
|----------|-----------|---------|
| `docs/findings/*.md` | finding | investigate, analyze, rca-bugfix, research |
| `docs/incidents/*.md` | incident | investigate, analyze |
| `docs/investigations/*.md` | investigate | rca-bugfix, analyze |
| `docs/RCAs/*.md` | rca-bugfix | investigate, analyze |
| `docs/research/*.md` | research | investigate, design, blueprint |
| `docs/analysis/*.md` | analyze | design, investigate, finding |
| `docs/design/*.md` | design | blueprint, (implementation) |
| `docs/blueprints/*.md` | blueprint | plan mode |
| `docs/prompts/*.md` | rca-bugfix, blueprint | plan mode |
| `system-map.md` | analyze | analyze (refreshed each run) |
