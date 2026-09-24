# VS Code — live preview in the Innopolis theme

Write the deck in VS Code and watch it render beside the editor, in the real theme.

## Extensions

| Extension | ID | For |
|-----------|----|-----|
| **Marp for VS Code** | `marp-team.marp-vscode` | Live slide preview, export — **required** |
| Draw.io Integration | `hediet.vscode-drawio` | Edit `.drawio` / `.drawio.svg` inside VS Code |
| Markdown Preview Mermaid Support | `bierner.markdown-mermaid` | Preview a `.mmd` snippet while writing it |

Vega-Lite specs are easiest to iterate in the [online Vega editor](https://vega.github.io/editor/);
paste the spec back into `media/*.vl.json` when it looks right.

Commit a recommendation file so colleagues get the prompt to install them —
`.vscode/extensions.json`:

```json
{
  "recommendations": [
    "marp-team.marp-vscode",
    "hediet.vscode-drawio",
    "bierner.markdown-mermaid"
  ]
}
```

## Register the theme

Marp for VS Code loads custom themes **only from inside the workspace** (or from a
URL) — not from an absolute path. With the skill installed per project
([installation § Option A](installation.md#option-a--per-project-recommended)), add
`.vscode/settings.json` and commit it:

```jsonc
{
  "markdown.marp.themes": [
    "./.claude/skills/inno-marp/themes/innopolis.css"
  ],
  // Raw <div> blocks (.columns, .takeaway, .box …) need all HTML allowed.
  "markdown.marp.html": "all"
}
```

- `markdown.marp.html: "all"` replaces the deprecated `markdown.marp.enableHtml`. It
  allows every HTML element — only do this in workspaces whose markdown you trust.
- If the skill is installed globally instead, copy `themes/innopolis.css` into the
  workspace (e.g. `./.marp/innopolis.css`) and point the setting there. Re-copy after
  updating the skill.
- A theme path that does not resolve fails **silently**: the preview falls back to the
  default Marp theme. If the preview shows no green headings and no progress bar, the
  path is wrong.

## Use it

1. Open `slides.md`.
2. **Open Preview to the Side** (`Ctrl+K V` / `Cmd+K V`), or the preview icon in the
   editor's top-right corner.
3. The Marp icon in the editor toolbar opens **Export Slide Deck…** (HTML, PDF, PPTX,
   PNG).

Use the preview for writing; use `scripts/build-deck.py` for the files you share. The
extension does not run the progress-map generator or the overflow check, and its export
uses its own settings rather than the command line's flags.

## What the preview will not show

- **The accumulating progress bar** until `build-progress-map.py` has written the map
  into the frontmatter — before that the bar shows one colour per slide.
- **Diagram changes** until the `.svg` is re-exported — the preview renders the SVG, not
  the `.mmd` or `.drawio`.
- **Overflow behind callouts.** The preview is a scrolling HTML view; text hidden behind
  a `.takeaway` looks the same there as in the PDF, so check the PDF.

## Editing diagrams in VS Code

With Draw.io Integration installed, opening a `.drawio` file shows the draw.io editor in
a tab. Save, then re-export the SVG so the deck picks it up:

```bash
python .claude/skills/inno-marp/scripts/build-diagram.py media/x.drawio
```

Once you have edited a `.drawio` by hand it is the source — never re-run its `.mmd`.
See [media conventions](../../references/media-conventions.md#4-source-of-truth).
