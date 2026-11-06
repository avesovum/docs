"""PreToolUse guard for the Cape House project (read-only check, never edits anything).

- DENY: reading/editing secret or runtime files (config, DB/WAL/SHM, bridge.log, .env).
- DENY: shell commands that reach outside the PC (ssh, scp, curl, systemctl) or touch those files.
- ASK:  any edit that would switch on live control flags, so Tony always gets a prompt.

Claude Code passes the tool call as JSON on stdin. We answer with JSON on stdout.
"""
import json
import re
import sys

PROTECTED = re.compile(
    r"(octopus_bridge_config\.json|simulator_history\.db|\.db-wal|\.db-shm|\.sqlite|bridge\.log|\.dev\.vars|(^|[\\/])\.env)",
    re.I,
)
REMOTE_CMD = re.compile(r"\b(ssh|scp|sftp|curl|wget|Invoke-WebRequest|systemctl)\b", re.I)
LIVE_FLAGS = re.compile(
    r"(_AUTO_DISPATCH_LIVE_ENABLED|_AUTO_OBSERVER_FIRE_ENABLED|ev_control_enabled)\s*[:=]\s*(True|true|1)\b"
)


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
    path = str(inp.get("file_path") or inp.get("path") or inp.get("notebook_path") or "")
    command = str(inp.get("command") or "")
    new_text = str(inp.get("content") or inp.get("new_string") or "")
    for e in inp.get("edits", []) or []:
        new_text += "\n" + str(e.get("new_string", ""))

    if PROTECTED.search(path) or (tool == "Grep" and PROTECTED.search(str(inp.get("glob") or ""))):
        reply("deny", f"Protected file ({path}). Secrets/runtime state: report only whether a setting exists, never read or edit it.")
    if command:
        if PROTECTED.search(command):
            reply("deny", "Shell command touches a protected secret/runtime file.")
        if REMOTE_CMD.search(command):
            reply("ask", "Shell command reaches outside this PC (ssh/scp/curl/systemctl). Needs Tony's explicit OK.")
    if LIVE_FLAGS.search(new_text):
        reply("ask", "This edit switches ON a live-control flag. Only allowed inside an approved commissioning task.")
    sys.exit(0)  # allow; normal permission rules still apply


if __name__ == "__main__":
    main()
