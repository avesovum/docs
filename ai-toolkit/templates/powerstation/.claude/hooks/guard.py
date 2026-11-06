"""PreToolUse guard for the Cape House project. Read-only check: it never edits anything.

Designed to stay out of Tony's normal work. It only steps in for:
- SECRET files (bridge config, .env, .dev.vars, key files):
  - Claude's Read/Edit/Write tools: DENY.
  - A shell command that names one: ASK, so Tony can approve a yes/no "key available?" check.
- RUNTIME files (simulator DB, WAL/SHM, bridge.log):
  - DENY edits through Claude's Edit/Write tools.
  - Reading them and running scripts that use them is NOT affected.
- Edits that switch ON a live-control flag: ASK. One approval click, even inside a commissioning run.
- Shell commands that reach the internet (curl/wget to a non-local address, ssh, scp): ASK.
  Local calls to 127.0.0.1 / localhost (the bridge) are NOT affected.

Everything else passes straight through to Claude Code's normal permission rules.
Claude Code passes the tool call as JSON on stdin; this script answers with JSON on stdout.
"""
import json
import re
import sys

SECRET = re.compile(
    r"(octopus_bridge_config\.json|\.dev\.vars|(^|[\\/\s\"'])\.env(\.[\w-]+)?($|[\s\"'])|\.(pem|key|jks|keystore|p12|pfx)($|[\s\"']))",
    re.I,
)
RUNTIME = re.compile(r"(simulator_history\.db|\.db-wal$|\.db-shm$|\.sqlite3?$|bridge\.log$)", re.I)
REMOTE_TOOL = re.compile(r"\b(curl|wget|Invoke-WebRequest|Invoke-RestMethod|iwr|irm)\b", re.I)
REMOTE_ALWAYS = re.compile(r"\b(ssh|scp|sftp|systemctl)\b", re.I)
URL = re.compile(r"https?://([^/\s:\"']+)", re.I)
LOCAL_HOSTS = {"127.0.0.1", "localhost", "0.0.0.0", "::1", "[::1]"}
LIVE_FLAGS = re.compile(
    r"(_AUTO_DISPATCH_LIVE_ENABLED|_AUTO_OBSERVER_FIRE_ENABLED|ev_control_enabled)[\"']?\s*[:=]\s*[\"']?(True|true|1)\b"
)
FILE_TOOLS = {"Read", "Edit", "Write", "MultiEdit", "NotebookEdit"}
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def reply(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {}) or {}
    path = str(inp.get("file_path") or inp.get("notebook_path") or "")
    command = str(inp.get("command") or "")
    new_text = str(inp.get("content") or inp.get("new_string") or "")
    for e in inp.get("edits", []) or []:
        new_text += "\n" + str(e.get("new_string", ""))

    if tool in FILE_TOOLS and SECRET.search(path):
        reply("deny", f"Protected secret file ({path}). Never read or edit it; report only whether a setting exists.")
    if tool in EDIT_TOOLS and RUNTIME.search(path):
        reply("deny", f"Runtime state file ({path}) must not be edited by Claude.")
    if command:
        if SECRET.search(command):
            reply("ask", "This command names a secret file. Tony: approve only if it reports a yes/no and never prints a value.")
        if REMOTE_ALWAYS.search(command):
            reply("ask", "This command reaches another machine (ssh/scp/systemctl). It needs Tony's explicit OK.")
        if REMOTE_TOOL.search(command):
            hosts = {h.lower() for h in URL.findall(command)}
            if not hosts or not hosts <= LOCAL_HOSTS:
                reply("ask", "This command contacts the internet (not the local bridge). It needs Tony's explicit OK.")
    if tool in EDIT_TOOLS and LIVE_FLAGS.search(new_text):
        reply("ask", "This edit switches ON a live-control flag. Approve only inside an approved commissioning task.")
    sys.exit(0)  # allow: Claude Code's normal permission rules still apply


if __name__ == "__main__":
    main()
