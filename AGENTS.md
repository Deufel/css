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
           core.color, core.type, core.shell,               /* the three cores — orthogonal */
           theme, base,                                      /* ALL config · bare-element defaults */
           composition, block, utility,                      /* layout primitives · components · the closed helper list */
           exception, visibility;                            /* variants, states, modes · the display gates, LAST */

- `core.color` surfaces and ink as positions on a three-anchor walk;
  `core.type` the type scale IS the spacing system (lh/em only);
  `core.shell` the `.page` shell and its pg-* regions. The cores read
  nothing from each other (the shell reads type's lh only).
- `theme` holds every knob's single home; `base` the bare defaults.
- `composition` the primitives (.row .column .grid .spread .stack .frame …).
- `block` the components — a `<blk-*>` tag owns one rule; a product's
  blocks live in the product's own sheets (a file per block, served as one `blocks.css`) in this
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
block's parts and states nest inside its one rule; nothing about a block
lives anywhere else — visibility is the one exception, by design, because
a part wears a device or pointer gate and the gate layer owns the only
two states. A block is ONE layout (v3.2.0): it never rearranges by its
cell's size. Enforcement is Go (EventOS: `engine_test.go` the laws on
the copy, `blocks_test.go` locality and the arranger rules,
`view/dialog_test.go` the dialogs and the page shapes,
`view/ratchet_test.go` inline geometry and the gap ladder; `prune`
reports an engine class no lab page wears as UNDEMOED — the fix is a
specimen, never a deletion).

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
- THE READABILITY SCALE (v3.2.5): `[data-ui-size="custom"]` reads two px
  numbers, `--read-floor` (the smallest size the person reads
  comfortably, step −3) and `--read-ceiling` (the largest they want, step
  +3), and sets the scale itself — base = √(floor·ceiling), ratio =
  (ceiling/floor)^(1/6), no viewport fluidity. A phone is read close, a
  TV from across the room: the setting is the device's, and everything
  in lh and ch follows it; a layout switch in `ch` on a container then
  asks how many characters fit at the type this person reads (in
  `@media`, `ch` ignores the page's font — the switch is a container
  query).
- `--focus` and `--border` are the derived token pair every surface
  computes: read them, never redefine them.

Publisher contract: a region, `.bg`, `.card` or `.surface` paints via
`background-color: var(--_bg)`. Internal `--_` variables are not the
API; if you reach for `--_sem-ink` you want `--hue-lock` + `--fg`.

## THE SHELL · THE GATES · THE FRAME · THE PAGE · THE BLOCK

The layout contract, restated by Mike (2026-10-20, EventOS gf-821) after
the Summary page drifted from it. Five parts, each with one job; a page
that strays from any of them is the bug.

THE SHELL IS ONE FUNCTION. The product has one shell (EventOS:
`screenShell(Screen)` in view/layout.templ) that emits the chrome — the
stacked header (crumbs · title + verbs · filters | actions), the tab
band, the n3 rail — and then `<main class="pg-main column">` with the
page's body as its child. Every region it writes is one grid area of
`.page` (`core.shell`): the two are designed for each other and nothing
else writes a region. CHROME IS EVERYTHING AROUND THE THING YOU WORK IN;
pg-main is the thing, the area that expands. A dynamic layout hides
chrome explicitly — focus mode collapses the grid, a phone's nav is the
hub and the dock — never by a page's own rule.

THE GATES ARE THE FOUNDATION. The `visibility` layer is last. A gate
class sets `display: none`, and the matching query sets `display:
revert-layer`, which hands the element back whatever display a lower
layer gave it — flex, grid, a block's one-off — so any component is
turned on and off declaratively, as a union of readable class names:
`.mobile .tablet .desktop .ultrawide` (viewport), `.c-mobile .c-tablet
.c-desktop` (the nearest container), `.small .medium .large` (density
tiers), `.fine .coarse` (pointer — the iOS layouts, the dock). One family
per element; the second family goes on a wrapper. A part of a block is
shown or hidden ONLY this way, in the templ — never by the block's own
`@container` or `@media`.

THE FRAME. `pg-main` never scrolls (`overflow: hidden`, an inline-size
container). A page's body is ONE `<section>`, in one of two shapes:
- a FILLING page — `section.cell.owns-scroll`: a size container at 100%
  height, clipped; the page fits, its blocks own any scrolling;
