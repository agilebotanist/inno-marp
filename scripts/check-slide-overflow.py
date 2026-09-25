#!/usr/bin/env python3
"""Report per-slide content extent in a Marp-rendered slides.pdf.

Marp slides are a fixed canvas: content that does not fit is silently clipped or
runs under the footer, so a deck can look fine while iterating and lose its last
box in the PDF. This measures how far down each slide's *content* reaches and
flags the ones that have run out of room.

Chrome renders the 1280x720 canvas at 960x540 pt. The theme puts the page number
and the footer citation on the same baseline at bottom ~528, so content must stay
above ~480 to clear them. Both furniture lines are excluded from the measurement,
as is the progress bar, which is a rect rather than text.

    python <skill-dir>/scripts/check-slide-overflow.py path/to/slides.pdf

Exit code 1 if any slide overflows or has text hidden behind a callout box.
Needs pdfplumber:  python -m pip install pdfplumber
"""

import sys
import warnings

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber is required:  python -m pip install pdfplumber")

# Slide titles legitimately contain characters cp1252 cannot encode - a MINUS
# SIGN (U+2212) in a formula title, for instance. On a Windows console that
# defaults to cp1252 this raised
# UnicodeEncodeError *mid-report*, after some rows had printed, and exited 1 -
# which is also the "a slide overflowed" code. A crash was therefore
# indistinguishable from a real failure, and a partial report looked like a
# whole one. Force UTF-8 rather than relying on PYTHONIOENCODING being set.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):      # already wrapped, or not a TTY
        pass

CONTENT_LIMIT = 0.889   # 480/540 — bottom of the usable content area
TIGHT = 0.86            # start warning here
# An unpaginated page with no image and at most this many text lines is a title or
# closing layout, which is allowed to place content anywhere. More lines than this, or
# any image, and it is a real slide that must fit — see the guard in main().
TITLE_MAX_LINES = 6


def furniture(text: str, bottom: float, h: float) -> bool:
    """True for the page-number and footer-citation lines the theme adds."""
    if bottom > 0.90 * h and text.strip().isdigit():
        return True                       # pagination
    return 0.94 * h < bottom < 0.99 * h   # footer citation band



def hidden_behind_box(page):
    """Text lines painted before an opaque callout box that covers them.

    A content-extent measurement cannot see this failure. Marp's .takeaway and
    .box callouts are opaque filled shapes in the normal flow: when the content
    above one is too tall, the columns grow *behind* it. The text is still in
    the PDF -- extract_text() returns it, and the slide measures well clear of
    CONTENT_LIMIT -- but a reader sees a coloured box with nothing under it.
    Two real clips shipped past the extent check this way, both around 87%.

    Chrome emits marked-content ids in paint order, so a character drawn before
    the box (lower mcid) and inside its bounds is invisible on the rendered
    page. The box's own text has a higher mcid and is correctly ignored.
    """
    boxes = [c for c in page.curves
             if c.get("fill") and c["mcid"] is not None
             and c["width"] > 0.3 * page.width and c["height"] > 8]
    hidden = {}
    for box in boxes:
        for c in page.chars:
            if c["mcid"] is None or c["mcid"] >= box["mcid"] or not c["text"].strip():
                continue
            if (c["x1"] > box["x0"] + 1 and c["x0"] < box["x1"] - 1
                    and c["bottom"] > box["top"] + 1 and c["top"] < box["bottom"] - 1):
                hidden.setdefault(round(c["top"]), []).append(c)
    return ["".join(c["text"] for c in sorted(cs, key=lambda c: c["x0"]))
            for _, cs in sorted(hidden.items())]


def _is_background(img, page) -> bool:
    """Whether an image is a full-bleed background rather than slide content.

    The title layout's Innopolis backdrop covers the whole canvas by design, so counting
    its bottom edge would report every title slide as 100% full.
    """
    return (
        img["width"] >= 0.95 * page.width
        and img["height"] >= 0.95 * page.height
    )


def main(path: str) -> int:
    warnings.filterwarnings("ignore")
    rows, buried = [], []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            h = page.height
            covered = hidden_behind_box(page)
            if covered:
                buried.append((i, covered))
            lines = {}
            for c in page.chars:
                lines.setdefault(round(c["top"]), []).append(c)

            bottom, paginated = 0.0, False
            for chars in lines.values():
                b = max(c["bottom"] for c in chars)
                text = "".join(c["text"] for c in sorted(chars, key=lambda c: c["x0"]))
                if furniture(text, b, h):
                    paginated |= text.strip().isdigit()
                else:
                    bottom = max(bottom, b)
            content_images = [img for img in page.images if not _is_background(img, page)]
            for img in content_images:
                bottom = max(bottom, img["bottom"])

            # Title and closing layouts place their content deliberately low and have no
            # limit to breach. They are recognised by their *content*, not by the absence
            # of a page number: `_class: lead` divider slides also render unpaginated in
            # this theme, and skipping those hid two genuine overflows — a divider with
            # an illustration is exactly the kind of slide that runs off the canvas.
            if not paginated and len(lines) <= TITLE_MAX_LINES and not content_images:
                continue

            # First line is the title — unless the slide carries a .demo note,
            # which sits above the title in the top margin.
            text_lines = [l for l in (page.extract_text() or "").split("\n")
                          if l.strip() and not l.startswith("DEMO ·")]
            title = (text_lines or [""])[0][:46]
            rows.append((bottom / h, i, title))

    rows.sort(reverse=True)
    bad = 0
    for frac, i, title in rows:
        if frac >= CONTENT_LIMIT:
            bad += 1
            print(f"  p{i:>3}  {frac:6.1%}  OVERFLOW  {title}")
        elif frac >= TIGHT:
            print(f"  p{i:>3}  {frac:6.1%}  tight     {title}")
    for i, covered in buried:
        print(f"  p{i:>3}  HIDDEN    text painted behind a callout box:")
        for line in covered:
            print(f"           | {line[:70]}")

    print(f"\n{len(rows)} slides, {bad} overflowing (limit {CONTENT_LIMIT:.0%}, "
          f"max {rows[0][0]:.1%} on p{rows[0][1]}), "
          f"{len(buried)} with text hidden behind a box")
    return 1 if bad or buried else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "slides.pdf"))
