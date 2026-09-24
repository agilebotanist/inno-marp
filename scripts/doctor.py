#!/usr/bin/env python3
"""Check that every tool the inno-marp pipeline uses is installed.

    python scripts/doctor.py

Prints one line per tool: OK, MISSING (required) or optional. Exit code 1 if a
required tool is missing. Installation instructions: docs/user/installation.md.
"""

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def version(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return (out.stdout or out.stderr).strip().splitlines()[0]
    except Exception:  # noqa: BLE001 — a version string is best effort
        return "found"


def drawio() -> str | None:
    # Reuse build-diagram.py's own search so the two can never disagree.
    spec = importlib.util.spec_from_file_location("bd", ROOT / "scripts" / "build-diagram.py")
    bd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bd)
    try:
        return bd.find_cli()
    except SystemExit:
        return None


def soffice() -> str | None:
    spec = importlib.util.spec_from_file_location("bdk", ROOT / "scripts" / "build-deck.py")
    bdk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bdk)
    try:
        return bdk.find_soffice()
    except SystemExit:
        return None


CHECKS = [
    # (label, required, how to find it, what it is for)
    ("node", True, lambda: shutil.which("node"), "runs marp, mmdc, vl2svg"),
    ("marp", True, lambda: shutil.which("marp"), "builds HTML / PDF / PPTX"),
    ("draw.io", True, drawio, "diagrams: .mmd -> .drawio -> .svg"),
    ("vl2svg", False, lambda: shutil.which("vl2svg"), "charts: .vl.json -> .svg"),
    ("mmdc", False, lambda: shutil.which("mmdc"), "fallback diagrams without draw.io"),
    ("soffice", False, lambda: soffice(), "editable PPTX (build-deck.py --pptx-editable)"),
]

PY_MODULES = [
    ("pdfplumber", False, "check-slide-overflow.py"),
    ("PIL", False, "build-theme.py --regen-jpeg (package: Pillow)"),
]


def main() -> int:
    missing = 0
    print(f"python   OK        {sys.version.split()[0]}"
          + ("" if sys.version_info >= (3, 10) else "   <- needs 3.10+"))
    if sys.version_info < (3, 10):
        missing += 1

    for label, required, find, purpose in CHECKS:
        path = find()
        if path:
            print(f"{label:<8} OK        {version([path, '--version'])}")
        else:
            tag = "MISSING " if required else "optional"
            missing += required
            print(f"{label:<8} {tag}  — {purpose}")

    for mod, required, purpose in PY_MODULES:
        ok = importlib.util.find_spec(mod) is not None
        tag = "OK      " if ok else ("MISSING " if required else "optional")
        missing += (required and not ok)
        print(f"{mod:<10} {tag}{'' if ok else '— ' + purpose}")

    theme = ROOT / "themes" / "innopolis.css"
    template = ROOT / "themes" / "innopolis.template.css"
    if not theme.exists():
        print("theme    MISSING   — run: python scripts/build-theme.py")
        missing += 1
    elif theme.stat().st_mtime < template.stat().st_mtime:
        print("theme    STALE     — template is newer; run: python scripts/build-theme.py")
    else:
        print(f"theme    OK        {theme.stat().st_size / 1024:.0f} KB")

    print()
    print("All required tools present." if not missing
          else f"{missing} required item(s) missing — see docs/user/installation.md")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
