#!/usr/bin/env python3
"""Regenerate the figures in docs/images/ from the example decks.

    python scripts/build-doc-images.py

Maintainer tool. Run it after changing the theme or an example deck, so the
pictures in README.md and docs/ show what the code actually renders. Every
figure is derived from committed sources — the only hand-made inputs in
docs/images/ are the diagram sources (.mmd, and skill-features.drawio, which is
hand-authored draw.io XML: edit it in draw.io).

Needs: marp, Pillow, draw.io (diagrams), and for the PPTX comparison
LibreOffice + pdfplumber. Missing optional tools skip their figures.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required:  python -m pip install Pillow")

ROOT = Path(__file__).resolve().parent.parent
THEME = ROOT / "themes" / "innopolis.css"
OUT = ROOT / "docs" / "images"
EX = ROOT / "examples"
SCRIPTS = ROOT / "scripts"

BG = (244, 244, 244)       # --inno-gray: sheet background
INK = (40, 40, 40)         # --inno-text
GREEN = (1, 149, 70)       # --inno-green
RED = (211, 47, 47)        # --inno-red
GAP = 16


def font(size: int) -> ImageFont.ImageFont:
    for name in ("tahoma.ttf", "Tahoma.ttf", "Verdana.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def render(deck: Path, tmp: Path, tag: str, theme: bool = True) -> list[Path]:
    """Every slide of a deck as a 1280x720 PNG, in order."""
    exe = shutil.which("marp") or sys.exit("marp not found")
    cmd = [exe, str(deck), "--allow-local-files", "--html",
           "--images", "png", "-o", str(tmp / f"{tag}.png")]
    if theme:
        cmd[2:2] = ["--theme", str(THEME)]
    subprocess.run(cmd, capture_output=True, check=True)
    return sorted(tmp.glob(f"{tag}.*.png"))


def label(img: Image.Image, text: str, colour=INK) -> Image.Image:
    """A caption bar above an image."""
    f = font(26)
    bar = 48
    out = Image.new("RGB", (img.width, img.height + bar), BG)
    out.paste(img, (0, bar))
    ImageDraw.Draw(out).text((4, 10), text, fill=colour, font=f)
    return out


def frame(img: Image.Image) -> Image.Image:
    """A 1 px grey border, so white slides do not melt into a white page."""
    out = Image.new("RGB", (img.width + 2, img.height + 2), (200, 200, 200))
    out.paste(img, (1, 1))
    return out


def grid(images: list[Image.Image], cols: int, width: int) -> Image.Image:
    """Tile images into a sheet `width` px wide, keeping each one's ratio."""
    cell_w = (width - GAP * (cols + 1)) // cols
    cells = [im.resize((cell_w, round(im.height * cell_w / im.width)), Image.LANCZOS)
             for im in images]
    rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
    heights = [max(c.height for c in r) for r in rows]
    sheet = Image.new("RGB", (width, sum(heights) + GAP * (len(rows) + 1)), BG)
    y = GAP
    for r, h in zip(rows, heights):
        for i, c in enumerate(r):
            sheet.paste(c, (GAP + i * (cell_w + GAP), y))
        y += h + GAP
    return sheet


def save(img: Image.Image, name: str) -> None:
    path = OUT / name
    img.save(path, optimize=True)
    print(f"  {name:<34} {img.width}x{img.height}  {path.stat().st_size / 1024:.0f} KB")


def slides(paths: list[Path], numbers: list[int]) -> list[Image.Image]:
    return [Image.open(paths[n - 1]).convert("RGB") for n in numbers]


def progress_strips(paths: list[Path], numbers: list[int]) -> Image.Image:
    """The bottom edge of several slides, stacked and enlarged, so the bar's
    accumulation is visible at documentation size."""
    f = font(24)
    strip_h, zoom, lab = 30, 2, 190
    rows = []
    for n in numbers:
        crop = Image.open(paths[n - 1]).convert("RGB").crop((0, 720 - strip_h, 1280, 720))
        crop = crop.resize((1280, strip_h * zoom), Image.NEAREST)
        row = Image.new("RGB", (lab + 1280, strip_h * zoom), BG)
        row.paste(crop, (lab, 0))
        ImageDraw.Draw(row).text((12, 16), f"slide {n} / {len(paths)}", fill=INK, font=f)
        rows.append(row)
    sheet = Image.new("RGB", (lab + 1280, sum(r.height for r in rows) + GAP * (len(rows) + 1)), BG)
    y = GAP
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height + GAP
    return sheet


