---
name: ui-check
description: UI quality gate for the dashboard. Screenshots the page with the Playwright browser, scores it against DESIGN.md, and lists fixes. Use after any change to index.html, styles.css or main.js, or when Tony says "ui check" or "does it look right".
disable-model-invocation: true
---

# /ui-check — look before you say "done"

Pre-req: the bridge/dashboard is already running locally (Tony started it). Never start, stop or restart the bridge yourself.
Never click buttons that can send commands. Read-only viewing only.

1. Read `DESIGN.md`.
2. With the Playwright MCP browser, open the local dashboard URL from CURRENT_SOURCE_FOR_CLAUDE.txt.
   Take screenshots at 1280px and 390px wide, in light and dark colour scheme. Expand the accordion(s) Tony names ($ARGUMENTS), otherwise only the top-level view.
3. Score 0–100 with this rubric (deduct points, list each deduction):
   - Safety badges (30): every device panel shows a state badge with word + icon; ARMED is the only solid red; missing data shows "— no data", not 0; live numbers show an age.
   - Consistency (25): only DESIGN.md tokens; spacing on the 4px scale; max 3 font sizes per panel; numbers tabular.
   - Readability (20): contrast, label/value hierarchy, units muted, nothing truncated at 390px.
   - Layout stability (15): section names, order and button labels unchanged unless the task said so.
   - Polish (10): no AI-default habits from DESIGN.md §7.
4. If score < 80: propose the smallest CSS-only fixes first. Do not apply them unless Tony approved UI edits in this task.
5. Report: score, screenshots, top 5 issues (file:line), proposed fixes, TWINS_IDENTICAL, STOP.
