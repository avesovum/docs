# DESIGN.md — Cape House Power Station dashboard

> Read this file before building or changing any UI (index.html, styles.css, main.js / main-live.js).
> It is the single source of truth for how the dashboard looks. If code and this file disagree, ask Tony.
> v2 (2026-11-06): updated after the pilot's blind review. STARTER VERSION: written without seeing the current styles.css. First job: compare with styles.css,
> keep what already works, and update the tokens below to match. Don't restyle the whole app in one go.

## 1. Style direction (pick one and stick with it)

**"Calm control room."** Quiet, dense, readable at a glance. Think aircraft instrument panel, not marketing site.

- Information first: numbers and states are the hero, not decoration.
- Low chrome: flat surfaces, 1px borders, no gradients, no glassmorphism, no glow, no emoji in UI.
- Colour only *means* something: every colour is tied to an energy flow or a safety state (see §3, §4).
- Same layout every time: Tony's test instructions point to "page → accordion → subheading → button", so
  section names, order and button labels must not move or be renamed without approval.

## 2. Tokens (CSS custom properties — put these at the top of styles.css)

```css
:root {
  /* surfaces */
  --bg:#F6F7F9; --surface:#FFFFFF; --border:#D9DEE5;
  --text:#14181F; --text-muted:#525B6B; --accent:#1F5FD6;
  /* energy flows (all ≥4.5:1 on --bg and --surface) */
  --solar:#A15C00; --export:#1B7A43; --import:#B3261E; --battery:#0B6E8A; --ev:#6B46C1;
  /* spacing — 4px base. Use ONLY these */
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px; --s7:48px;
  /* radius, type */
  --radius:6px; --radius-lg:10px;
  --font: system-ui, "Segoe UI", Roboto, sans-serif;
  --mono: ui-monospace, "Cascadia Mono", Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root {
  --bg:#0E1116; --surface:#161B22; --border:#2A313C;
  --text:#E6EAF0; --text-muted:#9AA4B2; --accent:#6EA8FE;
  --solar:#F2B33D; --export:#4CC38A; --import:#FF7B72; --battery:#4FC3E0; --ev:#B39DFF;
}}
```

Contrast was checked (WCAG AA, text ≥ 4.5:1) for every text/flow colour on both `--bg` and `--surface`, light and dark.

## 3. Energy-flow colours (never swap these)

| Flow | Token | Used for |
|---|---|---|
| Solar generation | `--solar` | PV kW, solar window |
| Export to grid | `--export` | export kW, retained export floor |
| Import from grid | `--import` | grid import (always a warning) |
| Powerwall | `--battery` | SoC %, charge/discharge kW |
| EV / Zappi | `--ev` | Zappi mode, EV kW, Eco+ |

## 4. Safety-state badges (most important rule in this file)

Every panel that shows device data **must** show one state badge. A badge is always **word + icon + colour**, never colour alone (colour-blind safe, screenshot-safe).

| State | Look | Notes |
|---|---|---|
| LIVE | outline `--export`, dot ● | fresh sample, show age e.g. "LIVE · 4s" |
| STALE | solid amber bg, dark text, ⚠ | sample older than limit; show age |
| CACHED / DEMO / DRY-RUN / ADVISORY / READ-ONLY | grey outline, text label | must never look like LIVE |
| NOT ARMED / LOCKED | grey outline, 🔒-style padlock icon (SVG) | the normal resting state |
| ARMED / LIVE-FIRE | **solid `--import` red fill, white text** | the only solid-red element on the page |

Rules: missing data shows "—  no data" in `--text-muted`, never `0`. Ages are always shown next to live numbers.
A page or panel showing demo/cached data must never show a LIVE badge.
Pass/fail is not a flow colour: a value below its limit (e.g. export below the 4.5 kW floor) uses the STALE amber
warning style for its bar/badge, never green. Green (`--export`) means only "exporting energy".
Don't repeat the same badge on every card: each section summary shows ONE line such as "1 stale feed, 1 missing";
cards only get a badge when they differ from that summary.

## 5. Type

- Body 14px / 1.45, `--font`. Labels 12px, sentence case, `--text-muted`. Never force uppercase: labels must read exactly
  as the section/field names Tony uses in test instructions.
- Key numbers (kW, %, £) 24–32px, `font-variant-numeric: tabular-nums`, weight 600. Units smaller and muted: **3.2** kW.
- IDs, MD5s, raw values, log lines: `--mono` 12px.
- Max 3 font sizes per panel.

## 6. Layout & components

- Page max-width 1280px, gutter `--s4` (16px on phones). Grid of cards: `repeat(auto-fit, minmax(280px, 1fr))`, gap `--s4`.
- Card: `--surface`, 1px `--border`, `--radius-lg`, padding `--s4`. Header row = title (left) + state badge (right).
- Accordions: native `<details><summary>`; summary shows section name + worst state inside it.
- Buttons: primary (filled `--accent`) only for safe actions, with a small "SAFE · read-only" tag.
  Any command-capable button: outlined `--import` red, padlock icon when unavailable, a "REAL COMMAND" tag, the exact
  action label ("Send Eco+ to Zappi"), a confirm step, and when blocked a bullet list of every condition blocking it.
  Never fill a command button solid while dispatch is LOCKED.
- Tables: right-align numbers, zebra off, row hover only. Below 600px wide, tables become stacked cards (one card per
  row, label: value) so no column is hidden, especially command_sent and dry_run.
- Phone (390px): no horizontal scroll ever. Use `min-width: 0` on grid/flex children, `overflow-wrap: anywhere` on long
  values, and `grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr))`.
- Touch targets ≥ 40px. Focus ring: 2px `--accent` outline, offset 2px. Never remove focus outlines.

## 7. Don'ts (AI-default habits to avoid)

No purple/blue gradients, no oversized hero, no centred marketing copy, no card shadows deeper than 0 1px 2px,
no rounded-full pills everywhere, no icon in every heading, no fake data that looks live, no new fonts from the web.

## 8. Quality gate before saying "done"

1. Screenshot at 1280px and 390px wide, light and dark (Playwright MCP). Check the page has no horizontal scroll at 390px.
2. Check every panel has a state badge and every number has a unit and an age.
3. Only tokens from §2 used (search styles.css for raw hex values and px outside the scale).
4. main.js and main-live.js still byte-identical.
5. Report: what changed, screenshots, anything that didn't match this file.
