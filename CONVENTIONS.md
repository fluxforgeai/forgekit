# ForgeKit Project Conventions

ForgeKit skills expect projects to follow these directory conventions. Create directories as needed.

## Expected Directory Structure

```
your-project/
├── CLAUDE.md                      # Project context (auto-loaded by Claude Code)
├── docs/
│   ├── incidents/                 # /incident writes here
│   ├── investigations/            # /investigate writes here
│   ├── RCAs/                      # /rca-bugfix writes RCA reports here
│   ├── prompts/                   # /rca-bugfix writes fix prompts here
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

Skills communicate through shared documents:

| Artifact | Written By | Read By |
|----------|-----------|---------|
| `docs/RCAs/*.md` | rca-bugfix | investigate, analyze |
| `docs/incidents/*.md` | incident | investigate, analyze |
| `docs/analysis/*.md` | analyze | design, investigate |
| `docs/design/*.md` | design | (implementation) |
| `docs/research/*.md` | research | investigate, design |
| `system-map.md` | analyze | analyze (refreshed each run) |
| `docs/prompts/*.md` | rca-bugfix | plan mode |
