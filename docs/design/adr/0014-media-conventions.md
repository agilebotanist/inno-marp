# ADR 0014 — Media conventions: flat `media/`, shared basenames, sources committed, provenance file

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Decks are reopened by other people, months later. What went wrong without conventions:
diagrams existing only as SVG, charts only as PNG, file names like `slide12.svg` that
went stale when slides moved, hand-edited diagrams overwritten by a rebuild, and
third-party images whose origin nobody could reconstruct.

## Decision

See `references/media-conventions.md`. In short:
- One flat `media/` per deck; shared media referenced, not copied.
- Names describe **content**, lowercase kebab-case; **source and render share the
  basename**; prefixes `fig-`, `shot-`, `photo-`, `ill-`, `logo-` for non-original kinds.
- **Commit sources and renders** (`.mmd` + `.drawio` + `.svg`, `.vl.json` + `.svg`) so the
  deck builds without draw.io or Node. Build outputs of the deck itself are ignored.
- **`media/SOURCES.md`** records origin, licence and caption for everything not made
  from scratch, and marks hand-owned diagrams.
- A figure taken from a source is **rebuilt faithfully**, not improved, so readers
  recognise it in the source.

## Consequences

- Any colleague can edit any picture in a deck they did not write.
- A small amount of bookkeeping per third-party file.
- Faithful rebuilds sometimes look less polished than an on-brand redraw — accepted,
  because recognisability is worth more.

## Alternatives considered

- **Sub-folders per kind** (`media/diagrams/`, `media/charts/`) — longer paths in every
  slide for no gain once prefixes exist.
- **Commit sources only** — forces every reader to install the whole toolchain.
