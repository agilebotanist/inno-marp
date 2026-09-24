# ADR 0002 — One registered theme file, not per-deck CSS

- **Status:** Accepted
- **Scope:** inno-marp

## Context

Early decks pasted the full theme into each deck's frontmatter `style:` block. Every
fix then had to be copied into every deck, and decks diverged within weeks.

## Decision

The theme is a single CSS file declaring `/* @theme innopolis */`. Decks reference it
with `theme: innopolis` and the build passes `--theme <skill-dir>/themes/innopolis.css`;
VS Code registers it in `markdown.marp.themes`. A deck's `style:` block is reserved for
**per-deck overrides** only.

## Consequences

- A theme fix reaches every deck on its next build.
- `theme: innopolis` resolves **only** when the CSS is registered; a missing `--theme`
  silently falls back to Marp's default theme. Documented in every build section.
- VS Code loads themes only from inside the workspace, which drives the per-project
  install recommendation ([installation](../../user/installation.md#option-a--per-project-recommended)).

## Alternatives considered

- **Per-deck CSS** — the status quo; rejected for drift.
- **Publishing the theme at a URL** — works in VS Code, but adds a network dependency
  and a hosting decision; can still be added later.
