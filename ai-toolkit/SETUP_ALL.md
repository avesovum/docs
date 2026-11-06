# One-paste setup (about 20–30 minutes, mostly Claude working)

**What you do:**
1. Unzip the toolkit into `Desktop\Tools Research\`, so you get `Desktop\Tools Research\ai-toolkit\`.
   (`C:\Users\Tony\ai-toolkit\` also works.)
2. Make your usual zip backup of **V40 Version Y Powerstation**. This is just habit: the setup doesn't touch its code.
3. Open the Claude desktop app → **Code** tab → start a new session in your **Desktop** folder.
4. Copy everything in the grey box below and paste it in.
5. You may see a few "Allow?" pop-ups for files inside `.claude` folders or `ai-toolkit`. Click **Allow**.
   Anything else, click **Deny** and tell me.
6. At the end, Claude shows a short table. Send it to me and I'll check it.

**What it will NOT do:**
- touch any project's code, logic, maths, tariffs, trials, packages or devices
- commit or push
- open private folders or secret files
- change how you normally work

**What you'll notice afterwards:** an approval pop-up only when Claude tries to:
- open Karen's paperwork
- switch ON a live-control setting
- contact the internet from Powerstation
- click a dashboard button with the browser tool

Plus one new thing: when you open Claude in a **brand-new** Desktop folder, it offers to set it up.

**Undo:** paste `UNDO.md` and everything goes back exactly as it was.

```
TONY HAS APPROVED THIS WHOLE SETUP JOB IN ADVANCE. It is the bounded task listed below and nothing else. Work through it
end to end without asking again. STOP and ask only if something is unexpected, a check fails, or a file isn't where
this says.

HARD LIMITS (never break these):
- Do NOT edit, move or delete any project code, data or runtime file (.py .js .html .css .kt .gradle .ps1 .db .log, configs, zips).
- Do NOT open: Images\, Karens Paperwork\, output\, octopus_bridge_config.json, .env, .dev.vars, key files, logs, databases.
- Do NOT commit, push, tag, or change any repository's git config. Do NOT send any device/MyEnergi/Tesla/Octopus command.
- Use Python for copying and editing files, not PowerShell. Paths: T = the folder this toolkit is in (normally
  C:\Users\Tony\OneDrive\Desktop\Tools Research\ai-toolkit, or C:\Users\Tony\ai-toolkit); in every copied skill or
  hook file replace C:\Users\Tony\ai-toolkit with T. D = C:\Users\Tony\OneDrive\Desktop,
  U = C:\Users\Tony\.claude
- Only these files may be created or changed:
  U\settings.json
  U\skills\new-project\, U\skills\new-app\
  U\hooks\new_folder_check.py
  T\project-template\, T\backups\
  D\APP FAMILY\tools\git-hooks\pre-commit
  D\Karens Tax Issue\.claude\settings.json, D\Karens Tax Issue\CLAUDE.md (one line)
  D\V40 Version Y Powerstation\.claude\settings.json, ...\.claude\hooks\(guard.py, twin_check.py, test_guards.py),
  ...\.claude\skills\ui-check\

PHASE 0 — SAFETY NET
0.1 Make T\backups\<YYYY-MM-DD_HHMM>\ (call it B). Copy into B every file above that ALREADY exists, keeping its
    folder path (e.g. B\U\settings.json, B\D\APP FAMILY\tools\git-hooks\pre-commit, B\D\Karens Tax Issue\CLAUDE.md).
0.2 python T\tools\snapshot.py take B\before.json  followed by every folder directly inside D (quote each path).
0.3 For each git repo in D: save "git status --short" to B\git_before.txt (read-only).
0.4 Start B\SETUP_LOG.md and write every created or changed file into it as you go.

PHASE 1 — READ-ONLY HEALTH CHECK (write findings to B\health.md, change nothing)
1.1 For each project with both CLAUDE.md and AGENTS.md: does CLAUDE.md contain "@AGENTS.md"? List the ones that don't.
1.2 In D\V40 Version Y Powerstation\.claude\settings.local.json: list allow rules broad enough to get around deny rules
    (e.g. Bash(python:*), PowerShell(*), Bash(*)). Rules only, no env values.
1.3 claude mcp get for rea, vectorcraft, maestro, photocraft: command/URL and package name only, no keys.

