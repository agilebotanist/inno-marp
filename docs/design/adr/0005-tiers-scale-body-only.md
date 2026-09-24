# ADR 0005 — Density tiers scale body text only; the H1 is fixed at 42 px

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Four density tiers (`dense`, default, `large`, `xl`) let a slide trade content for type
size. Originally the tier also scaled the H1 (36 / 42 / 46 / 58 px). With `xl` as the
deck default for laptop audiences, titles wrapped onto two lines on almost every slide.
Titles are the slide's key message; a wrapped claim reads as two fragments.

## Decision

Tiers change **body** sizes (text, H2, H3, tables, list spacing) and never the layout
or the H1. The H1 is 42 px in every tier. A title that wraps is **shortened**, not
resized, and the slide is not dropped a tier to fix a heading.

## Consequences

- Titles align across the whole deck; the eye finds them in the same place.
- Authors must write shorter titles — which is the point.
- `.lead` (52 px) and `.closing` (56 px) keep their own larger H1; they are layouts, not
  tiers.

## Alternatives considered

- **Scale H1 with the tier** — the original behaviour; rejected for wrapping.
- **Auto-fit title text** — needs JavaScript and hides the problem instead of fixing
  the title.
