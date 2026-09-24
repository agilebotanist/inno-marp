# ADR 0006 — Diagrams: Mermaid in, draw.io as editable source, SVG out

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Marp does not render Mermaid. Diagrams must be pre-rendered images. Pure Mermaid → SVG
(mmdc) makes every layout tweak a fight with the parser; screenshots are uneditable.
Diagrams are revised each time a deck is reused, often after hand adjustments.

## Decision

Write diagrams as **Mermaid** (`.mmd`), convert with **draw.io Desktop's CLI** to a
`.drawio` file, export an **SVG with the diagram XML embedded** (`-e`), and commit all
three. `scripts/build-diagram.py` runs the chain. Once a `.drawio` is edited by hand it
becomes the source of truth and is never regenerated from its `.mmd`; it is marked
`hand-owned` in `media/SOURCES.md`. mmdc remains a fallback for throwaway diagrams.

## Consequences

- Terse, agent-friendly authoring *and* a real editor for the last 10%.
- The exported SVG itself reopens in draw.io, so even a lost `.drawio` is recoverable.
- A dependency on draw.io Desktop (~150 MB) for anyone building diagrams. Decks still
  build without it, because the SVGs are committed.
- Risk of overwriting hand edits by re-running the `.mmd`; mitigated by the hand-owned
  marker and by `build-deck.py` never rebuilding diagrams.

## Alternatives considered

- **mmdc only** — no editing surface.
- **Hand-drawn XML only** — precise but slow; still supported for special cases.
- **Mermaid rendered at build time via a plugin** — not supported by Marp CLI output.
