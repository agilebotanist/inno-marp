# ADR 0009 — Charts as Vega-Lite specs compiled to SVG

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Charts pasted as images cannot be restyled or corrected. Marp renders no charting
language.

## Decision

Charts are **Vega-Lite** JSON specs (`media/*.vl.json`), compiled with `vl2svg` to SVG
and committed together. Every spec carries a shared `config` block (Tahoma, 14/16 px
axes, no view border), and templates live in `references/charts.md`. The mark is chosen
from the slide's claim, not the data's shape.

## Consequences

- Charts restyle with the theme and correct in seconds; data is visible in the source.
- A declarative spec is easy for an agent to write and review.
- Palette values are duplicated in the specs (no CSS variables in SVG output).

## Alternatives considered

- **matplotlib / plotly scripts** — heavier, and code rather than a spec.
- **PNG export** — font-size quirks inside Marp's `<foreignObject>`, blurry scaling.