def editable_pptx_pages(pdf: Path, tmp: Path) -> list[Image.Image] | None:
    """Round-trip the PDF through LibreOffice to PPTX and back to PDF, then
    rasterise it — this is what a recipient of the editable PPTX sees."""
    try:
        import pdfplumber
    except ImportError:
        print("  (pdfplumber missing — skipping the PPTX comparison)")
        return None
    sys.path.insert(0, str(SCRIPTS))
    import importlib.util
    spec = importlib.util.spec_from_file_location("bdk", SCRIPTS / "build-deck.py")
    bdk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bdk)
    try:
        soffice = bdk.find_soffice()
    except SystemExit:
        print("  (LibreOffice missing — skipping the PPTX comparison)")
        return None
    work = tmp / "lo"
    work.mkdir()
    shutil.copy(pdf, work / "deck.pdf")
    subprocess.run([soffice, "--headless", "--infilter=impress_pdf_import",
                    "--convert-to", "pptx:Impress MS PowerPoint 2007 XML",
                    "--outdir", str(work / "pptx"), str(work / "deck.pdf")], capture_output=True)
    subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                    "--outdir", str(work / "back"), str(work / "pptx" / "deck.pptx")], capture_output=True)
    back = work / "back" / "deck.pdf"
    if not back.exists():
        print("  (LibreOffice round trip failed — skipping the PPTX comparison)")
        return None
    with pdfplumber.open(back) as doc:
        return [p.to_image(width=1280).original.convert("RGB") for p in doc.pages]


# The same slide in each tier, so the figure compares sizes and nothing else.
TIER_SLIDE = """<!-- _class: {cls} -->

# Review Time Grows Faster Than the Diff

- Small PRs are reviewed in one sitting
- Large PRs are reviewed in fragments

| Diff size | Median hours to merge |
|-----------|----------------------:|
| < 50 lines | 3 |
| 200–500 lines | 22 |

<div class="takeaway">Split by <strong>reviewable intent</strong>, not by file count.</div>
"""

FRONT = "---\nmarp: true\ntheme: innopolis\npaginate: true\n---\n\n"


def section_deck(wipe_one: bool) -> str:
    """Eleven slides in three tagged sections. With wipe_one, slide 7 carries a
    bare `_class: large` — the classic mistake that drops the section colour."""
    s = ["<!-- _class: title -->\n\n# Deck", "<!-- class: b8 -->\n\n# Agenda"]
    for b, name in ((1, "One"), (2, "Two"), (3, "Three")):
        s.append(f"<!-- _class: lead b{b} -->\n<!-- class: b{b} -->\n\n# Section {name}")
        s += [f"# Content {b}.1", f"# Content {b}.2"]
    s = s[:-1]  # section three has one content slide
    s[6] = ("<!-- _class: large -->\n\n# Content 2.1" if wipe_one
            else "<!-- _class: large b2 -->\n\n# Content 2.1")
    s.append("<!-- _class: closing -->\n\n# Questions?")
    return FRONT + "\n\n---\n\n".join(s) + "\n"


def mapped_deck(md_text: str, tmp: Path, tag: str) -> list[Path]:
    """Write a deck, give it its progress map, render it."""
    md = tmp / f"{tag}.md"
    md.write_text(md_text, encoding="utf-8")
    subprocess.run([shutil.which("marp"), str(md), "--theme", str(THEME), "--html",
                    "-o", str(md.with_suffix(".html"))], capture_output=True, check=True)
    subprocess.run([sys.executable, str(SCRIPTS / "build-progress-map.py"), str(md)],
                   capture_output=True, check=True)
    return render(md, tmp, tag)


