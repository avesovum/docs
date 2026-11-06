---
name: new-project
description: Sets up a new Desktop project folder in Tony's house layout (the RearPeek / Karens Tax Issue structure) from the master template, with the guards switched ON. Use when Tony says "new project", "set up this folder", or when the start-up check reports that this folder is not set up yet.
disable-model-invocation: false
---

# /new-project — Tony's house layout, guards on from day one

Plain English throughout. Start every question with "Tony, …". Recommendations first.

## 0. Check where we are (read-only)
- Confirm the working folder is a direct child of `C:\Users\Tony\OneDrive\Desktop\` and has no `AGENTS.md`/`CLAUDE.md`.
  If it already has them, STOP: this is an existing project.
- Master template: `C:\Users\Tony\ai-toolkit\project-template\`.
  If it doesn't exist, STOP and offer to create it once (see "Creating the master template" below).

## 1. Ask Tony 4 things (one message)
1. Project name and a one-line "what it's for".
2. Size: **App** (full layout, for anything that will have code or screens) or **Light** (README, AGENTS.md,
   CLAUDE.md, PROJECT_STATE.md, docs/ only; for research, business or document folders).
3. Private folders? (e.g. someone's real paperwork, photos). These are never committed, and Claude asks before reading them.
4. Does it control devices or money, or hold personal data? (yes → also add the guard hook in step 4).

## 2. Copy the layout
Copy the master template's structure for the chosen size. Replace every `{{PROJECT_NAME}}`, `{{PURPOSE}}`, `{{DATE}}`
and `{{PRIVATE_FOLDERS}}`. Add the private folders with `.gitkeep`, plus matching `.gitignore` lines (`Folder/*` and `!Folder/.gitkeep`).
`CLAUDE.md` must start with `@AGENTS.md`. Under 200 lines each.

## 3. Switch the guards ON (the step older projects skipped)
Show Tony this, then wait for "yes":
- `.claude/settings.json`:
  - `"defaultMode": "default"`
  - deny: `Read`/`Edit` of `.env`, `.env.*`, `.dev.vars`, `*.key`, `*.pem`, `*.jks`, `*.keystore`
  - deny: `Edit(./<private folder>/**)` for each private folder
  - ask: `Read(./<private folder>/**)`, so Claude must get Tony's OK each time it opens a private file
  - deny: git push, remote add, reset --hard, clean, rebase, `commit --no-verify` / `-n`, in both Bash and PowerShell
  - ask: git commit and git tag
- Project pre-commit (`tools/git-hooks/pre-commit`): keep the template's blocks, add one block per private folder.
  It must actually run, so check that the global pre-commit hook chains to it (see `APPLY_ON_PC.md` step 3b).
  Prove it: stage a throwaway file in a private folder with `git add -f`, run the hook script directly, and confirm it
  BLOCKS. Then `git restore --staged` the file and delete it.
- If step 1 Q4 was yes: copy `C:\Users\Tony\ai-toolkit\templates\powerstation\.claude\hooks\guard.py` and
  `test_guards.py`, change the protected-file and flag names for this project, add the PreToolUse hook, and run the self-test.

## 4. Finish
- `git init` (branch `main`), nothing committed until Tony says so.
- App size: an empty `DESIGN.md` stub, plus a note to fill it with `/new-app` step 3 once a sketch is chosen.
- WRENMINT dashboard card (Tony's all-projects rule) and a dated setup report in `docs/reports/`.
- Report: full Windows paths created, guards ON (show the self-test / hook proof), what Tony still needs to decide. STOP.

## Creating the master template (one time only)
Copy `Desktop\Karens Tax Issue` (the newest, cleanest setup) to `C:\Users\Tony\ai-toolkit\project-template`, excluding `.git`, `Images`,
`Karens Paperwork`, `output` contents and `docs/research` / `docs/handovers` contents. Replace project-specific text with
`{{PLACEHOLDERS}}` and remove Karen-specific rules (keep them as an example block marked "example: private paperwork").
Add a `LIGHT.md` list of which files the Light size keeps. Show Tony the result before saving.
From then on, improve the template, not the last project, so every new project gets the improvement.
