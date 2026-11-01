"""Clone OWASP Juice Shop and log every source file to data/manifest.csv.
Usage: python tools/fetch_juiceshop.py
Raw files go to data/raw/juice-shop (git-ignored); the manifest is committed."""

import csv
import hashlib
import os
import subprocess
from datetime import date

REPO = "https://github.com/juice-shop/juice-shop.git"
DEST = "data/raw/juice-shop"
MANIFEST = "data/manifest.csv"
KEEP = {".ts", ".js", ".html", ".yml", ".yaml", ".json", ".info", ".md", ".sol", ".tf"}
SKIP_DIRS = {"node_modules", ".git", "dist", "i18n", "assets", "build", "coverage"}
SKIP_FILES = {"package-lock.json"}


def main():
    if not os.path.exists(DEST):
        os.makedirs(os.path.dirname(DEST), exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", REPO, DEST], check=True)
    commit = subprocess.check_output(["git", "-C", DEST, "rev-parse", "HEAD"], text=True).strip()
    print("Juice Shop commit:", commit)

    rows = []
    for root, dirs, files in os.walk(DEST):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_FILES or os.path.splitext(name)[1].lower() not in KEEP:
                continue
            path = os.path.join(root, name)
            rel = os.path.relpath(path, DEST).replace("\\", "/")
            with open(path, "rb") as f:
                data = f.read()
            rows.append(
                [
                    path.replace("\\", "/"),
                    f"https://github.com/juice-shop/juice-shop/blob/{commit}/{rel}",
                    date.today().isoformat(),
                    len(data),
                    hashlib.sha256(data).hexdigest()[:16],
                ]
            )

    os.makedirs("data", exist_ok=True)
    with open(MANIFEST, "w", newline="", encoding="utf-8") as mf:
        w = csv.writer(mf)
        w.writerow(["file", "source_url", "downloaded_on", "bytes", "sha256"])
        w.writerows(rows)

    fixes = sum(1 for r in rows if "/codefixes/" in r[0])
    print(f"Total source files: {len(rows)}")
    print(f"Code-fix files:     {fixes}")


if __name__ == "__main__":
    main()
