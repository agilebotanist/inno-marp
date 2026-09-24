# ADR 0003 — Embed the title background in the generated theme

- **Status:** Accepted
- **Scope:** inno-marp

## Context

The `.title` layout uses a photograph. With `url('../assets/bg.jpg')`, Marp resolves the
path relative to the **HTML output**, not the CSS file, so the background broke for
every deck outside the skill folder. The workaround — copying the image into each deck's
`media/` — was forgotten regularly.

## Decision

Keep a **template** (`themes/innopolis.template.css`) with a `{{BG_TITLE}}` placeholder.
`scripts/build-theme.py` replaces it with a base64 data URI of `assets/innopolis-bg.jpg`
(1280×720, quality 88, ~142 KB) and writes `themes/innopolis.css`. The full-resolution
PNG stays in `assets/` as the source; `--regen-jpeg` re-derives the JPEG.

## Consequences

- The generated CSS is the only file a deck needs; no per-deck image copies.
- The CSS grows to ~200 KB. Acceptable: it is loaded once per build.
- The generated file must **never be hand-edited**; its header and `doctor.py` (STALE
  check) say so.
- Both files are committed, so a `git pull` is enough to update — no build on install.

## Alternatives considered

- **Absolute paths / file URLs** — machine-specific.
- **Hosting the image** — network dependency at build time.
