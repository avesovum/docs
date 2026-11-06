"""Self-test for guard.py and twin_check.py. Safe: touches no project files.

Feeds pretend tool calls to the guards and uses a throwaway temp folder for the twin test.
Usage (from the project folder):  python .claude/hooks/test_guards.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "guard.py")
TWIN = os.path.join(HERE, "twin_check.py")


def run(script, payload, env=None):
    p = subprocess.run([sys.executable, script], input=json.dumps(payload), capture_output=True, text=True,
                       env={**os.environ, **(env or {})})
    out = p.stdout.strip()
    decision = json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow"
    return decision, p.returncode


cases = [
    ("read secret config", {"tool_name": "Read", "tool_input": {"file_path": r"C:\x\octopus_bridge_config.json"}}, "deny"),
    ("read .env", {"tool_name": "Read", "tool_input": {"file_path": r"C:\x\.env"}}, "deny"),
    ("read .dev.vars", {"tool_name": "Read", "tool_input": {"file_path": r"C:\x\.dev.vars"}}, "deny"),
    ("shell reads bridge.log", {"tool_name": "Bash", "tool_input": {"command": "type bridge.log"}}, "deny"),
    ("curl outside", {"tool_name": "Bash", "tool_input": {"command": "curl https://example.com"}}, "ask"),
    ("live flag ON", {"tool_name": "Edit", "tool_input": {"file_path": "octopus_bridge_server.py",
                      "new_string": "_AUTO_DISPATCH_LIVE_ENABLED = True"}}, "ask"),
    ("ev_control ON", {"tool_name": "Edit", "tool_input": {"file_path": "x.py", "new_string": "ev_control_enabled: true"}}, "ask"),
    ("normal css edit", {"tool_name": "Edit", "tool_input": {"file_path": "styles.css", "new_string": "color: red"}}, "allow"),
    ("live flag OFF", {"tool_name": "Edit", "tool_input": {"file_path": "x.py", "new_string": "_AUTO_DISPATCH_LIVE_ENABLED = False"}}, "allow"),
]
fails = 0
for name, payload, want in cases:
    got, _ = run(GUARD, payload)
    ok = got == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}  guard: {name:24} expected {want:5} got {got}")

with tempfile.TemporaryDirectory() as d:
    for n in ("main.js", "main-live.js"):
        with open(os.path.join(d, n), "w") as f:
            f.write("v1")
    payload = {"tool_input": {"file_path": os.path.join(d, "main.js")}, "cwd": d}
    _, code_same = run(TWIN, payload, {"CLAUDE_PROJECT_DIR": d})
    with open(os.path.join(d, "main.js"), "w") as f:
        f.write("v2")
    _, code_diff = run(TWIN, payload, {"CLAUDE_PROJECT_DIR": d})
for name, got, want in (("twins identical", code_same, 0), ("twins differ", code_diff, 2)):
    ok = got == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}  twin:  {name:24} expected exit {want} got {got}")

print("ALL PASS" if not fails else f"{fails} FAILED")
sys.exit(1 if fails else 0)
