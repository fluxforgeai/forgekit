---
description: Start new session with full context and greeting
---

Good morning/afternoon/evening Johan!

**Get current time first:**
```bash
date '+%A, %B %d, %Y at %H:%M %Z'
```

Then provide your greeting:

```
Good [morning/afternoon/evening] Johan!

It's [current_date_time] in Pretoria, South Africa.

I've read the session handoff and I'm now oriented with the this project.
```

**Read the following documents** (already auto-loaded via CLAUDE.md):
1. ✅ CLAUDE.md (auto-loaded)
2. ✅ NEXT_SESSION_PROMPT_{latest}.md (auto-imported)
3. ✅ APPLICATION_STATE_AND_GAP_ANALYSIS.md
4. ✅ INTERCOM_API_DATE_FILTERING_LIMITATIONS.md
5. ✅ PRD.md
6. ✅ IMPLEMENTATION_PLAN.md

**Check for active plan files:**
1. Check `docs/plans/` for recent plan files
2. Check `~/.claude/plans/` for any plans modified in last 7 days
3. If active plan exists, read it and note:
   - Current phase/status
   - What phases are complete
   - What's next

**Then summarize:**
- Project name and purpose
- Current status (what's working, what's missing)
- **Active plan status** (if any plan file exists)
- Current priorities (list top 3)
- What was completed last session
- Ask: "What would you like to work on today?"

**Format your response clearly with:**
- Greeting with time and location
- Project context
- Status summary (with ✅ and ❌)
- Active plan summary (if applicable)
- Priorities list
- Question about what to work on

This ensures Johan knows you have full context and are ready to work.
