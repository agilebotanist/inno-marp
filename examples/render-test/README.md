# Render-Test Deck

An 11-slide acceptance deck exercising every layout, tier and modifier in the theme.
Run it after **any** change to `themes/innopolis.template.css` or the scripts.

## Build

```bash
cd examples/render-test

# regenerate the diagram (needs draw.io Desktop)
python ../../scripts/build-diagram.py media/flow.mmd

# HTML + progress map + PDF + overflow check
python ../../scripts/build-deck.py slides.md --pdf

# optional: per-slide PNGs to inspect
marp slides.md --theme ../../themes/innopolis.css --allow-local-files --html --images png -o out.png
```

PNG/PDF export boots Chromium (~10–60 s). HTML alone takes a couple of seconds.

## Assertions

Check these on the rendered PDF or PNGs:

| Slide | Assertion |
|-------|-----------|
| 1 | Innopolis photo background fills the slide; title bottom-left; **no page number, no progress bar** |
| 2 | Dashed yellow **DEMO** note in the top-right margin, clear of the title (the title sits exactly where it does on slides without one); H1 green at top; bar green over a grey track; table header green with white text; blockquote with a green left rule; footer bottom-left; **page number on the same baseline as the footer** |
| 3 | `.lead` — content vertically centred, still left-aligned; bar turns **orange** (`b2`) and stays orange through slides 4–5 |
| 4 | **Thin grey vertical rule** between the columns; both `h2` render as full-width green pills; takeaway spans full width below |
| 5 | `.large` — visibly bigger body than slide 2, **title the same size** as slide 2; bar still orange |
| 6 | `.xl` — body at 32px, **title still 42px**; `<!-- class: "" -->` returns the bar to green for the rest of the deck |
| 7 | `.dense` — 5-row table and 4 card tints fit side by side without overflow |
| 8 | Two stat boxes with a green gradient; dashed green placeholder on the right |
| 9 | `.table-large` — table type larger than the prose above it |
| 10 | Diagram in the **Innopolis palette** (light-green fills, green strokes, dark-green edges) — not draw.io lavender |
| 11 | `.closing` — light green, centred; **no page number**, progress bar full width |
| all | Bar width tracks the page number: slide *n* of *N* fills *n/N* of the bottom edge |
| 6–11 | The bar **accumulates**: the orange stretch for slides 3–5 stays visible while green grows after it |
| — | `check-slide-overflow.py` reports 0 overflowing, 0 hidden |

## Known-good baseline

- Theme: ~200 KB (background embedded as base64 JPEG)
- `flow.svg`: a few KB with embedded draw.io XML (fonts not embedded)
- 11 slides, 11 PDF pages

## Regressions this deck has caught

- **Page number on `.title`/`.closing`.** `content: none` loses to Marp's own
  `section[data-marpit-pagination]::after`; `display: none !important` is required.
- **Diagram in draw.io lavender.** The Mermaid importer drops `%%{init}%%`, so
  `build-diagram.py` re-themes the `.drawio` after conversion.
- **Page number ~45 px above the footer.** Marpit's rule places it with
  `padding: inherit`; the theme sets explicit `bottom`/`right`.
- **Progress bar one flat colour.** The fill paints the section map at
  `background-size: 1280px 4px` — sized to the canvas, not the element — or narrowing
  it squeezes the map instead of clipping it.
- **Titles wrapping at `.xl`.** H1 used to scale with the tier (58 px at `.xl`); it is
  now fixed at 42 px.

## What is committed

`slides.md` and all of `media/` (`.mmd`, `.drawio`, `.svg`), so the deck renders
without draw.io. `slides.html`, `slides.pdf` and `out*.png` are ignored.
