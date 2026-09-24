# ADR 0004 — Declare design tokens on `section`, not `:root`

- **Status:** Accepted
- **Scope:** inno-marp

## Context

The theme exposes its palette as custom properties so decks can retune it. Declared on
`:root`, a deck's `section { --inno-rule: … }` override silently lost. Marp rewrites a
theme's `:root` to `:where(section):not([\20 root])`; the `:not([…])` contributes an
attribute selector's specificity, which outranks a plain `section` rule however late it
comes.

## Decision

Declare every `--inno-*` token on `section`. Theme and deck then have equal
specificity and the deck's `style:` block wins by source order.

## Consequences

- Per-deck overrides work as authors expect.
- Tokens are scoped to slides, which is the only place they are used.
- The reason is non-obvious; it is recorded in the template comment and in
  `references/css-reference.md` so nobody "fixes" it back to `:root`.

## Alternatives considered

- **`!important` in decks** — works, but makes overrides of overrides impossible.
