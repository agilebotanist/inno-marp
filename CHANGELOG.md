# Changelog

## 1.0.0 — 2026-09-24

First standalone release, extracted from a project-embedded skill.

### Added
- `scripts/build-deck.py` — one command for HTML → progress map → PDF → overflow check
  → PPTX.
- **Editable PPTX** (`--pptx-editable`): PDF → LibreOffice → `slides.editable.pptx`, with
  real text boxes. ~10 s instead of ~140 s for Marp's experimental flag.
- `scripts/doctor.py` — reports installed tools and a stale theme.
- `scripts/check-slide-overflow.py` — shipped with the skill (was project-local).
- `references/media-conventions.md`, `references/slide-writing.md`.
- User documentation (`docs/user/`) and design documentation with 16 ADRs
  (`docs/design/`).
- `build-diagram.py` finds draw.io on macOS and Linux too; `DRAWIO_CLI` override.

### Changed
- Section colours are documented as an ordered palette (spectrum order, `b8` for
  bookends), no longer tied to fixed topics.
- Mermaid guidance: no `%%{init}%%` on the draw.io route — it is dropped and can hang
  the importer.
- VS Code setting is `markdown.marp.html: "all"` (replaces deprecated `enableHtml`).
- Examples rewritten on neutral topics.

### Fixed
- Documentation claimed the H1 scales with the density tier (36/58 px); it is 42 px in
  every tier, as the CSS has it.
- Documented that the image cap never enlarges: small wide diagrams need `w:N`.
