# ADR 0010 — Progress bar in pure CSS, section map generated from rendered HTML

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Audiences watching in a window lose track of where they are in a talk. A progress bar
helps, and it is more useful when it also shows *which section* and *how many are done*.
CSS on slide *n* knows *n* and the total, but cannot know where other sections start.

## Decision

1. `section::before` is a 4 px bar whose width is
   `100% × attr(data-marpit-pagination) / attr(data-marpit-pagination-total)` with typed
   `attr()`. The grey track is painted on the section itself, because the `::before` is
   clipped to the fill width.
2. `.b1`–`.b8` set the current colour.
3. For accumulation, `build-progress-map.py` reads the **rendered HTML** (where Marp has
   resolved carried `class` directives), collapses runs into sections, and injects a
   `--inno-progress-map` gradient between markers in the deck's frontmatter. The bar
   paints the map at `background-size: 1280px 4px`, so narrowing the element clips the
   map instead of squeezing it.

## Consequences

- No JavaScript; correct in PDF and PPTX renders.
- Where typed `attr()` is unsupported, the width is dropped and the bar disappears — it
  cannot break a layout.
- The map is **baked hex**: stale after slide changes or theme colour changes until
  re-run. `build-deck.py` re-runs it on every build.
- Reading HTML, not markdown, avoids re-implementing Marp's directive semantics.

## Alternatives considered

- **JavaScript bar** — not executed in PDF export.
- **Parsing directives from the markdown** — duplicates Marp's rules and gets carried
  `class` edge cases wrong.
