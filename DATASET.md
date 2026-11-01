# Dataset

| File | Source URL | Pages | Licence / terms | Downloaded on |
|---|---|---|---|---|
| OWASP Juice Shop source code (TypeScript/Angular front end, Node.js routes, challenge definitions) | https://github.com/juice-shop/juice-shop (commit 717f5efa886b0417eeecb52378b03cf10567b7e2) | 918 source files (source code, so one file counts as one page) | MIT licence | 1 Nov 2026 |
| of which: code-fix files (`data/static/codefixes/`) | https://github.com/juice-shop/juice-shop/tree/717f5efa886b0417eeecb52378b03cf10567b7e2/data/static/codefixes | 160 files (.ts, .yml, .sol, .tf) | MIT licence | 1 Nov 2026 |

## How the data was collected

- Command: `python tools/fetch_juiceshop.py`
- It shallow-clones the Juice Shop repository into `data/raw/juice-shop/`, keeps source files only (.ts, .js, .html, .yml, .yaml, .json, .info, .md, .sol, .tf) and skips `node_modules`, `dist`, `i18n`, `assets` and similar folders.
- `data/manifest.csv` lists every kept file with its source URL, download date, size in bytes and SHA-256.
- Verified counts at commit 717f5ef: 918 source files, of which 160 are code-fix files.

Full data lives in `data/raw/` (not committed). A small sample is in `data/sample/`.