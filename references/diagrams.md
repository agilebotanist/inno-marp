# Diagrams — draw.io first, Mermaid as the input language

Marp does **not** render Mermaid in its output, so every diagram is a pre-rendered
**SVG** committed next to the deck. Two routes get you there.

| Route | Chain | Gives you |
|-------|-------|-----------|
| **draw.io** *(default)* | `.mmd` → `.drawio` → `.svg` | An **editable** `.drawio` you can hand-adjust, plus an SVG with the XML embedded |
| **mmdc** *(fallback)* | `.mmd` → `.svg` | An SVG only; every edit means editing the Mermaid |

Prefer draw.io. Diagrams get revised every time a deck is reused, and a `.drawio` can
be nudged by hand in the editor, while Mermaid can only be re-laid-out by its parser.
draw.io's importer does the initial layout, so you write the same terse Mermaid either
way. Rationale: [ADR 0006](../docs/design/adr/0006-diagrams-drawio-first.md).

---

## The draw.io route

Needs **draw.io Desktop** ([installation](../docs/user/installation.md#drawio-desktop)).
On Windows via scoop, **the binary is `draw.io`, with a dot**. If the script cannot find
it, set `DRAWIO_CLI` to the executable's full path.

### One command

```bash
python <skill-dir>/scripts/build-diagram.py media/review-flow.mmd
```

```
media/review-flow.mmd:
  review-flow.mmd -> review-flow.drawio
  themed review-flow.drawio (48 style edits)
  review-flow.drawio -> review-flow.svg (12.4 KB)
```

Embed the SVG:

```markdown
![Review flow: open, review, revise, merge](media/review-flow.svg)
```

Options: `--format png|pdf`, `--layout verticalFlow`, `--no-theme`. Batch:
`build-diagram.py media/*.mmd`.

### Write Mermaid in the most boring form available

```
flowchart LR
    A[Open PR] --> B[Review]
    B --> C[Revise]
    C --> B
    B --> D[Merge]
```

- **No `%%{init}%%` block.** draw.io's importer drops it — and worse, an init block can
  **hang the importer**: several `draw.io` processes held for over ten minutes with no
  output and no error, while the same diagram stripped to plain edges built in under 20 s.
- **No inline HTML** (`<b>`, `<br>`), **no entities** (`&amp;`), **no chained arrows**
  (`A --> B --> C`). One edge per line.
- Theming is the script's job, applied after import.
- **If `build-diagram.py` produces no output within about a minute, kill the `draw.io`
  processes and simplify the source** rather than waiting.

### What the theming pass does

draw.io's Mermaid importer honours per-node `style X fill:,stroke:,color:` lines but
**drops `%%{init}%%` themeVariables and `linkStyle`**. Unstyled output comes out in
draw.io's lavender, gray and Trebuchet MS. The script rewrites those defaults:

| draw.io default | Rewritten to |
|-----------------|--------------|
| `fillColor=light-dark(#ECECFF,#1f2020)` | `#f0f8f0` card green |
| `strokeColor=light-dark(#9370DB,#cccccc)` | `#019546` green |
| `fontColor=light-dark(#333333,#cccccc)` | `#282828` body text |
| `strokeColor=light-dark(#333333,#cccccc)` *(edges)* | `#2D6E2A` dark green |
| `fontFamily=Trebuchet MS,Verdana,Arial,sans-serif` | `Tahoma,Verdana,DejaVu Sans,sans-serif` |

`--no-theme` keeps draw.io's colours — for a deliberately off-palette diagram, such as
a third-party framework rebuilt in its own brand colours.

To emphasise a node, use a per-node `style` line — the one styling lever that survives
the import:

```
    style D fill:#019546,stroke:#2D6E2A,color:#FFFFFF
```

### Once a `.drawio` is hand-edited, it is the source

The `.mmd` records how a diagram *started*, not what it is. Re-running
`build-diagram.py` on it regenerates the `.drawio` and **silently destroys the hand
work** — layout, per-node styling, wording. Re-export from the `.drawio` instead, with
the same flags the script uses so the SVG still reopens in the editor:

```bash
draw.io -x -f svg -e -b 10 --embed-svg-fonts false -o media/x.svg media/x.drawio
```

or simply `python <skill-dir>/scripts/build-diagram.py media/x.drawio` (it skips
conversion for a `.drawio` input).

Record which diagrams are hand-owned in `media/SOURCES.md`
([media conventions](media-conventions.md#hand-owned-diagrams)) so the next person does
not helpfully rebuild them.

### Doing it by hand

```bash
draw.io -x -f xml -o media/flow.drawio media/flow.mmd                                   # convert
draw.io -x -f svg -e -b 10 --embed-svg-fonts false -o media/flow.svg media/flow.drawio  # export
```

- `-e` embeds the diagram XML inside the SVG, so **the export reopens in draw.io as an
  editable diagram**.
- `-b 10` adds a 10 px border so strokes are not clipped.
- `--embed-svg-fonts false` — the default (`true`) base64-inlines the whole font and,
  for HTML labels, rasterises them into embedded PNGs: a 7 KB diagram became 200 KB,
  with text no longer selectable. Off, the SVG keeps real `<text>` and the font falls
  back to the stack in the style ([ADR 0008](../docs/design/adr/0008-svg-without-embedded-fonts.md)).

> **Never export a `.mmd` straight to an image.** Direct Mermaid → SVG/PNG with `-e`
> crashes current draw.io Desktop on the embedded-XML step. Convert to `.drawio` first.

### Hand-authoring XML instead

For precise positioning or a specific shape library (UML detail, network, cloud icons),
write mxGraphModel XML straight to a `.drawio` and skip Mermaid. draw.io can still lay
it out:

```bash
python <skill-dir>/scripts/build-diagram.py media/d.drawio --layout verticalFlow
```

Layouts: `verticalFlow`, `horizontalFlow`, `organic`, `tree`, `circle` — the same engine
as *Arrange ▸ Layout* in the editor.

The official **`drawio` skill** from jgraph covers XML authoring, the full layout list
and shape libraries in depth — load it when a diagram needs more than a Mermaid import.
Installation: [docs/user/installation.md](../docs/user/installation.md#the-drawio-skill).

### Rebuilding a figure from a source

When a slide draws on a published figure, **rebuild that figure in draw.io — do not
screenshot it, and do not "improve" it.** Keep its structure, labels and shape, so a
reader who opens the source recognises the picture. See
[media conventions § Figures from a source](media-conventions.md#6-figures-from-a-source).

---

## The mmdc route

When draw.io is not available, or for a throwaway diagram nobody will edit by hand:

```bash
mmdc -i media/flow.mmd -o media/flow.svg -b transparent
```

Always pass `-b transparent`. On this route `%%{init}%%` **does** work, so theme it in
the source:

```
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#f0f8f0','primaryBorderColor':'#019546','primaryTextColor':'#282828',
  'lineColor':'#2D6E2A','fontFamily':'Tahoma, Verdana, sans-serif'}}}%%
flowchart LR
    A[Open PR] --> B[Review]
    B --> D[Merge]
```

Keep such a file mmdc-only — this init block is exactly what can hang the draw.io
importer. If a diagram may later move to draw.io, strip the block first.

| Styling mechanism | mmdc | draw.io import |
|-------------------|:----:|:--------------:|
| `%%{init}%%` themeVariables | ✅ | ❌ dropped, can hang |
| `linkStyle N stroke:…` | ✅ | ❌ dropped |
| `style X fill:,stroke:,color:` | ✅ | ✅ |

---

## Palette

| Use | Hex | Token |
|-----|-----|-------|
| Primary fill | `#019546` | `--inno-green` |
| Dark fill / lines | `#2D6E2A` | `--inno-green-dark` |
| Light fill | `#81c784` | `--inno-green-light` |
| Cluster / card background | `#f0f8f0` | `--inno-card-green` |
| Warning fill | `#fff8e1` | `--inno-card-yellow` |
| Warning border | `#ffc107` | `--inno-yellow` |
| Alert | `#d32f2f` | `--inno-red` |
| Text on light | `#282828` | `--inno-text` |
| Text on dark | `#FFFFFF` | — |

The palette is duplicated in `scripts/build-diagram.py` — keep the two in sync with the
template.

---

## Sizing

The theme caps every image (560 px on a default slide, 520 px in `.columns`, 460/440 px
on `.dense`) with `object-fit: contain`, so you usually do not size diagrams at all.

Reach for `![h:N](...)` only on **tall + narrow** diagrams that should use more height
than the cap allows:

```markdown
![Hierarchy h:520](media/hierarchy.svg)     ← tall diagram, h:N helps
![Pipeline](media/pipeline.svg)             ← wide diagram, let CSS handle it
```

Do **not** put `h:N` on a **wide + short** diagram: width clips to 100% first, the
image scales down to keep its ratio, and the explicit height leaves letterbox space
above and below. Rule of thumb: if `natural_height / natural_width × 1190 > N`, drop the
`h:N`.

**The cap only shrinks — it never enlarges.** A small draw.io export (a 4-box flow is
~450 px wide) renders at its natural size and looks lost on the slide. For a **wide**
diagram that is too small, use `w:N` (e.g. `![Flow w:900](media/flow.svg)`); width is
the safe axis for wide images.

**Recompute any `w:`/`h:` after re-cropping or re-exporting** — a changed aspect ratio
silently invalidates it.

If a diagram looks cramped after auto-scaling, **redraw it more compactly** (2 rows × 4
boxes instead of 1 × 8) rather than pushing the cap.
