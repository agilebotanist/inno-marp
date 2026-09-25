# Charts — Vega-Lite

Marp does not render Vega-Lite either. Write a `.vl.json` spec in `media/`, compile it
to **SVG**, embed the SVG.

```bash
vl2svg media/pr-size.vl.json media/pr-size.svg
```

```markdown
![Median review time by pull-request size](media/pr-size.svg)
```

Commit both the `.vl.json` (source) and the `.svg` (what the deck renders). SVG rather
than PNG: crisp at any size, small, and no font-sizing quirks inside Marp's
`<foreignObject>` ([ADR 0009](../docs/design/adr/0009-charts-vega-lite.md)).

`vl2svg` comes from the `vega-lite` npm package and needs `vega-cli` beside it —
[installation](../docs/user/installation.md#vega-lite). Iterate on a spec in the
[online Vega editor](https://vega.github.io/editor/) and paste it back.

---

## Pick the mark from the claim

**A chart must show the comparison its title claims.** Choose the mark from what the
slide asserts, not from the shape of the data.

- A **trend or a divergence** → put the driver on a shared x-axis (line chart). A
  title like *Actual Throughput Falls Away from Potential* needs both lines on one axis
  so the gap *is* on the page — label the band between them.
- **Facets** (`column` / `row`) are for genuinely independent comparisons. Facetting a
  trend by its own driver splits the finding across panels and hides it.
- **Ranking** → sorted horizontal bar.
- **Before / after** → grouped bar, light → dark.

When the chart rebuilds a figure from a source, keep that figure's form — see
[media conventions § Figures from a source](media-conventions.md#6-figures-from-a-source).

---

## Shared config block

Every chart carries this `config`, so axes and fonts match the slide typography:

```json
"config": {
  "font": "Tahoma, Verdana, sans-serif",
  "axis": { "labelFontSize": 14, "titleFontSize": 16, "labelColor": "#282828", "titleColor": "#282828" },
  "legend": { "labelFontSize": 14, "titleFontSize": 14 },
  "view": { "stroke": null }
}
```

`"view": {"stroke": null}` removes Vega's default border, which otherwise reads as a
stray box on a white slide. For an `.xl` deck, raise the sizes to 18/20.

---

## Palette

| Role | Hex | Token |
|------|-----|-------|
| Primary series | `#019546` | `--inno-green` |
| Secondary series | `#2D6E2A` | `--inno-green-dark` |
| Tertiary series | `#81c784` | `--inno-green-light` |
| Faint fill | `#c8e6c9` | — |
| Warning / target line | `#ffc107` | `--inno-yellow` |
| Negative / overrun | `#d32f2f` | `--inno-red` |

For a before/after pair use `["#c8e6c9", "#019546"]` — light to dark reads as
"then → now" without a legend lookup. Beyond three series the greens stop separating;
switch to the section palette (`#dc2626`, `#ea580c`, `#ca8a04`, `#0d9488`, `#2563eb`,
`#7c3aed`).

---

## Bar chart

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "width": 520, "height": 300,
  "data": { "values": [
    {"size": "< 50 lines",   "hours": 3},
    {"size": "50–200",       "hours": 9},
    {"size": "200–500",      "hours": 22},
    {"size": "> 500",        "hours": 51}
  ]},
  "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4},
  "encoding": {
    "x": {"field": "size", "type": "ordinal", "sort": null, "axis": {"labelAngle": 0, "title": "Diff size"}},
    "y": {"field": "hours", "type": "quantitative", "title": "Median hours to merge"},
    "color": {"value": "#019546"}
  },
  "config": {
    "font": "Tahoma, Verdana, sans-serif",
    "axis": {"labelFontSize": 14, "titleFontSize": 16},
    "view": {"stroke": null}
  }
}
```

## Horizontal bar — long category labels, ranking

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "width": 420, "height": 260,
  "data": { "values": [
    {"cause": "Waiting for a reviewer", "share": 46},
    {"cause": "Failing CI",              "share": 28},
    {"cause": "Merge conflicts",         "share": 17}
  ]},
  "mark": {"type": "bar", "cornerRadiusEnd": 4},
  "encoding": {
    "y": {"field": "cause", "type": "nominal", "sort": "-x", "axis": {"title": null}},
    "x": {"field": "share", "type": "quantitative", "title": "% of delay"},
    "color": {"value": "#019546"}
  },
  "config": {
    "font": "Tahoma, Verdana, sans-serif",
    "axis": {"labelFontSize": 14, "titleFontSize": 16},
    "view": {"stroke": null}
  }
}
```

## Grouped bar — before / after

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "width": {"step": 46}, "height": 260,
  "data": { "values": [
    {"team": "Web",    "when": "Before", "days": 4.1},
    {"team": "Web",    "when": "After",  "days": 1.6},
    {"team": "Mobile", "when": "Before", "days": 5.3},
    {"team": "Mobile", "when": "After",  "days": 2.2}
  ]},
  "mark": {"type": "bar", "cornerRadiusTopLeft": 3, "cornerRadiusTopRight": 3},
  "encoding": {
    "x": {"field": "when", "type": "nominal", "sort": ["Before", "After"], "axis": {"title": null}},
    "y": {"field": "days", "type": "quantitative", "title": "Days to merge"},
    "color": {"field": "when", "type": "nominal",
              "scale": {"domain": ["Before", "After"], "range": ["#c8e6c9", "#019546"]},
              "legend": {"title": null}},
    "column": {"field": "team", "header": {"title": null}}
  },
  "config": {
    "font": "Tahoma, Verdana, sans-serif",
    "axis": {"labelFontSize": 14},
    "view": {"stroke": null}
  }
}
```

## Multi-line — planned vs actual

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "width": 540, "height": 300,
  "data": { "values": [
    {"week": 1, "series": "Planned", "value": 10}, {"week": 1, "series": "Actual", "value": 9},
    {"week": 2, "series": "Planned", "value": 25}, {"week": 2, "series": "Actual", "value": 21},
    {"week": 3, "series": "Planned", "value": 45}, {"week": 3, "series": "Actual", "value": 35},
    {"week": 4, "series": "Planned", "value": 70}, {"week": 4, "series": "Actual", "value": 52}
  ]},
  "mark": {"type": "line", "point": true, "strokeWidth": 3},
  "encoding": {
    "x": {"field": "week", "type": "ordinal", "title": "Week"},
    "y": {"field": "value", "type": "quantitative", "title": "Cumulative work done"},
    "color": {"field": "series", "type": "nominal",
              "scale": {"domain": ["Planned", "Actual"], "range": ["#2D6E2A", "#ffc107"]},
              "legend": {"title": null}}
  },
  "config": {
    "font": "Tahoma, Verdana, sans-serif",
    "axis": {"labelFontSize": 14, "titleFontSize": 16},
    "point": {"size": 70, "filled": true},
    "view": {"stroke": null}
  }
}
```

## Burndown — actual vs ideal

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "width": 520, "height": 280,
  "data": { "values": [
    {"day": 0, "line": "Ideal", "left": 100}, {"day": 0, "line": "Actual", "left": 100},
    {"day": 2, "line": "Ideal", "left": 75},  {"day": 2, "line": "Actual", "left": 88},
    {"day": 4, "line": "Ideal", "left": 50},  {"day": 4, "line": "Actual", "left": 66},
    {"day": 6, "line": "Ideal", "left": 25},  {"day": 6, "line": "Actual", "left": 38},
    {"day": 8, "line": "Ideal", "left": 0},   {"day": 8, "line": "Actual", "left": 12}
  ]},
  "mark": {"type": "line", "point": true, "strokeWidth": 3},
  "encoding": {
    "x": {"field": "day", "type": "quantitative", "title": "Day"},
    "y": {"field": "left", "type": "quantitative", "title": "Work remaining"},
    "color": {"field": "line", "type": "nominal",
              "scale": {"domain": ["Ideal", "Actual"], "range": ["#81c784", "#019546"]},
              "legend": {"title": null}},
    "strokeDash": {"field": "line", "type": "nominal",
                   "scale": {"domain": ["Ideal", "Actual"], "range": [[6, 4], [1, 0]]},
                   "legend": null}
  },
  "config": {
    "font": "Tahoma, Verdana, sans-serif",
    "axis": {"labelFontSize": 14, "titleFontSize": 16},
    "view": {"stroke": null}
  }
}
```

---

## Reconstructed data

When a chart re-draws numbers read off someone else's figure rather than a published
table, say so on the slide, and record it in `media/SOURCES.md`:

```html
<div class="box n">Chart reconstructed from Author Year, Fig. 3, to show the trend. Values are approximate.</div>
```
