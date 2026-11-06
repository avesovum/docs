"""PostToolUse check: main.js and main-live.js must stay byte-identical.

Runs after every Edit/Write. If one of the twins was touched and they now differ,
exit code 2 sends the message back to Claude so it fixes it straight away.
"""
import hashlib
import json
import os
import sys

TWINS = ("main.js", "main-live.js")


def md5(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def main():
    data = json.load(sys.stdin)
    path = str((data.get("tool_input") or {}).get("file_path") or "")
    if os.path.basename(path) not in TWINS:
        sys.exit(0)
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.path.dirname(path)
    a, b = (os.path.join(root, t) for t in TWINS)
    if not (os.path.exists(a) and os.path.exists(b)):
        sys.exit(0)
    ha, hb = md5(a), md5(b)
    if ha != hb:
        print(f"main.js ({ha}) and main-live.js ({hb}) are no longer byte-identical. "
              f"Apply the same change to the other file (or copy it) before continuing.", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
