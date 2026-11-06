# Undo the one-paste setup

Open the Claude desktop app → **Code** tab → a session in your **Desktop** folder, and paste:

```
UNDO TASK, approved by Tony. Use Python, not PowerShell. Do not touch any project code, data or private folders.
1. Open the newest folder in C:\Users\Tony\ai-toolkit\backups\ and read its SETUP_LOG.md.
2. For every file the log says was CHANGED: copy the backup copy back over it.
   For every file or folder the log says was CREATED: delete it (only those exact paths).
3. Run  python C:\Users\Tony\ai-toolkit\tools\snapshot.py take <backup>\undo.json  for the same Desktop folders, then
   compare <backup>\before.json with <backup>\undo.json. Everything except the ai-toolkit folder must match the
   original (ADDED 0, CHANGED 0, REMOVED 0).
4. Report the compare result in plain English. STOP.
```
