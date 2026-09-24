# ADR 0013 — Check overflow on the PDF, including text hidden behind callouts

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Slides are a fixed canvas. Content that does not fit fails in two ways: it runs under
the footer, or it grows **behind** an opaque `.takeaway` / `.box`, which is in the normal
flow. Both look acceptable while scrolling the HTML, and the second is invisible to any
extent measurement — the text is still in the PDF and the slide measures short because
the box is what reaches the bottom. Two such clips shipped at ~87% against an 89% limit.

## Decision

`scripts/check-slide-overflow.py` analyses the **PDF** with pdfplumber:
- **Extent**: the lowest content line or image (excluding footer, page number, bar and
  full-bleed backgrounds) must stay above 89% of the page height; 86% warns.
- **Hidden text**: Chrome emits marked-content ids in paint order, so any character with
  a lower id than a filled box and inside its bounds is reported as hidden.
- Title/closing layouts are recognised by content (few lines, no image), not by the
  absence of a page number, because `.lead` dividers are unpaginated too.
It runs automatically in `build-deck.py --pdf`.

## Consequences

- The two common layout failures are caught before a deck is shared.
- It is a heuristic: authors still look at every changed slide. Documented as "a net,
  not a proof".
- Needs `pdfplumber`; the build skips the check with a message if it is absent.
- Forces UTF-8 output — a Unicode minus in a title once crashed it mid-report with the
  same exit code as a real failure.

## Alternatives considered

- **Checking the HTML DOM** — layout differs subtly from the PDF, which is the
  deliverable.
- **Visual diffing** — needs baselines per deck.
