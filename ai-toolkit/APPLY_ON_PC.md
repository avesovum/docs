# Apply the toolkit on your PC: paste-in steps

**How to use this file:**
- Unzip the toolkit to `C:\Users\Tony\ai-toolkit\`.
- Open the Claude desktop app, **Code** tab, and start a session in the folder each step names.
- Paste the step's prompt. Each prompt **looks first, shows you the exact change, and waits for your "yes"** before
  touching anything.
- Do one step per session, and do them in this order: the safest and quickest come first.

Before step 5, take your normal zip baseline of Powerstation.

---

## Step 1: Turn secret scanning back on in APP FAMILY (5 min)
**Why:** APP FAMILY holds tax/HMRC material, and it's the only project where gitleaks never runs.
**Folder:** `Desktop\APP FAMILY`

```
Inspect only, then STOP for my approval before any change.
This repo sets core.hooksPath to tools/git-hooks, so my global gitleaks pre-commit hook never runs here.
1. Show me tools/git-hooks/pre-commit and the output of: git config --get core.hooksPath ; gitleaks version
2. Propose the smallest change to tools/git-hooks/pre-commit so it ALSO runs:  gitleaks git --pre-commit --staged --redact -v
   (keep the existing Test-Documentation step; if gitleaks fails, the commit must stop).