def diagrams() -> None:
    """Mermaid sources go through the full pipeline; a .drawio with no .mmd beside
    it is hand-authored — export it as it is, colours untouched."""
    for src in sorted(OUT.glob("*.mmd")) + sorted(
            d for d in OUT.glob("*.drawio") if not d.with_suffix(".mmd").exists()):
        cmd = [sys.executable, str(SCRIPTS / "build-diagram.py"), str(src),
               "--format", "png", "--scale", "2"]
        if src.suffix == ".drawio":
            cmd.append("--no-theme")
        subprocess.run(cmd, capture_output=True)
        png = src.with_suffix(".png")
        print(f"  {png.name:<34} {'ok' if png.exists() else 'FAILED (draw.io?)'}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        print("rendering example decks…")
        starter = render(EX / "starter" / "slides.md", tmp, "starter")
        test = render(EX / "render-test" / "slides.md", tmp, "test")
        pits = render(EX / "pitfalls" / "slides.md", tmp, "pit")
        bare = render(EX / "starter" / "slides.md", tmp, "bare", theme=False)

        print("writing docs/images/:")
        # README — the one hero figure
        # Nine slides in deck order, cover to closing, so the progress bar is seen
        # filling up across the gallery.
        save(grid([frame(s) for s in slides(starter, [1, 2, 4, 5, 6, 7, 8, 10, 12])], 3, 1600),
             "gallery-starter.png")

        # css-reference / workflow — layouts and tiers
        lay = slides(test, [1, 2, 3, 4, 11])
        names = ["title", "default", "lead", "columns", "closing"]
        save(grid([label(frame(s), f".{n}" if n != "default" else "(default)")
                   for s, n in zip(lay, names)], 3, 1600), "layouts.png")
        tier_md = tmp / "tiers.md"
        tier_md.write_text(FRONT + "\n---\n\n".join(
            TIER_SLIDE.format(cls=c) for c in ("dense", "", "large", "xl")), encoding="utf-8")
        tiers = render(tier_md, tmp, "tiers")
        save(grid([label(frame(Image.open(p).convert("RGB")), n) for p, n in
                   zip(tiers, [".dense — body 20 px", "(default) — body 22 px",
                               ".large — body 26 px", ".xl — body 32 px"])],
                  2, 1400), "density-tiers.png")

        # density-and-progress-bar guide — the bar accumulating, and the classic mistake
        save(progress_strips(starter, [2, 4, 7, 10, 12]), "progress-bar.png")
        good = mapped_deck(section_deck(False), tmp, "secok")
        bad = mapped_deck(section_deck(True), tmp, "secbad")
        a = progress_strips(good, [len(good)])
        b = progress_strips(bad, [len(bad)])
        save(grid([label(a, "every slide tagged"),
                   label(b, "slide 7 has a bare _class: large — green gap mid-section", RED)],
                  1, 1470), "progress-bar-untagged-slide.png")

        # troubleshooting — pitfalls
        save(frame(Image.open(pits[0]).convert("RGB")), "pitfall-markdown-in-div.png")
        save(grid([label(frame(s), t) for s, t in
                   zip(slides(pits, [2, 3]), ["no size: natural width", "w:900"])], 2, 1400),
             "pitfall-diagram-size.png")
        save(label(frame(Image.open(pits[3]).convert("RGB")),
                   "HIDDEN: the last bullets are painted over by the box", RED),
             "pitfall-hidden-text.png")
        save(label(frame(Image.open(pits[4]).convert("RGB")),
                   "OVERFLOW: the list runs under the footer and off the canvas", RED),
             "pitfall-overflow.png")

        # vscode-preview — what a missing theme looks like
        save(grid([label(frame(s), t) for s, t in
                   zip([Image.open(starter[4]).convert("RGB"), Image.open(bare[4]).convert("RGB")],
                       ["theme registered", "theme NOT registered — Marp default"])], 2, 1400),
             "theme-registered-vs-missing.png")

        # pptx-export — image vs editable
        pdf = EX / "starter" / "slides.pdf"
        if pdf.exists():
            edit = editable_pptx_pages(pdf, tmp)
            if edit:
                pairs = []
                for n in (5, 8):
                    pairs += [label(frame(Image.open(starter[n - 1]).convert("RGB")),
                                    f"slide {n}: image PPTX / PDF"),
                              label(frame(edit[n - 1]), f"slide {n}: editable PPTX")]
                save(grid(pairs, 2, 1400), "pptx-image-vs-editable.png")
        else:
            print("  (no examples/starter/slides.pdf — build it first for the PPTX comparison)")

    print("diagrams:")
    diagrams()
    return 0


if __name__ == "__main__":
    sys.exit(main())
