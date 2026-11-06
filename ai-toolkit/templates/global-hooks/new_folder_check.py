"""SessionStart hook: notices when Claude Code starts in a Desktop folder that isn't set up as a project yet.

It creates nothing and changes nothing. It only adds a note to Claude's context so that Claude's first message
offers to run /new-project. Tony still says yes or no.

Install: copy to %USERPROFILE%\\.claude\\hooks\\new_folder_check.py and add a SessionStart hook in
%USERPROFILE%\\.claude\\settings.json (see APPLY_ON_PC.md step 10).
"""
import json
import os
import sys

MARKERS = ("CLAUDE.md", "AGENTS.md", os.path.join(".claude", "CLAUDE.md"))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if data.get("source", "startup") != "startup":
        sys.exit(0)  # only on a fresh start, not resume/clear/compact
    cwd = os.path.abspath(data.get("cwd") or os.getcwd())
    parent = os.path.basename(os.path.dirname(cwd)).lower()
    name = os.path.basename(cwd)
    if parent != "desktop" or name.startswith(("_", ".")):
        sys.exit(0)  # only real project folders directly on the Desktop; skips _PROJECT_TEMPLATE
    if any(os.path.exists(os.path.join(cwd, m)) for m in MARKERS):
        sys.exit(0)  # already set up
    note = (f"START-UP CHECK: the folder '{name}' is on Tony's Desktop but has no AGENTS.md or CLAUDE.md, so it isn't "
            f"set up as a project yet. Before doing anything else, ask: \"Tony, this folder isn't set up yet. Shall I set "
            f"it up in your usual layout with the guards switched on (/new-project)? Or is it just a scratch folder?\" "
            f"Do not create anything until Tony says yes.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": note}}))
    sys.exit(0)


if __name__ == "__main__":
    main()
