# ADR 0012 — Layout classes instead of Marp `![bg]` backgrounds

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Marp's advanced background syntax (`![bg](…)`) emits an extra pseudo-`<section>` that
pagination counts: "3 of 5" on a 4-slide deck, a blank step in presenter mode, and a PDF
with one page too many.

## Decision

Backgrounds are set by the theme on the `<section>` itself through layout classes
(`.title`, `.lead`, `.closing`). `![bg]` is not used.

## Consequences

- Pagination, the progress bar and PDF page counts stay correct.
- A PDF page count ≠ slide count is a reliable tell that `![bg]` crept in.
- Per-slide background images need a per-deck CSS class instead of a directive.

## Alternatives considered

- **`![bg]` with pagination adjustments** — fragile, fights Marp.
