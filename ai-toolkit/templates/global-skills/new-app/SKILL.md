---
name: new-app
description: Tony's repeatable new-app workflow - plan, sketch, build with DESIGN.md, quality gate, health check, ship. Use when Tony says "new app", "start a project", or describes an app idea from scratch.
disable-model-invocation: true
---

# /new-app — plan → sketch → build → gate → health check → ship

Work in small, checkable stages. STOP after each stage for Tony's OK. Plain English, no jargon.

## 1. Plan (≤ 15 min, one page)
Ask at most 5 questions, then write `PLAN.md`: who it's for, the 3 core jobs it does, screens list,
data it stores, anything that touches money/devices/personal data (= safety-critical → flag it), what "done" looks like.
Default stack unless Tony says otherwise: plain HTML + CSS + JS (no build step), Python backend only if needed.
Hosting option if wanted: Cloudflare Pages/Workers (free tier).

## 2. Sketch (prototypes beat specs for UI)
Make 3 quick, clearly different one-file HTML mockups of the main screen in `sketches/` (fake data, labelled DEMO).
Screenshot them. Tony picks one (or mixes). No real logic yet.

## 3. DESIGN.md
Write `DESIGN.md` from the chosen sketch: one style direction, colour tokens (WCAG AA checked), type scale,
4px spacing scale, components, and a "don'ts" list. Every later UI change must follow it.

## 4. Build
Write `CLAUDE.md` (≤ 60 lines: map, always/never, how to run, how to test). Build one screen at a time.
Run the app in the background so its logs are readable. After each screen: prove it works (run it, screenshot it).

## 5. Quality gate
Run `/ui-check` (or the same rubric): screenshots at 1280 and 390 px, light + dark, score ≥ 80 or fix.

## 6. Health check (before anyone else uses it)
- No keys/secrets in code or git history (run gitleaks if installed).
- Every endpoint that changes data needs sign-in; database rules not open to the world.
- Payment webhooks verify signatures. Inputs validated. Errors don't leak stack traces.
- Write a plain-English `APP_MAP.md`: screens, data, where secrets live (names only), how to roll back.

## 7. Ship
Checklist: README with run steps, version tag / dated zip (only if Tony asks), rollback target noted, changelog line.
