"""Read-only MD5 report used by the /preflight skill. Prints one line per file, nothing else.

Usage:  python .claude/hooks/md5_report.py
"""
import hashlib
import os

FILES = [
    "octopus_bridge_server.py", "_trial_runner_L.py",
    "index.html", "main.js", "main-live.js", "styles.css",
]
root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
sums = {}
for name in FILES:
    p = os.path.join(root, name)
    if os.path.exists(p):
        with open(p, "rb") as f:
            sums[name] = hashlib.md5(f.read()).hexdigest()
        print(f"{sums[name]}  {os.path.getsize(p):>9}  {name}")
    else:
        print(f"{'MISSING':32}  {'':>9}  {name}")
if "main.js" in sums and "main-live.js" in sums:
    print("TWINS_IDENTICAL =", "YES" if sums["main.js"] == sums["main-live.js"] else "NO")
