# Installation

Everything the pipeline uses, what each tool is for, and how to install it on Windows,
macOS and Linux. When you are done, run:

```bash
python scripts/doctor.py
```

| Tool | Needed for | Required? |
|------|------------|-----------|
| [Node.js](#nodejs) ≥ 18 | runs marp, mmdc, vl2svg | yes |
| [Marp CLI](#marp-cli) | building HTML / PDF / PPTX | yes |
| Chrome, Edge or Chromium | PDF, PNG and PPTX export (Marp drives it) | yes for PDF |
| [Python](#python) ≥ 3.10 | the scripts in `scripts/` | yes |
| [draw.io Desktop](#drawio-desktop) | diagrams: `.mmd` → `.drawio` → `.svg` | yes, for diagrams |
| [Vega-Lite CLI](#vega-lite) | charts: `.vl.json` → `.svg` | for charts |
| [Mermaid CLI](#mermaid-cli) | fallback diagrams without draw.io | optional |
| [LibreOffice](#libreoffice) | editable PPTX | optional |
| [pdfplumber](#python) | overflow check on the PDF | recommended |
| [VS Code + extensions](vscode-preview.md) | live preview while writing | recommended |
| [Claude Code](#the-skill-itself) + skills | writing decks with an agent | optional |

On Windows, [scoop](https://scoop.sh) is the least painful way to install all of it;
`winget` works too. Commands for both are given.

---

## Node.js

| OS | Command |
|----|---------|
| Windows | `scoop install nodejs` · or `winget install OpenJS.NodeJS.LTS` |
| macOS | `brew install node` |
| Linux | your distribution's package, or [nvm](https://github.com/nvm-sh/nvm) |

## Marp CLI

```bash
npm install -g @marp-team/marp-cli
marp --version
```

Install it **globally** and call `marp`. `npx @marp-team/marp-cli` re-resolves the
package on every call and can hang for minutes.

Marp exports PDF/PPTX/PNG through an installed Chromium-family browser (Chrome, Edge,
Chromium). If it cannot find one, set `CHROME_PATH` to the browser executable.

## Python

Python **3.10 or newer** — the scripts use modern type syntax.

```bash
python -m pip install pdfplumber      # check-slide-overflow.py
python -m pip install Pillow          # only for build-theme.py --regen-jpeg
```

## draw.io Desktop

The diagram pipeline drives draw.io's **command-line mode** (`draw.io -x …`), which
ships with the desktop app.

| OS | Command | CLI binary |
|----|---------|------------|
| Windows (scoop) | `scoop bucket add extras` then `scoop install draw.io` | `draw.io` — **with a dot** |
| Windows (winget) | `winget install JGraph.Draw` | `%LOCALAPPDATA%\Programs\draw.io\draw.io.exe` or `C:\Program Files\draw.io\draw.io.exe` |
| macOS | `brew install --cask drawio` | `/Applications/draw.io.app/Contents/MacOS/draw.io` |
| Linux | `.deb` / `.rpm` / AppImage from [github.com/jgraph/drawio-desktop/releases](https://github.com/jgraph/drawio-desktop/releases) | `drawio` |

`scripts/build-diagram.py` looks in all of these. If yours is elsewhere, set
`DRAWIO_CLI` to the full path.

On a headless Linux box draw.io needs a display: run it under `xvfb-run`.

### The drawio skill

The official draw.io skill from jgraph teaches an agent to author draw.io XML, apply
ELK layouts and use shape libraries — useful when a diagram needs more than a Mermaid
import. In Claude Code:

```
/plugin marketplace add jgraph/drawio-mcp
/plugin install drawio@drawio
```

Source: [github.com/jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp)
(`plugins/claude-code/`).

## Vega-Lite

```bash
npm install -g vega-lite vega-cli
vl2svg --help
```

`vl2svg` is shipped by `vega-lite` and uses `vega` from `vega-cli`. For interactive
editing, the [online Vega editor](https://vega.github.io/editor/) renders a spec as you
type.

## Mermaid CLI

Only needed for the fallback route (a throwaway diagram, or no draw.io):

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc --version
```

It downloads its own headless Chromium on install; behind a proxy set
`HTTPS_PROXY` first.

## LibreOffice

Only for **editable** PowerPoint output — see [pptx-export.md](pptx-export.md).

| OS | Command |
|----|---------|
| Windows | `scoop install libreoffice` · or `winget install TheDocumentFoundation.LibreOffice` |
| macOS | `brew install --cask libreoffice` |
| Linux | `sudo apt install libreoffice-impress` (or your distribution's equivalent) |

`build-deck.py` finds `soffice` on `PATH` and in the default install locations; set
`SOFFICE` to override.

## Fonts

The theme uses **Tahoma**, a system font on Windows and macOS. On Linux, install the
Microsoft core fonts or accept the metric-compatible fallback (Verdana, then DejaVu
Sans) — the layout is tuned so the fallbacks fit.

---

## The skill itself

### Option A — per project (recommended)

Put the skill **inside** the repository that holds your decks. VS Code can only load a
theme from inside the workspace, so this is the layout that makes the live preview
work ([vscode-preview.md](vscode-preview.md)).

```bash
cd my-decks-repo
git clone https://github.com/agilebotanist/inno-marp .claude/skills/inno-marp
```

Or, to share one clone between several projects, link it:

```powershell
# Windows — a junction needs no admin rights
New-Item -ItemType Junction -Path .claude\skills\inno-marp -Target C:\path\to\inno-marp
```

```bash
# macOS / Linux
ln -s /path/to/inno-marp .claude/skills/inno-marp
```

Add `.claude/skills/inno-marp/` to the project's `.gitignore` if you link or clone it
rather than vendoring it.

### Option B — for every project

```bash
git clone https://github.com/agilebotanist/inno-marp ~/.claude/skills/inno-marp
```

Claude Code picks it up in every session. For the VS Code preview you then still need
a copy of `themes/innopolis.css` inside each workspace.

### Updating

```bash
git -C <skill-dir> pull
```

`themes/innopolis.css` is committed, so a pull is enough — no rebuild.

### The minto-pyramid skill

Recommended for reviewing drafted decks ([workflow.md § 6](workflow.md#6-review-with-the-minto-pyramid-skill)):

```bash
git clone https://github.com/millwright-labs/minto-pyramid-skill ~/.claude/skills/minto-pyramid
```

```powershell
git clone https://github.com/millwright-labs/minto-pyramid-skill "$env:USERPROFILE\.claude\skills\minto-pyramid"
```

Update with `git pull` in that folder. It is markdown only — no scripts, no hooks.

---

## Check

```bash
python <skill-dir>/scripts/doctor.py
python <skill-dir>/scripts/build-deck.py <skill-dir>/examples/starter/slides.md --pdf
```

The second command should end with `0 overflowing … 0 with text hidden behind a box`
and leave `slides.html` and `slides.pdf` beside the example.
