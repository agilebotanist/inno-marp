---
marp: true
theme: innopolis
paginate: true
class: xl
---

<!-- Deliberately broken deck. Every slide shows one common mistake.
     check-slide-overflow.py MUST exit 1 on it — see README.md. -->

<div class="demo">Pitfall — markdown inside a <code>&lt;div&gt;</code> is not parsed; use <code>&lt;strong&gt;</code>, <code>&lt;em&gt;</code></div>

# Markdown Inside a Box Is Not Parsed

<div class="takeaway">This takeaway uses **markdown bold** and *italics* — they render literally.</div>

<div class="takeaway">This one uses <strong>HTML bold</strong> and <em>italics</em> — they render.</div>

---

<div class="demo">Pitfall — no size given: the SVG shows at its natural, small width</div>

# A Small Diagram Is Not Enlarged

![Review flow, no size given](../starter/media/review-flow.svg)

---

<div class="demo">Fix — <code>w:900</code> in the alt text enlarges a wide diagram</div>

# A Small Diagram Is Not Enlarged

![Review flow, sized with w:900 w:900](../starter/media/review-flow.svg)

---

<div class="demo">Pitfall — columns too tall grow behind the opaque takeaway; the checker reports HIDDEN</div>

# Too Much in the Columns Hides Behind the Box

<div class="columns">
<div>

## Before

- Reviewed in one sitting
- Comments are specific
- Revert is cheap
- Tests run in minutes
- Nobody waits long
- Main stays green
- Release is boring

</div>
<div>

## After

- Reviewed in fragments
- Comments turn into LGTM
- Revert takes the good too
- Tests run for an hour
- Everyone waits
- Main breaks weekly
- Release is an event

</div>
</div>

<div class="takeaway">The last bullets of both columns are painted over by this box.</div>

---

<div class="demo">Pitfall — content past the bottom runs under the footer; the checker reports OVERFLOW</div>

# A Long List Runs Under the Footer

- First point on the slide
- Second point on the slide
- Third point on the slide
- Fourth point on the slide
- Fifth point on the slide
- Sixth point on the slide
- Seventh point on the slide
- Eighth point on the slide
- Ninth point on the slide
- Tenth point, into the footer
- Eleventh point, cut off
- Twelfth point, gone

<!-- footer: Footer citation, Author Year -->