3. After I say yes: make the change, then test it by running the hook script directly (no commit), and show the output.
Do not commit, push, or change git config.
```

## Step 2: Block Claude from reading secret files in every project (5 min)
**Why:** today only shell commands are checked. Claude's own Read tool can still open `.env` and `.dev.vars` files.
**Folder:** any (this changes your user settings)

```
Inspect only, then STOP for my approval before any change.
1. Show me the "permissions" part of %USERPROFILE%\.claude\settings.json (hook names only, no values).
2. Propose adding these deny rules (merge, don't remove anything):
   "Read(//**/.env)", "Read(//**/.env.*)", "Read(//**/.dev.vars)", "Read(//**/octopus_bridge_config.json)"
3. After I say yes: add them, check the file is still valid JSON (python -m json.tool), and show the new permissions block.
4. Then, read-only, in Desktop\WRENMINT Control run:  git check-ignore -v .dev.vars   and tell me if .dev.vars is
   ignored by git (do NOT open the file).
```
**Check afterwards:** in a new session, ask "read .env in WRENMINT Control". It should be refused.

## Step 3: Git safety rules for Karens Tax Issue (5 min)
**Why:** it holds someone's tax documents and has no Claude safety rules at all.
**Folder:** `Desktop\Karens Tax Issue`

```
Inspect only, then STOP for my approval before any change.
Show me the permissions in Desktop\PROJAA\.claude\settings.json (rules only). Propose creating
.claude\settings.json here with the same git deny and ask rules (push, remote add, reset --hard, clean, rebase,
commit --no-verify; ask on commit and tag), plus "defaultMode": "default". After I say yes, create it and validate the JSON.
```

## Step 4: Read-only health check (10 min, changes nothing)
**Why:**
- Claude may be ignoring your AGENTS.md files.
- One "allow" rule that's too broad can undo your blocks.
- You should know what every connected tool is.

**Folder:** `Desktop`

```
READ-ONLY. Do not edit, run project code, install or send anything. Don't open secret/config/log/db files.
1. For each Desktop project that has BOTH CLAUDE.md and AGENTS.md, check whether CLAUDE.md contains a line "@AGENTS.md".
   Claude Code only reads CLAUDE.md when both exist, so list projects where AGENTS.md is NOT imported, and in one line
   each, what AGENTS.md says that CLAUDE.md doesn't.
2. In "V40 Version Y Powerstation\.claude\settings.local.json", list any allow rule broad enough to get around the deny
   rules (e.g. Bash(python:*), Bash(powershell:*), PowerShell(*), Bash(*), Read(**), anything with a bare *).
   Rules only, no env values.
3. Run  claude mcp get  for rea, vectorcraft, maestro, photocraft: report the command or URL and package name of each
   (no keys or env values).
Report as three short tables, then STOP.
```
Send me the result and I'll tell you what to change.

## Step 5: Safety guards + screenshot check for Powerstation (20 min)
**Why:** these were proven in the pilot. Without guards, Claude switched live dispatch ON even with your rules loaded.
With guards it was stopped, and the secret config could not be read.
**Folder:** `Desktop\V40 Version Y Powerstation`. Take your zip baseline first.

```
Docs/config-only task. Do not touch runtime files (.py, .js, .html, .css), config, logs, DB or secrets.
Inspect first, then STOP for my approval.
1. Confirm .claude\settings.json does NOT exist yet (only settings.local.json), and list .claude\hooks if it exists.
2. Plan to copy from C:\Users\Tony\ai-toolkit\templates\powerstation\.claude\ ONLY:
   hooks\guard.py, hooks\twin_check.py, hooks\test_guards.py, settings.json, skills\ui-check\  (NOT preflight/checkpoint;
   I already have cape-* skills). Show me settings.json and say if any rule clashes with settings.local.json.
3. After I say yes: copy them, run  python .claude\hooks\test_guards.py  and show the output (must say ALL PASS).
4. Tell me to restart Claude Code here, then type /hooks to see PreToolUse and PostToolUse listed.
Report: files added, MD5s of runtime files unchanged (before/after), TWINS_IDENTICAL, STOP.
```
**Check afterwards (new session):**
- Ask "read octopus_bridge_config.json". It should be refused.
- Ask "set _AUTO_DISPATCH_LIVE_ENABLED to True". You should get an approval prompt: say **No**.

## Step 6: Powerstation DESIGN.md (30 min, look and propose first)
**Why:** your two CSS files use different colour sets. One rulebook keeps every screen consistent and makes safety
states clear. In the pilot it raised the safety-clarity score.
**Folder:** `Desktop\V40 Version Y Powerstation`

```
Inspect only, then STOP. Read C:\Users\Tony\ai-toolkit\templates\powerstation\DESIGN.md (v2). Compare it with the
CSS variables in executive_snapshot.css and 000000000000\styles.css and the badge/state styles in index.html.
Propose a project DESIGN.md that KEEPS what already works in my dashboard (my current colours/sections/button
labels) and adopts the v2 rules for state badges, command buttons, below-limit colours and phone layout.
Show me a short list of differences. Do not edit CSS/HTML. After I say yes, write DESIGN.md only, and add one line to
CLAUDE.md: "Before any UI change, read @DESIGN.md".
```
Later, a separate approved UI task applies DESIGN.md to the CSS a little at a time, with `/ui-check` after each change.

## Step 7: Wrenmint brand DESIGN.md (30 min)
**Why:** the website and WRENMINT Control should look like one brand.
**Folder:** `Desktop\Wrenmint.com website`

```
Inspect only, then STOP. From src/styles/site.css, design/mockups, and Desktop\WRENMINT Control\public\style.css and
its mockups, propose one shared Wrenmint DESIGN.md (one style direction, colour tokens with WCAG AA contrast checked,
type scale, 4px spacing, components, don'ts). Show me where the two apps currently differ. After I say yes, write
DESIGN.md in both projects (same file) and add "Before any UI change, read @DESIGN.md" to each CLAUDE.md
(create CLAUDE.md with "@AGENTS.md" on line 1 for the website, which has none).
```

## Step 8: Slim the Powerstation CLAUDE.md (1–2 hours, plan first)
**Why:** it's 701 lines, and the docs say keep it under 200. Long files cost tokens every message, and Claude follows
them less reliably. This is likely your biggest source of token burn.

```
Plan only, STOP before editing. CLAUDE.md is 701 lines. Propose how to cut it to under 200 lines WITHOUT losing any
rule: keep the always-needed safety rules in CLAUDE.md, move topic detail into my existing cape-* skills or into
.claude\rules\*.md files with paths: so they only load for matching files. Show a table: section → stays / moves to → why.
Nothing is deleted, only moved. Wait for my approval of the table.
```

## Step 9: Optional extras
- `/plugin install frontend-design@claude-plugins-official`: Anthropic's design skill. Tell it "calm, data-first, follow DESIGN.md".
- Fix the duplicate header and the too-broad trigger words in your Cape House skill: claude.ai → Settings → Skills.
- Copy `templates\global-skills\new-app\` to `%USERPROFILE%\.claude\skills\new-app\` so you get `/new-app` for future apps.
