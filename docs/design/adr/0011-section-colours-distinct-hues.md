# ADR 0011 — Section colours: distinct hues in spectrum order

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Two attempts to separate parts within a section by shade failed at 4 px: an area colour
beside the magenta spare (`#dc2626` next to `#db2777`, near-identical lightness) blurred
into one red line, and 600-on-900 shades read as one muddy streak. Brand green as a
section colour made untagged and tagged slides indistinguishable.

## Decision

- `.b1`–`.b7` are seven **distinct hues** (red, orange, gold, teal, blue, violet,
  magenta), walked **in spectrum order** as sections go by. `.b8` (slate) marks the
  bookends — agenda, wrap-up, logistics.
- Brand green is **not** in the sequence; it means "untagged".
- **Tag every section.** A deck with a few tagged sections is green most of the time and
  the bar stops informing.
- `.b1d`–`.b6d` (light shades) remain for compatibility and are not recommended.

## Consequences

- Adjacent sections are always distinguishable, on a projector or in a small window.
- Colours carry no fixed meaning across decks; a series may layer its own mapping on
  top and document it.
- More than seven content sections exhausts the palette — which is also more sections
  than a 90-minute talk should have.

## Alternatives considered

- **Shades of the brand colour** — failed twice, see context.
- **Fixed topic → colour mapping in the theme** — too specific to one series of decks.
