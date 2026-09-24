# Media conventions — the `media/` folder

Every deck keeps its pictures in one `media/` folder next to `slides.md`. These rules
exist so that a deck can be handed to a colleague, reopened a year later, and edited —
not just re-rendered. Rationale: [ADR 0014](../docs/design/adr/0014-media-conventions.md).

## 1. Layout

```
my-talk/
├── slides.md
└── media/
    ├── SOURCES.md              # provenance — required once media/ holds anything you did not make
    ├── review-flow.mmd         # diagram: what you wrote
    ├── review-flow.drawio      # diagram: editable source of truth
    ├── review-flow.svg         # diagram: what the deck renders (XML embedded)
    ├── pr-size.vl.json         # chart: source
    ├── pr-size.svg             # chart: rendered
    ├── fig-delivery-model.drawio # a figure rebuilt from a source
    ├── fig-delivery-model.svg
    ├── shot-ci-dashboard.png   # screenshot
    └── photo-team-board.jpg    # photograph
```

- **Flat.** No sub-folders inside `media/`; the prefix does the grouping.
- **One deck, one `media/`.** A file used by several decks lives in one shared folder
  and is referenced relatively (`../shared-media/x.svg`) — not copied. If a copy is
  unavoidable (a deck must travel alone), keep the **same file name**, so identical
  content stays findable.
- **Never** put the title background in `media/` — it is embedded in the theme.

## 2. Naming

```
[prefix-]<what-it-shows>.<ext>        lowercase, kebab-case, ASCII
```

| Rule | Good | Bad |
|------|------|-----|
| Name the **content**, not the slide position | `review-flow.svg` | `slide12.svg`, `diagram3.svg` |
| Lowercase kebab-case, ASCII only | `pr-size.vl.json` | `PR Size.json`, `größe.svg` |
| **Source and render share the basename** | `x.mmd` → `x.drawio` → `x.svg` | `x.mmd` → `x-final-v2.svg` |
| Basenames **unique across the folder** | `pr-size.vl.json` + `pr-flow.mmd` | `pr.vl.json` + `pr.mmd` (both → `pr.svg`) |
| No versions or dates in names | `review-flow.drawio` | `review-flow-v3-2024.drawio` — git keeps history |

| Prefix | For |
|--------|-----|
| *(none)* | Your own diagrams and charts — the common case |
| `fig-` | A figure **rebuilt from a published source** (paper, book, standard) |
| `shot-` | A screenshot of a tool, UI or web page |
| `photo-` | A photograph |
| `ill-` | An illustration or strip on a divider |
| `logo-` | A third-party logo |

## 3. Formats

| Kind | Source (commit) | Rendered (commit) | Notes |
|------|-----------------|-------------------|-------|
| Diagram | `.mmd` **and** `.drawio` | `.svg` with XML embedded | [diagrams.md](diagrams.md) |
| Diagram, hand-authored | `.drawio` | `.svg` | No `.mmd` |
| Diagram, mmdc-only | `.mmd` | `.svg` | Throwaway only |
| Chart | `.vl.json` | `.svg` | [charts.md](charts.md) |
| Screenshot | — | `.png` | Crop to the relevant part; ≤ 1920 px wide |
| Photograph | — | `.jpg` | ≤ 1920 px wide, quality ~85 |
| Illustration / strip | — | `.png` / `.gif` / `.jpg` as delivered | Never re-encode someone else's work |

**Vectors are SVG, rasters are PNG (flat colour) or JPG (photo).** Never a screenshot of
a diagram you could draw, and never a PNG export of a chart you have the spec for.

**Commit the rendered files too.** A colleague without draw.io or Node must still be
able to build the deck. `slides.html`, `slides.pdf` and `slides.pptx` are build outputs:
ignore them (or commit the PDF only, if the repo is where people fetch it).

## 4. Source of truth

