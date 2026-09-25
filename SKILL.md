---
name: inno-marp
description: |
  Create professional Marp presentations with Innopolis University styling
  (green #019546, Tahoma, 5 layouts, 4 density tiers, section-coloured progress
  bar, draw.io diagram pipeline, Vega-Lite charts). Use this skill whenever the
  user mentions "marp", "inno-marp", "slides", "deck", "presentation" or
  "lecture", or asks to turn content into slides — even if they don't say
  "marp". Also use for speaker notes, draw.io or Mermaid diagrams, and
  Vega-Lite charts in a deck.
---

# Inno-Marp — Innopolis University slide decks

Markdown → HTML / PDF / PPTX via [`@marp-team/marp-cli`](https://github.com/marp-team/marp-cli),
styled in Innopolis University green.

In every command below, **`<skill-dir>` is this skill's own directory** — the folder
holding this `SKILL.md`. Resolve it once and substitute it; never assume a fixed path.

## Quick start

```markdown
---
marp: true
theme: innopolis
paginate: true
---

<!-- _class: title -->

# Small Pull Requests Merge Faster
## Engineering practices · Session 3

Speaker name · Innopolis University

---

# Review Time Grows Faster Than the Diff

<div class="columns">
<div>

## Small PR

- Reviewed in one sitting
- Comments are specific

</div>
<div>

## Large PR

- Reviewed in fragments
- Comments turn into "LGTM"

</div>
</div>

<div class="takeaway">Split by <strong>reviewable intent</strong>, not by file count.</div>

---

<!-- _class: closing -->

# Questions?
```

Full worked deck: [examples/starter/slides.md](examples/starter/slides.md).

## Build

```bash
python <skill-dir>/scripts/build-deck.py slides.md          # HTML, fast
python <skill-dir>/scripts/build-deck.py slides.md --pdf    # + PDF + overflow check
```

`build-deck.py` runs the steps in the order they must happen: HTML → progress map
(if the deck tags sections) → HTML again → PDF → overflow check. By hand:

```bash
marp slides.md --theme <skill-dir>/themes/innopolis.css --allow-local-files --html -o slides.html
```

- `--allow-local-files` is required for local images; `--html` for raw `<div>` blocks.
- **Ship HTML and PDF.** HTML is for iterating; the PDF is what reaches people without
  the repo. If the PDF fails (usually no Chromium/Chrome/Edge), say so — do not quietly
  ship HTML alone. Check the PDF page count equals the slide count.
- **Never run two PDF builds at once** — each boots Chromium and they can deadlock.
- Call `marp`, not `npx @marp-team/marp-cli`: `npx` re-resolves the package on every
  call and can hang for minutes.
- `-o slides.pptx` gives a PowerPoint of slide *images* — fine for handing over, not
  for editing.

Then **check overflow on the PDF** (`build-deck.py --pdf` does it):
`python <skill-dir>/scripts/check-slide-overflow.py slides.pdf`. It catches content
running under the footer *and* text painted over by an opaque `.takeaway`/`.box`. It
is a net, not proof — render the slides you changed and look at them.

## Markdown in slides

Marp accepts CommonMark / GFM. Slides are separated by `---` on its own line.
Headings, lists, tables, blockquotes, code, links and images pick up the theme.

| You want… | Use… |
|-----------|------|
| A layout or size class on one slide | `<!-- _class: title -->` / `lead` / `dense` / `large` / `xl` / `closing` |
| The same class on every following slide | `<!-- class: xl -->` (no underscore — it carries) |
| Per-slide source citation | `<!-- footer: Author Year, Short Title -->` — reset with `<!-- footer: "" -->` |
| Speaker notes | Any HTML comment that is not a directive: `<!-- Say this… -->` |
| Two columns with a centre rule | `<div class="columns"><div>…</div><div>…</div></div>` |
| Three / four columns | `.columns-3`, `.columns-4` (no rule) |
| Key-insight box | `<div class="takeaway">…</div>` |
| A single big number | `<div class="stat-box"><span class="number">2×</span><span class="label">…</span></div>` |
| Content cards | `<div class="box">`, `.box.y` caution, `.box.r` alert, `.box.n` aside |
| Inline label | `<span class="chip">NEW</span>` |
| A diagram / chart not drawn yet | `<div class="placeholder">Diagram: …</div>` |
| A diagram | draw.io pipeline → [references/diagrams.md](references/diagrams.md) |
| A chart | Vega-Lite → [references/charts.md](references/charts.md) |
| Any file in `media/` | [references/media-conventions.md](references/media-conventions.md) |

## The 5 layouts

| Class | Purpose |
|-------|---------|
| `.title` | Cover, Innopolis photo background, no page number, no progress bar |
| *(default)* | Content slide, white, H1 pinned top |
| `.columns` | Two columns with a centre rule; an `h2` inside becomes a green pill |
| `.lead` | Section divider, vertically centred, left-aligned |
| `.closing` | Questions / contact, light green, centred, full progress bar |

## Density tiers — body size only

| Tier | Body | H2 | Table | Use |
|------|-----:|---:|------:|-----|
| `.dense` | 20 | 24 | 17 | Reference tables, deep bullets |
| *(default)* | 22 | 28 | 19 | Most slides |
| `.large` | 26 | 30 | 22 | One idea, summaries |
| `.xl` | 32 | 36 | 28 | Hero stat, punchline — and the **deck default for online delivery** |

**The slide title (H1) is 42 px in every tier.** A title is the slide's key message and
must not wrap. If it wraps, shorten the title; do not override its size and do not drop
the slide a tier to fix a heading. `.table-large` / `.table-xlarge` enlarge a table
without enlarging the prose.

For decks watched in a window on a laptop, set `class: xl` in the frontmatter and
downgrade the few slides that cannot take it — `large` for two tables side by side or a
full-width diagram, `dense` for a genuine reference table. Getting a slide to fit at `xl`
is usually a content problem: cut words first.

## Progress bar — a colour per section

With `paginate: true` every slide gets a 4 px bar along its bottom edge, as wide as the
slide's share of the deck. `.b1`–`.b8` recolour it. **Tag every section**, walking the
palette in spectrum order — `b1` red → `b2` orange → `b3` gold → `b4` teal → `b5` blue →
`b6` violet → `b7` magenta — and keep `b8` slate for the bookends (agenda, wrap-up).
Untagged slides are brand green.

```markdown
<!-- _class: lead b3 -->      ← this divider slide
<!-- class: xl b3 -->         ← every slide after it

# Section Three
```

- `class` **replaces** the whole list — repeat the tier (`xl b3`).
- A per-slide `<!-- _class: large -->` inside a section wipes the colour — write
  `<!-- _class: large b3 -->`.
- Two shades of one hue do not separate at 4 px. Use a different `bN`, never `bNd`.

To make the bar **accumulate** (finished sections keep their colour), run
`build-progress-map.py` after an HTML build — `build-deck.py` does it automatically. It
bakes literal hex into the deck's frontmatter, so re-run it after adding, removing or
retagging slides, and after any change to the theme's `--inno-b*` colours.

## Writing the slides

Full rules: [references/slide-writing.md](references/slide-writing.md). The core:

1. **Title = the key message**, not a topic label, and graspable cold with no other
   slide in view. "Wideband Delphi Converges in 2–3 Rounds", not "Estimation Methods".
2. **Dividers are the exception** — a `.lead` `h1` names the section plainly; the `h2`
   says what it teaches.
3. **One idea per slide. Bullets, not prose.** A bullet running past one line is a
   sentence in disguise. Full sentences are for quotes and the one-line `.takeaway`.
4. **No markdown inside HTML blocks** — Marp does not parse it. Use `<strong>`, `<em>`, `<br>`.
5. **No `![bg]` directives** — they add a pseudo-slide that breaks pagination. Use the
   class layouts.
6. **Reset footers** with `<!-- footer: "" -->` or the citation bleeds on.
7. **Two parallel lists the reader must match up is a table.**
8. **A chart must show the comparison its title claims.**

**Review the deck with the `minto-pyramid` skill** when it is drafted: extract the titles
(`grep '^# ' slides.md`) and ask for a *so-what pass* and a *buried-lede test* on that
list, then a *reason audit* per section. See
[docs/user/workflow.md](docs/user/workflow.md#6-review-with-the-minto-pyramid-skill).

## Diagrams — draw.io first

Marp does not render Mermaid, so diagrams are pre-rendered SVGs. Write terse Mermaid,
convert through draw.io so an **editable `.drawio`** exists:

```bash
python <skill-dir>/scripts/build-diagram.py media/flow.mmd
```

Writes `flow.drawio` (editable source, re-themed to the Innopolis palette) and
`flow.svg` (XML embedded, reopens in draw.io). Embed with `![Flow](media/flow.svg)`.

- Write Mermaid in the **most boring form**: no `%%{init}%%`, no inline HTML, no
  entities, one edge per line. draw.io's importer drops `init`/`linkStyle` anyway, and
  an init block can hang it. If nothing happens within a minute, kill `draw.io` and
  simplify the source.
- **Once a `.drawio` is hand-edited, it is the source** — never re-run the `.mmd`.
  Re-export: `draw.io -x -f svg -e -b 10 --embed-svg-fonts false -o media/x.svg media/x.drawio`.
- The `drawio` skill (official, from jgraph) covers XML authoring and shape libraries —
  load it when a diagram needs more than a Mermaid import.

Details: [references/diagrams.md](references/diagrams.md).

## Charts — Vega-Lite

```bash
vl2svg media/chart.vl.json media/chart.svg
```

Every chart carries the shared `config` block (Tahoma, 14/16 px axes, no view border).
Templates: [references/charts.md](references/charts.md).

## Per-deck folder

```
my-talk/
├── slides.md          # the deck
├── slides.html        # generated
├── slides.pdf         # generated — the deliverable
└── media/             # see references/media-conventions.md
    ├── SOURCES.md     # provenance of every file you did not make
    ├── review-flow.mmd
    ├── review-flow.drawio
    ├── review-flow.svg
    ├── pr-size.vl.json
    └── pr-size.svg
```

The title background is embedded in the theme — never copy it into `media/`.

## Duration planning

| Length | Slides | Structure |
|--------|-------:|-----------|
| 45 min | 15 | 5 parts × 3 slides |
| 60 min | 20 | 5 parts × 4 slides |
| 90 min | 30–35 | 8 parts × 4 slides |

Each part = one `.lead` divider + 3–5 content slides; ~2.5–3 min per slide.

## Changing the theme

`themes/innopolis.css` is **generated** — edit `themes/innopolis.template.css`, then:

```bash
python <skill-dir>/scripts/build-theme.py
```

Then rebuild `examples/render-test/` and check its assertions. Rationale for every
design choice: [docs/design/](docs/design/architecture.md).

## Reference files

| Need to… | Open |
|----------|------|
| Full class catalogue, tokens, per-deck overrides | [references/css-reference.md](references/css-reference.md) |
| Build a diagram | [references/diagrams.md](references/diagrams.md) |
| Build a chart | [references/charts.md](references/charts.md) |
| Name, store and credit media files | [references/media-conventions.md](references/media-conventions.md) |
| Illustrations on dividers | [references/illustrations.md](references/illustrations.md) |
| Slide-writing rules | [references/slide-writing.md](references/slide-writing.md) |
| Explain tiers and the progress bar to a person, with pictures | [docs/user/layouts-tiers-progress.md](docs/user/layouts-tiers-progress.md) |
| A complete deck | [examples/starter/](examples/starter/slides.md) |
| Verify the theme after a change | [examples/render-test/](examples/render-test/README.md) |

## Critical rules recap

- **Pass `--theme`** (or register it in VS Code). `theme: innopolis` resolves only then.
- **`--allow-local-files`** for images; **`--html`** for `<div>` blocks.
- **No markdown inside `<div>`**; **no `![bg]`**; **reset footers**.
- **H1 stays 42 px** — shorten a wrapping title.
- **Tag every section** with `b1`…`b8`, spectrum order.
- **Never edit `themes/innopolis.css`** — edit the template, rebuild.
- **Commit the `.drawio` next to the `.svg`**; a hand-edited `.drawio` is never regenerated.
- **Build HTML and PDF, one PDF at a time, and check overflow.**
