# ADR 0001 — Markdown + Marp as the authoring format

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Decks were built in PowerPoint: binary files, no meaningful diffs, styling drifting per
author, and no way for a coding agent to write or review them reliably. Slides are
revised every time they are reused, often by someone other than the original author.

## Decision

Author decks as Markdown and render them with **Marp CLI** (`@marp-team/marp-cli`).
Layouts and components are CSS classes applied through Marp directives
(`<!-- _class: … -->`) and a small set of raw HTML blocks (`<div class="columns">`).

## Consequences

- Decks diff, merge and review like code; an agent can write and edit them.
- One theme gives every deck the same look without per-author effort.
- Raw HTML blocks need `--html`, and markdown inside them is **not** parsed — authors
  must use `<strong>`/`<em>` there. This is the most common authoring mistake and is
  repeated in `SKILL.md`.
- Pixel-level free placement is not available; layouts are what the theme offers.
- PowerPoint becomes an export target, not a source ([ADR 0016](0016-outputs-html-pdf-pptx.md)).

## Alternatives considered

- **PowerPoint templates** — familiar, but not diffable and not agent-friendly.
- **reveal.js / Slidev** — more interactive, but heavier toolchains and weaker PDF
  output; Marp's PDF export via Chromium is simple and faithful.