| Situation | Source of truth | Regenerate with |
|-----------|-----------------|-----------------|
| Diagram never touched in the editor | `.mmd` | `build-diagram.py x.mmd` |
| Diagram edited in draw.io | **`.drawio`** — the `.mmd` is now history | `build-diagram.py x.drawio` |
| Chart | `.vl.json` | `vl2svg x.vl.json x.svg` |
| Anything else | the file itself | — |

### Hand-owned diagrams

Once a `.drawio` has been edited by hand, re-running its `.mmd` destroys the edits
silently. Mark it in `SOURCES.md` (below) with **`hand-owned`**. Keep the `.mmd` as
provenance. `build-deck.py` never rebuilds diagrams for exactly this reason.

## 5. `SOURCES.md` — provenance

Every file in `media/` that you **did not create from scratch** gets one row, and every
hand-owned diagram gets one too. Create the file the first time you need a row.

```markdown
# Media sources

| File | What | Origin | Licence / permission | Caption on slide |
|------|------|--------|----------------------|------------------|
| fig-delivery-model.svg | Rebuilt Fig. 2 | Author et al. 2021, *Title*, Fig. 2 | Redrawn; cited | "After Author et al. 2021, Fig. 2" |
| shot-ci-dashboard.png | CI dashboard | Own screenshot, 2024-03 | Own; internal data redacted | — |
| photo-team-board.jpg | Task board | Unsplash, photographer name, URL | Unsplash licence | "Photo: name / Unsplash" |
| ill-deadline.png | Divider strip | Generated with <tool>, prompt below | Tool terms | "Generated with <tool>" |
| review-flow.drawio | — | Own | — | **hand-owned** — do not rebuild from .mmd |
```

- **Origin** is specific enough to find the item again: author, year, title, figure
  number or URL, retrieval date.
- A **generated image** records the tool and the prompt (below the table), so it can be
  regenerated or replaced.
- Record what you **rejected** too, when the search was expensive, so it is not repeated.

## 6. Figures from a source

When a published figure exists for the idea on the slide, **rebuild that figure, not a
better one.** A reader who later opens the source should recognise the picture; an
improved, on-brand redraw breaks that link, and the link is worth more than the
improvement.

| | |
|---|---|
| **Rebuild in draw.io**, don't screenshot | Editable, readable across a room, and it does not carry the publisher's image |
| **Keep the structure, wording and labels** — including figure-internal numbering | Those labels are pointers *into the source*; they look like noise and are the connection |
| **Keep the shape even when another shape would argue better** | A flat continuum the authors call non-linear must not become a staircase — the redraw would assert something the source denies |
| **What may be added** | Your own gloss *underneath* — clearly yours, the source's content untouched |
| **What must be recorded** | Which figure (`Fig. 4`) of which source, in `SOURCES.md` and in the footer or caption |

Check the source figure **before** drawing, not after. Use the `fig-` prefix and
`--no-theme` if the figure's own colours carry meaning.

## 7. Embedding

```markdown
![Review flow: open, review, revise, merge](media/review-flow.svg)
```

- **Alt text describes what the picture shows** — it is what a reader of the markdown
  sees, and it survives into accessibility tooling. Not "diagram", not the file name.
- Let the theme size images. Use `w:`/`h:` only for the cases in
  [diagrams.md § Sizing](diagrams.md#sizing), and **recompute them after any re-crop**.
- Credit on the slide — footer or `.comic-caption` — whenever `SOURCES.md` has a caption.
- Paths are **relative to `slides.md`** and use forward slashes, so the deck builds on
  every OS.

## 8. Checklist before sharing a deck

- [ ] Every `![…](media/…)` resolves; no file in `media/` is unreferenced (or it is
      listed in `SOURCES.md` as kept on purpose)
- [ ] Every diagram has its `.drawio` next to its `.svg`
- [ ] Every chart has its `.vl.json` next to its `.svg`
- [ ] Every non-original file has a `SOURCES.md` row and an on-slide credit where needed
- [ ] Hand-owned diagrams are marked
- [ ] No personal data, internal URLs or credentials visible in screenshots
