# Pitfalls deck — deliberately broken

Five slides, each showing one common mistake. Its renders illustrate
[docs/user/troubleshooting.md](../../docs/user/troubleshooting.md), and it doubles as a
**regression test for the overflow checker**, which must fail on it:

```bash
cd examples/pitfalls
python ../../scripts/build-deck.py slides.md --pdf     # must exit 1
```

Expected report — slide 5 overflows, slide 4 has text hidden behind the takeaway:

```
  p  5   91.3%  OVERFLOW  A Long List Runs Under the Footer
  p  4   87.3%  tight     Too Much in the Columns Hides Behind the Box
  p  4  HIDDEN    text painted behind a callout box:
           | ReleaseisboringReleaseisanevent
5 slides, 1 overflowing (limit 89%, max 91.3% on p5), 1 with text hidden behind a box
```

Note slide 4 measures only 87.3% — *under* the limit. The extent check alone would pass
it; only the hidden-text check catches it.

Slide 5 reports 91.3%, yet its eleventh item is printed over the footer and the twelfth
is off the canvas. Lines inside the footer band are excluded as "footer", so **the
percentage understates how far an overflow goes** — treat any `OVERFLOW` as "look at
the slide", not as a measurement.

If the checker ever passes this deck, it has regressed.

| Slide | Mistake | Fix |
|------:|---------|-----|
| 1 | `**bold**` inside a `<div>` renders literally | `<strong>`, `<em>` inside HTML blocks |
| 2–3 | A small diagram is shown at natural size — the theme only shrinks images | `![… w:900](…)` on wide diagrams |
| 4 | Columns taller than their room grow **behind** the opaque takeaway | Cut bullets, or drop the slide a tier |
| 5 | A long list runs under the footer and off the canvas | Cut, split, or drop a tier |
