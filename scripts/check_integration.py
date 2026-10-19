#!/usr/bin/env python3
"""Structural release gate. Never represents tests as legal verification."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import argparse
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CORE = ("index.html", "executive-summary.html", "work-rules.html", "coverage-options.html",
        "findings.html", "verification.html", "flagged.html", "archives.html", "playbook.html")
SKIP = {".git", ".cache", "__pycache__", "node_modules", "dist", "build", ".venv"}

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag in ("a", "link") and a.get("href"):
            self.refs.append(a["href"])
        if tag in ("img", "script", "source", "iframe") and a.get("src"):
            self.refs.append(a["src"])

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", help="Check staged artifact instead of source tree")
    args = parser.parse_args()
    root = (ROOT / args.site).resolve() if args.site else ROOT
    errors = []
    data = json.loads((root / "data/core.json").read_text())
    for row in data["findings"]:
        review = row.get("review", {})
        if not review.get("checked_on") or not review.get("locator"):
            errors.append(f"{row['id']}: no dated review location")
        if row["status"] == "unverified" and row["value"]:
            errors.append(f"{row['id']}: unverified value filled")
    records = {r["id"]: r for r in data["findings"]}
    for fid in ("F37", "F39", "F40", "F41", "F42", "F67", "F71", "F73", "F74"):
        if records[fid]["value"] or records[fid]["status"] != "unverified":
            errors.append(f"{fid}: unknown personal/tax value must stay blank and unverified")
    if "half-time" not in records["F05"]["value"] or "OR" not in records["F05"]["value"]:
        errors.append("half-time education must be an independent alternative")
    for name in CORE:
        text = (root / name).read_text()
        for stale in ("<!-- integration-links -->", "<!-- EXTENDED-FLAGS:START -->", "tobacco use", "$63,840"):
            if stale in text:
                # The flag page may cite an old figure explicitly as not certified.
                if stale == "$63,840" and name in ("flagged.html", "executive-summary.html", "verification.html"):
                    continue
                errors.append(f"{name}: stale/unsupported primary content {stale}")
        if 'id="main-content"' not in text or 'href="#main-content"' not in text:
            errors.append(f"{name}: missing accessible skip target")
    if len((root / "index.html").read_bytes()) > 32000:
        errors.append("landing page duplicates too much detail; keep the full tables on category pages")
    if not args.site:
        before = {p: digest(ROOT / p) for p in CORE}
        subprocess.run([sys.executable, "scripts/build_site.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        if any(digest(ROOT / p) != before[p] for p in CORE):
            errors.append("extended generator modified primary pages owned by build_core.py")
    # CSS merge remnants may silently invalidate a selector while links pass.
    for pattern in ("*.html", "*.css", "*.js"):
        for asset in root.rglob(pattern):
            if any(part in SKIP for part in asset.relative_to(root).parts):
                continue
            if re.search(r"^(?:<<<<<<< |=======$|>>>>>>> )", asset.read_text(), re.M):
                errors.append(f"Merge marker in {asset.relative_to(root)}")
    docs = {}
    for p in root.rglob("*.html"):
        if any(part in SKIP for part in p.relative_to(root).parts):
            continue
        doc = Document()
        doc.feed(p.read_text(encoding="utf-8"))
        docs[p.resolve()] = doc
        duplicates = [x for x,n in Counter(doc.ids).items() if n > 1]
        if duplicates:
            errors.append(f"{p.relative_to(root)}: duplicate ids {duplicates}")
    links = 0
    for path, doc in docs.items():
        for ref in doc.refs:
            u = urlsplit(ref)
            if u.scheme or u.netloc or ref.startswith("//"):
                continue
            target_path = unquote(u.path)
            if target_path.startswith("/MaltaProj8/"):
                dest = root / target_path[len("/MaltaProj8/"):]
            elif target_path.startswith("/"):
                dest = root / target_path.lstrip("/")
            else:
                dest = path.parent / target_path if target_path else path
            dest = dest.resolve()
            if not dest.is_relative_to(root):
                errors.append(f"{path.name}: path escapes publication root: {ref}")
                continue
            if dest.is_dir():
                dest = dest / "index.html"
            links += 1
            if not dest.is_file():
                errors.append(f"{path.relative_to(root)}: missing local file {ref}")
            elif u.fragment and dest in docs and unquote(u.fragment) not in docs[dest].ids:
                errors.append(f"{path.relative_to(root)}: missing fragment {ref}")
    if args.site:
        if (root / ".git").exists() or (root / ".github").exists():
            errors.append("private/build internals in public artifact")
        for path in docs:
            if path.relative_to(root).as_posix() not in CORE and "Preserved reference — not freshly certified" not in path.read_text():
                errors.append(f"{path}: historical status warning missing")
    if errors:
        print("FAIL\n" + "\n".join(errors))
        return 1
    print(f"PASS: {len(docs)} pages, {links} local links/assets/fragments; {len(records)} review records; ownership and blank-value guards.")
    print("Structural checks only: external HTTP availability and legal truth are not tested.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
