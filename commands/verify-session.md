---
description: Verify session handoff files are correct
---

Run verification checks to ensure session handoff is properly configured:

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

# 1. Check which handoff CLAUDE.md imports
echo "📋 CLAUDE.md imports:"
grep "@NEXT_SESSION_PROMPT" "$PROJECT_ROOT/CLAUDE.md"

# 2. Check if that file exists
echo ""
echo "📄 Handoff file exists:"
ls -lh "$PROJECT_ROOT"/NEXT_SESSION_PROMPT_*.md

# 3. Check for multiple handoffs in root (should be only 1)
echo ""
echo "🔍 Number of handoffs in root:"
ls -1 "$PROJECT_ROOT"/NEXT_SESSION_PROMPT_*.md 2>/dev/null | wc -l

# 4. Check latest session summary
echo ""
echo "📊 Latest session summary:"
ls -lht "$PROJECT_ROOT"/SESSION_SUMMARY_*.md 2>/dev/null | head -1

# 5. Check archived handoffs
echo ""
echo "📦 Archived handoffs:"
ls -lht "$PROJECT_ROOT/docs/archive/sessions"/NEXT_SESSION_PROMPT_*.md 2>/dev/null | head -3

# 6. Check for active plan files in project
echo ""
echo "📝 Project plan files (docs/plans/):"
ls -lht "$PROJECT_ROOT/docs/plans"/*.md 2>/dev/null | head -3 || echo "   No plan files in project"

# 7. Check for recent global plan files (last 7 days)
echo ""
echo "🌐 Recent global plan files (~/.claude/plans/):"
find ~/.claude/plans -name "*.md" -mtime -7 -exec ls -lh {} \; 2>/dev/null || echo "   No recent global plans"

# 8. Check Findings Tracker status with lifecycle verification
echo ""
echo "🔎 Findings Trackers:"
TRACKERS=$(ls -t "$PROJECT_ROOT"/docs/findings/*_FINDINGS_TRACKER.md 2>/dev/null)
if [ -n "$TRACKERS" ]; then
    echo "$TRACKERS" | while read TRACKER; do
        echo ""
        echo "   --- $(basename "$TRACKER") ---"
        echo "   Last Updated:"
        grep "Last Updated" "$TRACKER" 2>/dev/null | head -1 | awk '{print "      " $0}'
        SCOPE=$(grep "^\\*\\*Scope\\*\\*:" "$TRACKER" 2>/dev/null | head -1)
        if [ -n "$SCOPE" ]; then
            echo "   $SCOPE"
        fi
        echo "   Finding statuses (with Stage):"
        grep -E "^\| F[0-9]" "$TRACKER" 2>/dev/null | awk '{print "      " $0}'
        OPEN=$(grep -c "\- \[ \]" "$TRACKER" 2>/dev/null)
        DONE=$(grep -c "\- \[x\]" "$TRACKER" 2>/dev/null)
        TOTAL=$((OPEN + DONE))
        echo "   Tasks: $DONE completed, $OPEN remaining (of $TOTAL total)"
        echo "   Lifecycle progress:"
        # Extract F-numbers and their stages
        grep -E "^\*\*Stage\*\*:" "$TRACKER" 2>/dev/null | while read STAGE_LINE; do
            echo "      $STAGE_LINE"
        done
    done
    # Stage consistency checks
    echo ""
    echo "   Stage consistency checks:"
    echo "   (Verify: investigation report exists → Stage ≥ Investigating)"
    echo "   (Verify: RCA exists → Stage ≥ RCA Complete)"
    echo "   (Verify: design exists → Stage ≥ Designing)"
    echo "   (Verify: blueprint exists → Stage ≥ Blueprint Ready)"
    echo "   (Verify: plan exists → Stage ≥ Planned)"
    echo "   (Run manually: cross-reference docs/investigations/, docs/RCAs/, docs/design/, docs/blueprints/, docs/plans/ against tracker stages)"
else
    echo "   No Findings Trackers found (docs/findings/*_FINDINGS_TRACKER.md)"
fi

# 9. Check key project documents were updated
echo ""
echo "📚 Key project documents (should be updated on session-end):"
echo "   IMPLEMENTATION_PLAN.md:"
ls -lh "$PROJECT_ROOT/IMPLEMENTATION_PLAN.md" 2>/dev/null | awk '{print "      " $6, $7, $8, $9}'
grep "Last Updated" "$PROJECT_ROOT/IMPLEMENTATION_PLAN.md" 2>/dev/null | head -1 | awk '{print "      Version:", $0}'
echo "   ARCHITECTURE.md:"
ls -lh "$PROJECT_ROOT/ARCHITECTURE.md" 2>/dev/null | awk '{print "      " $6, $7, $8, $9}' || echo "      Not found"
echo "   CLAUDE.md Last Updated:"
grep "Last Updated" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null | head -1 | awk '{print "      " $0}'
```

**Interpret results:**

✅ **All good if:**
- CLAUDE.md imports exactly one NEXT_SESSION_PROMPT file
- That file exists in root directory
- Only ONE handoff in root (the latest)
- Session summary exists for same date
- Old handoffs are in archive
- Global plan files are copied to project (docs/plans/)
- IMPLEMENTATION_PLAN.md "Last Updated" matches session date
- CLAUDE.md "Last Updated" matches session date
- All relevant Findings Trackers have "Last Updated" matching session date (if findings work was done)
- Findings Tracker task checkboxes reflect work completed this session
- Findings Tracker Stage column is consistent with existing artifacts (e.g., if investigation report exists, Stage should be ≥ Investigating)
- Lifecycle tables have rows for each completed stage transition

❌ **Problems if:**
- CLAUDE.md imports a file that doesn't exist
- Multiple handoffs in root directory
- No session summary for latest handoff
- Old handoffs not archived
- Recent global plan files not copied to project
- IMPLEMENTATION_PLAN.md not updated (stale "Last Updated")
- Key project documents out of sync with handoff
- Any Findings Tracker not updated after related work was done (stale checkboxes or status)
- Findings Tracker changelog missing entry for current session
- Findings Tracker Stage inconsistent with artifacts (e.g., investigation exists but Stage still `Open`)
- Lifecycle table missing rows for completed stage transitions

**If problems found, suggest fixes:**
- Update CLAUDE.md line 24 to point to correct file
- Archive extra handoffs to docs/archive/sessions/
- Create missing session summary
- Copy global plan files to docs/plans/ for persistence
- Update IMPLEMENTATION_PLAN.md with current session status
- Ensure all "Last Updated" timestamps match session date
- Update Findings Tracker: check off completed tasks, update finding statuses and stages, backfill lifecycle rows, add changelog entry
