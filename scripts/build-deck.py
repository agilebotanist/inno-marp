#!/usr/bin/env python3
"""Build a deck end to end, in the order the pipeline needs.

    python <skill-dir>/scripts/build-deck.py path/to/slides.md            # HTML only
    python <skill-dir>/scripts/build-deck.py path/to/slides.md --pdf      # + PDF + overflow check
    python <skill-dir>/scripts/build-deck.py path/to/slides.md --pdf --pptx

Steps:
  1. marp -> slides.html                  (fast, ~2 s)
  2. build-progress-map.py                (only if the deck uses b1-b8 section classes)
  3. marp -> slides.html again            (so the map takes effect)
  4. marp -> slides.pdf                   (--pdf; boots Chromium, ~10-20 s)
  5. check-slide-overflow.py slides.pdf   (--pdf; needs pdfplumber, skipped if absent)
  6. marp -> slides.pptx                  (--pptx; slide images + speaker notes)
  7. LibreOffice: slides.pdf -> slides.editable.pptx
                                          (--pptx-editable; real text boxes, NO notes,
                                           tables need fixing by hand — see
                                           docs/user/pptx-export.md)

Builds run one at a time on purpose: two concurrent PDF builds each boot a
Chromium and can deadlock.

Diagrams and charts are NOT rebuilt here — they are sources with their own
lifecycle (a hand-edited .drawio must never be regenerated from its .mmd).
See references/media-conventions.md.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME = ROOT / "themes" / "innopolis.css"
SCRIPTS = ROOT / "scripts"
SECTION_CLASS = re.compile(r"<!--\s*_?class:[^>]*\bb[1-8]d?\b")


def marp(slides: Path, out: Path) -> None:
    exe = shutil.which("marp")
    if not exe:
        sys.exit("marp not found — npm install -g @marp-team/marp-cli")
    cmd = [exe, str(slides), "--theme", str(THEME),
           "--allow-local-files", "--html", "-o", str(out)]
    print(f"marp -> {out.name}", flush=True)
    if subprocess.run(cmd).returncode != 0 or not out.exists():
        sys.exit(f"marp failed building {out.name}")


SOFFICE_CANDIDATES = [
    "soffice",
    str(Path.home() / "scoop" / "apps" / "libreoffice" / "current" / "LibreOffice" / "program" / "soffice.exe"),
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "libreoffice",
]


def find_soffice() -> str:
    env = os.environ.get("SOFFICE")
    if env and Path(env).exists():
        return env
    for cand in SOFFICE_CANDIDATES:
        if Path(cand).is_absolute():
            if Path(cand).exists():
                return cand
        elif shutil.which(cand):
            return shutil.which(cand)
    sys.exit("LibreOffice not found — install it, or point SOFFICE at soffice(.exe)")


def editable_pptx(pdf: Path) -> Path:
    """PDF -> PPTX through LibreOffice's PDF importer: every text run becomes a
    real, editable text box and SVG charts/diagrams become shapes.

    This is the same route marp's own `--pptx-editable` takes, but starting from
    the PDF we already built: ~10 s instead of ~2 min for a 12-slide deck.
    Written to slides.editable.pptx so it never clobbers the image PPTX."""
    out = pdf.with_suffix(".editable.pptx")
    print(f"soffice -> {out.name}", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [find_soffice(), "--headless", "--infilter=impress_pdf_import",
               "--convert-to", "pptx:Impress MS PowerPoint 2007 XML",
               "--outdir", tmp, str(pdf)]
        subprocess.run(cmd, capture_output=True)
        produced = Path(tmp) / pdf.with_suffix(".pptx").name
        if not produced.exists():
            sys.exit("LibreOffice produced no PPTX — is another soffice instance "
                     "open? Close LibreOffice and retry.")
        shutil.move(str(produced), out)
    return out


def py(script: str, *args: str) -> int:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args]).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slides", type=Path)
    ap.add_argument("--pdf", action="store_true", help="also build the PDF and check overflow")
    ap.add_argument("--pptx", action="store_true",
                    help="also build a PPTX of slide images, with speaker notes")
    ap.add_argument("--pptx-editable", action="store_true",
                    help="also build an editable PPTX via LibreOffice (implies --pdf)")
    ap.add_argument("--no-map", action="store_true", help="skip the progress-bar section map")
    args = ap.parse_args()

    slides = args.slides.resolve()
    if not slides.exists():
        sys.exit(f"Not found: {slides}")
    if not THEME.exists():
        sys.exit(f"Missing {THEME} — run: python {SCRIPTS / 'build-theme.py'}")

    html = slides.with_suffix(".html")
    marp(slides, html)

    if not args.no_map and SECTION_CLASS.search(slides.read_text(encoding="utf-8")):
        if py("build-progress-map.py", str(slides)) != 0:
            return 1
        marp(slides, html)

    status = 0
    if args.pdf or args.pptx_editable:
        pdf = slides.with_suffix(".pdf")
        marp(slides, pdf)
        try:
            import pdfplumber  # noqa: F401
        except ImportError:
            print("overflow check skipped — python -m pip install pdfplumber")
        else:
            status = py("check-slide-overflow.py", str(pdf))

    if args.pptx:
        marp(slides, slides.with_suffix(".pptx"))

    if args.pptx_editable:
        editable_pptx(slides.with_suffix(".pdf"))

    return status


if __name__ == "__main__":
    sys.exit(main())
