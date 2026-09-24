# ADR 0007 — Re-theme draw.io output after import; write plain Mermaid

- **Status:** Accepted
- **Scope:** inno-marp

## Context

draw.io's Mermaid importer honours per-node `style X fill:…` but **drops `%%{init}%%`
themeVariables and `linkStyle`**, producing draw.io's lavender/grey/Trebuchet defaults.
Worse, sources carrying an init block (with inline HTML and entities) **deadlocked** the
importer: several `draw.io` processes held for over ten minutes with no output. The same
diagrams stripped to one plain edge per line built in under 20 seconds.

## Decision

1. After conversion, `build-diagram.py` rewrites the importer's known default style
   strings in the `.drawio` to the Innopolis palette (fills, strokes, edges, font).
2. Mermaid for this pipeline is written in the **most boring form**: no init block, no
   inline HTML, no entities, no chained edges. Per-node `style` lines are the only
   in-source styling.

## Consequences

- Diagrams come out on-brand with no per-diagram effort.
- The regexes are coupled to draw.io's current default strings. If draw.io changes
  them, the edit count drops to 0 and diagrams come out lavender — render-test slide 10
  catches it.
- `--no-theme` exists for deliberately off-palette diagrams.

## Alternatives considered

- **Rely on `%%{init}%%`** — ignored, and dangerous.
- **Post-process the SVG instead of the `.drawio`** — would leave the editable source
  unthemed, so the next re-export would lose the theme.