- a READING column — `section.column.content-2|3`: natural height, the
  section scrolls itself (the frame's rule for a lone section).
Nothing else. A wrapper div, a bare `.column`, a `.grow` on the body are
the three ways a page has drifted.

THE PAGE ARRANGES. On a filling page the body's one child is the
ARRANGER — a `<blk-page>` (EventOS: `blk-event`, `blk-report`) whose rule
is a grid of named areas that fills the cell: `block-size: 100%`, strip
rows `auto`, the rest `minmax(0, 1fr)`, every area named for the block
it holds, no `overflow: auto` on the arranger. The page should fit with
no scrolling; where a thing may run long, its BLOCK scrolls it locally.
ONE switch, a container query in `ch` on the arranger's parent (the
cell), stacks the areas when fewer characters fit than the columns need;
stacked, the rows are `max-content` and the arranger scrolls — the
honest degradation the engine states for `.rise`. (The Summary is the
one page allowed to run long; it still has this shape.)

    @layer block {
      :where(blk-event) {
        display: grid; block-size: 100%; min-block-size: 0; overflow: hidden; gap: 0.75lh 2em;
        grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1fr);
        grid-template-rows: auto auto minmax(0, 1fr) minmax(0, 1fr);
        grid-template-areas: "metrics date weather location" "metrics date contacts location" "orders orders orders orders" "sales sales sales photos";
        & > :where(*) { min-inline-size: 0; min-block-size: 0; }
        & > :where(blk-orders) { grid-area: orders; }                     /* … one line a block … */
        @container (width < 96ch) { overflow-y: auto; grid-template-columns: minmax(0, 1fr); grid-template-rows: none; grid-auto-rows: max-content;
          grid-template-areas: "metrics" "date" "weather" "location" "contacts" "orders" "sales" "photos"; }
      }
    }

THE CELL under it: `.cell` is a size container — a grid track, a region.
The layout hands a cell its size; size containment collapses it under an
auto-height parent, and a flex-grown cell answers its queries with
nothing (Chrome evaluates them at the flex base size) — a cell is a
definite track or a region sized by knobs, never flex alone.

THE BLOCK. `<blk-name>` is the component and its only hook. ONE FLEX
LAYOUT, ONE RULE, in the product's own file for it (EventOS:
`view/blocks/<name>.css`, served as one `blocks.css`, layer `block`,
every selector `:where()`-wrapped, no `!important`). CO-LOCATION IS A
PAIRING, TESTED (EventOS gf-668/669): the file is named for the tag and
opens with a head naming every templ that opens it (`/* blk-orders —
opened by view/board.templ */`); each such templ names the file in the
comment of the component that opens it; a templ never styles a block in
a `<style>`; a file no templ opens is stale. A block FILLS whatever box
it is handed, NEVER REARRANGES ITSELF (no `@container`, no `@media` of
its own — the gates in the templ decide what shows), and gives its
overflowing part (a list, a table, a chart) `overflow: auto` with
`min-block-size: 0`: the title on a hairline with its verbs at the right,
the content under it, no card; spaced in lh (the unit that moves with
`--type`), never em. It is iterated as it is built — the block and its
file together, on the bench — rather than designed from a principles
page (Mike, 2026-10-10):

    @layer block {
      :where(blk-orders) {
        display: flex; flex-direction: column; gap: 0.25lh; …   /* its box */
        & > :where(header) { … }                                 /* parts, by element */
        & > :where(div) { flex: 1 1 auto; min-block-size: 0; overflow: auto; }   /* the part that may run long */
        &:where([data-ui-state~="armed"]) { … }                  /* states, ~= tokens */
      }
    }

- Parts are semantic elements (header h3 small strong figure ul li time
  mark progress footer …); a part class (.ring .dot .av) means something
  only inside its block.
- A part that must go on a phone wears a VIEWPORT gate (`.tablet
  .desktop`) or a container gate (`.c-tablet .c-desktop`) in the templ;
  a block asks its own width in ch only when the person says a part
  must go — never lh, px or an aspect.
- Knobs for colour and type, inline only where a value is DATA (an
  avatar's hue); helpers only from the closed utility list; state as
  `data-ui-state="a b"` tokens matched `~=`, after native and ARIA
  state (disabled, aria-pressed, :open); nothing reaches outside the tag.
- A block COMPOSES other blocks by giving each a `.cell` of its own in a
  definite track (never an auto one — containment collapses it).
- FEWEST LINES: the engine's defaults first; a block rule restates
  nothing the family (`_lined.css`) or the base already says; a repeated
  fragment is one rule in a shared `_file.css`; a rule that exists to
  cancel another rule is a bug.
- A block is written FOR THE BENCH FIRST: the product's Layout bench
  (`/admin/layout`) puts one block in ONE region the person resizes;
  it is looked at wide and narrow before a page wears it.

UNITS AND READABILITY. Space in `lh`, width in `ch`, never `px`. A
layout switch asks "how many characters fit here at the type this person
reads", so it is a CONTAINER query in `ch` — in `@container`, `ch`
follows the container's font and so the person's scale; in `@media` it
resolves against the browser's initial font and ignores it. Media
queries stay for the device's own facts: pointer, print, hover. (The
engine's gate thresholds are still px and rem — a change pending its own
version.)

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
`.nowrap`, `.truncate`, `.grow`, `.fill`, `.far` (pushed to the far end of its row), `.center`, `.vr` (an hr stood
on end), `section.owns-scroll` (the component-scrolled section every
full-height roster is built on). `--gap` takes ONLY the ladder's rungs:
block `0 · 0.25lh · 0.5lh · 1lh`, inline `0.25em · 0.5em · 1em`. THE
CONTENT LADDER: `.content-1` (a column, 40ch) · `.content-2` (reading,
70ch) · `.content-3` (working, 100ch), in the wearer's own ch; rosters
take no rung. A width written as a length is a regression.

