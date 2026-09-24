#!/usr/bin/env python3
"""
Build a slide-ready SVG diagram through the draw.io pipeline, themed for Innopolis.

    Mermaid (.mmd)  ->  .drawio  ->  [re-theme]  ->  .svg (with XML embedded)

Why the extra theming pass: draw.io's Mermaid importer honours per-node
`style X fill:,stroke:,color:` directives but SILENTLY DROPS `%%{init}%%`
themeVariables and `linkStyle` lines. So unstyled nodes come out in draw.io's
default lavender, edges in its default gray, and the font as Trebuchet MS.
This script rewrites those defaults to the Innopolis palette after conversion.

Usage:
    python scripts/build-diagram.py media/flow.mmd
    python scripts/build-diagram.py media/flow.drawio          # skip conversion
    python scripts/build-diagram.py media/*.mmd                # batch
    python scripts/build-diagram.py media/flow.mmd --format png
    python scripts/build-diagram.py media/flow.mmd --no-theme  # keep draw.io defaults
    python scripts/build-diagram.py media/d.drawio --layout verticalFlow

Outputs land next to the input. Commit all three files: the .mmd you wrote,
the .drawio (editable source of truth), and the .svg the deck renders.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Innopolis palette — keep in sync with themes/innopolis.template.css
GREEN = "#019546"
GREEN_DARK = "#2D6E2A"
CARD_GREEN = "#f0f8f0"
TEXT = "#282828"
FONT = "Tahoma,Verdana,DejaVu Sans,sans-serif"

# draw.io defaults produced by its Mermaid importer, and what to replace them with
DEFAULT_REWRITES = [
    # unstyled node fill / stroke / text
    (r"fillColor=light-dark\(#ECECFF,#1f2020\)", f"fillColor={CARD_GREEN}"),
    (r"strokeColor=light-dark\(#9370DB,#cccccc\)", f"strokeColor={GREEN}"),
    (r"fontColor=light-dark\(#333333,#cccccc\)", f"fontColor={TEXT}"),
    # edge stroke
    (r"strokeColor=light-dark\(#333333,#cccccc\)", f"strokeColor={GREEN_DARK}"),
    # font family, everywhere
    (r"fontFamily=Trebuchet MS,Verdana,Arial,sans-serif", f"fontFamily={FONT}"),
]

CANDIDATE_CLI = [
    "draw.io",  # Windows scoop shim (note the dot)
    "drawio",   # Linux .deb / snap
    str(Path.home() / "scoop" / "shims" / "draw.io.exe"),
    r"C:\Program Files\draw.io\draw.io.exe",
    str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "draw.io" / "draw.io.exe"),
    "/Applications/draw.io.app/Contents/MacOS/draw.io",
    "/opt/drawio/drawio",
]


def find_cli() -> str:
    env = os.environ.get("DRAWIO_CLI")
    if env and Path(env).exists():
        return env
    for cand in CANDIDATE_CLI:
        if os.path.isabs(cand):
            if Path(cand).exists():
                return cand
        elif shutil.which(cand):
            return shutil.which(cand)
    sys.exit(
        "draw.io Desktop CLI not found.\n"
        "Install draw.io Desktop (see docs/user/installation.md), or point\n"
        "DRAWIO_CLI at the executable. On Windows via scoop the binary is\n"
        "`draw.io` (with a dot), not `drawio`."
    )


def run(cli: str, args: list[str]) -> None:
    proc = subprocess.run([cli, *args], capture_output=True, text=True)
    # draw.io Desktop exits 0 even on some failures, so check the output file instead
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout + proc.stderr)
        raise RuntimeError(f"draw.io exited {proc.returncode}")


def theme_drawio(path: Path) -> int:
    """Rewrite draw.io importer defaults to the Innopolis palette. Returns #edits."""
    xml = path.read_text(encoding="utf-8")
    total = 0
    for pattern, repl in DEFAULT_REWRITES:
        xml, n = re.subn(pattern, repl, xml)
        total += n
    if total:
        path.write_text(xml, encoding="utf-8")
    return total


def build(src: Path, fmt: str, cli: str, do_theme: bool, layout: str | None) -> None:
    if src.suffix == ".mmd":
        drawio = src.with_suffix(".drawio")
        run(cli, ["-x", "-f", "xml", "-o", str(drawio), str(src)])
        if not drawio.exists():
            raise RuntimeError(f"conversion produced no output: {drawio}")
        print(f"  {src.name} -> {drawio.name}")
    elif src.suffix == ".drawio":
        drawio = src
    else:
        raise ValueError(f"expected .mmd or .drawio, got {src.suffix}")

    if layout:
        run(cli, ["-x", "-f", "xml", "--layout", layout, "-o", str(drawio), str(drawio)])
        print(f"  layout {layout} applied")

    if do_theme:
        n = theme_drawio(drawio)
        print(f"  themed {drawio.name} ({n} style edits)")

    out = drawio.with_suffix(f".{fmt}")
    # -e embeds the diagram XML so the export reopens in draw.io as editable
    args = ["-x", "-f", fmt, "-e", "-b", "10"]
    if fmt == "svg":
        # --embed-svg-fonts defaults to TRUE, which base64-inlines the whole
        # font and, for HTML labels, rasterises them into embedded PNGs. That
        # turned a 7 KB diagram into 200 KB and a 22 KB one into 404 KB, with
        # the text no longer selectable or scalable. Off: real <text>, ~95%
        # smaller, and the font falls back to the stack named in the style.
        args += ["--embed-svg-fonts", "false"]
    run(cli, args + ["-o", str(out), str(drawio)])
    if not out.exists():
        raise RuntimeError(f"export produced no output: {out}")
    print(f"  {drawio.name} -> {out.name} ({out.stat().st_size/1024:.1f} KB)")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("inputs", nargs="+", type=Path, help=".mmd or .drawio files")
    ap.add_argument("--format", default="svg", choices=["svg", "png", "pdf"],
                    help="export format (default: svg)")
    ap.add_argument("--no-theme", action="store_true",
                    help="keep draw.io's default colors instead of the Innopolis palette")
    ap.add_argument("--layout", help="ELK layout to apply: verticalFlow, horizontalFlow, organic, tree, circle")
    args = ap.parse_args()

    cli = find_cli()
    failed = 0
    for src in args.inputs:
        if not src.exists():
            print(f"SKIP {src} (not found)", file=sys.stderr)
            failed += 1
            continue
        print(f"{src}:")
        try:
            build(src, args.format, cli, not args.no_theme, args.layout)
        except Exception as exc:  # noqa: BLE001 — report and continue the batch
            print(f"  FAILED: {exc}", file=sys.stderr)
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
