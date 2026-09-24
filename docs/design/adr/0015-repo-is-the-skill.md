# ADR 0015 — The repository is the skill directory

- **Status:** Accepted
- **Scope:** inno-marp

## Context

The skill started life vendored inside one project, so it could not be shared without
copying — and copies drift. Claude Code discovers a skill as a directory containing
`SKILL.md` under `.claude/skills/` (project) or `~/.claude/skills/` (user).

## Decision

`SKILL.md` sits at the **repository root**. Installing is cloning (or linking) the repo
as `.claude/skills/inno-marp`. All paths inside the skill are relative to the skill
directory (`<skill-dir>` in docs), never to a particular project.

## Consequences

- One source, updated with `git pull`; projects can share one clone via a junction or
  symlink.
- Human docs (`docs/`) ship inside the skill directory. They cost nothing unless an
  agent opens them.
- **Anything placed in the skill directory is part of the skill** — no backups or
  scratch folders there.
- The per-project install is what makes VS Code preview work (themes must be inside the
  workspace).

## Alternatives considered

- **Skill in a sub-folder of the repo** — extra path segment on every link, and
  the repo could not be cloned directly into place.
- **Claude Code plugin/marketplace** — possible later; a plain clone is simpler for now.
