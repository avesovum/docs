---
name: checkpoint
description: Writes a short, verified checkpoint entry to CURRENT_SOURCE_FOR_CLAUDE.txt and MASTER_DEFERRED_TODO.md at the end of a work block. Docs-only. Use when Tony says "checkpoint", "save progress" or "update the docs".
disable-model-invocation: true
allowed-tools: Read, Edit, Bash(python .claude/hooks/md5_report.py)
---

# /checkpoint — docs only, never runtime files

1. Run `python .claude/hooks/md5_report.py`.
2. Append (never rewrite) one entry at the end of `CURRENT_SOURCE_FOR_CLAUDE.txt`:

```
=== CHECKPOINT <YYYY-MM-DD HH:MM> ===
Accepted baseline MD5s: <from report>
TWINS_IDENTICAL: YES/NO
What changed this session: <3 bullets max>
Proven: <bullets>   Still missing: <bullets>
Safety state: dispatch LOCKED / NOT ARMED (or exact supervised trial state)
Next step: <one line>
```

3. In `MASTER_DEFERRED_TODO.md`: tick items that were verified done, add new deferred items at the end. Do not reorder.
4. Do not package, lock, zip, or touch README.txt / PACKAGE_NOTE.txt.
5. Report: files changed, new MD5s of the two docs, STOP.
