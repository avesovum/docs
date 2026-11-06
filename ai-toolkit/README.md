# Tony's AI toolkit: design better, build faster, stay safe

> **Start here:**
> - `pilot/PILOT_REPORT.md`: what was tested and what it proved, in plain English.
> - `APPLY_ON_PC.md`: paste-in steps to put it on your real projects, safest first.
>   Each step shows you the change and waits for your "yes".
>
> Sections 1–5 below are the research and reasoning behind it.

A living guide. Copy this folder to `C:\Users\Tony\ai-toolkit\` on your PC. Templates are in `templates/`.
Last researched: **2026-11-06**. See the changelog at the bottom.

---

## 1. What I learned about how you work

- **Machine:** Windows PC ("Tony-PC"). You use the Claude desktop app and Claude Code, with Remote Control.
  Projects live under `C:\Users\Tony\OneDrive\Desktop\`.
- **Projects:**
  - **V40 Version Y Powerstation** (Cape House / Abbots Way): your main project.
    - Plain `index.html` + `styles.css` + `main.js`/`main-live.js` dashboard, with no framework and no build step.
    - Large Python bridge (`octopus_bridge_server.py`) talking to Powerwall, Zappi, Octopus and Tesla.
    - Safety-critical.
  - **PROJAA** and **CHARGECLAIM**: in your Remote Control list, but I couldn't open them (see §5, item 7).
- **How you work:** strict inspect → approve → smallest change → verify → report → STOP. You keep these by hand:
  - status files (`CURRENT_SOURCE_FOR_CLAUDE.txt`, `MASTER_DEFERRED_TODO.md`)
  - MD5 checks
  - byte-identical `main.js` and `main-live.js`
  - zip packages with markers (`_ZC`, `_ZD` …)
- **Pain points** (from your rules skill):
  - token burn from re-reading big files
  - Claude redoing prep after you say "go"
  - vague test instructions
  - PowerShell trouble
  - fear of leaked keys or accidental device commands
- **Already set up:**
  - a 800-line custom skill (`cape-house-power-station-safety-rules`)
  - plugins: Cloudflare, GitHub, Kling AI (images/video), S&P Global
  - connectors: Gmail, Claude Docs
  - no CLAUDE.md, hooks or MCP servers that I could see
- **Not reachable from the cloud:** your three PC folders. Your PC lists them, but doesn't offer them to cloud sessions.
  Everything here is tailored from your rules skill, not from reading your code.

**The big insight:** your rules are mostly *written instructions* that Claude has to remember. Several of them can be
*enforced automatically* by hooks and permissions instead:
- never read the config
- keep the twin JS files identical
- ask before live flags
- no ssh or curl

Enforcing them is safer and uses fewer tokens.

---

## 1b. After your PC audit (2026-11-06): this replaces the top 10 below

This came from a read-only audit of all 12 Desktop folders, run on your PC. You already had more in place than §1 assumed.

**Already in place, so skip:**
- gitleaks (global pre-commit)
- Playwright + context7 MCP
- review/debug/security/test agents
- Powerstation checkpoint, rollback, package and safe-edit skills, plus MD5 sidecars
- deny rules for dangerous commands
- git-safety rules in PROJAA and APP FAMILY
- a global secret check on shell commands
- design work done prototype-first (mockups, approved and rejected folders)
- Claude Code 2.1.312 and Python 3.14

That means my `/preflight` and `/checkpoint` aren't needed, and gitleaks and Playwright are already installed.

**Safety gaps (small, do first):**

| # | Gap | Fix | Time |
|---|---|---|---|
| S1 | **APP FAMILY runs no secret scan.** Its own hooks folder replaces the global one. This project holds HMRC/tax material | Add a gitleaks call to `tools/git-hooks/pre-commit` | 5 min |
| S2 | Local pre-commit hooks in PROJAA, Karens and RearPeek never run. The global hooks folder replaces them, so PROJAA's `.env`/`Images/` block is off | Make the global pre-commit also run `tools/git-hooks/pre-commit` when a repo has one | 10 min |
| S3 | Claude's **Read** tool isn't blocked from secret files. Only shell commands are checked | Global deny rules in `~/.claude/settings.json` for `.env`, `.env.*`, `.dev.vars` and `octopus_bridge_config.json`. Also check that WRENMINT Control's `.dev.vars` is git-ignored | 5 min |
| S4 | Powerstation has no automatic hooks: live-flag ask, twin check, config read block. Playwright *can* click dashboard buttons | Pilot pack: `guard.py`, `twin_check.py`, and "ask" rules for Playwright click/type | 20 min |
| S5 | From a terminal or VS Code, Claude Code 2.1.283+ **starts in auto mode** | `"defaultMode": "default"` in Powerstation settings | 2 min |
| S6 | Karens Tax Issue has no Claude settings | Copy PROJAA's git push/reset deny rules | 5 min |
| S7 | Powerstation has 147 allow rules. A broad one (e.g. any `python` command) can get around the deny rules | Read-only review | 10 min |
| S8 | MCP servers `rea`, `vectorcraft`, `maestro` and `photocraft` aren't ones I recognise | Run `claude mcp get <name>` and confirm you know who made each | 5 min |

**Speed and token gaps:**
- **P1.** With both CLAUDE.md and AGENTS.md present, **Claude reads only CLAUDE.md**, unless CLAUDE.md contains `@AGENTS.md`.
  This applies to 7 projects. Check each CLAUDE.md for that line.
- **P2.** Powerstation `CLAUDE.md` is **701 lines**. The docs say to keep it under 200, because "longer files consume more context and reduce adherence".
  - It loads on top of the 109-line global file and the 800-line account skill.
  - Move the details into your cape-* skills or `.claude/rules/` files. Rules files load only when Claude touches files that match them.
- **P3.** Powerstation has 1,040 top-level items, including 97 zips and about 70 `_pre_*` backup folders.
  - Claude's search can turn up stale backup copies.
  - Grep skips git-ignored files. So if you don't commit the backups, listing them in `.gitignore` hides them from search.
  - The alternative is moving them to an archive folder next to the project.

**Design gaps:**
- **D1. There's no DESIGN.md anywhere.** Turn each project's `design/approved` folder into one. Priority order:
  1. A shared **Wrenmint** brand file for Wrenmint.com website and WRENMINT Control.
  2. Powerstation, where two CSS files use different variable sets.
  3. PROJAA and RearPeek.
- **D2.** `/ui-check` scoring plus a look-only rule. Playwright is already installed.
  For the Android apps, `maestro` may cover the same job, if it's Maestro mobile testing.
- **D3.** `frontend-design` plugin. The command-line tool currently has no plugins installed.

**Optional:**
- Floorplan health check for WRENMINT Control (it's a Workers app with a database and endpoints).
- m3e-canvas for sketching Android screens. Four projects have `android/`.

---

## 2. Top 10, ranked by value ÷ effort for you (first draft, before the audit; see §1b)

| # | What | Heading | Setup time | Cost |
|---|---|---|---|---|
| 1 | Safety hooks + permissions (`templates/powerstation/.claude/`) | (b) faster / safer | 20 min | free |
| 2 | `DESIGN.md` + Anthropic's official **frontend-design** plugin | (a) design | 15 min | free |
| 3 | **Playwright MCP** + `/ui-check` (Claude sees its own UI, read-only) | (a) design | 15 min | free |
| 4 | `/preflight` + `/checkpoint` skills (stop redoing prep) | (b) faster | 10 min | free |
| 5 | Lean `CLAUDE.md` + 6 context habits | (b) faster | 10 min | free |
| 6 | **gitleaks** secret scan before every zip | (c) other | 5 min | free |
| 7 | Fix Remote Control folder sharing + voice dictation | (c) other | 10 min | free |
| 8 | **Impeccable** `detect` (read-only "AI look" linter) | (a) design | 5 min | free |
| 9 | **Floorplan** (plain-English app map + security health panel) | (c) other | 15 min | free |
| 10 | **Serena** in read-only mode for the big Python file | (b) faster | 30 min | free (GPL) |

Nothing on this list is paid. Paid extras exist (Context7 Pro, Serena's JetBrains plugin), but you don't need them.

### (a) Design better apps

**#2 · DESIGN.md + frontend-design plugin**
- **What:** a one-page style rulebook Claude reads before any UI work, plus Anthropic's own design-judgement skill.
  The skill is plain markdown: no code, no hooks.
- **Why you:** your dashboard needs to show *safety states* (live, stale, dry-run, armed …) clearly and consistently.
  The starter `DESIGN.md` defines:
  - a badge system for those states
  - energy-flow colours, all WCAG AA contrast-checked in light and dark
  - a rule that section names and buttons never move, so your step-by-step test instructions stay valid
- **Setup:**
  1. Copy `templates/powerstation/DESIGN.md` into the project folder.
  2. Tell Claude: "Compare DESIGN.md with styles.css. Propose token changes only. Don't edit." Review, then approve.
  3. In Claude Code: `/plugin install frontend-design@claude-plugins-official`
  4. When asking for UI, say: "calm, data-first, follow DESIGN.md, only edit styles.css and class names in index.html."
     The plugin leans bold, which suits landing pages, not dashboards.
- **Optional reference:** github.com/VoltAgent/awesome-design-md (126k★, MIT). Download one calm brand's DESIGN.md
  (e.g. `linear.app`) *only* as inspiration. Each file is about 6k tokens, so don't keep it in the project.

**#3 · Playwright MCP + `/ui-check`**
- **What:** gives Claude a browser so it can take screenshots of its own work and score them against DESIGN.md
  (0–100, fix anything under 80).
- **Why you:** it ends the "Tony, please check the panel" round-trips for *visual* checks.
- **Safety:** the `/ui-check` skill is look-only. It never clicks buttons, and only runs while the bridge is
  build-disabled / LOCKED. A browser agent *could* click "Send Eco+".
- **Setup:**
  1. Run this in a terminal on your PC (one line):
     `claude mcp add --scope project playwright -- cmd /c npx -y @playwright/mcp@latest --isolated`
  2. Copy `templates/powerstation/.claude/skills/ui-check/` into the project's `.claude\skills\`.
  3. Use it: start the bridge as normal, then type `/ui-check`.

**#8 · Impeccable detect** (github.com/pbakaus/impeccable, 104k★, Apache-2.0)
- **What:** a deterministic linter that flags "AI-generated look" habits in HTML/CSS.
- **Setup:** in the project folder run `set DO_NOT_TRACK=1`, then `npx impeccable detect index.html styles.css`.
- **Do NOT** run `impeccable install`. It adds hooks that run after every edit and downloads a binary.
- **Python alternative:** `pip install uxskill`, then `uxskill lint .` (offline, no telemetry). Use the pip CLI, not its plugin.

### (b) Build faster / productivity

**#1 · Safety hooks + permissions**
- **What:** three small Python scripts plus a `settings.json`. Claude Code runs them automatically.
  - `guard.py`
    - **Blocks** reading or editing `octopus_bridge_config.json`, DB/WAL/SHM files, `bridge.log` and `.env`.
    - **Asks you** before any ssh/scp/curl command, and before any edit that sets
      `_AUTO_DISPATCH_LIVE_ENABLED`, `_AUTO_OBSERVER_FIRE_ENABLED` or `ev_control_enabled` to True.
  - `twin_check.py`: after every edit, if `main.js` and `main-live.js` differ, it tells Claude to fix it immediately.
  - `settings.json`
    - deny rules for secrets
    - starts in normal "ask" mode, not auto mode (auto mode is now the default on new installs)
    - disables "bypass permissions" mode for this project
- **Why you:** these are your own rules, made automatic. Claude can't forget them, and they cost no tokens.
- **Setup:**
  1. In a terminal run `python --version`. If that fails, try `py --version`. If `py` works, change every
     `"command": "python"` in `settings.json` to `"command": "py"`.
  2. Copy `templates/powerstation/.claude/` into the project folder, so you get `.claude\settings.json`,
     `.claude\hooks\` and `.claude\skills\`.
  3. Restart Claude Code in that folder. Type `/hooks` and you should see PreToolUse and PostToolUse listed.
  4. Test: ask Claude to "read octopus_bridge_config.json". It should be refused.
  5. If your Claude Code is older than v2.1.295, delete the `"onFailure": "block"` line.
- **Fail-safe:** if Python isn't found, `onFailure: block` makes Claude stop rather than skip the guard.

**#4 · `/preflight` and `/checkpoint`**
- **What:** two slash commands.
  - `/preflight` is read-only. It gives you a 20-line baseline: MD5s against the accepted baseline, twins identical,
    newest status, top 3 open items, next step.
  - `/checkpoint` appends a verified entry to your two status docs and never touches runtime files.
- **Why you:** your skill spends many lines telling Claude how to prep. These turn that into one command, so Claude
  stops re-reading everything.
- **Setup:** copy `templates/powerstation/.claude/skills/preflight` and `.../checkpoint` into `.claude\skills\`.

**#5 · Lean CLAUDE.md + habits**
- **What:** `templates/powerstation/CLAUDE.md`, about 40 lines. It holds the map, always/never rules, commands and
  report format, and it pulls in DESIGN.md.
- **Habits:**
  1. Type `/context` now and then. Start fresh (`/clear` plus a 3-line brief) above roughly 40–60%.
  2. If an attempt goes wrong, press **Esc Esc → /rewind** instead of correcting on top of it.
     Note: rewind does not undo changes made through shell commands, so keep your zip/MD5 baselines.
  3. Say "prove it works": run the scenario test and `py_compile`, and show the output.
  4. For big searches, say "use a subagent and give me only the conclusion".
  5. Press Shift+Tab into **plan mode** for anything safety-adjacent. Claude can't edit until you approve.
  6. Use `/compact keep: MD5 baseline, safety state, open blockers` instead of waiting for auto-compact.
- **Also fix your skill** (edit it on claude.ai → Skills):
  - Its frontmatter appears twice at the top.
  - Its trigger words ("Claude prompts", "checkpoints", "packages") are so broad that all 800 lines load often.
  - Consider moving the trial rules into a separate `solar-sponge-trials` skill that loads only for trials.

**#10 · Serena, read-only** (github.com/oraios/serena, 31k★, GPL-3.0)
- **What:** finds a function inside your large Python file without reading the whole file.
- **Setup:**
  1. `winget install astral-sh.uv`
  2. `uv tool install -p 3.13 serena-agent`
  3. `set SERENA_USAGE_REPORTING=false`
  4. `claude mcp add --scope project serena -- serena start-mcp-server --context claude-code --project-from-cwd`
  5. Set `read_only: true` in the project's Serena config.
- **Why read-only:** Serena tells Claude to use *its own* edit tools, which would get around your hooks and the
  twin check. Lookups only.

### (c) Anything else

**#6 · gitleaks**
- **What:** scans a folder for keys and tokens, works without git, and is MIT licensed.
- **Setup:**
  1. Install: `winget install Gitleaks.Gitleaks`.
  2. Before building any zip, run `gitleaks dir -v "C:\Users\Tony\OneDrive\Desktop\V40 Version Y Powerstation"`.
  3. Add "gitleaks clean" to your package report.
- **Avoid trufflehog's default mode:** it checks keys it finds by sending them to the live service.

**#7 · Unblock Remote Control + voice**
- Your folders show as "not offered to cloud sessions". The usual fix is to **update the Claude desktop app on
  Tony-PC**, then check Settings → Claude Code → Remote Control. After that, cloud sessions like this one can work in
  your real folders.
- Voice: Claude Code has hold-to-talk dictation that works natively on Windows. It's faster than typing long briefs.
- Desktop **scheduled tasks** can run read-only jobs locally, for example a weekday 07:30 `/preflight`.
  Never schedule anything that arms or sends commands.

**#9 · Floorplan** (github.com/haydenschmitty/floorplan, 3k★, MIT)
- **What:**
  - a plain-English interactive map of an app
  - a Health panel showing where secrets live (names only)
  - flags open endpoints, open database rules and fakeable webhooks
- **Safety:** the cleanest install I reviewed. No hooks, no MCP server, local-only.
- **Best for:** CHARGECLAIM and PROJAA, or a new app before it goes online.
- **Setup:**
  1. `claude plugin marketplace add haydenschmitty/floorplan`
  2. `claude plugin install floorplan@floorplan`

---

## 3. Your "new app" workflow

Copy `templates/global-skills/new-app/` to `C:\Users\Tony\.claude\skills\new-app\`. Then type `/new-app` in any new folder.

1. **Plan:** a one-page `PLAN.md` from at most 5 questions. Flag anything touching money, devices or personal data.
2. **Sketch:** 3 quick, clearly different mock-ups of the main screen. You pick one. Prototypes beat specs for UI.
3. **DESIGN.md:** written from the chosen sketch, with one style direction and contrast-checked colours.
4. **Build:** a lean CLAUDE.md, one screen at a time, app running in the background, a screenshot after each screen.
5. **Quality gate:** `/ui-check`, score of 80 or more.
6. **Health check:**
   - gitleaks
   - Floorplan health panel
   - sign-in on endpoints that change data
   - verified payment webhooks
   - an `APP_MAP.md` file
7. **Ship:** README, rollback point, changelog line.

Default stack: plain HTML/CSS/JS, plus Python only if needed. Cloudflare Pages/Workers if it needs hosting
(you already have the Cloudflare plugin, and its free tier is enough).

---

## 4. Checked and not recommended (for you, today)

| Tool | Why not |
|---|---|
| styleseed, onlook, oh-my-design (full), sunil-dsb/design.md | Built for React/Next/Tailwind. Some add hooks, update checks or stealth scraping |
| open-design | Telemetry on by default, registers itself in every project |
| layr | Deliberately touches the whole app, which goes against your scope rule. Custom non-open licence |
| m3e-canvas, frontend-slides | Wrong job (Material mobile sketches, slide decks). Fine for side projects |
| claude-squad, agent-of-empires | Need tmux, so WSL only on Windows. claude-squad has an auto-yes mode |
| ccpm, spec-kitty | Built around GitHub Issues/git worktrees for teams. Overkill for you |
| Understand-Anything | Heavy token use, and its hooks tell Claude "don't ask the user" |
| ruler | Rewrites CLAUDE.md for 30 agents. You use one |
| context7 | Your APIs (Tesla, myenergi, Octopus) are mostly unofficial, so there's little to gain |
| "2api" account-pooling proxies, Claude Code runtime patches | Break provider terms and are a key-theft risk |

**Still useful to read** (no install):
- github.com/shanraisshan/claude-code-best-practice. Its tips are confirmed and summarised in §2 #5.
- The Part 2/3 prompts of github.com/KhazP/vibe-coding-prompt-template, for turning a vague idea into a clear spec.

---

## 5. Install checklist (Windows, about 75 minutes for everything)

Do these in a **copy** of the project first, or after a fresh zip baseline.

- [ ] `python --version` works (or switch `settings.json` to `py`)
- [ ] Copy `.claude\` (settings, hooks, skills) + `CLAUDE.md` + `DESIGN.md` into the project
- [ ] Restart Claude Code → `/hooks` shows the two hooks → config-read test is refused
- [ ] `/preflight` gives the 20-line report
- [ ] `/plugin install frontend-design@claude-plugins-official`
- [ ] `claude mcp add --scope project playwright -- cmd /c npx -y @playwright/mcp@latest --isolated`
- [ ] `/ui-check` with the bridge LOCKED gives screenshots and a score
- [ ] `winget install Gitleaks.Gitleaks` → `gitleaks dir -v .`
- [ ] Update the Claude desktop app → Remote Control folders become usable from cloud sessions
- [ ] Optional: Impeccable detect, Floorplan, Serena (read-only)

---

## Changelog

- **2026-11-06 (folder setup):** Reviewed the Karens Tax Issue setup. The layout is good, but its guards were left OFF.
  - Added a `/new-project` command: builds the house layout from one master template, with the guards ON, in App or Light size.
  - Added a `new_folder_check.py` start-up check. Tested with real Claude Code: in a new Desktop folder, Claude offers
    setup first and creates nothing.
  - `APPLY_ON_PC.md`:
    - step 3 switches Karen's guards on
    - step 3b makes each project's own save-check run
    - step 10 automates future folders
  - `/new-app` now calls `/new-project`.

- **2026-11-06 (pilot):** Ran the pilot on a demo dashboard (see `pilot/PILOT_REPORT.md`).
  - **Guards:** with guards, Claude was blocked from reading secrets and from enabling live dispatch. Without them it
    enabled live dispatch. The twin check kept main.js and main-live.js identical.
  - **Design** (blind scores, design / safety):
    - no rulebook: 83 / 80
    - rulebook v1: 74 / 85
    - rulebook v2 + quality gate: 84 / 90
  - **DESIGN.md v2:**
    - sentence-case labels
    - amber for below-limit values
    - command buttons: padlock, REAL COMMAND tag, blocked reasons, dashed while blocked
    - stacked tables on phone
    - no sideways scroll
    - one summary line per section
  - `/ui-check` now uses the two scorecards.
  - Added `test_guards.py` (11 checks) and `APPLY_ON_PC.md`.
  - Dropped `/preflight` and `/checkpoint` from the Powerstation pack, since your cape-* skills cover them.

- **2026-11-06 (later):** Added §1b from the read-only audit of all 12 Desktop folders.
  - Marked as already in place: gitleaks, Playwright, agents, checkpoint skills.
  - Added safety gaps S1–S8, speed gaps P1–P3 and design gaps D1–D3.
  - Checked against the docs: the AGENTS.md rule, auto-mode start and Grep skipping `.gitignore` files.
  - `guard.py` now also blocks `.dev.vars`.
  - Powerstation `settings.json` now asks before Playwright clicks or types.

- **2026-11-06:** First version.
  - Researched about 30 tools: GitHub topics vibe-coding / claude-code / agent-skills / design, and the official
    Claude Code docs. Read install scripts and SKILL.md files before recommending anything.
  - Wrote templates: DESIGN.md, CLAUDE.md, settings.json, `guard.py`, `twin_check.py`, `md5_report.py`, and the
    `/preflight`, `/ui-check`, `/checkpoint` and `/new-app` skills.
  - Hooks were tested against sample inputs in a Linux sandbox, not yet on Windows.
  - Pilot not yet run: waiting for your approval and access to a project folder.