THE GATES' LINES (the families are the contract's, above): viewport
576px / 768px, `.ultrawide` 1920px and up at an aspect of 2:1 or wider;
the tiers `< 8rem` · `8–20rem` · `≥ 20rem` on the nearest container
("and-up" is the multi-class idiom `class="medium large"`). A gate goes
on a wrapper that also carries a layout primitive — revert-layer
restores the primitive's display, not a default.

Focus mode is a stored pref (`data-ui-state="focus"` on `.page`). Print
strips every region but pg-main*, surfaces to white, ink to black.

## COMPONENTS (styled semantics + a few words)

`.card` (lifted panel; `.Card` the voiced edge), `.surface` (a lift step
with no line), `.tag` (pill; pair a hue helper), `.avatar`, `.crumbs`
(a crumb `<a>` is a bare link), `.tree`, `.tabs` / `.tabs-underline`,
`.button-group` (a member is a button with aria-pressed OR `<label
class="btn"><input type="radio"> word</label>` — the dot hidden, the
checked member pressed, v3.1.17; `.tabs` hides its radios the same way,
no `.vh`), `.range-pair` (two ranges on ONE track — a low and a high
thumb, the band between them painted from `--lo`/`--hi` percents the page
stamps; the page keeps the low below the high, v3.2.6), `.nav-item`/`.nav-icon`, `.drawer` (+ .left/.right/
.top/.bottom, `.glass`), `.modal` (a `.content-*` rung; `.content-1` the confirm,
`.content-3` the workbench), `.menu` (popover), `.search-box`, `.icon`
(THE icon-only square — explicit, aria-label required), `.roster` (THE
SERVER-DRIVEN TABLE: truncating cells, the hugging column model, tonal
head, `.scroll-x` — the roster's horizontal scroller fades its edges; a table inside any scroller is transparent so the fade shows, v3.2.1), `.glass` (the surface at `--glass-alpha` over a
`--glass-blur`; 0.65 a dialog, 0.88 an overlay that must read over
anything), `.veil` (a glass card over its `.stack` sibling), `.hud`
(viewport overlay slots t/c/b × l/c/r), `.wash`, `.stress` (the lab's
resize handle, both axes), `.county-map`.

THE DOCK (v3.1.8, after iOS Calendar's bar): a hud whose `.bl` and
`.br` slots are `.glass` — a glass corner slot is a PILL (margin,
padding, full radius, the quiet edge) holding hud fabs, bare glyphs at
rest; the hud wearing `data-ui-state="away"` slides its bottom slots
down past the edge (a translate), and a `.cr` fab is the handle that
stays. The dock takes no clearance: the canvas runs under the pills,
the handle is the relief; only the toast pile clears it while it is on
screen (v3.1.9).

Dialogs are native `<dialog class="modal">` at a rung of the content
ladder, opened in HTML — `commandfor="<id>" command="show-modal"` — and
closed by their head's × (EventOS `dialogHead`: it closes a modal or a
popover alike) or a bare `command="close"`; `closedby="any"` and
`data-preserve-attr="open"` are MANDATORY on a live page (a morph would
close it; EventOS `view/dialog_test.go` refuses a dialog without them, a
`.sm`/`.lg` word, or a dialog nested in a form). A verb that posts then
closes has ONE spelling, `dialogPost(url, form, then…)` — the post, then
on success the dialog closes; a refusal that answers an error keeps it
open with what was typed. The foot is `dialogFoot`: Cancel left (a native
reset), the verb right. `.modal.anchored` sits by `position-area` off its
opener. Menus are `popover` + `popovertarget`; a closed `.menu` must be
`display:none`.
Anatomy glyphs are DECLARED boxes (`width="24" height="24"`); `.icon`
self-centres. Know what a word IS before composing it: `.sec` is a
BUTTON voice — on a wrapper it paints a ghost box.

THE FORM CANON (restored 2026-10-20 — the text gf-610 dropped):

