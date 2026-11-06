---
name: ui-check
description: UI quality gate for the dashboard. Screenshots the page with the Playwright browser, scores it on two scorecards (design quality and safety clarity) against DESIGN.md, and lists fixes. Use after any change to index.html, styles.css or main.js, or when Tony says "ui check" or "does it look right".
disable-model-invocation: true
---

# /ui-check — look before you say "done"

Pre-req: the bridge/dashboard is already running locally (Tony started it) in its safe build-disabled /
dispatch LOCKED state. Never start, stop or restart the bridge yourself.
Read-only viewing only: use navigate, screenshot, snapshot, resize and evaluate-free page reads. Do NOT use
click/type/fill/press tools, except opening `<details>` accordions Tony named. If any button text mentions Eco+,
Stop, arm, fire, send, dispatch or OCPP, never touch it. If unsure, stop and ask.

1. Read `DESIGN.md`.
2. With the Playwright MCP browser, open the local dashboard URL from CURRENT_SOURCE_FOR_CLAUDE.txt.
   Screenshots at 1280px and 390px wide, light and dark colour scheme. Open the accordion(s) Tony names ($ARGUMENTS),
   otherwise the top-level view. At 390px check the page does not scroll sideways (page wider than the screen).
3. Score two scorecards, listing every deduction with where it is:

   **A. Design quality (100):** hierarchy & readability 30 · consistency (only DESIGN.md tokens, 4px spacing,
   ≤3 font sizes per panel) 25 · phone works, no sideways scroll, nothing hidden or cut off 20 · dark mode 15 · polish 10.

   **B. Safety clarity (100):** live / stale / cached / demo / no-data obvious at a glance 30 · red only for real
   danger, never for the safe LOCKED state, no green on below-limit values 20 · missing data never shown as 0 15 ·
   command buttons clearly different from safe ones and clearly blocked 20 · section names and buttons unchanged 15.

4. If either score is under 80: propose the smallest CSS-only fixes first. Apply them only if Tony approved UI edits
   in this task, then re-run steps 2–3 once and show both scores again.
5. Report: both scores, screenshots, top 5 issues (file:line), fixes made or proposed, TWINS_IDENTICAL, STOP.
