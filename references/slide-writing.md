# Slide-writing rules

The theme makes a slide look right. These rules make it *say* something. They were
learned by getting them wrong on real decks; each has a reason attached.

## Titles

### 1. A content slide's title is its key message

The title states the claim; the body supports it (Minto's pyramid — answer first).

| Topic label | Key message |
|-------------|-------------|
| "Estimation Methods" | "Wideband Delphi Converges in 2–3 Rounds" |
| "Code Review" | "Review Time Grows Faster Than the Diff" |
| "Monitoring Overview" | "Alert on Symptoms, Not on Causes" |

### 2. …and graspable cold, in one glance

Read the title with no other slide in view. If you cannot say what the slide will tell
you to *do*, rewrite it. A title that only lands once you already hold the concept is a
topic label wearing a claim's clothes. Keep a paradox — it is often the real finding —
but put it in the body, where the slide has room to set it up.

### 3. The title names its own subject

No pronoun pointing at the previous slide, no statistic standing in for a subject.
"Seasoned Developers Call **It** a Junior Colleague" → "…Call **the Assistant** a Junior
Colleague".

### 4. The title stays on one line

H1 is 42 px in every tier. If it wraps, shorten it — never shrink it.

### 5. A divider names its section

`.lead` slides are the exception to rule 1. The `h1` is the section name, plain and
unclever — **the same words the agenda slide uses**, so the audience can track both. The
`h2` says what the section teaches. When a section is renamed, the divider and the
agenda move together.

## Body

### 6. One idea per slide

Cut the non-essential to pay for it. The detail is not deleted; it moves to the speaker
notes or a handout.

### 7. Bullets, not prose

A paragraph on a slide gets *read*, and the audience stops listening while they read
it. Bullets are fragments; no full stops needed. **Full sentences are for quotes** and
the one-line claim inside a `.takeaway` or `.box`. A bullet longer than one line at the
deck's tier is a sentence in disguise — cut it.

### 8. Two parallel lists the reader must match up is a table

When the left column lists items and the right column lists one thing per item, the
columns are a table with the rows pulled apart, and the reader does the join by eye. It
also doubles the height — which is how takeaways end up painted over the last bullet.
Make it `| Item | Example | Why it matters |`.

### 9. A number must change what the audience does

Put a number on a slide only when the slide can say "…so do X". Keep at most the one
number that carries a contrast; say the rest in plain words. Statistical apparatus
(β, *p*, CI, sample composition) belongs in the notes, not on the slide.

### 10. A chart shows the comparison its title claims

Pick the mark from the claim, not from the data's shape. A trend or divergence needs
its driver on a shared x-axis; facets are for independent comparisons. See
[charts.md](charts.md#pick-the-mark-from-the-claim).

### 11. A takeaway must not take back what the slide just taught

Watch for takeaways hinging on **but / however / although / that said** where the second
half retracts the first. Keep the assertion, delete the retraction. A needed caveat
belongs on the slide that owns it, or in the notes.

### 12. A caveat off the slide means an example on

When a qualification comes off a slide, put a quote, case or worked example in its
place. Examples are what make material teachable; caveats are what make it hedged.

### 13. Never narrate your own production process

The audience is not interested in how the deck was made: which source you could not
find, why a diagram was redrawn, what an earlier version said. If you have no source
for something, teach it as practice or cut it. Production notes go in the commit
message or a planning file.

### 14. The history of an idea is not the idea

A slide about *who published it, when, in which edition, on what sample* is the idea's
biography. Teach what it is, what you see when it happens, and what you do about it.
Dates and authorship go in the footer citation and the notes.

## Cross-references

### 15. Refer to other sessions by name or code, not by weekday

"As we saw on Friday" is meaningless to someone reading the PDF a week later, and binds
the deck to one calendar. Say "in Session 2". Concentrate dates on the title and closing
slides, so they are the only ones to edit when the deck is reused.

### 16. Do not reveal an assessment item on a slide

If the deck feeds a quiz or exam, the mapping of slides to questions is planning
material. Teach the thing; let the assessment find it. The date and format of an
assessment on the closing slide is fine — its questions are not.

### 17. A cross-reference is a dependency

When a slide says "bring what your group produced last time", changing last time
breaks it silently. Grep related decks for references to each other whenever one
changes.

### 18. The last content slide poses the next question

Before the close, leave the audience holding the question the next session answers —
not a table of contents.

## Mechanics

- **No markdown inside `<div>`** — use `<strong>`, `<em>`, `<br>`.
- **No `![bg]`** — it breaks pagination.
- **Footer citations**: `<!-- footer: Author Year, Short Title -->`, reset with
  `<!-- footer: "" -->` on the next slide.
- **Speaker notes**: any non-directive HTML comment. Put the story, the example and the
  numbers the slide left out there.

## Review with the `minto-pyramid` skill

A drafted deck is decision-bearing writing: its title sequence is an argument. The
[`minto-pyramid`](https://github.com/millwright-labs/minto-pyramid-skill) skill audits
exactly that. How to run it on a deck:
[docs/user/workflow.md § 6](../docs/user/workflow.md#6-review-with-the-minto-pyramid-skill).
