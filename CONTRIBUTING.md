# Contributing

## Changing the theme

1. Edit `themes/innopolis.template.css` — **never** `themes/innopolis.css`.
2. `python scripts/build-theme.py`
3. Rebuild the acceptance deck and check its assertion table:
   ```bash
   cd examples/render-test
   python ../../scripts/build-deck.py slides.md --pdf
   ```
4. Update `references/css-reference.md` (and `SKILL.md` if the change affects everyday
   authoring).
5. If you changed a `--inno-b*` colour: say so in the changelog — every built deck needs
   its progress map re-run.
6. If you changed a palette colour: update `scripts/build-diagram.py` and
   `references/charts.md` too.

## Changing a script

- Stdlib-only for the core scripts; optional dependencies are imported lazily with a
  clear install message.
- Keep them cross-platform: `pathlib`, no shell-specific syntax, tool discovery with an
  environment-variable override.
- Run `python scripts/doctor.py` and both example decks afterwards.

## Changing a convention

Conventions (`references/slide-writing.md`, `references/media-conventions.md`) come from
decks that went wrong. When you add or change one, give the reason next to it — the
failure it prevents. If it reverses an earlier decision, add an ADR from
`docs/design/adr/template.md` and mark the old one superseded.

## What must never be committed

- Personal data, email addresses, internal URLs.
- Course- or project-specific content. Examples stay on neutral topics.
- Build outputs (`slides.html`, `slides.pdf`, `*.pptx`, PNG renders) — see `.gitignore`.
- Anything that is not part of the skill: this directory is loaded as a skill, so a
  backup folder here becomes a duplicate skill.

## Changelog

Add a line to `CHANGELOG.md` under *Unreleased* for anything a deck author would notice.
