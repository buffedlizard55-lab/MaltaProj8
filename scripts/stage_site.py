#!/usr/bin/env python3
"""Stage a static Pages artifact, never Git internals/caches/credentials.

Historical outputs are preserved, with a visible current-guide notice added
in the published copy only. Source files in the repository remain intact.
"""
from pathlib import Path
import shutil
import os

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "dist"
DIRS = ("assets", "site", "data", "docs", "research", "coverage-guide", "scripts", "tools")
EXTS = {".html", ".css", ".js", ".json", ".md", ".csv", ".pdf", ".py", ".txt", ".png", ".jpg", ".svg"}
SKIP = {".git", ".cache", "__pycache__", "node_modules", "dist", "build", ".venv"}
CORE = {"index.html", "executive-summary.html", "work-rules.html", "coverage-options.html",
        "findings.html", "verification.html", "flagged.html", "archives.html"}

def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
    files = [p for p in ROOT.iterdir() if p.is_file() and p.suffix in EXTS]
    for directory in DIRS:
        files.extend(p for p in (ROOT / directory).rglob("*")
                     if p.is_file() and not p.is_symlink() and p.suffix in EXTS
                     and not any(part in SKIP for part in p.relative_to(ROOT).parts))
    for path in sorted(files):
        rel = path.relative_to(ROOT)
        dest = DEST / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".html" and rel.as_posix() not in CORE:
            prefix = os.path.relpath(DEST, dest.parent).replace(os.sep, "/")
            text = path.read_text(encoding="utf-8")
            notice = ('<aside role="note" style="padding:14px 20px;background:#fff7e6;color:#563c12;'
                      'border-bottom:1px solid #d6b36a;font:15px/1.5 system-ui">'
                      '<strong>Preserved reference — not freshly certified as current advice.</strong> '
                      f'Read the <a href="{prefix}/executive-summary.html">current executive summary</a> '
                      f'and <a href="{prefix}/flagged.html">Flagged for Review</a> before relying on an older claim. '
                      'Some historical tables have unresolved source-link gaps.</aside>')
            import re
            text, count = re.subn(r'(<body\b[^>]*>)', lambda m: m.group(1) + notice, text, count=1, flags=re.I)
            if count != 1:
                raise SystemExit(f"Missing body: {rel}")
            dest.write_text(text, encoding="utf-8")
        else:
            shutil.copyfile(path, dest)
    (DEST / ".nojekyll").touch()
    print(f"Staged {len(files)} public files to dist; historical pages visibly labelled.")

if __name__ == "__main__":
    main()