PHASE 2 — SAFETY (each part: do it, test it, and if the test fails restore that part from B and log it)
2.1 APP FAMILY secret scan. Append to D\APP FAMILY\tools\git-hooks\pre-commit, before its final exit, a gitleaks
    step that stops the commit if gitleaks fails:  gitleaks git --pre-commit --staged --redact -v  (keep everything else).
    TEST in a throwaway repo, not APP FAMILY: make %TEMP%\hooktest, git init, add a file containing
    ghp_ followed by 36 letters/digits, stage it, run "gitleaks git --pre-commit --staged --redact" there and confirm it
    reports a leak. Delete %TEMP%\hooktest.
2.2 Block Claude reading secret files everywhere. In U\settings.json add (merge, keep everything else, including my
    secret-check hook) permissions.deny: "Read(//**/.env)", "Read(//**/.env.*)", "Read(//**/.dev.vars)",
    "Read(//**/octopus_bridge_config.json)". Validate with python -m json.tool.
    Then read-only: in D\WRENMINT Control run  git check-ignore -v .dev.vars  and log whether it is ignored.
2.3 Karens Tax Issue guards. Create D\Karens Tax Issue\.claude\settings.json with:
    ask Read(./Karens Paperwork/**); deny Edit(./Karens Paperwork/**), Edit(./Images/**);
    deny Bash and PowerShell git push / git remote add / git reset --hard / git clean / git rebase /
    git commit --no-verify / git commit -n (copy the exact rule wording from D\PROJAA\.claude\settings.json);
    ask git commit, git tag. Validate the JSON. In its CLAUDE.md change only the sentence saying the guards are
    "not yet switched on" so it says the Claude settings guard is ON (2026 setup) and the pre-commit guard is still off.
2.4 Powerstation guards. Copy from T\templates\powerstation\.claude\ ONLY:
    settings.json, hooks\guard.py, hooks\twin_check.py, hooks\test_guards.py, skills\ui-check\
    into D\V40 Version Y Powerstation\.claude\. Do NOT copy preflight or checkpoint, and do NOT touch settings.local.json.
    If .claude\settings.json already exists there, STOP and show me instead.
    TEST: from that folder run  python .claude\hooks\test_guards.py  → it must print ALL PASS. If not, remove the
    copied files and log it.

PHASE 3 — FUTURE PROJECTS SET THEMSELVES UP
3.1 Copy T\templates\global-skills\new-project\ and \new-app\ to U\skills\.
3.2 Copy T\templates\global-hooks\new_folder_check.py to U\hooks\. Add to U\settings.json hooks (merge):
    "SessionStart": [{"hooks": [{"type": "command", "command": "python",
      "args": ["C:/Users/Tony/.claude/hooks/new_folder_check.py"], "timeout": 10}]}]
    Validate the JSON. TEST without starting Claude: feed it {"source":"startup","cwd":"<D>\\zz-test"} on stdin
    → it must print a START-UP CHECK message; feed it cwd = D\RearPeek → it must print nothing.
3.3 Build the master template at T\project-template by following "Creating the master template" in
    U\skills\new-project\SKILL.md, from D\Karens Tax Issue. Copy ONLY rule/doc/tool files and empty folders with .gitkeep:
    never .git, Images, Karens Paperwork, output, docs\research or docs\handovers contents.
    Replace Karen-specific text with {{PLACEHOLDERS}}.

PHASE 4 — PROVE NOTHING ELSE CHANGED
4.1 python T\tools\snapshot.py take B\after.json (same folders as 0.2), then
    python T\tools\snapshot.py compare B\before.json B\after.json > B\compare.txt
4.2 Every ADDED or CHANGED file must be on the allowed list above. REMOVED must be 0. If anything else changed, STOP and
    tell me; don't try to fix it.
4.3 git status --short again for each repo → B\git_after.txt. Only the allowed files may differ.

FINAL REPORT (plain English, short):
- table: what was set up | where | test result | how to undo
- the health check findings (phase 1) in one line each
- compare result: UNCHANGED count, ADDED/CHANGED list, REMOVED = 0
- "Code, logic, maths, data and device settings: unchanged (proven by compare.txt)"
- backup folder path B. STOP.
```
