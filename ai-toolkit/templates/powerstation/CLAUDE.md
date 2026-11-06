# CLAUDE.md — Cape House / Abbots Way Power Station

Safety-critical home-energy project (Tesla Powerwall, MyEnergi Zappi, Octopus, Solar Sponge).
Full rules live in the `cape-house-power-station-safety-rules` skill. This file is the short version
Claude reads every turn. Keep it under ~60 lines.

## Map (read these, not the whole folder)
- Backend: `octopus_bridge_server.py` (large; Grep for the function, then Read only that range).
- Trial runner: `_trial_runner_L.py`. Scenario tests: `_es_*_scentest.py`.
- Frontend: `index.html`, `styles.css`, `main.js` == `main-live.js` (must stay byte-identical; a hook checks this).
- Status: newest ~80 lines of `CURRENT_SOURCE_FOR_CLAUDE.txt` + open items in `MASTER_DEFERRED_TODO.md`.
- UI rules: @DESIGN.md (read before any UI change).

## Always
- Inspect → explain → state risks → STOP for approval → smallest change → verify → short report → STOP.
- Never guess runtime facts. Missing data is not zero. Label live / dry-run / stale / cached / demo / armed.
- Prove changes: run the relevant `_es_*_scentest.py` and `python -m py_compile` on edited .py files; show the output.
- Use Python for edits/checks. No PowerShell for edits, packaging, endpoints or broad scans.
- Don't re-read files already read this session unless they changed. Don't dump large files.
- If an approach fails twice, stop and suggest /rewind instead of patching on top.

## Never (also enforced by hooks + permissions)
- Read/print config, logs, DB, tokens or keys. Report only booleans like `CONTROL_KEY_AVAILABLE_LOCALLY = YES`.
- Send Zappi/MyEnergi/OCPP/Tesla/Powerwall/HA/Alexa commands, arm, fire, or enable live flags without Tony's explicit approval.
- Package, lock, zip, deploy, SSH/SCP, curl external services without explicit approval.

## Slash commands
- `/preflight` — read-only baseline check (MD5s, twins, newest status).
- `/ui-check` — screenshot + score the dashboard against DESIGN.md.
- `/checkpoint` — append a verified checkpoint to the status docs.

## Report format
Pre-check · Files changed · New MD5s · Verification · Safety state · No-action statement · Commissioning update · Next · STOP
