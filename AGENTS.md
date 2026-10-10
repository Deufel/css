# mike.css — the engine, the blocks, the charts

mike.css is a small design **engine**, not a component library. You style
semantic HTML (button, table, form), compose a handful of layout classes,
and theme everything by setting a few inherited custom properties. There
are no variant classes. A button is a button; its look comes from the
`--bg`/`--fg`/`--hue` it inherits. The source is the `Deufel/css` repo
(`mike.css`, `mike-email.css`, AGENTS.md — this text — and a README); a
product commits a copy at `static/mike.css` and never edits it in place:
an engine change is a commit there, a tag, a copy here.

## ONE file, one spine

Twelve layers, declared once; the layer order IS the cascade:

    @layer reset,
           core.color, core.type, core.shell, core.shape,   /* the four cores — orthogonal */
           theme, base,                                      /* ALL config · bare-element defaults */
           composition, block, utility,                      /* layout primitives · components · the closed helper list */
           exception, visibility;                            /* variants, states, modes · the display gates, LAST */

- `core.color` surfaces and ink as positions on a three-anchor walk;
  `core.type` the type scale IS the spacing system (lh/em only);
  `core.shell` the `.page` shell and its pg-* regions; `core.shape` the
  self-describing cell. The cores read nothing from each other (shell and
  shape read type's lh only).
- `theme` holds every knob's single home; `base` the bare defaults.
- `composition` the primitives (.row .column .grid .spread .stack .frame …).
- `block` the components — a `<blk-*>` tag owns one rule; a product's
  blocks live in the product's own sheet (`static/blocks.css`) in this
  same layer.
- `utility` the CLOSED helper list, late so a helper beats a block.
- `exception` what overrides from outside: skins, radius, standing states
  (`data-ui-state`), modes (print, focus, view transitions).
- `visibility` the gates — `display: revert-layer` — last, so a gate
  outranks every display a block sets.

THE THREE LAWS. (1) Zero specificity: every selector is `:where()`-
wrapped; within a layer only source order breaks a tie; a specificity
fight is a bug to root-cause, never to out-specify. (2) No `!important`,
anywhere (an important declaration inverts the layers and beats the
gates; paper is a plain print block in `exception`). (3) Locality: a
block's parts, states and shape arrangements nest inside its one rule;
nothing about a block lives anywhere else — visibility is the one
exception, by design, because a part declares WHICH shapes it belongs
in and the gate layer owns the only two states.

Enforcement is Go: the product's `engine_test.go` pins the spine and the
laws on the committed copy; `blocks_test.go` pins locality on
`blocks.css`; `view/ratchet_test.go` ratchets inline geometry and the
gap ladder in the templates; `prune` reports an engine class no lab
page wears as UNDEMOED (the fix is a specimen, never a deletion).

## THE PAINTER MODEL (colour)

Colour is computed, never picked. You never write a hex.

- `--hue` (0–360) sets a subtree's hue; `--hue-shift` nudges it
  relative to context; `--hue-lock` pins it absolutely — ONLY for
  semantics (`.suc .inf .wrn .dgr`), never as a colouring tool.
- `--bg` is an ABSOLUTE surface position on a −1…+1 walk through three
  anchors (−1 neutral floor, 0 paper, +1 full chroma). `--lift` is a
  RELATIVE surface, N above the host. `--chroma` scales saturation.
- `--fg` is the INK: sign picks neutral (−) or chromatic (+), magnitude
  the strength. `--fg: -1` full neutral ink; `--fg: 0.85` vivid ink at
  the hue (how coloured numbers glow); `-0.5…-0.6` quiet.
- `--type` is a STEP on the type scale and inherits; the scale is
  absolute so steps never compound. Type IS spacing: one step re-rhythms
  text, gaps and control heights. Components never re-type themselves;
  a usage site nudges, through the knob. `--scale` is the regional zoom.
- `--focus` and `--border` are the derived token pair every surface
  computes: read them, never redefine them.

Publisher contract: a region, `.bg`, `.card` or `.surface` paints via
`background-color: var(--_bg)`. Internal `--_` variables are not the
API; if you reach for `--_sem-ink` you want `--hue-lock` + `--fg`.

## THE CELL, THE SHAPES, THE BLOCK CONTRACT

"Each block is able to manage itself" (Mike, 2026-10-08): the shell is
the chrome, pg-main a grid of cells, and a `<blk-*>` in a cell arranges
itself for the cell it is given. Locality of behaviour and few helpers
are what let an agent write a stable component.

THE CELL: `.cell` is a size query container named `shape` — a grid
track, a region, a chip. The layout hands a cell its size; size
containment collapses it under an auto-height parent, and a flex-grown
cell answers its queries with nothing (Chrome evaluates them at the flex
base size). A cell is EXACTLY ONE SHAPE, in its own lh so `--type` and
`--scale` move the boundaries with the text:

    spot  w<3lh h<3lh · line  w≥3lh h<3lh · rail  w<3lh h≥3lh
    slip | sheet   ratio < 7/8          short side (w)  < 8lh | ≥ 8lh
    tile | panel   7/8 ≤ ratio < 15/8   min(w,h)        < 8lh | ≥ 8lh
    strip | banner ratio ≥ 15/8         short side (h)  < 8lh | ≥ 8lh

THE BLOCK: the tag is the component and its only hook — `<blk-kpi>`,
`<blk-location>`. ONE rule per block in the product's `static/blocks.css`:

    @layer block {
      :where(blk-location) {
        display: grid; …                                 /* its box */
        & :where(header) { … }                           /* parts, by element */
        &:where([data-ui-state~="armed"]) { … }          /* states, ~= tokens */
        flex-direction: var(--is-strip, row) var(--no-strip, column);   /* arrangement per shape */
      }
    }

THE SHAPE, PUBLISHED (v3.1.0): the shape layer sets `--shape` (one of the
nine words) and `--size` (small | large) on every child of a cell — the
block — and its parts inherit them. A PART arranges per shape by querying
them by name, flat, one line a case, nested in the block's rule:

    & > :where(.num) {
      --type: 3;
      @container style(--shape: spot) { --type: -2; }
      @container style(--shape: line) { --type: 0; }
      @container style(--size: small) { --fg: -1; }
    }

A style query reads the nearest ancestor, so a part reads its block and
the block's OWN BOX cannot read itself. For the block's own arrangement
(its direction, writing mode, padding) the SHAPE TOGGLES (v2.1.0) stay:
`--is-X` is guaranteed-invalid (`initial`) when the cell IS X, so
`var(--is-X, value)` takes its fallback; `--no-X` is the reverse;
`var(--is-X, A) var(--no-X, B)` is A in X, B elsewhere. X is a shape or a
family: `small` (spot line rail slip tile strip — one figure), `tall`
(rail slip sheet), `run` (line strip — one row across). TWO CASES AT MOST:
a third case nests a pair inside a fallback, and a pyramid of fallbacks
drops its whole declaration on one wrong paren — that is what the
published words exist to replace (its test refuses a line nested three
deep). A product writes NO size container query (`@container shape (…)`
is a second definition of a shape) and NO `display: none`: the shapes
are defined once, in the engine, and hiding is the gates' job.

- Parts are semantic elements (header h3 small strong figure ul li time
  mark progress footer …); a part class (.ring .dot .av) means something
  only inside its block.
- A part lists the shapes it belongs in with the shape classes
  (`<small class="line strip banner">`); the gate layer shows it only
  there. A block never hides a part and never writes a container query.
- Knobs for colour and type, inline only where a value is DATA (an
  avatar's hue); helpers only from the closed utility list; state as
  `data-ui-state="a b"` tokens matched `~=`, after native and ARIA
  state (disabled, aria-pressed, :open); every selector wrapped; no
  `!important`; nothing reaches outside the tag.
- A block is written FOR THE BENCH FIRST: the product's Layout bench
  (`/admin/layout`) puts one block in a resizable cell with a shape tag
  that names the shape; every shape is looked at before a page wears
  the block. The lab's Shapes page is the engine's own specimen.

## LAYOUT — the shell and the primitives

Regions are grid areas on `.page`: pg-banner, pg-header, pg-subheader,
pg-navigation (n1), pg-toolbar (the n3 rail), pg-main-header, pg-main-
subheader (tabs, crumbs, strips that must not scroll), pg-main, pg-main-
aside, pg-main-footer, pg-aside, pg-footer. Set `--bg` on any to repaint.
Rails are min-width, type-derived and SERVER-DRIVEN (`--pg-navigation-w`
/ `--pg-toolbar-w` stamped once on `.page`; collapse is a stored pref,
labels drop through the tiers). Asides are content-sized. ONE topology:
no alternate grids at narrow widths — a region that cannot fit gates
itself and its track collapses.

Flow primitives: `.row` / `.column` (flex; `.row` centres its items —
`.start` to top-align), `.grid` (auto-fit, `--grid-min`), `.split`,
`.spread` (space-between), `.spread-column`, `.lcr`, `.flank`/`.flank-
start`/`.flank-end`, `.stack` (overlap — one grid area), `.frame` (a box
at `--ratio`, 16/9 by default, its child filling it), `.oneline`,
`.nowrap`, `.truncate`, `.grow`, `.fill`, `.center`, `.vr` (an hr stood
on end), `section.owns-scroll` (the component-scrolled section every
full-height roster is built on). `--gap` takes ONLY the ladder's rungs:
block `0 · 0.25lh · 0.5lh · 1lh`, inline `0.25em · 0.5em · 1em`. THE
CONTENT LADDER: `.content-1` (a column, 40ch) · `.content-2` (reading,
70ch) · `.content-3` (working, 100ch), in the wearer's own ch; rosters
take no rung. A width written as a length is a regression.

THE GATES (visibility, revert-layer) — three families, three jobs:
- viewport: `.mobile .tablet .desktop` (576px / 768px); container
  equivalents `.c-mobile .c-tablet .c-desktop` on the nearest container;
- density tiers: `.small` (< 8rem) · `.medium` (8–20rem) · `.large`
  (≥ 20rem), measured on the nearest container — a rail's content gates
  on these ("and-up" is the multi-class idiom `class="medium large"`);
- shapes: the nine, answered by the nearest `.cell`.
- `.fine` / `.coarse` gate on pointer type.
Gate classes go on a dedicated wrapper that also carries a layout
primitive (revert-layer restores the primitive's display, not a default).

Focus mode is a stored pref (`data-ui-state="focus"` on `.page`). Print
strips every region but pg-main*, surfaces to white, ink to black.

## COMPONENTS (styled semantics + a few words)

`.card` (lifted panel; `.Card` the voiced edge), `.surface` (a lift step
with no line), `.tag` (pill; pair a hue helper), `.avatar`, `.crumbs`
(a crumb `<a>` is a bare link), `.tree`, `.tabs` / `.tabs-underline`,
`.button-group`, `.nav-item`/`.nav-icon`, `.drawer` (+ .left/.right/
.top, `.glass`), `.modal` (a `.content-*` rung; `.content-1` the confirm,
`.content-3` the workbench), `.menu` (popover), `.search-box`, `.icon`
(THE icon-only square — explicit, aria-label required), `.roster` (THE
SERVER-DRIVEN TABLE: truncating cells, the hugging column model, tonal
head, `.scroll-x`), `.glass` (the surface at `--glass-alpha` over a
`--glass-blur`; 0.65 a dialog, 0.88 an overlay that must read over
anything), `.veil` (a glass card over its `.stack` sibling), `.hud`
(viewport overlay slots t/c/b × l/c/r), `.wash`, `.stress` (the lab's
resize handle, both axes), `.county-map`.

Dialogs are native `<dialog class="modal">` opened and closed in HTML —
`commandfor="<id>" command="show-modal"`, a bare close `command="close"`,
`closedby="any"`; `data-preserve-attr="open"` is MANDATORY on a live
page (a morph would close it). A verb that posts then closes is
Datastar's `@post(…); el.closest('dialog').close()`. Menus are
`popover` + `popovertarget`; a closed `.menu` must be `display:none`.
Anatomy glyphs are DECLARED boxes (`width="24" height="24"`); `.icon`
self-centres. Know what a word IS before composing it: `.sec` is a
BUTTON voice — on a wrapper it paints a ghost box.

THE FORM CANON: fieldsets own structure; `label → small → control`, the
small is the STATE slot (never a caption); everything fills the width;
`--row-width` is a bare number; Datastar submits, handlers answer 204;
THE EDIT CARD is the one record-form shape (h3 + pencil unlocks, Cancel
a native reset, Save posts).

## THE NUMBER FAMILY (utility — keep apart from the hue locks)

`.num` (nowrap, tabular, auto-spaces a `.delta`), `.delta`, `.num-good`
/ `.num-bad` (chromatic green/red INK — colour the VALENCE, not the
sign), `.num-flat`, `.number` (a live readout `--digits` wide; nothing
shifts), `.est` (italic, ~: an estimate), `.past` (quiet: a prior
period), `.num-table`. Colour encodes valence, typography encodes
certainty and time; the axes never collide. Which digits appear is Go
(rounding, currency, k/M); how they look is CSS.

## SVG CHARTS — painted by the engine

A chart is a Go function returning an SVG string, dropped in with
`@templ.Raw(...)` (view/chartrender.go holds the general builders and
the shared helpers — `foLabel`, `hueShift`/`hueStyle`, `ff2`, `scEsc`,
`niceStep`, `chartMax`, `ChartPoint`; page-owned builders import them,
never copy them). No client library, no canvas, NO COLOUR: every stroke
and fill is `currentColor`, and `--fg` on the element or its `<g>` is the
ink. The ladder (shipped values — do not invent rungs):

| layer | `--fg` |
|---|---|
| faint gridlines | −0.13 |
| axis lines | −0.4 |
| labels (foLabel default, `--type: -2`) | −0.8 |
| data marks | 1 (full chroma — the data is the star) |
| a single neutral series | −0.85 |
| quiet outlines, a silhouette behind the data | −0.25 at low fill-opacity |
| a prior period | −0.55 dashed |

Series step `--hue-shift` +30° apiece from the theme hue (`hueShift`/
`hueStyle`): a fixed step, never divided by count. `--hue-lock` in a
chart ONLY where a colour IS a meaning (kept = suc, spent = dgr).

Builder anatomy: fixed `viewBox` (W × H in logical units), margins for
labels, `xp`/`yp` closures, ~8% headroom, back-to-front `<g>` layers each
setting `--fg` once, `<title>` in every mark (free tooltips), ALL text
through `foLabel` (a foreignObject the engine types — never SVG `<text>`,
never a font or px literal). THE SCALING TRAP: the drawing scales by
rendered width over viewBox width, text included — pin the nominal W to
the host's width and say so. Area-proportional bubbles (r ∝ √value).
`%` in `Fprintf` is `%%`; `%g` for coordinates; raw strings for fragments.

Integration: data in a renderer method (never computed in a template), a
view struct per mark, the builder in the template. Interaction is
BACKEND-DRIVEN: a toggle or a grouping is a query-param link or a posted
signal, the handler re-renders the whole page; legends double as filters,
tinted by the same `hueShift` index the marks use. The quieting doctrine:
no per-mark totals (gridlines and titles do the work, one selective
direct label at most), a legend toggle keeps identical content in both
states, a single series gets no legend, sorted marks wherever order is
free, ONE axis always — two measures are two charts. Never `<progress>`
for a chart. The lab's Charts page is the shelf to copy from.

## Authoring checklist

- Theme with the knobs, never a class; never a hex, an ID selector or
  `!important`; never fight specificity.
- Compose the primitives; NO NEW CSS CLASSES (gf-185): a thing
  composition cannot express is a conversation at the lab bench, never a
  silent class. A product's component is a `<blk-*>` rule in blocks.css.
- Inline `style=` carries ONLY knobs or anchor plumbing; the geometry
  ratchet counts everything else and counts may only go down.
- Native dialog and popover for open/close; Datastar only for logic
  beyond that.
- VERIFY WITH EYES: a specimen in the lab (`/admin/lab`) or
  `go run ./cmd/snap`, then READ the PNGs at three widths before the
  one deploying commit.

## The FOUC ledger (do not relearn)

Cross-document view transitions are OFF (gf-200: a ~4 s stall on every
same-origin navigation, measured); the opt-in stays commented in the
exception layer with the `html[data-vt-ran]` probe armed. Assets are
VERSIONED (`av()` stamps `?v=`; immutable caches) so HTML never pairs
with a stale sheet. One view-transition name, one rendered box —
overlays whose content differs per page get `view-transition-name:
none`. The baked `meta color-scheme` keeps plain document swaps
dark-to-dark. Restart the app before judging a CSS change: staticfs
caches assets at boot.
