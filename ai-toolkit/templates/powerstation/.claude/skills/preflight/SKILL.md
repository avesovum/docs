---
name: preflight
description: Read-only start-of-session check for the Cape House project. Verifies MD5s, main.js/main-live.js byte identity and reads only the newest entries of the status docs. Use at the start of a session or when Tony says "preflight" or "where are we".
disable-model-invocation: true
allowed-tools: Read, Grep, Bash(python .claude/hooks/md5_report.py)
---

# /preflight — fast, read-only, no edits

Goal: get Tony to a known baseline in one short report, without scanning the whole project.

1. Run `python .claude/hooks/md5_report.py` once. Do not re-hash files any other way.
2. Read ONLY the newest entries:
   - `CURRENT_SOURCE_FOR_CLAUDE.txt`: the last ~80 lines (use Read with offset; do not read the whole file).
   - `MASTER_DEFERRED_TODO.md`: the open items section only.
3. Compare the MD5s with the "accepted baseline" MD5s written in CURRENT_SOURCE_FOR_CLAUDE.txt.
4. Do NOT read config, logs, DB or secret files. Do NOT send any command. Do NOT edit anything.

Report in exactly this shape (≤ 20 lines):

```
PRECHECK: PASS | FAIL (reason)
MD5 vs accepted baseline: <file: match/MISMATCH>
TWINS_IDENTICAL: YES | NO
Safety state (from docs, not live): dispatch LOCKED/NOT ARMED …
Top 3 open items: …
Suggested next step: … (one line)
STOP
```
