import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")

with app.setup:
    from pathlib import Path


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # CSS System
    # Layers

    The toolbox CSS uses cascade layers to make every rule's role explicit. The order is fixed; the meaning of each layer is fixed; deciding where a new rule goes should be a 10-second decision.

    ```
    @layer
        reset.fix,
        reset.opinion,
        core.color,
        core.type,
        core.space,
        theme,
        layout.app,
        layout.doc,
        layout.composition,
        component.base,
        component.simple,
        component.complex,
        utility.layout,
        utility.exceptions,
        utility.important;
    ```

    Read top to bottom. Every layer assumes the ones above it have already happened.

    ---

    ## reset.fix

    Browser bug fixes and ancient-CSS workarounds. Things that are objectively wrong defaults — `box-sizing`, default margins, baseline-aligned images, table isolation. If a rule could be defended as "this is what the spec should have done," it goes here.

    **Belongs:** universal selectors, baseline element fixes, `:where(html)` font-smoothing.
    **Doesn't belong:** anything that reflects taste. If two reasonable people would disagree, it's `reset.opinion`.

    ## reset.opinion

    Project-level structural preferences applied across all elements. Still resets, but driven by taste, not by spec correctness — `text-wrap: balance` on headings, scrollbar-width, link `text-decoration: none`. Think of these as "the structural defaults I want every project to inherit."

    Rules in this layer **must not consume custom properties from the core system** (`--_bg`, `--s`, `--type`, etc.). It's structural baseline only — properties like `text-wrap`, `cursor`, `box-sizing`, `overflow-wrap`. Anything that needs `--_bg` or computes against `--s` goes in `theme` (visual) or `component.base` (per-element typography).

    **Belongs:** structural baseline rules using `:where(...)` for zero specificity.
    **Doesn't belong:** anything that consumes a core token. Anything that requires a class (that's `component.*` or `utility.*`).

    ## core.color

    The color formula. One layer, one job: take a small set of inputs (`--bg`, `--hue`, `--depth`, `--fg-contrast`, etc.) and compute one output (`--_bg`, plus `color`, `--border`, `--Border`). Every other layer consumes those outputs.

    Also includes the rules that resolve `--_bg` into actual paint — the `:where(*) { background-color: ... }` rule, the `.surface` cascade, and the SVG color-bridge rules that translate the same outputs to `fill`/`stroke`.

    **Belongs:** color math, `--_bg` painting, surface depth tracking, SVG color bridging.
    **Doesn't belong:** semantic hue presets (`.suc`/`.inf`) — those are theme decisions about *which* hue means success, not how the math works. Theme blocks (`@media prefers-color-scheme`, `[data-ui-theme="dark"]`) — those are also theme.

    ## core.type

    The fluid-type formula. `--cfg-type-min`, `--cfg-type-max`, `--cfg-fluid-min-vp`, `--cfg-fluid-max-vp`, plus the `:where(*)` rule that interpolates `font-size` against viewport width. The `--type` step variable composes through `pow()` against the configured ratio.

    **Belongs:** the type formula, type config tokens, line-height and letter-spacing derived from `--type`.
    **Doesn't belong:** font-family declarations (those are `theme`), per-element type sizing (that's `component.base` for default elements, or per-component for everything else).

    ## core.space

    [removed]

    ## theme

    Project-level visual decisions. This is where the "vibe" of the page lives — anything you'd change to give the whole project a different mood without touching component logic.

    Concretely:
    - **Theme blocks**: `@media (prefers-color-scheme)`, `[data-ui-theme="light"]`, `[data-ui-theme="dark"]` — the values for `--cfg-color-top-l` etc. that make light/dark possible.
    - **Semantic hue presets**: `.suc`, `.inf`, `.wrn`, `.dgr` — fixed-hue overrides for success/info/warning/danger contexts.
    - **State classes**: `.hover`, `.active`, `.disabled` — color-formula nudges (`--l-shift`, `--c-shift`, `--fg-contrast` adjustments) that the pointer-events script applies. These look like component logic, but they're not — they're pure visual deltas to the existing color math, applied uniformly across every component. Lives here because (a) the math is theme-level, and (b) consistent state appearance across components is a theme concern.
    - **Visual decoration helpers**: `.shadow`, `.glow` — drop-shadow filters that respond to the current `--_bg`.
    - **Density/motion presets**: `[data-ui-size="sm/md/lg"]`, `[data-ui-motion="off/on"]`, `[data-ui-space="sm/md/lg"]`.
    - **Font family declarations**: `--font-heading`, `--font-body`, `--font-mono`, `--font-kbd`.
    - **Selection and focus visuals**: `::selection`, `:focus-visible` — the styling, not the JS.

    **Belongs:** vibe. If swapping it changes how the page *feels* without changing what it *does*, it's theme.
    **Doesn't belong:** color math (that's `core.color`). Layout decisions (`layout.*`). Per-component visual choices (those live with the component).

    ## layout.app

    The application shell layout. A 3×3 grid (header / nav · main · aside / footer) with drawer-style nav and aside that collapse to fixed-position modal drawers below a container-query breakpoint. Opt-in via `<body class="app">`.

    **Belongs:** the app-shell grid template, drawer behavior, container-query breakpoint logic.
    **Doesn't belong:** anything that assumes a different page shape — that's `layout.doc`. Composition primitives (`layout.composition`). Components that live *inside* a slot.

    ## layout.doc

    [removed may add back at some point]
    The document/paper layout. Used when the consumer wants a fixed-aspect "piece of paper" centered on a backdrop, with print awareness. Opt-in via `<body class="doc">` or applied directly via a `.paper` class on a child article. Sets up the backdrop, the paper's aspect-ratio container, the print `@page` rules.

    **Belongs:** paper sizing math, backdrop centering, print media rules for fixed-page documents.
    **Doesn't belong:** the paper's *contents* — that's per-document `me {}`. App-shell behavior (`layout.app`).

    ## layout.composition

    Stateless layout primitives that compose with anything. `.stack`, `.row`, `.split`, `.cluster`, `.grid`, `.flank`, `.flank-end`, `.span`. Plus a few small positioning helpers like `.fab-row` (fixed bottom-right action row) and the directional grid-overlap classes (`.↖`, `.↗`, etc.).

    **Belongs:** classes that arrange children with no opinion about what the children are.
    **Doesn't belong:** classes that style their children. Classes that assume a specific page structure (those are `layout.app/doc`).

    ## component.base

    Default-element styling. `h1`–`h6`, `p`, `small`, `code`, `pre`, `figcaption`, `blockquote`, `address`, `cite`, `mark`, `hr`.

    These rules apply via tag selectors (`h1 { ... }`) so consumers get reasonable typography by default without classes. Each rule sets `--type`, `--contrast`, `font-family` — the formula does the rest.

    **Belongs:** styling for unclassed HTML elements.
    **Doesn't belong:** anything requiring a class. Class-based versions of the same idea (`.badge`, `.tag`) are `component.simple`.

    ## component.simple

    Generic, reusable components keyed by class. `.btn`, `.tag`, `.card`, `.popover`, etc. Each composes with the color/type/space systems and works in any context.

    A component qualifies as "simple" if (a) it's small (one or two visual units), (b) it's general enough that the same class makes sense in any project, and (c) it doesn't assume a particular surrounding structure.

    **Belongs:** generic components.
    **Doesn't belong:** anything project-specific. If the class name has a domain noun in it (`.timeline`, `.xp`, `.aside`, `.invoice`), it's not simple — it's app code, and it lives with the app as a `me {}` block.

    ## component.complex

    Complex generic components — modal dialogs, calendars, data tables. Same purity rule as `component.simple`: project-specific things don't belong here.

    This layer should usually be small. Most things that feel "complex" turn out to be either (a) a `component.simple` doing too much and needing decomposition, or (b) app code that belongs in a `me {}` block.

    **Belongs:** generic complex components.
    **Doesn't belong:** see `component.simple`.

    ## utility.layout

    Display-context utilities. `.mobile`, `.tablet`, `.desktop` for responsive show/hide. `.nowrap`, `.truncate`. `@media print { ... }` rules that adjust general behavior for print.

    **Belongs:** small classes that flip layout-related properties.
    **Doesn't belong:** anything visual or behavioral beyond layout.

    ## utility.exceptions

    Reserved for cases where a rule must override the cascade in a way that doesn't fit elsewhere. `.vh` (visually hidden) lives here.

    **Belongs:** rare exceptions.
    **Doesn't belong:** anything you can put in another layer.

    ## utility.important

    Rules that use `!important` to override inline styles or other cases where the cascade legitimately can't reach. `[hidden] { display: none !important }`, `@media print { .np { display: none !important } }`.

    In practice this layer should be very small — often empty. It exists so that *when* you do need `!important`, there's a defined place for it instead of scattering high-priority rules through the rest of the system.

    **Belongs:** rules that legitimately need `!important` for cascade reasons.
    **Doesn't belong:** anything that could work without `!important`. If you reach for this layer, ask why first.

    ---

    ## Decision rules

    When adding a new rule, ask in order:

    1. **Is it stylistically opinionated?** No → `reset.fix`. Yes → continue.
    2. **Is it a structural baseline that doesn't consume any core tokens?** Structural and token-free → `reset.opinion`. Anything that reads `--_bg`, `--s`, `--type`, etc. is not a reset — it's `theme` (project-wide visual) or `component.base` (per-element typography). Continue.
    3. **Is it color/type/space math?** Yes → the matching `core.*` layer. No → continue.
    4. **Is it a project-wide visual decision?** Yes → `theme`. No → continue.
    5. **Does it shape the page layout?** Yes → `layout.app` (drawer shell), `layout.doc` (paper), or `layout.composition` (primitives). No → continue.
    6. **Is it a default-element rule?** Yes → `component.base`. No → continue.
    7. **Is it a class-keyed component?** Yes — and is it generic? Yes → `component.simple` or `.complex`. No → it's app code, write a `me {}` block.
    8. **Is it a small layout flag?** Yes → `utility.layout`.
    9. **Does it genuinely fit nowhere else but is still legitimate?** `utility.exceptions`. This layer is intentionally a buffer — expected to be empty in practice, kept declared so the scaffold is in place for the rare case you need it.
    10. **Does it need `!important`?** Yes → `utility.important`. Otherwise → reconsider — most rules don't need this layer.

    If a rule doesn't fit any layer, the answer is almost always "it's not generic; it should be a `me {}` block in the app code."

    ## Declarations outside layers

    Nothing should be declared outside a layer except things that the language requires to be unlayered: `@property` declarations, `@font-face`, `@import`. Everything else — every selector, every `@media`, every `@container` — goes inside a `@layer` block. This is what makes the cascade predictable; rules outside layers always win, which silently breaks the whole order.

    ## What does *not* belong in any layer

    App-specific components. Anything with a domain noun in the class name. The resume's timeline, sidebar, role cards, header — none of these are toolbox concerns. They're app code, expressed as `me {}` blocks scoped to the elements they belong to.

    The toolbox is the substrate; the app is what you build on it. Keeping that line clean is what makes the toolbox reusable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # CSS

    ## Layer Decleration

    ```css

    @layer
      reset.fix,
      reset.opinion,
      core.color,
      core.type,
      theme,
      layout.page,
      layout.composition,
      component.base,
      component.simple,
      component.complex,
      utility.layout,
      utility.exceptions,
      utility.important;

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Property Declarations
    > later mmove to be closer to their layer (locality of behavior prefeared here)

    ```css
    /* ════════════════════════════════════════════════════════════════
       @property declarations
       These must live outside @layer (CSS spec requirement).
       ════════════════════════════════════════════════════════════ */

    /* State shift hooks — applied per-element. See @layer theme. */
    @property --l-shift { syntax: "<number>"; inherits: false; initial-value: 0 }
    @property --c-shift { syntax: "<number>"; inherits: false; initial-value: 0 }

    /* Global theme config — radius, motion. Values must be absolute. */
    @property --cfg-radius { syntax: "<length>"; inherits: true; initial-value: 6px }
    @property --cfg-motion { syntax: "<number>"; inherits: true; initial-value: 1 }



    /* Layout */
    @property --gap { syntax: "<length>"; inherits: true; initial-value: 8px }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reset

    ```css
    /* ============================================================
       reset.css — reset.fix + reset.opinion

       reset.fix: spec-correctness fixes only. No taste.
       reset.opinion: structural project-wide preferences. NO core
                      token consumption (no --_bg, --s, --type).
                      Visual rules that consume tokens go to theme.
       ============================================================ */

    @layer reset.fix {
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            background-repeat: no-repeat;
        }

        :root {
            interpolate-size: allow-keywords;
        }

        /* No color-scheme here. Theme is decided by [data-ui-theme]
           and the prefers-color-scheme media query inside core.color.
           Setting color-scheme at html level would let the browser
           independently style native UI (scrollbars, form controls)
           and fight our explicit theme attribute.

           No line-height default. core.type computes per-element
           line-height from --type; setting one here would conflict
           with that formula. */
        :where(html) {
            -moz-text-size-adjust: none;
            -webkit-text-size-adjust: none;
            text-size-adjust: none;
        }

        :where(body, figure, blockquote, dl, dd, p) {
            margin-block-end: 0;
        }

        :where(img, picture, svg) {
            max-width: 100%;
            display: block;
            height: auto;
        }

        :where(table, thead, tbody, tfoot, tr) {
            isolation: isolate;
        }

        :where(input, button, textarea, select) {
            font: inherit;
        }
    }

    @layer reset.opinion {
        :where(body) {
            overflow-wrap: break-word;
        }

        :where(html) {
            scrollbar-width: thin;
        }

        :where(p) {
            text-wrap: pretty;
        }

        :where(h1, h2, h3, h4, h5, h6) {
            text-wrap: balance;
        }

        :where(img, picture, video, canvas, svg) {
            height: auto;
        }

        :where(svg) {
            color: currentColor;
        }

        :where(button, [role="button"], summary, label[for],
               input[type="file"]::file-selector-button) {
            cursor: pointer;
            user-select: none;
            -webkit-user-select: none;
        }

        :where(:disabled, [aria-disabled="true"]) {
            cursor: not-allowed;
        }

        :where(table) {
            border-collapse: collapse;
        }

        :where(fieldset) {
            border: 0;
            padding: 0;
            margin: 0;
            min-inline-size: 0;
        }

        :where(legend) {
            padding: 0;
        }

        :where(textarea) {
            resize: vertical;
        }

        :where(textarea:not([rows])) {
            min-block-size: 10em;
        }

        :where(abbr[title]) {
            cursor: help;
            text-decoration: underline dotted;
        }

        :where(summary) {
            list-style: none;
        }

        :where(a) {
            text-decoration: none;
        }

        /* The :autofill rule that previously lived here consumed --_bg,
           which violates reset.opinion's "no core tokens" rule.
           Moved to theme.css. */

        :where(ul, ol):where([role="list"]) {
            list-style: none;
            padding: 0;
        }


    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## core.color

    ```css
    /* ════════════════════════════════════════════════════════════════
       stick.css v3 — color formula (stage-anchored)

       Public API (5 tokens):
         --bg          [0, 1]   surface (0) → loud (1)
         --fg          [-1, 1]  neutral ink (-1) → 0 → chromatic ink (1)
         --hue         [0, 360] base hue
         --hue-shift   delta added to --hue (semantic palettes, charts)
         --hue-lock    overrides hue+shift when set (branded content)

       Configuration: 19 cfg-* tokens for theme tuning.
       Curves and floor are hardcoded system constants.
       ════════════════════════════════════════════════════════════ */

    /* ── Public API ─────────────────────────────────────────────── */
    @property --bg         { syntax: "<number>"; inherits: true; initial-value: 0 }
    @property --fg         { syntax: "<number>"; inherits: true; initial-value: -1 }
    @property --hue        { syntax: "<number>"; inherits: true; initial-value: 220 }
    @property --hue-lock   { syntax: "*";        inherits: true }
    @property --hue-shift  { syntax: "<number>"; inherits: true; initial-value: 0 }

    /* ── Configuration: theme switch ────────────────────────────── */
    @property --cfg-dark { syntax: "<number>"; inherits: true; initial-value: 0 }

    /* ── Configuration: chroma ramp endpoints ───────────────────── */
    @property --cfg-color-loud-l-light  { syntax: "<percentage>"; inherits: true; initial-value: 50% }
    @property --cfg-color-loud-c-light  { syntax: "<number>";     inherits: true; initial-value: 0.22 }
    @property --cfg-color-loud-l-dark   { syntax: "<percentage>"; inherits: true; initial-value: 70% }
    @property --cfg-color-loud-c-dark   { syntax: "<number>";     inherits: true; initial-value: 0.22 }
    @property --cfg-color-surf-chroma   { syntax: "<number>";     inherits: true; initial-value: 0.018 }
    @property --cfg-fg-tint             { syntax: "<number>";     inherits: true; initial-value: 0.02 }
    @property --cfg-color-alpha         { syntax: "<number>";     inherits: true; initial-value: 1 }

    /* ── Configuration: stage ramp ──────────────────────────────── */
    @property --cfg-surf-top-light   { syntax: "<number>"; inherits: true; initial-value: 97 }
    @property --cfg-surf-bot-light   { syntax: "<number>"; inherits: true; initial-value: 90 }
    @property --cfg-surf-top-dark    { syntax: "<number>"; inherits: true; initial-value: 28 }
    @property --cfg-surf-bot-dark    { syntax: "<number>"; inherits: true; initial-value: 10 }

    /* ── Configuration: contrast flip ───────────────────────────── */
    @property --cfg-fg-flip { syntax: "<number>"; inherits: true; initial-value: 0.55 }

    /* ── Configuration: interaction states ──────────────────────── */
    @property --cfg-hover-bg-shift  { syntax: "<number>"; inherits: true; initial-value: 0.12 }
    @property --cfg-active-bg-shift { syntax: "<number>"; inherits: true; initial-value: -0.06 }
    @property --cfg-active-fg-mul   { syntax: "<number>"; inherits: true; initial-value: 0.7 }

    /* ── Structural ─────────────────────────────────────────────── */
    @property --depth { syntax: "<number>"; inherits: false; initial-value: 0 }

    /* ── Private intermediates ──────────────────────────────────── */
    @property --_bg              { syntax: "<color>";      inherits: true;  initial-value: oklch(97% 0.018 220) }
    @property --_h               { syntax: "<number>";     inherits: false; initial-value: 220 }
    @property --_surf-top        { syntax: "<number>";     inherits: false; initial-value: 97 }
    @property --_surf-bot        { syntax: "<number>";     inherits: false; initial-value: 90 }
    @property --_t-stage         { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_surf-l          { syntax: "<percentage>"; inherits: true;  initial-value: 97% }
    @property --_bg-clamped      { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_bg-chromatic    { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_bg-effective    { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_bg-curved       { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_floor           { syntax: "<number>";     inherits: false; initial-value: 0.08 }
    @property --_l               { syntax: "<percentage>"; inherits: false; initial-value: 97% }
    @property --_c               { syntax: "<number>";     inherits: false; initial-value: 0.018 }
    @property --_loud-l          { syntax: "<percentage>"; inherits: false; initial-value: 50% }
    @property --_loud-c          { syntax: "<number>";     inherits: false; initial-value: 0.22 }
    @property --_fg-pos          { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-neg          { syntax: "<number>";     inherits: false; initial-value: 1 }
    @property --_fg-pos-curved   { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-onpos        { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-pole         { syntax: "<percentage>"; inherits: false; initial-value: 4% }
    @property --_fg-ramp-l       { syntax: "<percentage>"; inherits: false; initial-value: 90% }
    @property --_fg-ramp-c       { syntax: "<number>";     inherits: false; initial-value: 0.05 }
    @property --_fg-l            { syntax: "<percentage>"; inherits: false; initial-value: 4% }
    @property --_fg-c            { syntax: "<number>";     inherits: false; initial-value: 0.02 }
    @property --_surf-dark       { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_flip-threshold  { syntax: "<percentage>"; inherits: false; initial-value: 55% }
    @property --_chroma-present  { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_interact-bg     { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_interact-fg-mul { syntax: "<number>";     inherits: false; initial-value: 1 }
    @property --_fg-effective    { syntax: "<number>";     inherits: false; initial-value: -1 }

    @layer core.color {

      :where(*) {
        /* Hue resolution — lock overrides shift+base */
        --_h: var(--hue-lock, calc(var(--hue) + var(--hue-shift)));

        /* Theme-aware loud endpoint */
        --_loud-l: calc(var(--cfg-color-loud-l-light) * (1 - var(--cfg-dark)) + var(--cfg-color-loud-l-dark) * var(--cfg-dark));
        --_loud-c: calc(var(--cfg-color-loud-c-light) * (1 - var(--cfg-dark)) + var(--cfg-color-loud-c-dark) * var(--cfg-dark));

        /* Theme-aware floor: light needs a tiny floor (0.05) so low --bg
           cells have a visible chromatic step. Dark needs more (0.22)
           because perceptual L deltas in dark range require larger jumps. */
        --_floor: calc(0.05 * (1 - var(--cfg-dark)) + 0.22 * var(--cfg-dark));

        /* Chroma ramp pipeline (stage-anchored, [0, 1]).
           Interaction perturbs --bg directly; L/C lifts emerge from ramp. */
        --_bg-clamped:   clamp(0, calc(var(--bg) + var(--_interact-bg)), 1);
        --_bg-chromatic: clamp(0, calc(var(--_bg-clamped) * 1000000), 1);
        --_bg-effective: calc((var(--_floor) + (1 - var(--_floor)) * var(--_bg-clamped)) * var(--_bg-chromatic));
        --_bg-curved:    pow(var(--_bg-effective), 1.5);

        /* Final L/C: lerp from inherited stage to theme loud endpoint */
        --_l: calc(var(--_surf-l) * (1 - var(--_bg-curved)) + var(--_loud-l) * var(--_bg-curved));
        --_c: calc(var(--cfg-color-surf-chroma) * (1 - var(--_bg-curved)) + var(--_loud-c) * var(--_bg-curved));

        --_bg: oklch(clamp(4%, var(--_l), 97%) var(--_c) var(--_h) / var(--cfg-color-alpha));

        /* Foreground: --fg < 0 → neutral ink, --fg > 0 → chromatic ink */
        --_fg-effective: calc(var(--fg) * var(--_interact-fg-mul));
        --_fg-pos: clamp(0, var(--_fg-effective), 1);
        --_fg-neg: clamp(0, calc(-1 * var(--_fg-effective)), 1);

        /* Contrast pole flip — chroma-biased so high-chroma cells flip earlier */
        --_chroma-present: clamp(0, calc(var(--_c) * 30), 1);
        --_flip-threshold: calc(
          var(--cfg-fg-flip) * 100%
          + var(--_chroma-present) * 3%
          + var(--_c) * 60%
        );
        --_surf-dark: clamp(0, calc((var(--_flip-threshold) - var(--_l)) / 1% * 20), 1);
        --_fg-pole: calc(4% * (1 - var(--_surf-dark)) + 97% * var(--_surf-dark));

        /* Chromatic-ink ramp (positive --fg side) — same shape as bg */
        --_fg-pos-curved: pow(var(--_fg-pos), 1.5);
        --_fg-ramp-l: calc(var(--_surf-l) + var(--_fg-pos-curved) * (var(--_loud-l) - var(--_surf-l)));
        --_fg-ramp-c: calc(var(--cfg-color-surf-chroma) + var(--_fg-pos-curved) * (var(--_loud-c) - var(--cfg-color-surf-chroma)));
        --_fg-onpos: clamp(0, calc(var(--_fg-pos) * 1000000), 1);

        /* Merge neutral and chromatic fg branches via step function */
        --_fg-l: calc(
          (clamp(4%, var(--_l), 97%) * (1 - var(--_fg-neg)) + var(--_fg-pole) * var(--_fg-neg)) * (1 - var(--_fg-onpos))
          + var(--_fg-ramp-l) * var(--_fg-onpos)
        );
        --_fg-c: calc(
          (var(--_c) * (1 - var(--_fg-neg)) + var(--cfg-fg-tint) * var(--_fg-neg)) * (1 - var(--_fg-onpos))
          + var(--_fg-ramp-c) * var(--_fg-onpos)
        );

        color: oklch(clamp(4%, var(--_fg-l), 97%) var(--_fg-c) var(--_h) / 1);

        /* Border tokens derived from current bg */
        --border: oklch(
          from var(--_bg)
          calc(l + (var(--cfg-dark) * 2 - 1) * 0.14)
          calc(c * 0.3)
          h
        );
        --Border: oklch(
          from var(--_bg)
          calc(l + (var(--cfg-dark) * 2 - 1) * 0.22)
          clamp(0.08, calc(c + 0.12), 0.18)
          calc(h + 8)
        );
      }


      /* Stage ramp — only stages compute --_surf-l. Descendants
         inherit, so chips/text/buttons anchor their chroma ramp to
         whatever stage they're sitting in. */
      :where(body, .stage, .stage-0, .stage-1, .stage-2, .stage-3) {
        --_surf-top: calc(var(--cfg-surf-top-light) * (1 - var(--cfg-dark)) + var(--cfg-surf-top-dark) * var(--cfg-dark));
        --_surf-bot: calc(var(--cfg-surf-bot-light) * (1 - var(--cfg-dark)) + var(--cfg-surf-bot-dark) * var(--cfg-dark));
        --_t-stage:  clamp(0, calc(var(--depth) / 3), 1);
        --_surf-l:   calc((var(--_surf-top) + var(--_t-stage) * (var(--_surf-bot) - var(--_surf-top))) * 1%);
      }


      :where(svg) { color: currentColor }

      /* Interaction states — hover/active perturb --bg directly, sliding
         the element along the stage→loud axis. L and C lifts emerge
         automatically from the ramp.
           .clickable  — full interactive treatment, gets pointer cursor
           .hoverable  — hover response only, no cursor, no active state */
      :where(button, a, [role="button"], [tabindex], .clickable):not([tabindex="-1"]) {
        cursor: pointer;
      }
      :where(button, a, [role="button"], [tabindex], .clickable):not([tabindex="-1"]):hover {
        --_interact-bg: var(--cfg-hover-bg-shift);
      }
      :where(button, a, [role="button"], [tabindex], .clickable):not([tabindex="-1"]):active {
        --_interact-bg: var(--cfg-active-bg-shift);
        --_interact-fg-mul: var(--cfg-active-fg-mul);
      }
      :where(.hoverable):hover {
        --_interact-bg: var(--cfg-hover-bg-shift);
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## core.color stages

    ```css
    @layer core.color {
      /* Stage cascade — bare .stage infers depth from nesting.
         Variants stay outside this cascade. */
      .stage                                  { --depth: 0 }
      .stage:has(.stage)                      { --depth: 1 }
      .stage:has(.stage .stage)               { --depth: 2 }
      .stage:has(.stage .stage .stage)        { --depth: 3 }

      /* Explicit stage variants — pin a stage to a specific depth. */
      .stage-0 { --depth: 0 }
      .stage-1 { --depth: 1 }
      .stage-2 { --depth: 2 }
      .stage-3 { --depth: 3 }

      /* Paint — stages always paint their bg. */
      :where(*) { background-color: oklch(from var(--_bg) l c h / var(--_bg-chromatic)) }
      :where(body, .stage, .stage-0, .stage-1, .stage-2, .stage-3) {
        background-color: var(--_bg);
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## core.type

    ```css
    /* ════════════════════════════════════════════════════════════════
       Type + scale — the unified scale formula

       Public API (2 tokens):
         --type    local scale step (non-inheriting)
                     integer steps; -2 = small, 0 = body, +2 = display
         --scale   regional multiplier (inheriting)
                     1 = default; set on a region to rescale everything

       All spacing — component em-padding, lh-based component sizing,
       layout primitive gaps — derives from these two knobs through
       font-size and line-height.

       Configuration:
         --cfg-type-min        body size at narrow viewport
         --cfg-type-max        body size at wide viewport
         --cfg-type-min-ratio  scale step ratio at narrow viewport
         --cfg-type-max-ratio  scale step ratio at wide viewport
         --cfg-fluid-min-vp    viewport bounds for fluid interpolation
         --cfg-fluid-max-vp
       ════════════════════════════════════════════════════════════ */

    @property --cfg-fluid-min-vp    { syntax: "<length>"; inherits: true; initial-value: 320px }
    @property --cfg-fluid-max-vp    { syntax: "<length>"; inherits: true; initial-value: 1280px }
    @property --cfg-type-min-ratio  { syntax: "<number>"; inherits: true; initial-value: 1.2 }
    @property --cfg-type-max-ratio  { syntax: "<number>"; inherits: true; initial-value: 1.28 }
    @property --scale               { syntax: "<number>"; inherits: true; initial-value: 1 }
    @property --type                { syntax: "<number>"; inherits: false; initial-value: 0 }

    @layer core.type {
      :root {
        --cfg-type-min: 0.8rem;
        --cfg-type-max: 1rem;
      }

      :where(*) {
        /* Step sizes at each viewport endpoint — ratio^type from base */
        --_t-min: calc(var(--cfg-type-min) * pow(var(--cfg-type-min-ratio), var(--type)));
        --_t-max: calc(var(--cfg-type-max) * pow(var(--cfg-type-max-ratio), var(--type)));

        /* Fluid interpolation between the two endpoints, then regional scale */
        font-size: calc(
          clamp(
            var(--_t-min),
            calc(
              var(--_t-min)
              + (var(--_t-max) - var(--_t-min))
              * (100vi - var(--cfg-fluid-min-vp))
              / (var(--cfg-fluid-max-vp) - var(--cfg-fluid-min-vp))
            ),
            var(--_t-max)
          )
          * var(--scale)
        );

        letter-spacing: clamp(-0.04em, calc(0.01em - var(--type) * 0.012em), 0.04em);
        line-height:    clamp(1.1, calc(1.5 - var(--type) * 0.075), 1.6);
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Theme

    ```css
    @property --cfg-bg-loud { syntax: "<number>"; inherits: true; initial-value: 0.55 }


    /* ════════════════════════════════════════════════════════════════
       theme — project-level visual decisions
       The "vibe" of the page. Theme blocks (light/dark), state classes
       that nudge the color formula, font families, etc.
       State classes are uniform across all components.
       ════════════════════════════════════════════════════════════ */
    @layer theme {

        :root {
          /* Identity */
          --hue: 220;
          --cfg-color-loud-l-light: 45%;
          --cfg-color-loud-c-light: 0.18;
          --cfg-color-loud-l-dark: 65%;
          --cfg-color-loud-c-dark: 0.18;
          --cfg-color-surf-chroma: 0.012;
          --cfg-fg-tint: 0.005;

          /* Surfaces — light mode warm cream, dark mode warm charcoal */
          --cfg-surf-top-light: 99;
          --cfg-surf-bot-light: 91;
          --cfg-surf-top-dark: 22;    /* was 28 — slightly darker leaf */
          --cfg-surf-bot-dark: 12;    /* was 10 — body lightens */

          /* Geometry & motion */
          --cfg-radius: 6px;
          --gap: 0.75rem;

          /* Fonts */
          --font-ui:    -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", system-ui, sans-serif;
          --font-display: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
          --font-mono:  ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        }
        body { font-family: var(--font-ui); }

        @media (prefers-color-scheme: dark) { :root:not([data-ui-theme]) { --cfg-dark: 1 } }
        [data-ui-theme="light"] { --cfg-dark: 0 }
        [data-ui-theme="dark"]  { --cfg-dark: 1 }

        .suc { --hue-lock: 145 }
        .inf { --hue-lock: 240 }
        .wrn { --hue-lock: 75  }
        .dgr { --hue-lock: 25  }
        .bw { --cfg-color-surf-chroma: 0; --cfg-color-loud-c-light: 0; --cfg-color-loud-c-dark: 0; }

        [data-ui-motion="off"]   { --cfg-motion: 0 }
        [data-ui-motion="on"]    { --cfg-motion: 1 }
        [data-ui-motion="debug"] { --cfg-motion: 10 }
        @media (prefers-reduced-motion: reduce) { :root, [data-ui-motion] { --cfg-motion: 0 } }

        body { transition: --scale calc(var(--cfg-motion) * 0.2s) ease-out; }
        [data-ui-type="sm"] { --scale: 0.875 }
        [data-ui-type="md"] { --scale: 1     }
        [data-ui-type="lg"] { --scale: 1.125 }

        * {
          scrollbar-width: thin;
          scrollbar-color: var(--Border) transparent;
        }


    /* ── Syntax highlighting — Custom Highlight API ─────────────
         The ::highlight() pseudo only honors color, background-color,
         text-decoration, text-shadow. Custom properties set on
         ::highlight() do NOT cascade into the painted text, so each
         rule sets `color` directly. Each rule reads --_bg, --_l, and
         --cfg-dark from the originating element via relative-color
         syntax — the same surface anchoring the rest of the formula
         uses, so token colors automatically follow theme switches
         and surface depth.

         Two formulas:
           --token-color   chromatic ink, pinned to a fixed L/C
                           in OKLCH so it reads against any surface;
                           hue shift varies per category.
           --comment-color dim ink, lightness pulled toward the
                           surface so comments recede; tiny chroma
                           tint via --cfg-fg-tint.

         Token L/C endpoints live here as system constants — they're
         specific to the highlight use case (must read against both
         light and dark surfaces) and aren't reused elsewhere. Adjust
         by editing these eight values. ─────────────────────────── */

      ::highlight(css-comment),
      ::highlight(html-comment),
      ::highlight(python-comment),
      ::highlight(javascript-comment) {
        /* Light-mode comment: dark ink that's been mixed toward the surface.
           Dark-mode comment: light ink mixed toward the surface.
           Result: visibly dimmer than active code, but still legible. */
        color: oklch(from var(--_bg)
          calc(
            /* light: 35% (dark ink). dark: 70% (light ink, dim). */
            (35% * (1 - var(--cfg-dark)) + 70% * var(--cfg-dark))
          )
          calc(c + var(--cfg-fg-tint))
          calc(h + 0)
        );
      }

      /* Strings — warm shift */
      ::highlight(css-string),
      ::highlight(html-value),
      ::highlight(python-string),
      ::highlight(javascript-string) {
        color: oklch(from var(--_bg)
          calc(45% * (1 - var(--cfg-dark)) + 75% * var(--cfg-dark))
          0.13
          calc(h - 36)
        );
      }

      /* Numbers / units */
      ::highlight(css-number),
      ::highlight(css-unit),
      ::highlight(python-number),
      ::highlight(javascript-number) {
        color: oklch(from var(--_bg)
          calc(45% * (1 - var(--cfg-dark)) + 75% * var(--cfg-dark))
          0.13
          calc(h - 24)
        );
      }

      /* Punctuation / operators / brackets */
      ::highlight(css-punctuation),
      ::highlight(html-bracket),
      ::highlight(python-operator),
      ::highlight(python-punctuation),
      ::highlight(javascript-operator),
      ::highlight(javascript-punctuation) {
        color: oklch(from var(--_bg)
          calc(45% * (1 - var(--cfg-dark)) + 75% * var(--cfg-dark))
          0.10
          calc(h - 12)
        );
      }

      /* Identifiers — properties, vars, selectors, tags, attributes */
      ::highlight(css-property),
      ::highlight(css-var-name),
      ::highlight(css-selector),
      ::highlight(html-tag),
      ::highlight(html-attribute),
      ::highlight(html-doctype),
      ::highlight(html-entity) {
        color: oklch(from var(--_bg)
          calc(45% * (1 - var(--cfg-dark)) + 75% * var(--cfg-dark))
          0.13
          calc(h + 12)
        );
      }

      /* Functions, classes, builtins */
      ::highlight(python-function),
      ::highlight(python-class),
      ::highlight(python-builtin),
      ::highlight(javascript-function),
      ::highlight(javascript-class),
      ::highlight(javascript-builtin) {
        color: oklch(from var(--_bg)
          calc(45% * (1 - var(--cfg-dark)) + 75% * var(--cfg-dark))
          0.14
          calc(h + 24)
        );
      }

      /* Keywords / atrules / decorators — strongest cool shift */
      ::highlight(css-atrule),
      ::highlight(python-keyword),
      ::highlight(python-decorator),
      ::highlight(javascript-keyword),
      ::highlight(javascript-decorator) {
        color: oklch(from var(--_bg)
          calc(45% * (1 - var(--cfg-dark)) + 75% * var(--cfg-dark))
          0.15
          calc(h + 36)
        );
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Layout.page

    ```css
    @layer layout.page {
      .page {
        display: grid;
        grid-template:
          "b  b  b" auto
          "h  h  h" auto
          "s  s  s" auto
          "nh mh a" auto
          "n  m  a" 1fr
          "nf mf a" auto
          "f  f  f" auto /
          auto 1fr auto;
        height: 100svh;
        overflow: hidden;

        & > [class ^="pg-"]       { padding: calc(0.25 * 1lh); }

        & > .pg-banner            { grid-area: b;  }
        & > .pg-header            { grid-area: h;  }
        & > .pg-subheader         { grid-area: s;  }
        & > .pg-navigation-header { grid-area: nh; }
        & > .pg-navigation        { grid-area: n;  overflow-y: auto; scrollbar-gutter: stable; min-height: 0; }
        & > .pg-navigation-footer { grid-area: nf; }
        & > .pg-main-header       { grid-area: mh; }
        & > .pg-main              { grid-area: m;  overflow-y: auto; scrollbar-gutter: stable; min-height: 0; }
        & > .pg-main-footer       { grid-area: mf; }
        & > .pg-aside             { grid-area: a;  overflow-y: auto; scrollbar-gutter: stable; min-height: 0; }
        & > .pg-footer            { grid-area: f;  }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## layout.drawers

    ```css
    @layer component.complex {
        .drawer {
            --_dur: calc(var(--cfg-motion) * 0.25s);

            position: fixed;
            inset: auto;
            margin: 0;
            max-block-size: none;
            max-inline-size: none;
            transition:
                translate var(--_dur) ease-out,
                opacity   var(--_dur) ease-out,
                display   var(--_dur) allow-discrete,
                overlay   var(--_dur) allow-discrete;
            translate: 0 0;
            opacity: 1;

            &:not(:is([open], :popover-open)) {
                opacity: 0;
                translate: var(--_translate-closed);
            }
            @starting-style {
                &:is([open], :popover-open) {
                    opacity: 0;
                    translate: var(--_translate-closed);
                }
            }

            &.left   { --_translate-closed: -100% 0; inset: 0 auto 0 0; inline-size: min(85vw, 320px); block-size: 100svh; }
            &.right  { --_translate-closed:  100% 0; inset: 0 0 0 auto; inline-size: min(85vw, 320px); block-size: 100svh; }
            &.top    { --_translate-closed: 0 -100%; inset: 0 0 auto 0; inline-size: 100vw; block-size: min(85svh, 240px); }
            &.bottom { --_translate-closed: 0  100%; inset: auto 0 0 0; inline-size: 100vw; block-size: min(85svh, 240px); }
        }

        dialog.drawer {
            --_dur: calc(var(--cfg-motion) * 0.25s);
            --_dim: oklch(0% 0 0 / 0.5);

            &::backdrop {
                background: var(--_dim);
                transition:
                    background-color var(--_dur) ease-out,
                    display          var(--_dur) allow-discrete,
                    overlay          var(--_dur) allow-discrete;
            }
            &:not([open])::backdrop { background: oklch(0% 0 0 / 0); }
            @starting-style {
                &[open]::backdrop { background: oklch(0% 0 0 / 0); }
            }
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Layout.compose

    Honestly a wear layer, these do not alwas work well with grid / flex interaperability (need to clean up some day)

    ```css
    /* ════════════════════════════════════════════════════════════════
       layout.composition — stateless layout primitives

       Gap derives from line-height (calc(0.25 * 1lh)), scaling with
       the ambient --type. To control spacing, control --type. To
       rescale a region, set --scale.
       ════════════════════════════════════════════════════════════ */

    @layer layout.composition {

      .read   { max-inline-size: 65ch; margin-inline: auto; }
      .column { display: flex; flex-direction: column; gap: calc(0.25 * 1lh) }
      .row    { display: flex; flex-direction: row; flex-wrap: wrap; gap: calc(0.25 * 1lh); align-items: center }

      .split {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: calc(0.25 * 1lh);
      }

      .spread {
        display: flex; flex-direction: row; flex-wrap: wrap;
        justify-content: space-between; align-items: center; gap: calc(0.25 * 1lh);
      }
      .spread-column {
        display: flex; flex-direction: column;
        justify-content: space-between; gap: calc(0.25 * 1lh);
      }

      .lcr {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        gap: calc(0.25 * 1lh);

        & > :first-child:not(style):not(script)         { justify-self: start  }
        & > :nth-child(2 of :not(style):not(script))    { justify-self: center }
        & > :last-child:not(style):not(script)          { justify-self: end    }

        & > style, & > script { display: none }
      }

      .tmb {
        display: grid;
        grid-template-rows: 1fr auto 1fr;
        justify-items: center;
        gap: calc(0.25 * 1lh);

        & > :first-child:not(style):not(script)         { align-self: start  }
        & > :nth-child(2 of :not(style):not(script))    { align-self: center }
        & > :last-child:not(style):not(script)          { align-self: end    }

        & > style, & > script { display: none }
      }

      .flank, .flank-start {
        display: flex; flex-direction: row; align-items: center; gap: calc(0.25 * 1lh);

        & > :first-child:not(style):not(script) { flex: 0 0 auto }
        & > :last-child:not(style):not(script)  { flex: 1 1 auto; min-inline-size: 0 }

        & > style, & > script { display: none }
      }

      .flank-end {
        display: flex; flex-direction: row; align-items: center; gap: calc(0.25 * 1lh);

        & > :first-child:not(style):not(script) { flex: 1 1 auto; min-inline-size: 0 }
        & > :last-child:not(style):not(script)  { flex: 0 0 auto }

        & > style, & > script { display: none }
      }

      .frame {
        aspect-ratio: 16 / 9;
        overflow: hidden;

        & > * { inline-size: 100%; block-size: 100%; object-fit: cover }
      }

      .grid {
        display: grid; gap: calc(0.25 * 1lh);
        grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--grid-min, 16rem)), 1fr));
      }

      .stack {
        display: grid;
        grid-template-areas: "stack";

        & > * { grid-area: stack }
      }

      .hero {
        display: grid;
        grid-template:
          "t t t" auto
          "l m r" 1fr
          "b b b" auto /
          auto 1fr auto;
        height: 100%;
        overflow: hidden;

        & > .top    { grid-area: t; }
        & > .bottom { grid-area: b; }
        & > .left   { grid-area: l; overflow-y: auto; scrollbar-gutter: stable; min-height: 0; }
        & > .main   { grid-area: m; overflow-y: auto; scrollbar-gutter: stable; min-height: 0; }
        & > .right  { grid-area: r; overflow-y: auto; scrollbar-gutter: stable; min-height: 0; }
      }

    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Layout.hud

    ```css
    @layer layout.composition{

      /* ── .hud-grid — nine distinct cells, chrome+content ───── */
        .hud-overlay {
            display: grid;
            grid-template-areas: "hud";
            height: 100%;
            pointer-events: none;

            & > * {
              grid-area: hud;
              justify-self: center;
              align-self: center;
              pointer-events: auto;
            }

            & > .↖ { justify-self: start;  align-self: start  }
            & > .↑ { justify-self: center; align-self: start  }
            & > .↗ { justify-self: end;    align-self: start  }
            & > .← { justify-self: start;  align-self: center }
            & > .• { justify-self: center; align-self: center }
            & > .→ { justify-self: end;    align-self: center }
            & > .↙ { justify-self: start;  align-self: end    }
            & > .↓ { justify-self: center; align-self: end    }
            & > .↘ { justify-self: end;    align-self: end    }
      }

      /* ── .hud-grid — nine distinct cells, chrome+content ───── */
      .hud-grid {
            display: grid;
            grid-template:
              "↖ ↑ ↗" auto
              "← • →" 1fr
              "↙ ↓ ↘" auto /
              auto 1fr auto;
            height: 100%;
            overflow: hidden;

            & > .↖ { grid-area: ↖; }
            & > .↑ { grid-area: ↑; }
            & > .↗ { grid-area: ↗; }
            & > .← { grid-area: ←; overflow-y: auto; scrollbar-gutter: stable; }
            & > .• { grid-area: •; overflow-y: auto; scrollbar-gutter: stable; min-height: 0; }
            & > .→ { grid-area: →; overflow-y: auto; scrollbar-gutter: stable; }
            & > .↙ { grid-area: ↙; }
            & > .↓ { grid-area: ↓; }
            & > .↘ { grid-area: ↘; }
      }

    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## component.base

    ```css
    /* ============================================================
       component-base.css — component.base

       Default styling for unclassed HTML elements.
       ============================================================ */

    @layer component.base {
      /* (filled in as the system grows) */
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### KBD

    ```css
    @layer component.base {
     /* kbd — keyboard key marker. Mono surface that evokes a physical
         keycap. Border slightly louder than .input so keys pop in prose. */
      kbd {
        --bg: 0;
        --fg: -1;
        --type: -1.5;
        display: inline-flex;
        align-items: center;
        padding: 0.1em 0.45em;
        border: 1px solid var(--Border);
        border-radius: 0.35em;
        font-family: ui-monospace, monospace;
        font-weight: 600;
        line-height: 1.4;

        & * { --type: -1.5; }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Components Simple
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### glass helper

    > [alpha] translucent backgroudn modifier.

    ```css
    @layer component.simple {
      /* glass — translucent stage. Sits over content with a blur,
         surface paints with --cfg-color-alpha < 1 so what's behind
         shows through. Common for modal overlays, drawer dims, and
         floating chrome on media. */
      .glass {
        --cfg-color-alpha: 0.65;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Button

    > class = ".btn"

    ```css
    .btn {
      --bg: 0;
      --fg: -1;
      --type: -1;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.4em;
      block-size: 2.4lh;        /* was 2lh */
      padding-inline: 0.7em;
      border: 1px solid var(--border);
      border-radius: var(--cfg-radius);
      font-weight: 600;
      line-height: 1;           /* was missing */
      white-space: nowrap;
      user-select: none;

      & * { --type: -1; }
      & svg { inline-size: 1em; block-size: 1em; display: block; flex-shrink: 0; }

      @media (max-width: 480px) {
        min-block-size: 44px;
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Icon Button
    > class = ".icon-btn"

    ```css

    @layer component.simple {
      /* icon-btn — square icon-only button. Same height as .btn (2.4lh)
         with a square aspect ratio.                                     */
      .icon-btn {
        --bg: 0;
        --fg: -1;
        --type: -1;

        display: inline-flex;
        align-items: center;
        justify-content: center;

        flex: 0 0 auto;
        align-self: center;
        block-size: 2.4lh;
        aspect-ratio: 1;

        border: 1px solid var(--border);
        border-radius: var(--cfg-radius);
        line-height: 1;
        user-select: none;

        & svg {
          inline-size: 1em;
          block-size: 1em;
          display: block;
        }

        @media (max-width: 480px) {
          min-block-size: 44px;
          min-inline-size: 44px;
        }
      }
    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tag
    > class = ".tag"
    Toggleable on/off marker via `aria-pressed`. Click to flip. Active translate on press.
    use: filter toggles, multi-select chips, persistent boolean settings.

    ```css
    @layer component.simple {
     /* tag — labeled state indicator. Use a <span> for a static label
         (always shows the vivid "on" look). Use a <button> with
         aria-pressed for an interactive toggle:
           aria-pressed="false" → off state (transparent, dim)
           aria-pressed="true"  → on state  (vivid chromatic, same
                                             as a static tag)
         Same component, two intents disambiguated by element + ARIA.   */
      .tag {
        --bg: 0.8;
        --fg: -1;
        --type: -2;
        display: inline-flex;
        align-items: center;
        padding: 0.3em 0.5em 0.2em;
        border: 1px solid transparent;
        border-radius: var(--cfg-radius);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        line-height: 1;
        user-select: none;
        transition:
          background-color calc(var(--cfg-motion) * 0.1s) ease-out,
          color            calc(var(--cfg-motion) * 0.1s) ease-out,
          border-color     calc(var(--cfg-motion) * 0.1s) ease-out;

        & * { --type: -2; }

        &[aria-pressed="false"] {
          --bg: 0;
          --fg: -0.6;
          border-color: var(--border);
        }
        &:focus-visible {
          outline: 2px solid var(--Border);
          outline-offset: 2px;
        }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### tabs - box / underline

    ```css
    @layer component.simple {


      /* tabs — segmented control. Outer container matches .btn height
         (2.4lh) so a tab strip aligns with adjacent buttons.            */
      .tabs {
        --bg: 0;
        display: inline-flex;
        align-items: stretch;
        block-size: 2.4lh;
        padding: 0.2em;
        border: 1px solid var(--border);
        border-radius: var(--cfg-radius);
        gap: 0.15em;
        line-height: 1;

        & > button {
          --bg: -1;
          --fg: -0.55;
          --type: -1;
          border: 0;
          padding-inline: 0.85em;
          border-radius: max(0px, calc(var(--cfg-radius) - 0.2em));
          font-weight: 600;
          line-height: 1;
          white-space: nowrap;
          user-select: none;
          transition:
            background-color calc(var(--cfg-motion) * 0.2s) ease-out,
            color            calc(var(--cfg-motion) * 0.2s) ease-out,
            border-color     calc(var(--cfg-motion) * 0.2s) ease-out;
        }
        & > button * { --type: -1; }
        & > button:hover { --fg: -1; }
        & > button[aria-selected="true"] {
          --bg: var(--cfg-bg-loud);
          --fg: -1;
        }

        @media (max-width: 480px) {
          min-block-size: 44px;
        }

        /* underline — alternate look. */
        &.underline {
          padding: 0;
          border: 0;
          border-radius: 0;
          border-block-end: 1px solid var(--border);
          gap: 0;

          & > button {
            --bg: 0;
            margin-block-end: -1px;
            padding: 0.4em 0.85em;
            border-radius: 0.4em 0.4em 0 0;
            border-block-end: 2px solid transparent;
          }
          & > button[aria-selected="true"] {
            --bg: 0;
            --fg: 0.8;
            border-block-end-color: currentColor;
          }
        }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### breadcrumbs

    ```css
     /* crumbs — breadcrumb trail. <a> for clickable steps,
         <span aria-current="page"> for the current page. Separators
         are rendered via ::before, painted with --border so they sit
         quieter than the crumb labels.                                  */

    @layer component.simple {
      .crumbs {
        display: inline-flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5em;

        & > * {
          --type: -1;
          --fg: -0.55;
          text-decoration: none;
          line-height: 1;
        }
        & > a:hover {
          --fg: 0.8;
          --_interact-bg: 0;
        }
        & > [aria-current] {
          --fg: -1;
          font-weight: 600;
        }
        & > * + *::before {
          content: "/";
          margin-inline-end: 0.5em;
          color: var(--border);
        }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Avatar

    ```css
    @layer component.simple {
       /* avatar ───────────────────────────────────────────────── */
        .avatar {
          --bg: 0;
          --fg: -1;
          --type: 0;
          box-sizing: border-box;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          block-size: 2.4lh;
          aspect-ratio: 1;
          border: 1px solid var(--border);
          border-radius: var(--cfg-radius);
          font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
          font-weight: 500;
          letter-spacing: 0.02em;
          text-transform: uppercase;
          line-height: 1;

          & * { --type: 1; }
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Progress

    ```css
    @layer component.simple {
          /* progress — native <progress>. The parent runs both formulas
         simultaneously: --bg computes the low-chromatic track, --fg
         computes the high-chromatic fill. Track paints from --_bg, fill
         paints from currentColor (the resolved --fg). Indeterminate
         uses an animated gradient on the parent.                        */
      progress {
        --bg: 0.2;
        --fg: 0.8;
        appearance: none;
        inline-size: 12em;
        block-size: 0.5em;
        border: 1px solid var(--border);
        border-radius: 999em;
        overflow: hidden;

        &::-webkit-progress-bar {
          background: var(--_bg);
          border-radius: 999em;
        }
        &::-webkit-progress-value {
          background: currentColor;
          border-radius: 999em;
          transition: inline-size 0.2s;
        }
        &::-moz-progress-bar {
          background: currentColor;
          border-radius: 999em;
        }
        &:indeterminate {
          animation: progress-pulse 1.2s ease-in-out infinite;
          &::-webkit-progress-bar { background: var(--_bg); }
          &::-webkit-progress-value { background: currentColor; }
          &::-moz-progress-bar { background: currentColor; }
        }
      }
      @keyframes progress-pulse {
        0%, 100% { opacity: 0.5 }
        50%      { opacity: 1   }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### link

    ```css
    @layer component.simple {
          /* link — for in-prose anchors. Chromatic ink so the link reads
         as clickable amid neutral text; underline sits in the quiet-
         tone band so it whispers rather than competes with the word.
         On hover, the underline brightens to currentColor.              */
      .link {
        --fg: 0.8;
        text-decoration: underline;
        text-decoration-color: var(--border);
        text-decoration-thickness: 1px;
        text-underline-offset: 0.18em;
        transition: text-decoration-color 0.15s;

        &:hover {
          --_interact-bg: 0;
          --fg: 1;
          text-decoration-color: var(--Border);
        }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### hr

    ```css
    @layer component.simple {
      /* hr — horizontal divider. Painted from --border to match the
         quiet-tone band used throughout.                                */
      hr {
        block-size: 0;
        border: 0;
        border-block-start: 1px solid var(--border);
        margin-block: 1em;
        inline-size: 100%;
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### card

    ```css
    @layer component.simple {
      .card {
        padding: var(--gap);
        border: 1px solid var(--border);
        border-radius: var(--cfg-radius);
      }
      .Card {
        padding: var(--gap);
        border: 1px solid var(--Border);
        border-radius: var(--cfg-radius);
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inputs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Form
    > will need some clean up
    >

    ```css
    @layer component.simple {
      /* input — text inputs, textareas, selects. Same neutral surface
         as .btn so they line up in forms. Block-size pinned to 2.4lh
         to match .btn / .icon-btn / .tabs at any --type.               */
      .input {
        --bg: 0;
        --fg: -1;
        --type: -1;
        block-size: 2.4lh;
        padding-inline: 0.7em;
        border: 1px solid var(--border);
        border-radius: var(--cfg-radius);
        font: inherit;
        line-height: 1;
        min-inline-size: 0;

        & * { --type: -1; }
        &:focus {
          border-color: var(--Border);
          outline: none;
        }
        &::placeholder { color: var(--border); }

        @media (max-width: 480px) {
          min-block-size: 44px;
        }
      }

      /* select — strip native chevron, draw our own via --border color. */
      select.input {
        appearance: none;
        padding-inline-end: 1.8em;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 0.6em center;
      }

      /* textarea — natural multi-line block-size; opt out of the
         2.4lh single-row height and restore prose line-height for
         readable wrapped text.                                        */
      textarea.input {
        block-size: 6em;
        resize: vertical;
        line-height: 1.5;
        padding-block: 0.4em;

        @media (max-width: 480px) {
          min-block-size: 6em;
        }
      }

      /* check, radio — toggle indicators. */
      .check, .radio {
        --bg: 0;
        appearance: none;
        margin: 0;
        inline-size: 1em;
        block-size: 1em;
        border: 1px solid var(--border);
        border-radius: 0.25em;
        flex-shrink: 0;
        cursor: pointer;

        &:checked {
          --bg: var(--cfg-bg-loud);
          --fg: -1;
          border-color: transparent;
        }
        &:focus-visible {
          outline: 2px solid var(--Border);
          outline-offset: 2px;
        }
      }
      .radio { border-radius: 50%; }

      .check:checked {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='3.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='4 12 10 18 20 6'/%3E%3C/svg%3E");
        background-size: 70%;
        background-repeat: no-repeat;
        background-position: center;
      }
      .radio:checked {
        background-image: radial-gradient(circle, currentColor 32%, transparent 36%);
      }
    }

    @layer component.simple {
      /* fieldset — semantic input grouping that lays out as a row of
         equal-width siblings.                                          */
      fieldset {
        margin: 0;
        padding: 0;
        border: 0;
        min-inline-size: 0;
        display: flex;
        gap: 0.5em;

        & > * {
          flex: 1;
          min-inline-size: 0;
          display: flex;
          flex-direction: column;
          gap: 0.2em;
        }
      }

      /* Form input auto-stretch — donut scope. */
      @scope (form) to (fieldset) {
        .input {
          inline-size: -webkit-fill-available;
          inline-size: -moz-available;
          inline-size: stretch;
        }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## utility

    ```css
    /* ============================================================
       utility.css — utility.layout + utility.exceptions + utility.important

       Three small utility layers consolidated. Kept together because
       each has only a handful of rules and they're conceptually
       adjacent (small classes that tweak behavior).

       utility.layout    — display/wrap helpers, responsive show/hide
       utility.exceptions — buffer layer; intentionally near-empty
       utility.important — !important rules for cascade-immune cases
       ============================================================ */
    @layer utility.layout {
      :where(.nowrap)   { white-space: nowrap; }
      :where(.truncate) { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      :where(.tr) { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      :where(.tr:is(:hover, :focus, :focus-within)) {
        white-space: normal;
        overflow: visible;
        text-overflow: clip;
        overflow-wrap: anywhere;
      }
      :where(.select-all) { -webkit-user-select: all; user-select: all; }
    }

    @layer utility.exceptions {
        /* Visually hidden — screen-reader-only content. */
        :is(.vh) {
            inline-size: 0;
            block-size: 0;
            overflow: hidden;
        }
    }

    @layer utility.important {
        :where([hidden]) { display: none !important }

        /* Responsive show/hide. The viewport class is a participation gate —
           it has to win against any inline `@scope` rule that sets `display`
           on the element to define its internal layout. `revert-layer` returns
           the element to its natural display when it should be visible. */
        :where(.mobile, .tablet, .desktop) { display: none !important }
        @media (         width <   480px) { :where(.mobile)  { display: revert-layer !important } }
        @media (480px <= width <  1024px) { :where(.tablet)  { display: revert-layer !important } }
        @media (         width >= 1024px) { :where(.desktop) { display: revert-layer !important } }

        /* No-print: hide an element when printing. */
        @media print {
            :where(.np) { display: none !important }
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Scratch work;
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
