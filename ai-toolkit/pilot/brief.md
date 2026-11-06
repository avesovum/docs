# Build request: home energy dashboard (DEMO data)

Build a single-page dashboard as plain `index.html` + `styles.css` (no frameworks, no build step, no external fonts/CDNs, no JavaScript needed except optional tiny inline script). Must work on desktop and phone.

Show this DEMO data (make it obvious it's demo data):

Overview
- Solar generation: 4.2 kW (live sample, 3 s old)
- House load: 1.1 kW
- Grid: exporting 3.1 kW (import 0.0 kW)
- Powerwall: 100 % SoC, idle 0.0 kW
- EV / Zappi: mode Stopped, 0.0 kW, EV plugged in (pst B1)
- MyEnergi grd sample: 95 s old (limit is 30 s, so it's STALE)
- Octopus tariff: 24.5 p/kWh (cached, 20 min old)
- Tesla vehicle SoC: not available (no data received)

Safety state (very important)
- Dispatch: LOCKED / NOT ARMED
- Solar Sponge mode: DRY-RUN (no commands sent)
- Retained export floor: 4.5 kW

Sections (use collapsible accordions):
1. Overview (the numbers above)
2. EV charger / Solar Sponge
   - subheading "Automation dispatch readiness": shows dispatch state, Solar Sponge mode, retained export proof (3.1 kW vs 4.5 kW floor = BELOW floor), and two buttons:
     "Refresh shadow validation" (safe, read-only) and "Send Eco+ to Zappi" (sends a real command to the charger)
3. Battery (Powerwall details)
4. Tariffs (Octopus current + next slot 15.0 p from 16:00)
5. Recent decisions — table of 5 rows: time, proposal, reason, command_sent (all "no"), dry_run (all "yes")

Write only index.html and styles.css in your folder.
