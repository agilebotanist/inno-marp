# Illustrations on section dividers

A `.lead` divider can carry one illustration — a comic strip, a photo, a sketch. It
gives the audience a beat between topics and makes an online talk less of a wall of
text. It is optional: `h1` + `h2` alone is a clean divider.

## Placeholder first, image later

While drafting, write the slot. It documents what the image should be, so finding or
making it later is mechanical.

```html
<div class="comic-placeholder">
📁 ill-part1-review-queue.png | 🎨 840x315px | Three panels: dev opens a 2,000-line PR; reviewer's face; reviewer types "LGTM".
</div>
<p class="comic-caption">Credit line goes here</p>
```

| Field | Meaning |
|-------|---------|
| `📁 filename` | Target name in `media/` — `ill-part[N]-<topic>.<ext>` |
| `🎨 WxHpx` | **840×315 (8:3)** for a 3-panel strip |
| Description | Enough for someone to search for or draw it |

## Replacing a placeholder

```markdown
![Dev opens a huge PR; the reviewer approves it unread w:900](media/ill-part1-review-queue.png)
<p class="comic-caption">Artist / Publisher, YYYY-MM-DD</p>
```

- Alt text describes the **scene**, not "comic".
- `w:900` suits a wide 3-panel strip on a divider; recompute after any re-crop.
- The `h2` above it should say what the section teaches **and** anchor the image, so
  the picture reads as an illustration of that line rather than a joke that arrived
  alone.

## Where images come from — in order of preference

1. **A real, licensed work whose point *is* the teaching point.** Credit it exactly as
   its licence requires, **do not crop or edit it**, and record it in `media/SOURCES.md`.
   A loosely fitting real strip on the section's theme beats none, and beats a
   generated approximation of one.
2. **An original sketch or a neutral stock image** with a permissive licence.
3. **A generated image**, only when neither exists. Name the tool in the caption, record
   the prompt in `SOURCES.md`, and **never imitate a recognisable copyrighted character
   or artist's style** — an uncredited pastiche in material you share is a problem you
   do not want.

When nothing fits, ship the divider without an image and note the gap in `SOURCES.md`
so the next search starts from there.

## Search the analogy, not the literal topic

Older strips and stock libraries describe ideas in the vocabulary of their own era. A
literal search for a modern topic can return nothing while a search for its analogy
(the robot, the outsourced team, the consultant) finds exactly the right strip. Record
what you searched and what you rejected.

## Attribution is not optional

Every image you did not make carries a credit on the slide (`.comic-caption` or
footer) and a row in `media/SOURCES.md`. See
[media-conventions.md § SOURCES.md](media-conventions.md#5-sourcesmd--provenance).

## Other visual slots

| Class | Use |
|-------|-----|
| `.placeholder` | A diagram not yet drawn — dashed green box, one line of description |
| `.stat-box` | A single number that deserves the whole eye |
| `.box.n` | A caveat under a chart ("reconstructed from the source's figure") |
