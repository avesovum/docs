"""Before/after fingerprint of project folders, so we can PROVE the setup changed nothing it shouldn't.

  python snapshot.py take   <out.json> <folder> [<folder> ...]
  python snapshot.py compare <before.json> <after.json>

- Normal files: MD5 of their contents (any change shows up).
- Private/secret/runtime files and folders (Images, Karens Paperwork, output, config, .env, keys, DB, logs, zips):
  NOT opened. Only size and modified-time are recorded.
- Skips .git folders and the ai-toolkit folder itself. Read-only: never writes anywhere except <out.json>.
"""
import hashlib
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", ".gradle", "build", "__pycache__", ".venv", "ai-toolkit"}
PRIVATE_DIRS = {"images", "karens paperwork", "output", "secrets", "credentials"}
NO_OPEN = re.compile(r"(config.*\.json$|\.env(\..*)?$|\.dev\.vars$|\.(key|pem|jks|keystore|p12|pfx|db|db-wal|db-shm|"
                     r"sqlite3?|log|zip|apk|aab)$|token|secret|credential)", re.I)


def take(out, roots):
    snap = {}
    for root in roots:
        root = os.path.abspath(root)
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            private = any(part.lower() in PRIVATE_DIRS for part in os.path.relpath(dirpath, root).split(os.sep))
            for f in files:
                p = os.path.join(dirpath, f)
                try:
                    st = os.stat(p)
                    if private or NO_OPEN.search(f) or st.st_size > 50_000_000:
                        snap[p] = f"stat:{st.st_size}:{int(st.st_mtime)}"
                    else:
                        h = hashlib.md5()
                        with open(p, "rb") as fh:
                            for chunk in iter(lambda: fh.read(1 << 20), b""):
                                h.update(chunk)
                        snap[p] = "md5:" + h.hexdigest()
                except OSError as e:
                    snap[p] = f"error:{e.__class__.__name__}"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, indent=0)
    print(f"Recorded {len(snap)} files from {len(roots)} folder(s) -> {out}")


def compare(a, b):
    A = json.load(open(a, encoding="utf-8"))
    B = json.load(open(b, encoding="utf-8"))
    added = sorted(set(B) - set(A))
    removed = sorted(set(A) - set(B))
    changed = sorted(p for p in set(A) & set(B) if A[p] != B[p])
    print(f"UNCHANGED: {len(set(A) & set(B)) - len(changed)} files")
    for title, items in (("ADDED", added), ("CHANGED", changed), ("REMOVED", removed)):
        print(f"{title}: {len(items)}")
        for p in items:
            print("   ", p)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "take":
        take(sys.argv[2], sys.argv[3:])
    elif len(sys.argv) == 4 and sys.argv[1] == "compare":
        compare(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(1)
