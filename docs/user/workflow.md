# Workflow — from idea to shared deck

Seven steps. Steps 1 and 6 are where decks get good; the rest is mechanics that the
scripts handle.

![Seven steps: plan, draft slides, media, build, check, review with minto, share — with a loop from review back to drafting](../images/workflow-steps.png)

With Claude Code, you can drive every step in plain language — *"plan a 45-minute deck
on X"*, *"draw the review flow as a diagram"*, *"build the PDF and check overflow"*,
*"review the titles with the minto skill"*. The `inno-marp` skill loads itself whenever
slides are mentioned.

## 1. Plan

Before any slide, write a short plan — a `plan.md` beside the deck, or the first
message to the agent:

- **Duration → slide count.** 45 min ≈ 15 slides, 60 ≈ 20, 90 ≈ 30–35.
- **Parts.** 5 parts for up to an hour, 8 for 90 minutes. Each part = one divider + 3–5
  content slides.
- **The one-sentence through-line** — the answer the whole deck argues. If it does not
  account for every part, a part does not belong or the sentence is wrong.
- **Visuals per part**: which diagram, which chart, which source figure.

## 2. Draft the slides

Start from [examples/starter/slides.md](../../examples/starter/slides.md). Each of its
slides carries a yellow **DEMO** note naming the feature it shows — read them, then
delete every `<div class="demo">…</div>` line. Set the frontmatter:

```yaml
---
marp: true
theme: innopolis
paginate: true
class: xl          # deck default for online / laptop audiences
---
```

- Write **every title first**, as a claim ([slide-writing § Titles](../../references/slide-writing.md#titles)).
  The title list alone should read as the argument.
- Tag each section on its divider: `<!-- _class: lead bN -->` + `<!-- class: xl bN -->`,
  `b1`…`b7` in order, `b8` for agenda and wrap-up.
- Choose the tier per slide only where `xl` does not fit — `large`, then `dense`.

Layouts, the `dense` / `large` / `xl` tiers and the section-coloured progress bar are
explained with pictures in [layouts-tiers-progress.md](layouts-tiers-progress.md).

![The same slide in four density tiers](../images/density-tiers.png)
- Put the detail you cut — numbers, caveats, the story — in speaker notes
  (`<!-- … -->`) the moment you cut it, not later.
- Leave `<div class="placeholder">` for visuals you have not made yet.

## 3. Media

Everything goes in `media/`, named for its content, source next to render —
[media conventions](../../references/media-conventions.md).

```bash
# diagram: write media/review-flow.mmd (plain Mermaid, one edge per line), then
python <skill-dir>/scripts/build-diagram.py media/review-flow.mmd

# chart: write media/pr-size.vl.json (copy a template from references/charts.md), then
vl2svg media/pr-size.vl.json media/pr-size.svg
```

Anything you did not make gets a row in `media/SOURCES.md` and a credit on the slide.

## 4. Build

```bash
python <skill-dir>/scripts/build-deck.py slides.md           # while iterating (~2 s)
python <skill-dir>/scripts/build-deck.py slides.md --pdf     # when it settles
```

Or use the live preview in VS Code ([vscode-preview.md](vscode-preview.md)) while
writing, and build only to check.

## 5. Check

`build-deck.py --pdf` runs the overflow check automatically:

```
10 slides, 0 overflowing (limit 89%, max 84.0% on p3), 0 with text hidden behind a box
```

- `OVERFLOW` — content runs under the footer. Cut words; then drop that slide one tier.
- `HIDDEN` — text sits behind an opaque `.takeaway` / `.box`. Same fix.
- `tight` — fine, but look at it.

`HIDDEN` is the one you would miss by eye in a hurry — the slide looks nearly right, and
it measured *under* the overflow limit:

![A two-column slide whose last bullets are cut off by the yellow takeaway box painted over them](../images/pitfall-hidden-text.png)

More failure pictures: [troubleshooting.md](troubleshooting.md).

Then **open the PDF and look at every slide you changed.** The checker is a net, not a
proof. Also check:

- PDF page count = slide count (a mismatch means a `![bg]` crept in).
- Progress-bar sections match your parts (`build-progress-map.py` prints them).
- No title wraps onto a second line.

## 6. Review with the minto-pyramid skill

A deck is decision-bearing writing: the sequence of titles is an argument, and the most
common faults — a topic label where a claim should be, the real point buried on slide
14, a section whose slides do not support its claim — are exactly what the
[Minto Pyramid](https://github.com/millwright-labs/minto-pyramid-skill) skill audits.
Install it once ([installation](installation.md#the-minto-pyramid-skill)).

**Review the title list, not the markdown.** The skill works on prose, and the titles
*are* the deck's prose. Extract them:

```bash
grep -n '^# ' slides.md
```

Then run three passes. With Claude Code, just ask:

| Pass | Ask | What it catches |
|------|-----|-----------------|
| **So-what pass** | *"Run a minto so-what pass on these slide titles."* | Titles that are topic labels ("Monitoring Overview") instead of claims |
| **Buried-lede test** | *"Minto buried-lede test: is the deck's main point on the first content slides?"* | The answer arriving at the end instead of up front |
| **Reason audit** | *"Minto reason audit on part 2: do these slide titles support the divider's claim, MECE?"* | A section whose slides overlap, leave a gap, or argue something else |

Optionally: *"Minto email version of this deck"* — a three-paragraph summary to send to
people who will not attend. It is also a good test: if the email is hard to write, the
deck's through-line is not clear yet.

Three things to know:

- The skill **offers** restructurings; it does not rewrite your draft unasked. Apply
  what you agree with, then rebuild.
- It **declines** chronological material — agendas, timelines, procedures — because the
  order is the content there. Leave agenda and logistics slides out of what you give it.
- **Dividers are the exception** to "title = claim". A `.lead` slide names its section
  plainly; tell the skill so, or leave dividers out of the list.

## 7. Share

- Send the **PDF**. It is the deliverable; the HTML needs the media folder beside it.
- PowerPoint: `--pptx` (slide images, with notes) or `--pptx-editable` (real text, no
  notes) — see [pptx-export.md](pptx-export.md).
- Sharing the **source**: the deck folder with `slides.md` and all of `media/`,
  including `.drawio`, `.vl.json` and `SOURCES.md`. Build outputs can be regenerated.

## Reusing a deck later

- Dates and calendar references belong on the title and closing slides only, so those
  are the only two to edit.
- Diagrams marked **hand-owned** in `SOURCES.md` are re-exported from their `.drawio`,
  never rebuilt from `.mmd`.
- After updating the skill, rebuild: the progress map bakes the theme's colours into
  each deck.
