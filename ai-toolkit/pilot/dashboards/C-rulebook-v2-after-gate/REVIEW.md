# /ui-check result: design 74/100 (below 80, so revise), safety 85/100
Fix these, smallest change first, following DESIGN.md (v2):
1. Phone overflow: at 390px the page is 419px wide; card right borders are cut off. Must be no horizontal scroll.
2. "Retained export floor 4.5 kW" in the top strip is green, and the export bar in "Automation dispatch readiness" is filled green while it says BELOW FLOOR. Use the warning (stale amber) style for below-limit.
3. "Send Eco+ to Zappi" is too quiet: add padlock icon, "REAL COMMAND" tag and a bullet list of every blocking condition (dispatch LOCKED / NOT ARMED, Solar Sponge DRY-RUN, export 3.1 kW below 4.5 kW floor, grd sample stale 95 s > 30 s).
4. Weak hierarchy: every card looks equally important and LOCKED / NOT ARMED repeats three times in a row. Give each section one summary line (e.g. "1 stale feed, 1 missing"); only badge cards that differ from it.
5. Recent decisions table: no/yes cells sit off the row baseline. On phone (<600px) make rows stacked cards.
6. Chevron glyphs differ between sections: use one consistent marker.
7. Labels are forced uppercase ("TESLA VEHICLE SOC"). Use sentence case exactly as the brief names them.
