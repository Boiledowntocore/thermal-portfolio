# Prince Chauhan — Thermal Engineer portfolio

**Live:** https://princechauhan-thermal.github.io/

Static single-page site. No build step. Open `index.html` or serve the folder.

## Run locally

```bash
python -m http.server 4178 --directory "E:/cowork/thermal-portfolio"
```

Then open http://localhost:4178 — or use the Claude Code preview: server name **`portfolio`**.

## Design — "Plate Set"

One long page, read top to bottom. No modal, no carousel, no cards. Every project
is already open on the page. The visual model is a set of numbered drawing plates
pinned to a grey board.

| Decision | Value |
|---|---|
| Ground | `--paper #f2f3f4` — cool grey, not warm cream |
| Plates | `--panel #fff` with a 1px `--ink-20` hairline. No shadows |
| Ink | `#16181a` / `#4a4e52` / `#82878c` / `#c7cbce` |
| Accent | `--correction #cc2a1e`, used **only** where something marks a limit or a measured finding — roughly five places on the whole page |
| Type | Archivo (400/500) for everything readable; monospace for alphanumeric data only — codes, years, figures, axis labels |
| Radius | 0 (max 2px). No gradients, no blur, no drop shadows anywhere |

Light only, deliberately. A drawing has one ground.

## Structure

| File | Purpose |
|---|---|
| `index.html` | Section shells only, no content |
| `styles.css` | All styling |
| `main.js` | Renders every section from `window.SITE`, plus the motion |
| `data/content.js` | **All copy lives here** as one `window.SITE` object |
| `assets/media/*.svg` | The six figure plates |
| `assets/media/_dark-backup/` | Pre-redesign dark versions, kept for reference |

## Content model

Each project is one record: `code`, `title`, a **single** `sentence`, then
`role` / `scale` / `outcome` as a metadata row, then `figs[]`. The metadata row —
not a second sentence — carries the proof, which is what keeps the prose down.

Running prose across the whole site is about 175 words, down from ~1,400. If you
add copy, add it as a data field, not a paragraph.

Sections in order: lede → work (index table + TH-01…TH-04 + earlier) → position →
experience → patents → skills → education → contact.

## The plates

Six SVGs, re-inked from the old dark theme to black-on-white line art:

| Fig. | File | On |
|---|---|---|
| 1 | `prawaas-loop.svg` | TH-01 |
| 2 | `architecture-loop.svg` | TH-02 |
| 3 | `btms-capacity.svg` | TH-02 |
| 4 | `ctms-loop.svg` | TH-03 |
| 5 | `rectifier-derating.svg` | TH-03 |
| 6 | `sor-states.svg` | TH-04 |

Colour is **not** an information channel any more. Flow is encoded with
arrowheads and linetype instead — warm coolant solid, chilled coolant dashed —
so the drawings survive greyscale printing and colour-blind readers. The one
exception is `--correction`, which marks a measured finding (the shortfall traces
in FIG. 3 and FIG. 5, the "hold 25–35 °C" callout in FIG. 1).

Each SVG's own title and kicker were stripped and its viewBox cropped past them
(`viewBox="0 82 1000 478"`), because the plate frame already prints
`FIG. n <title>` above and a caption below. Do not add a title back inside a plate.

## Motion — read this before changing it

**Do not reintroduce `IntersectionObserver` for anything that reveals content.**
It was used originally and silently never fired in some contexts, which left
every `.reveal` section stuck at `opacity: 0` — a blank page with no error.
Reveals now run off a rAF-throttled scroll handler (`watch()` / `sweep()` in
`main.js`), plus a 4-second timeout that shows anything not yet reached.

The hidden state is also scoped to `html.anim`, a class `main.js` adds only once
it is running. So if the script fails, errors, or is blocked, the page renders in
full rather than blank. **The animation is an enhancement, never a prerequisite
for content being visible.** Keep both safeguards.



`main.js` fetches each SVG and inlines it, so the strokes can be animated —
an `<img>` is opaque to script. On first scroll-in, a plate **plots itself**:
paths draw via `stroke-dashoffset`, then labels fade in behind them.

Paths that already carry a `stroke-dasharray` (chilled runs, sensor lines) encode
meaning with it, so those fade rather than draw — overwriting the dash to animate
would destroy the distinction. Geometry inside `<defs>` is skipped entirely;
animating it blanks the arrowheads instead of drawing them.

Everything is gated on `prefers-reduced-motion`, which falls back to a plain
`<img>`-equivalent static render.

## Cache-busting

Asset refs in `index.html` carry `?v=N`. Bump N after editing `content.js`,
`main.js`, or `styles.css`. Note `index.html` itself is not cache-busted, so a
hard reload is sometimes needed after changing the shell.

## Making it dynamic — later

`main.js` never hard-codes content; it only reads `window.SITE`. Replace the
`<script src="data/content.js">` include with a fetch returning the same shape.

## Content note — read before publishing

Case-study detail is deliberately generalised where it touches proprietary
Sun Mobility or supplier design: no vendor names, no component geometry, no
absolute flow/head/capacity figures. The two comparison charts are normalised to
% of rated — **do not put the absolute numbers back**.

Kept: figures already on the public résumé, the public patent numbers, and
generic industry facts. Colleague and mentor names are deliberately omitted.

The photographs under `assets/media/raw/` are internal factory material and are
**not** referenced by the build. They need Sun Mobility sign-off before any
public hosting.

## Photographs

**Photographs are full colour.** They were briefly desaturated to protect the
single-red-accent rule; Prince chose colour on 2026-09-07 and that stands. The
schematics are still pure black line art, so the drawing-set character holds
without the grade, and a hiring page is the wrong place to spend warmth. Run
`tools/grade_photos.py` after adding any image — it crops and compresses only.

The **portrait** is the drawing set's *title block* — the cell that records who
drew the sheets — not a seventh figure. That is why it sits at Contact with a
"Drawn by" tag and no FIG. number, and why the face reads as provenance rather
than personal branding. `main.js` probes the file before injecting it, so the
site is publishable before the photograph exists.

A 22px face also rides the running head, because a reader who bounces before
Contact would otherwise never see a person at all.

## Before sharing the link

`index.html` carries og:/twitter: tags for the link preview card
(`assets/media/og-card.jpg`). **Both `og:url` and `og:image` must be absolute
URLs on the real deploy host** — they are set to the live Pages origin.
If the site ever moves (custom domain, different host), update all three tags
or the preview breaks silently.
A relative path renders no preview image at all, silently. This card is the only
part of the site that reaches someone who never opens the link, so it matters
more than its size suggests.
