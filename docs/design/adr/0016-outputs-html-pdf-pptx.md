# ADR 0016 — Ship HTML and PDF; PPTX in two flavours

- **Status:** Accepted
- **Scope:** inno-marp

## Context

HTML is fast to iterate but needs the `media/` folder beside it. Recipients without the
repository need a single file. Some need PowerPoint — either to present, or to edit
words. Marp's `--pptx` produces slide images with speaker notes; its
`--pptx-editable` is experimental, goes through LibreOffice, and took ~140 s for a
12-slide deck.

## Decision

- Every deck is built to **HTML and PDF**; the PDF is the deliverable. A failed PDF
  build is reported, never silently skipped.
- **Image PPTX** (`--pptx`): Marp's native export, faithful, keeps speaker notes.
- **Editable PPTX** (`--pptx-editable` in `build-deck.py`): the already-built PDF is
  imported by LibreOffice (`--infilter=impress_pdf_import`) and saved as PPTX, written
  to `slides.editable.pptx`. Same approach as Marp's flag, same result in testing, ~10 s.
- PDF builds run **serially** — two concurrent Chromium instances can deadlock.

## Consequences

- Recipients choose between fidelity + notes and editability, with the trade-off
  documented in `docs/user/pptx-export.md`.
- Editable PPTX loses notes and table structure (cells become fixed-width text boxes)
  and is a one-way hand-over, not a round trip.
- LibreOffice becomes an optional dependency.

## Alternatives considered

- **Marp's `--pptx-editable` only** — slower, experimental; kept as a documented
  alternative.
- **Generating native PPTX with python-pptx / pptxgenjs** — a second renderer to
  maintain, and it would drift from the theme.
