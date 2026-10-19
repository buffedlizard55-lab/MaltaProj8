#!/usr/bin/env python3
"""Rebuild in explicit ownership order; primary pages are written only by core."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    for command in (["node", "tools/build-site.js"],
                    [sys.executable, "scripts/build_site.py"],
                    [sys.executable, "scripts/build_core.py"]):
        subprocess.run(command, cwd=ROOT, check=True)

if __name__ == "__main__":
    main()
