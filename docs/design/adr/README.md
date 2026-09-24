# Architecture Decision Records

Each record captures one decision: the problem, what was decided, and what it costs.
They are **why** the theme and scripts look the way they do — read the relevant one
before changing a behaviour, and add a new one (from [template.md](template.md)) when
you change a decision. Superseded records stay, marked as such.

| # | Decision |
|---|----------|
| [0001](0001-markdown-and-marp.md) | Markdown + Marp as the authoring format |
| [0002](0002-theme-as-registered-css.md) | One registered theme file, not per-deck CSS |
| [0003](0003-embed-title-background.md) | Embed the title background in the generated theme |
| [0004](0004-tokens-on-section.md) | Declare design tokens on `section`, not `:root` |
| [0005](0005-tiers-scale-body-only.md) | Density tiers scale body text only; the H1 is fixed at 42 px |
| [0006](0006-diagrams-drawio-first.md) | Diagrams: Mermaid in, draw.io as editable source, SVG out |
| [0007](0007-retheme-after-import.md) | Re-theme draw.io output after import; write plain Mermaid |
| [0008](0008-svg-without-embedded-fonts.md) | Export SVG without embedded fonts |
| [0009](0009-charts-vega-lite.md) | Charts as Vega-Lite specs compiled to SVG |
| [0010](0010-progress-bar.md) | Progress bar in pure CSS, section map generated from rendered HTML |
| [0011](0011-section-colours-distinct-hues.md) | Section colours: distinct hues in spectrum order |
| [0012](0012-layouts-not-bg-directives.md) | Layout classes instead of Marp `![bg]` backgrounds |
| [0013](0013-overflow-check-on-pdf.md) | Check overflow on the PDF, including text hidden behind callouts |
| [0014](0014-media-conventions.md) | Media conventions: flat `media/`, shared basenames, sources committed, provenance file |
| [0015](0015-repo-is-the-skill.md) | The repository is the skill directory |
| [0016](0016-outputs-html-pdf-pptx.md) | Ship HTML and PDF; PPTX in two flavours |

Overview of how they fit together: [../architecture.md](../architecture.md).