- ANATOMY: `<fieldset>` owns the row; `<label>` owns the field as
  `span` (the word) → `small` (THE STATE SLOT) → the control, in that
  order, and the engine lays them on a grid: the word and the state on
  line one, the control full width under. The `small` is ALWAYS present,
  empty when there is nothing to say (`<small></small>` reserves the
  line, so a message never shifts the form), and it carries STATE —
  "saved ✓", "needed", the error — never a caption. A checkbox or radio
  label is `input` then `span`, its small under the span.
- A FIELDSET IS ONE ROW: its children share it by `--row-width`, a bare
  number on each child (`style="--row-width: 3"` beside a 1 — a 3:1
  split); it does nothing outside a fieldset. A row with one child is a
  column. `<legend>` names the group; its `small` is the GROUP's state.
- EVERYTHING FILLS THE WIDTH; a button in a fieldset hugs its word.
  `required` draws the asterisk — never typed. `[role="form"]` is the
  formless spelling (a card of controls that posts per change).
- THE STATE GRAMMAR, the engine's: `aria-invalid="true"` on the control
  lights the small and rims the field red — the server renders it (the
  problem judged at render, the message in the small) or a signal
  patches it as the person types (`data-attr:aria-invalid` +
  `data-text` on the small, the profile form's loop). A tone on the
  LABEL (`label.wrn`, `.suc`, `.inf`, `.dgr`) lights its small and rims
  its control in that tone; a tone on the FIELDSET lights the legend's
  small. A class on the small itself does nothing — the slot's ink is
  neutral by design. There is no native-validity hook (`:user-invalid`
  styles nothing): the browser's bubble is never the message.
- A REFUSAL ABOUT A FIELD goes to that field's small, not a toast; a
  refusal about nothing in particular is the toast.
- THE LOCKED FORM: `form[data-ui-state="locked"]` + `readonly` on the
  fields — chrome stands down, the action row collapses; the pencil
  unlocks. THE ACTION ROW is `.spread`, Cancel left (a native reset —
  the fields fall back to their stored values, no seed strings), the
  verb right. Datastar submits (`data-on:submit__prevent="@post(…,
  {contentType: 'form'})"`), handlers answer 204 and the morph re-lands.
- THE EDIT CARD (EventOS `editCard`) is the one record-form shape: h3 +
  pencil unlocks, Cancel a native reset, Save posts. The lab's Forms
  page is the practice bench; every specimen there is the canon.

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
the shared helpers — `foLabel`, `foLine`, `hueShift`/`hueStyle`, `ff2`, `scEsc`,
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

LABELS NEVER COLLIDE (EventOS, 2026-10-19: a long product name wrapped
inside a 16-unit foreignObject and printed over the next row). A label's
box is the space it OWNS, never a guess: a row label owns its row's
height, a column label its column's width (`step`, not a constant), a
value label the gap to the next mark. A label that must stay on one line
goes through `foLine` (one line, `.truncate`, the whole text in its
title); `foLabel` is for short words a builder controls (ticks, figures);
`foWrapLabel` only where its box has the height for two lines. Size the
label margin from the data (the longest label, capped — `dotPlotSVG`
reserves up to two fifths of the width), never a fixed 130. Before a
builder ships, feed it the longest real label and twenty points and READ
the PNG; a chart fed by a model or a person gets labels nobody chose.

THE TUFTE RULES (The Visual Display of Quantitative Information — the
Ask agent's direction carries the same words): above all show the data;
maximise the data-ink, erase what carries none (no frames, no 3-D, no
fills behind text, no legend a direct label can replace); a chart earns
its place only when it shows more than a sentence can — two or three
numbers go in the sentence or a small table; the title states the
finding ("Ultra sold the most, $3.39K"), not the axis; label the marks
directly; several measures of the same items are SMALL MULTIPLES (the
same labels, the same order, side by side), never one crowded chart;
integrate words and graphics — the prose says what the chart means, it
never re-reads the chart's numbers.

LIVE CHARTS (the Ask beta): a model-written SVG with Datastar attributes
is UNTRUSTED CODE. It never runs in the page's document: `view.LiveFrame`
puts it in an iframe `sandbox="allow-scripts"` (no same-origin: no
cookie, no session, no post as the person) with a CSP of no connect, form
or frame source; the engine and the runtime load inside (the static
handler answers `Origin: null` for `datastar.js` alone). Inside, the same
ink ladder and `foreignObject` text apply; motion is CSS transitions on
transform and opacity driven by signals, under a second.

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

PRINT (the media layer, v3.1.2): the sheet is letter with half-inch
margins; `.page` prints as a block, the main runs auto-high, and a main's
`section.cell` gets the sheet's height less the head — a size container
under a block page has no height and printed nothing (EventOS gf-687).
Every region but pg-main* is stripped — the subheader (the tabs) with
them — and PAPER TAKES NO ACTION (v3.1.3): no button, popover, crumb
trail, tab or fab prints; surfaces go white, ink black.
