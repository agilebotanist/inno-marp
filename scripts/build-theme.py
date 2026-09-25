#!/usr/bin/env python3
"""
Generate themes/innopolis.css from themes/innopolis.template.css by replacing
{{BG_*}} placeholders with base64-encoded data URIs of the background images.

Why: when Marp inlines a theme via --theme, url('../assets/...') in the CSS
resolves relative to the HTML output, not the CSS source — so relative paths
break for any deck outside the skill folder. Embedding makes the theme fully
self-contained: no deck ever needs a copy of the background in its media/.
See docs/design/adr/0003-embed-title-background.md.

The embedded asset is innopolis-bg.jpg (1280x720, ~142 KB → ~194 KB base64),
downscaled from the 2111x1187 PNG original. The original is kept in assets/
as the source of truth; regenerate the JPEG with --regen-jpeg if it changes.

Usage:
    python scripts/build-theme.py
    python scripts/build-theme.py --regen-jpeg   # re-derive the JPEG from the PNG first
"""

import argparse
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "themes" / "innopolis.template.css"
OUTPUT = ROOT / "themes" / "innopolis.css"
ASSETS = ROOT / "assets"

BG_MAPPING = {
    "{{BG_TITLE}}": "innopolis-bg.jpg",
}

# Source PNG -> embedded JPEG, for --regen-jpeg
JPEG_SOURCE = ASSETS / "innopolis-bg.png"
JPEG_TARGET = ASSETS / "innopolis-bg.jpg"
JPEG_SIZE = (1280, 720)
JPEG_QUALITY = 88

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def data_uri(path: Path) -> str:
    mime = MIME.get(path.suffix.lower())
    if mime is None:
        raise ValueError(f"Unsupported image type: {path.suffix}")
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"url('data:{mime};base64,{b64}')"


def regen_jpeg() -> None:
    """Re-derive the embedded JPEG from the full-resolution PNG."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow is required for --regen-jpeg:  python -m pip install Pillow")
    if not JPEG_SOURCE.exists():
        sys.exit(f"Missing source image: {JPEG_SOURCE}")
    im = Image.open(JPEG_SOURCE).convert("RGB").resize(JPEG_SIZE, Image.LANCZOS)
    im.save(JPEG_TARGET, quality=JPEG_QUALITY, optimize=True, progressive=True)
    kb = JPEG_TARGET.stat().st_size / 1024
    print(f"Regenerated {JPEG_TARGET.name} ({kb:.1f} KB) from {JPEG_SOURCE.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--regen-jpeg",
        action="store_true",
        help="re-derive innopolis-bg.jpg from the PNG original before building",
    )
    args = parser.parse_args()

    if args.regen_jpeg:
        regen_jpeg()

    if not TEMPLATE.exists():
        sys.exit(f"Missing template: {TEMPLATE}")

    css = TEMPLATE.read_text(encoding="utf-8")

    for placeholder, fname in BG_MAPPING.items():
        img = ASSETS / fname
        if not img.exists():
            sys.exit(f"Missing asset: {img}\nRun with --regen-jpeg to derive it from the PNG.")
        if placeholder not in css:
            sys.exit(f"Placeholder {placeholder} not found in {TEMPLATE.name}")
        css = css.replace(placeholder, data_uri(img))

    leftover = [p for p in BG_MAPPING if p in css]
    if leftover:
        sys.exit(f"Unreplaced placeholders: {leftover}")

    # LF on every OS, matching .gitattributes — or a rebuild on Windows shows
    # the whole 200 KB file as modified.
    OUTPUT.write_text(css, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(css):,} chars, {len(css)/1024:.1f} KB)")


if __name__ == "__main__":
    main()
