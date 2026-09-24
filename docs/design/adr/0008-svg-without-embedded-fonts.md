# ADR 0008 — Export SVG without embedded fonts

- **Status:** Accepted
- **Scope:** inno-marp

## Context

draw.io's `--embed-svg-fonts` defaults to true. It base64-inlines the whole font and,
for HTML labels, rasterises them into embedded PNGs. A 7 KB diagram became 200 KB and a
22 KB one 404 KB, with text no longer selectable or crisp.

## Decision

Export with `--embed-svg-fonts false`. The SVG keeps real `<text>`, and the font falls
back to the stack in the style (`Tahoma, Verdana, DejaVu Sans, sans-serif`).

## Consequences

- ~95% smaller SVGs, selectable text, crisp at any zoom, and editable labels in the
  LibreOffice PPTX route.
- Rendering depends on the viewer having Tahoma or a fallback — the same assumption the
  theme already makes.

## Alternatives considered

- **Default (embedded)** — rejected for size and rasterised text.
