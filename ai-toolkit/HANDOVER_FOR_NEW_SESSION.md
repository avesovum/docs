# Handover: AI toolkit setup (from cloud session, 2026-11-06)

**For the Claude Code session that starts in `Desktop\Tools Research`.** Read this first, then follow "First actions".

## Who and what
- **Tony:** Windows PC, Claude desktop app and Claude Code 2.1.312, Python 3.14. Not a professional developer.
  - Wants plain English, recommendations first, exact steps, and "Tony, …" at the start of questions.
  - Wants nothing that interferes with how his projects work today.
- **Projects** (all on `C:\Users\Tony\OneDrive\Desktop`):
  - V40 Version Y Powerstation: safety-critical home-energy bridge plus dashboard; it has its own Cape House skill and rules
  - PROJAA, RearPeek, WRENMINT Control, Wrenmint.com website: apps
  - Karens Tax Issue, APP FAMILY: these hold tax and personal data
  - Docs-only folders: App Family invention, MEMORY BEAR BUSINESS, APP FAMILY RESEARCH, Tesla Music, APPS and CONNECTORS
- **Tools Research:** the home of this toolkit and of future AI-tools research.
  The toolkit lives at `Desktop\Tools Research\ai-toolkit\`.

## What the cloud session did (all inside the toolkit; nothing on the PC was changed)
1. **Researched about 30 AI design and coding tools.** It read their install scripts for safety. Results and the
   "skip" list are in `README.md` §1b and §4.
2. **Audited all 12 folders on the PC (read-only).** It found:
   - APP FAMILY runs no secret scan
   - Claude's Read tool isn't blocked from secret files
   - Karen's guards are switched off
   - the project save-checks don't run
   - Powerstation's CLAUDE.md is 701 lines
   - CLAUDE.md doesn't import AGENTS.md in some projects
   - there's no DESIGN.md anywhere
3. **Ran a pilot on a demo dashboard** (`pilot/PILOT_REPORT.md`):
   - **Guards:** with guards, real Claude Code could not read the secret file or switch live dispatch ON. Without
     guards, it switched it ON.
   - **DESIGN.md + `/ui-check`:** blind scores went from 83/80 to 84/90 (design / safety clarity).
4. **Narrowed the guards so they don't interfere.** 23 self-tests pass, 10 of them proving normal work still runs.
5. **Built:**
   - `SETUP_ALL.md`: one-paste setup with backups and before/after proof
   - `UNDO.md`
   - `/new-project` and the start-up check, so future folders set themselves up with the guards on
   - `/new-app`

## Decisions Tony has made
- Do the safe setup ("take control and set all of this up"), but nothing may break or change code, logic, maths or devices.
- Keep his existing way of working: the cape-* skills, checkpoints, handovers and the RearPeek/Karen folder layout.
- Future project folders: Claude offers setup automatically; Tony says yes or no.

## NOT done yet, and not approved
DESIGN.md for real apps, slimming Powerstation's CLAUDE.md, making each project's own pre-commit hook run (step 3b),
and changing permission start modes. Offer these only after the setup is finished and checked.

## First actions in this session
1. Confirm `Desktop\Tools Research\ai-toolkit\SETUP_ALL.md` exists. If the toolkit is elsewhere, STOP and ask Tony.
2. Tell Tony in 3–4 plain lines what you're about to do (SETUP_ALL), what he'll notice afterwards, and how to undo.
3. Run `SETUP_ALL.md` with **T = `C:\Users\Tony\OneDrive\Desktop\Tools Research\ai-toolkit`**. Tony approved this job.
   - Wherever the copied skill or hook files say `C:\Users\Tony\ai-toolkit`, replace it with T.
   - Put the backup folder B under T. snapshot.py skips any folder named `ai-toolkit`, so the backups don't show up as
     changes.
4. Show Tony the final table. Then offer, recommendations first: (a) set up Tools Research itself as a **Light**
   project with `/new-project`; (b) the not-yet-approved items above, one at a time.
