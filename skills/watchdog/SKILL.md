# Watchdog - Passive Monitoring Skill

## Trigger

```
/watchdog {what to monitor - description of fix or process}
```

## Examples

```
/watchdog Monitor extraction after retry logic fix - watch for timeout errors
/watchdog Watch backend after GCS upload fix - look for upload failures
/watchdog Monitor batch job API after endpoint fix
```

---

## Description

A **fully autonomous bash script** that monitors logs after a fix is implemented. Runs independently without Claude - creates incident files and sends Telegram alerts when errors occur.

### Key Behaviors

| Setting | Value |
|---------|-------|
| Monitoring style | **Passive** - watch logs/messages |
| Check interval | **60 seconds** |
| On error detected | **Create incident file + Telegram alert** |
| Error de-duplication | **Don't repeat same/similar errors** |
| After incident | **Continue monitoring** (don't stop) |
| Manual stop | **Run until user stops it** |
| Alerts | **Log + Telegram** (different alerts for system vs fix-related) |
| Incident tagging | **"system" vs "fix-related"** based on pattern matched |
| Status surfacing | **Every 60 seconds** to status file |
| **Autonomy** | **Runs independently** - no Claude session required |

### Autonomous Operation

**IMPORTANT**: Once started, the watchdog runs as a standalone bash script:

1. **Does NOT require Claude** to be running
2. **Does NOT require user to be awake**
3. **Sends Telegram alerts** directly to your phone
4. **Creates incident JSON files** for later review

**Workflow when you're asleep:**
```
1. You start watchdog and go to sleep
2. Watchdog detects error at 3am
3. Creates incident file: /tmp/watchdog_{id}_incidents/fix-related_20260122_030000.json
4. Sends Telegram: "🎯🔴 WATCHDOG: Fix-Related Error! Run /incident in Claude"
5. You wake up, see Telegram notification
6. Start Claude, run: /incident {error summary}
   OR read incident files: cat /tmp/watchdog_{id}_incidents/*.json
```

**What the script can do autonomously:**
- Check docker logs every 60 seconds
- Detect errors using pattern matching
- Tag incidents as "system" or "fix-related"
- Create JSON incident files with full stack traces
- Send Telegram alerts with error details
- Update status file for later review
- De-duplicate repeated errors

**What requires Claude (when you're back):**
- Running `/incident` to create formal incident report
- Investigating the root cause
- Implementing fixes

---

## Instructions

### Step 1: Parse Input and Understand Context

1. **Parse the user's input** to understand:
   - What was fixed
   - What process to monitor
   - What errors to watch for

2. **Read recent context documents** (if relevant):
   - Recent `docs/RCAs/*.md` files
   - Recent `docs/plans/*.md` files
   - Recent `docs/investigations/*.md` files

3. **Identify FIX-SPECIFIC error patterns** based on the fix context. These are CRITICAL for tagging incidents correctly.

   Examples:
   - If fix was for "retry logic for timeouts" → fix patterns: `ReadTimeout|ConnectTimeout|timed out`
   - If fix was for "GCS upload" → fix patterns: `GCS|upload.*fail|storage`
   - If fix was for "URL refresh" → fix patterns: `refresh|_fetch_all_export_files|URLExpired`

4. **Store patterns in two categories**:
   - `SYSTEM_PATTERNS`: General errors (always the same)
   - `FIX_PATTERNS`: Specific to what was fixed (varies per session)

### Step 2: Create Monitoring Session

1. **Generate a unique session ID**:
   ```bash
   SESSION_ID=$(date -u '+%Y%m%d_%H%M%S')_$(head -c 4 /dev/urandom | xxd -p)
   ```

2. **Identify log sources** to monitor:
   - Backend container: `docker logs {container_name} --since 1m`
   - Other relevant containers or log files
   - Ask the user which container(s) or log files to monitor

3. **Create the monitoring report** at `docs/monitoring/{YYYY-MM-DD_HHMM}_{name}.md`

4. **Define the fix-specific patterns** based on Step 1 analysis

### Step 3: Write Monitoring Report

Create a report at: `docs/monitoring/{YYYY-MM-DD_HHMM}_{name}.md`

Use this template:

```markdown
# Watchdog Session: {Description}

**Started**: {YYYY-MM-DD HH:MM} UTC
**Status**: Active (monitoring in background)
**Session ID**: {session_id}
**Mode**: Passive log watching (60s interval)
**De-duplication**: Enabled
**Incident Tagging**: system | fix-related

---

## Context

**What Was Fixed**: {from user input and recent RCAs/plans}
**What We're Watching For**: {error patterns relevant to the fix}

---

## Log Sources

| Source | Command |
|--------|---------|
| Backend container | `docker logs {container_name} --since 1m` |

---

## Error Patterns

### System-Wide Patterns (Smart Matching for JSON Logs)

| Pattern | Indicates | Notes |
|---------|-----------|-------|
| `"level":\s*"error"` | Error-level log entries | Matches actual errors, not field names |
| `"level":\s*"warning"` | Warning-level log entries | Catches warnings too |
| `Traceback` | Python tracebacks | Stack trace start |
| `_error"\|_failed"` | Event names ending in error/failed | e.g., `download_error`, `upload_failed` |
| `Exception:\|Error:` | Exception messages | Actual exception text |
| `CRITICAL\|FATAL` | Critical/fatal logs | Severe errors |

**Why Smart Matching?**
- Old pattern `error` matched `"parse_errors": 0` (false positive)
- New pattern `"level":\s*"error"` only matches actual error-level logs
- Prevents false positives from field names containing "error"

### Fix-Related Patterns (Specific to This Session)

| Pattern | Indicates |
|---------|-----------|
| {fix_pattern_1} | {description} |
| {fix_pattern_2} | {description} |
| {fix_pattern_3} | {description} |

---

## Control Commands

**Check watchdog status (reads latest status file)**:
```bash
cat /tmp/watchdog_{session_id}_status.json
```

**Check full watchdog log**:
```bash
tail -50 /tmp/watchdog_{session_id}.log
```

**Check reported incidents**:
```bash
cat /tmp/watchdog_{session_id}_reported.txt
```

**Check for incident files**:
```bash
ls -la /tmp/watchdog_{session_id}_incidents/
```

**Stop watchdog**:
```bash
kill $(cat /tmp/watchdog_{session_id}.pid) 2>/dev/null && echo "Stopped"
```

---

## System Incidents

| Time | Error | Incident File |
|------|-------|---------------|
| (none yet) | | |

---

## Fix-Related Incidents

| Time | Error | Incident File |
|------|-------|---------------|
| (none yet) | | |

---

## Latest Status

(Auto-updated every 60 seconds - read from `/tmp/watchdog_{session_id}_status.json`)
```

### Step 4: Start Background Monitoring Script

Use the Bash tool with `run_in_background: true` to start the monitoring script.

**IMPORTANT**: The script must:
1. Run in an infinite loop
2. Check logs every 60 seconds
3. De-duplicate errors using MD5 hashes
4. **Tag incidents as "system" or "fix-related"**
5. Create incident files with category tag
6. **Send DIFFERENT Telegram alerts** for each category
7. **Write status file every 60 seconds** for Claude to read
8. Continue monitoring after incidents (don't exit)

Here is the complete background script to execute:

```bash
#!/bin/bash
# Watchdog - Passive monitoring with incident tagging and status surfacing
# Tags incidents as "system" vs "fix-related"
# Different Telegram alerts per category
# Writes status file every 60 seconds for Claude to read

SESSION_ID="{session_id}"
LOG_FILE="/tmp/watchdog_${SESSION_ID}.log"
PID_FILE="/tmp/watchdog_${SESSION_ID}.pid"
REPORTED_FILE="/tmp/watchdog_${SESSION_ID}_reported.txt"
INCIDENT_DIR="/tmp/watchdog_${SESSION_ID}_incidents"
STATUS_FILE="/tmp/watchdog_${SESSION_ID}_status.json"
INTERVAL=60

# ========================================
# PATTERN DEFINITIONS - CUSTOMIZE FIX_PATTERNS
# ========================================

# System-wide patterns (SMART matching for structured JSON logs)
# - Matches "level": "error" or "level": "warning" in JSON logs
# - Matches Python tracebacks
# - Matches event names ending in _error or _failed
# - Does NOT match field names like "parse_errors": 0
SYSTEM_PATTERNS='"level":\s*"error"|"level":\s*"warning"|Traceback|_error"|_failed"|Exception:|Error:|CRITICAL|FATAL'

# Fix-related patterns (CUSTOMIZE THIS based on what was fixed)
# Replace these with actual patterns from the fix context
FIX_PATTERNS="{fix_patterns_pipe_separated}"
FIX_DESCRIPTION="{fix_description}"

# ========================================
# SETUP
# ========================================

mkdir -p "$INCIDENT_DIR"

# Counters for status
SYSTEM_COUNT=0
FIX_COUNT=0
CHECK_COUNT=0
START_TIME=$(date -u '+%Y-%m-%d %H:%M:%S UTC')

# Get Telegram credentials from backend container (customize container name)
TELEGRAM_BOT_TOKEN=$(docker exec ${CONTAINER_NAME} printenv TELEGRAM_BOT_TOKEN 2>/dev/null || echo "")
TELEGRAM_CHAT_ID=$(docker exec ${CONTAINER_NAME} printenv TELEGRAM_CHAT_ID 2>/dev/null || echo "")

# ========================================
# FUNCTIONS
# ========================================

send_telegram() {
    local msg="$1"
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=${msg}" \
            -d "parse_mode=HTML" > /dev/null 2>&1
    fi
}

is_duplicate() {
    local error_sig="$1"
    local hash=$(echo "$error_sig" | md5 2>/dev/null || echo "$error_sig" | md5sum | cut -d' ' -f1)
    if grep -q "$hash" "$REPORTED_FILE" 2>/dev/null; then
        return 0  # Is duplicate
    else
        echo "$hash" >> "$REPORTED_FILE"
        return 1  # Is new
    fi
}

# Determine if error matches fix-related patterns
is_fix_related() {
    local error_line="$1"
    if [ -n "$FIX_PATTERNS" ] && echo "$error_line" | grep -qiE "$FIX_PATTERNS"; then
        return 0  # Is fix-related
    else
        return 1  # Is system
    fi
}

create_incident() {
    local category="$1"      # "system" or "fix-related"
    local error_type="$2"
    local summary="$3"
    local stack_trace="$4"
    local timestamp=$(date -u '+%Y-%m-%d %H:%M:%S UTC')
    local incident_file="$INCIDENT_DIR/${category}_$(date -u '+%Y%m%d_%H%M%S').json"

    # Escape stack trace for JSON
    local escaped_trace=$(echo "$stack_trace" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')

    cat > "$incident_file" << INCIDENTEOF
{
  "timestamp": "$timestamp",
  "category": "$category",
  "error_type": "$error_type",
  "summary": "$summary",
  "stack_trace": $escaped_trace,
  "session_id": "$SESSION_ID",
  "log_file": "$LOG_FILE",
  "fix_context": "$FIX_DESCRIPTION"
}
INCIDENTEOF

    echo "[$category] INCIDENT: $summary" >> "$LOG_FILE"
    echo "   File: $incident_file" >> "$LOG_FILE"

    # Different Telegram alerts based on category
    if [ "$category" = "fix-related" ]; then
        # Fix-related: Red alert with target emoji
        send_telegram "🎯🔴 <b>WATCHDOG: Fix-Related Error!</b>

<b>Category:</b> FIX-RELATED
<b>Type:</b> $error_type
<b>Summary:</b> $(echo "$summary" | head -c 200)
<b>Time:</b> $timestamp

⚠️ <i>This error is related to the fix being monitored!</i>
<b>Fix context:</b> $FIX_DESCRIPTION

Run in Claude: <code>/incident $summary</code>"
        ((FIX_COUNT++))
    else
        # System: Yellow warning
        send_telegram "⚠️ <b>WATCHDOG: System Error</b>

<b>Category:</b> SYSTEM
<b>Type:</b> $error_type
<b>Summary:</b> $(echo "$summary" | head -c 200)
<b>Time:</b> $timestamp

<i>General system error (not related to current fix)</i>

Run in Claude: <code>/incident $summary</code>"
        ((SYSTEM_COUNT++))
    fi
}

# Write status file for Claude to read
write_status() {
    local timestamp=$(date -u '+%Y-%m-%d %H:%M:%S UTC')
    local uptime_seconds=$(($(date +%s) - $(date -d "$START_TIME" +%s 2>/dev/null || echo "0")))

    cat > "$STATUS_FILE" << STATUSEOF
{
  "session_id": "$SESSION_ID",
  "status": "active",
  "started": "$START_TIME",
  "last_check": "$timestamp",
  "checks_completed": $CHECK_COUNT,
  "incidents": {
    "system": $SYSTEM_COUNT,
    "fix_related": $FIX_COUNT,
    "total": $((SYSTEM_COUNT + FIX_COUNT))
  },
  "fix_context": "$FIX_DESCRIPTION",
  "fix_patterns": "$FIX_PATTERNS",
  "last_log_lines": $(tail -5 "$LOG_FILE" 2>/dev/null | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),
  "message": "Watchdog active. $CHECK_COUNT checks completed. $((SYSTEM_COUNT + FIX_COUNT)) incidents found ($FIX_COUNT fix-related, $SYSTEM_COUNT system)."
}
STATUSEOF
}

# ========================================
# MAIN LOOP
# ========================================

# Save PID
echo $$ > "$PID_FILE"

echo "========================================" >> "$LOG_FILE"
echo "Watchdog Started: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$LOG_FILE"
echo "Mode: Passive monitoring with incident tagging" >> "$LOG_FILE"
echo "De-duplication: Enabled" >> "$LOG_FILE"
echo "Interval: ${INTERVAL}s" >> "$LOG_FILE"
echo "Fix patterns: $FIX_PATTERNS" >> "$LOG_FILE"
echo "Fix context: $FIX_DESCRIPTION" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Write initial status
write_status

send_telegram "🐕 <b>Watchdog Started</b>

<b>Session:</b> ${SESSION_ID}
<b>Mode:</b> Passive monitoring
<b>Interval:</b> 60 seconds
<b>Tagging:</b> system | fix-related

<b>Watching for:</b>
$FIX_DESCRIPTION

Status file: <code>/tmp/watchdog_${SESSION_ID}_status.json</code>"

while true; do
    TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M:%S UTC')
    ((CHECK_COUNT++))

    echo "" >> "$LOG_FILE"
    echo "--- Check #$CHECK_COUNT: $TIMESTAMP ---" >> "$LOG_FILE"

    # Fetch recent logs from backend container (customize container name)
    LOGS=$(docker logs ${CONTAINER_NAME} --since "${INTERVAL}s" 2>&1)

    # Check for errors (case insensitive, all patterns)
    ALL_PATTERNS="$SYSTEM_PATTERNS"
    if [ -n "$FIX_PATTERNS" ]; then
        ALL_PATTERNS="$ALL_PATTERNS|$FIX_PATTERNS"
    fi

    ERRORS=$(echo "$LOGS" | grep -iE "$ALL_PATTERNS" | grep -v "No errors" | head -20)

    if [ -n "$ERRORS" ]; then
        echo "Found potential errors:" >> "$LOG_FILE"
        echo "$ERRORS" >> "$LOG_FILE"

        # Process each unique error line
        echo "$ERRORS" | while IFS= read -r ERROR_LINE; do
            [ -z "$ERROR_LINE" ] && continue

            # Determine category
            if is_fix_related "$ERROR_LINE"; then
                CATEGORY="fix-related"
            else
                CATEGORY="system"
            fi

            # Extract error type
            ERROR_TYPE=$(echo "$ERROR_LINE" | grep -oE "(Error|Exception|Timeout|Failed)" | head -1)
            ERROR_TYPE=${ERROR_TYPE:-"Error"}

            # Check if duplicate (include category in signature)
            if ! is_duplicate "$CATEGORY:$ERROR_TYPE:$ERROR_LINE"; then
                # Get more context
                STACK_TRACE=$(echo "$LOGS" | grep -A 10 -B 2 "$(echo "$ERROR_LINE" | head -c 50)" | head -30)
                create_incident "$CATEGORY" "$ERROR_TYPE" "$ERROR_LINE" "$STACK_TRACE"
            else
                echo "  [$CATEGORY] (duplicate - skipped)" >> "$LOG_FILE"
            fi
        done
    else
        echo "✓ No errors detected" >> "$LOG_FILE"
    fi

    # Write status file every check (for Claude to read)
    write_status

    sleep $INTERVAL
done
```

### Step 5: Execute Background Script

**CRITICAL**: Before executing, you MUST replace these placeholders:
- `{session_id}` - The generated session ID
- `{fix_patterns_pipe_separated}` - Pipe-separated regex patterns for the fix (e.g., `ReadTimeout|ConnectTimeout|timed out`)
- `{fix_description}` - Human-readable description of what was fixed

Use the Bash tool with these parameters:

```
command: <the script above with placeholders replaced>
run_in_background: true
description: "Watchdog monitoring - passive log watcher with incident tagging"
```

### Step 6: Confirm to User (Keep It Simple!)

After starting the background process, respond with a **simple, clean confirmation**:

```
Watchdog started. Session: {session_id}

Watching for: {brief description of fix patterns}
Alerts: Telegram + incident files
Interval: 60 seconds

Safe to sleep - I'll alert you via Telegram if errors occur.

To check status: "check watchdog"
To stop: "stop watchdog"
```

**DO NOT include:**
- Complex tables
- Long file paths
- Redundant information
- Technical details about patterns

Keep it short and actionable.

### Step 7: STOP and Await

**IMPORTANT**: After confirming to the user, **STOP** your response. The monitoring is running in the background.

- Do NOT continuously check the logs
- Do NOT poll the background process
- The status file is updated every 60 seconds
- Telegram alerts provide immediate push notifications

The user can:
- Ask you to check watchdog status (you'll read the status file)
- Ask you to read incident files
- Ask you to stop the watchdog
- Continue with other work while watchdog runs

---

## When User Asks to Check Watchdog

If the user asks "check watchdog" or similar:

1. **Read the status file and incident files**:
   ```bash
   cat /tmp/watchdog_{session_id}_status.json
   cat /tmp/watchdog_{session_id}_incidents/*.json 2>/dev/null
   ```

2. **Present a SIMPLE status report showing ACTUAL ERRORS**:

   ```
   **Watchdog Status**

   Running: Yes | Checks: {count} | Since: {start_time}

   **Incidents: {total_count}** ({fix_count} fix-related, {system_count} system)

   {IF incidents exist, show them directly:}

   ---
   🎯 **Fix-Related Error** (high priority)
   Time: {timestamp}
   Error: {actual error message from JSON}
   Stack: {first 3 lines of stack trace}
   ---

   ⚠️ **System Error**
   Time: {timestamp}
   Error: {actual error message}
   ---

   {IF no incidents:}
   No errors detected so far.
   ```

3. **SHOW THE ACTUAL ERRORS** - do not just list file paths!
   - Extract `summary` and `stack_trace` from each incident JSON
   - Display the error message directly
   - Show first few lines of stack trace
   - User should NOT need to run any commands to see errors

---

## When User Asks to Stop Watchdog

If the user asks "stop watchdog" or similar:

1. **Stop the process**:
   ```bash
   kill $(cat /tmp/watchdog_{session_id}.pid) 2>/dev/null && echo "Stopped" || echo "Not running"
   ```

2. **Read final status and any incidents**:
   ```bash
   cat /tmp/watchdog_{session_id}_status.json
   cat /tmp/watchdog_{session_id}_incidents/*.json 2>/dev/null
   ```

3. **Present final summary WITH any errors shown directly**:

   ```
   **Watchdog Stopped**

   Session: {session_id}
   Runtime: {duration}
   Total checks: {count}

   **Final Incident Summary:**
   - Fix-related: {count}
   - System: {count}

   {IF incidents exist, list each error summary directly}

   {IF no incidents:}
   No errors detected during monitoring.
   ```

---

## Error Patterns Reference

### System-Wide Patterns (Category: "system")

These patterns use **smart matching** to avoid false positives from field names:

| Pattern | Regex | Indicates |
|---------|-------|-----------|
| Error-level logs | `"level":\s*"error"` | Actual error log entries |
| Warning-level logs | `"level":\s*"warning"` | Warning log entries |
| Python tracebacks | `Traceback` | Stack traces |
| Error events | `_error"\|_failed"` | Event names like `download_error` |
| Exception text | `Exception:\|Error:` | Exception messages |
| Critical logs | `CRITICAL\|FATAL` | Severe errors |

**Note**: Does NOT match field names like `"parse_errors": 0`

### Fix-Specific Patterns (Category: "fix-related")

These are determined per-session based on what was fixed. Examples:

| Fix Context | Patterns |
|-------------|----------|
| Retry logic for timeouts | `ReadTimeout\|ConnectTimeout\|timed out` |
| GCS upload fix | `GCS\|upload.*fail\|storage\|bucket` |
| URL refresh fix | `refresh\|_fetch_all_export_files\|URLExpired` |
| Batch job fix | `batch.*fail\|job.*fail\|initiate_export` |
| Stream download fix | `stream.*download\|StreamingChunk\|iter_bytes` |

---

## Notes

### Autonomous Operation
- **Runs as standalone bash script** - does NOT need Claude running
- **Safe to start and go to sleep** - will alert you via Telegram
- **Survives Claude session end** - keeps running until manually stopped
- **Creates incident files** - review them when you wake up

### Monitoring Behavior
- Status file updated every 60 seconds
- Fix-related incidents get red Telegram alerts (🎯🔴) - high priority!
- System incidents get yellow Telegram alerts (⚠️) - lower priority
- De-duplication prevents spam for repeated errors

### Cleanup
- Always stop watchdog when no longer needed: `kill $(cat /tmp/watchdog_{id}.pid)`
- Incident files persist in `/tmp/` until system reboot or manual cleanup
- Incident JSON files can be used with `/incident` skill for formal reports
