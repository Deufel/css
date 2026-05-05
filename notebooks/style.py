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

    Same shape as `core.type`, but for spacing. The `--s` length is a fluid value derived from `--space` step + base + ratio + viewport clamp. Utility shorthands `.m/.p/.mx/.my/.px/.py` apply `--s` to the conventional axes.

    **Belongs:** the space formula, the four shorthand classes.
    **Doesn't belong:** layout primitives that *use* `--s` for `gap` (those are `layout.composition`).

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
      layout.app,
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

    ```css
    /* ════════════════════════════════════════════════════════════════
       @property declarations
       These must live outside @layer (CSS spec requirement).
       ════════════════════════════════════════════════════════════ */

    /* Color */
    @property --bg         { syntax: "<number>"; inherits: true; initial-value: -1 }
    @property --fg         { syntax: "<number>"; inherits: true; initial-value: -1 }
    @property --hue        { syntax: "<number>"; inherits: true; initial-value: 220 }
    @property --hue-lock   { syntax: "*";        inherits: true }
    @property --hue-shift  { syntax: "<number>"; inherits: true; initial-value: 0 }
    @property --depth      { syntax: "<number>"; inherits: false; initial-value: 0 }

    @property --cfg-color-muted-l     { syntax: "<percentage>"; inherits: true; initial-value: 96% }
    @property --cfg-color-muted-c     { syntax: "<number>";     inherits: true; initial-value: 0.025 }
    @property --cfg-color-vivid-l     { syntax: "<percentage>"; inherits: true; initial-value: 35% }
    @property --cfg-color-vivid-c     { syntax: "<number>";     inherits: true; initial-value: 0.18 }
    @property --cfg-color-surf-chroma { syntax: "<number>";     inherits: true; initial-value: 0.008 }
    @property --cfg-fg-tint           { syntax: "<number>";     inherits: true; initial-value: 0.012 }

    @property --cfg-color-top-l     { syntax: "<number>"; inherits: true; initial-value: 88 }
    @property --cfg-color-base-step { syntax: "<number>"; inherits: true; initial-value: 4 }
    @property --cfg-color-curve-k   { syntax: "<number>"; inherits: true; initial-value: 0.6 }
    @property --cfg-color-surf-mid  { syntax: "<number>"; inherits: true; initial-value: 60.5 }
    @property --cfg-color-surf-rng  { syntax: "<number>"; inherits: true; initial-value: 55 }
    @property --cfg-color-alpha     { syntax: "<number>"; inherits: true; initial-value: 1 }

    @property --_bg        { syntax: "<color>";      inherits: true;  initial-value: oklch(88% 0.018 220) }
    @property --_naive     { syntax: "<number>";     inherits: false; initial-value: 88 }
    @property --_t         { syntax: "<number>";     inherits: false; initial-value: 0.5 }
    @property --_surf-l    { syntax: "<percentage>"; inherits: false; initial-value: 88% }
    @property --_c01       { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_col-l     { syntax: "<percentage>"; inherits: false; initial-value: 90% }
    @property --_col-c     { syntax: "<number>";     inherits: false; initial-value: 0.1 }
    @property --_k         { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_l         { syntax: "<percentage>"; inherits: false; initial-value: 88% }
    @property --_c         { syntax: "<number>";     inherits: false; initial-value: 0.018 }
    @property --_h         { syntax: "<number>";     inherits: false; initial-value: 220 }
    @property --_dark      { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-pos    { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-neg    { syntax: "<number>";     inherits: false; initial-value: 1 }
    @property --_fg-l      { syntax: "<percentage>"; inherits: false; initial-value: 4% }
    @property --_fg-c      { syntax: "<number>";     inherits: false; initial-value: 0.02 }
    @property --_fg-onpos  { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-pole   { syntax: "<percentage>"; inherits: false; initial-value: 4% }
    @property --_fg-ramp-l { syntax: "<percentage>"; inherits: false; initial-value: 90% }
    @property --_fg-ramp-c { syntax: "<number>";     inherits: false; initial-value: 0.05 }
    @property --_surf-dark { syntax: "<number>";     inherits: false; initial-value: 0 }

    /* State shift hooks — applied per-element. See @layer theme. */
    @property --l-shift { syntax: "<number>"; inherits: false; initial-value: 0 }
    @property --c-shift { syntax: "<number>"; inherits: false; initial-value: 0 }

    /* Global theme config — radius, motion. Values must be absolute. */
    @property --cfg-radius { syntax: "<length>"; inherits: true; initial-value: 6px }
    @property --cfg-motion { syntax: "<number>"; inherits: true; initial-value: 1 }

    /* Type */
    @property --cfg-fluid-min-vp    { syntax: "<length>"; inherits: true; initial-value: 320px }
    @property --cfg-fluid-max-vp    { syntax: "<length>"; inherits: true; initial-value: 1280px }
    @property --cfg-type-scale      { syntax: "<number>"; inherits: true; initial-value: 1 }
    @property --cfg-type-min-ratio  { syntax: "<number>"; inherits: true; initial-value: 1.2 }
    @property --cfg-type-max-ratio  { syntax: "<number>"; inherits: true; initial-value: 1.28 }
    @property --type                { syntax: "<number>"; inherits: false; initial-value: 0 }

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
    @layer core.color {
      :root {
        --hue: 38;
        --cfg-color-muted-l: 96%;
        --cfg-color-muted-c: 0.025;
        --cfg-color-vivid-l: 35%;
        --cfg-color-vivid-c: 0.180;
        --cfg-color-surf-chroma: 0.005;
        --cfg-fg-tint: 0.012;
      }

      :where(*) {
        --_h: var(--hue-lock, calc(var(--hue) + var(--hue-shift)));
        --_naive:  calc(var(--cfg-color-top-l) - var(--depth) * var(--cfg-color-base-step));
        --_t:      calc((var(--_naive) - var(--cfg-color-surf-mid)) / var(--cfg-color-surf-rng));
        --_surf-l: calc((var(--_naive) - var(--depth) * var(--cfg-color-base-step) * var(--cfg-color-curve-k) * var(--_t) * var(--_t)) * 1%);
        --_c01:   clamp(0, var(--bg), 1);
        --_col-l: calc(var(--cfg-color-muted-l) + var(--_c01) * (var(--cfg-color-vivid-l) - var(--cfg-color-muted-l)));
        --_col-c: calc(var(--cfg-color-muted-c) + var(--_c01) * (var(--cfg-color-vivid-c) - var(--cfg-color-muted-c)));
        --_k: clamp(0, calc(var(--bg) + 1), 1);
        --_l: calc(var(--_surf-l) * (1 - var(--_k)) + var(--_col-l) * var(--_k) + var(--l-shift) * 100%);
        --_c: calc(var(--cfg-color-surf-chroma) * (1 - var(--_k)) + var(--_col-c) * var(--_k) + var(--c-shift));
        --_dark: clamp(0, calc((60 - var(--cfg-color-top-l)) / 30), 1);

        --_bg: oklch(clamp(4%, var(--_l), 97%) var(--_c) var(--_h) / var(--cfg-color-alpha));

        --_fg-pos: clamp(0, var(--fg), 1);
        --_fg-neg: clamp(0, calc(-1 * var(--fg)), 1);
        --_surf-dark: clamp(0, calc((50% - var(--_l)) / 1% * 20), 1);
        --_fg-pole: calc(4% * (1 - var(--_surf-dark)) + 97% * var(--_surf-dark));
        --_fg-ramp-l: calc(var(--cfg-color-muted-l) + var(--_fg-pos) * (var(--cfg-color-vivid-l) - var(--cfg-color-muted-l)));
        --_fg-ramp-c: calc(var(--cfg-color-muted-c) + var(--_fg-pos) * (var(--cfg-color-vivid-c) - var(--cfg-color-muted-c)));
        --_fg-onpos: clamp(0, calc(var(--_fg-pos) * 1000000), 1);

        --_fg-l: calc(
          (clamp(4%, var(--_l), 97%) * (1 - var(--_fg-neg)) + var(--_fg-pole) * var(--_fg-neg)) * (1 - var(--_fg-onpos))
          + var(--_fg-ramp-l) * var(--_fg-onpos)
        );
        --_fg-c: calc(
          (var(--_c) * (1 - var(--_fg-neg)) + var(--cfg-fg-tint) * var(--_fg-neg)) * (1 - var(--_fg-onpos))
          + var(--_fg-ramp-c) * var(--_fg-onpos)
        );

        color: oklch(clamp(4%, var(--_fg-l), 97%) var(--_fg-c) var(--_h) / 1);

        --border: oklch(from var(--_bg) calc(l + (var(--_dark) * 2 - 1) * 0.14) calc(c * 0.3) h);
        --Border: oklch(from var(--_bg) calc(l + (var(--_dark) * 2 - 1) * 0.22) clamp(0.08, calc(c + 0.12), 0.18) calc(h + 8));

        --surf-up:   oklch(from var(--_bg) calc(l + var(--cfg-color-base-step) * 0.01) c h);
        --surf-down: oklch(from var(--_bg) calc(l - var(--cfg-color-base-step) * 0.01) c h);
      }

      :where(*) { background-color: oklch(from var(--_bg) l c h / var(--_k)) }
      :where(body, .surface) { background-color: var(--_bg) }
      :where(.btn, .chip, .tag) {
        background-color: color-mix(in oklch, var(--surf-down), var(--_bg) calc(var(--_k) * 100%));
      }
      .surface:has(.surface)                   { --depth: 1 }
      .surface:has(.surface .surface)          { --depth: 2 }
      .surface:has(.surface .surface .surface) { --depth: 3 }
    /* ════════════════════════════════════════════════════════════════
       core.color.css

       The color formula. One axis (--bg) for surface, one axis (--fg)
       for text. Both run through three bands:

         [-1, 0]  surface / contrast-ink  (mode-flip at zero)
         [0, 1]   chromatic ramp          (muted → vivid)
         [3, 4]   P3                      (vivid → P3 endpoint)

       Values in (1, 3) clamp to chromatic max — intentional dead zone.
       Authors reach for chromatic OR P3 deliberately; no smooth ramp
       between them.

       Outputs:
         --_bg     resolved background color
         color     resolved text color (computed automatically from --fg)
         --border  quiet border, theme-aware
         --Border  louder border, theme-aware

       Required outside any @layer (CSS spec): all the @property
       declarations below.
       ════════════════════════════════════════════════════════════════ */


    /* ────────────────────────────────────────────────────────────
       @property declarations — must live OUTSIDE @layer per spec.
       These give the formula tokens proper types, defaults, and
       make them animatable.
       ──────────────────────────────────────────────────────────── */

    /* ── Public inputs ──────────────────────────────────────────── */
    @property --bg          { syntax: "<number>"; inherits: true; initial-value: -1 }
    @property --fg          { syntax: "<number>"; inherits: true; initial-value: -1 }
    @property --hue         { syntax: "<number>"; inherits: true; initial-value: 220 }
    @property --hue-lock    { syntax: "*";        inherits: true }
    @property --hue-shift   { syntax: "<number>"; inherits: true; initial-value: 0 }
    @property --depth       { syntax: "<number>"; inherits: false; initial-value: 0 }
    @property --l-shift     { syntax: "<number>"; inherits: false; initial-value: 0 }
    @property --c-shift     { syntax: "<number>"; inherits: false; initial-value: 0 }

    /* ── Config — chromatic endpoints ───────────────────────────── */
    @property --cfg-color-muted-l     { syntax: "<percentage>"; inherits: true; initial-value: 96% }
    @property --cfg-color-muted-c     { syntax: "<number>";     inherits: true; initial-value: 0.025 }
    @property --cfg-color-vivid-l     { syntax: "<percentage>"; inherits: true; initial-value: 35% }
    @property --cfg-color-vivid-c     { syntax: "<number>";     inherits: true; initial-value: 0.18 }

    /* ── Config — P3 endpoints (used by both --bg and --fg) ─────── */
    @property --cfg-color-p3-l        { syntax: "<percentage>"; inherits: true; initial-value: 80% }
    @property --cfg-color-p3-c        { syntax: "<number>";     inherits: true; initial-value: 0.38 }

    /* ── Config — surface curve and theme knobs ─────────────────── */
    @property --cfg-color-surf-chroma { syntax: "<number>";     inherits: true; initial-value: 0.008 }
    @property --cfg-fg-tint           { syntax: "<number>";     inherits: true; initial-value: 0.012 }
    @property --cfg-color-top-l       { syntax: "<number>";     inherits: true; initial-value: 88 }
    @property --cfg-color-base-step   { syntax: "<number>";     inherits: true; initial-value: 4 }
    @property --cfg-color-curve-k     { syntax: "<number>";     inherits: true; initial-value: 0.6 }
    @property --cfg-color-surf-mid    { syntax: "<number>";     inherits: true; initial-value: 60.5 }
    @property --cfg-color-surf-rng    { syntax: "<number>";     inherits: true; initial-value: 55 }
    @property --cfg-color-alpha       { syntax: "<number>";     inherits: true; initial-value: 1 }

    /* ── Private computed tokens — DO NOT assign these directly ── */
    @property --_bg          { syntax: "<color>";      inherits: true;  initial-value: oklch(88% 0.018 220) }
    @property --_naive       { syntax: "<number>";     inherits: false; initial-value: 88 }
    @property --_t           { syntax: "<number>";     inherits: false; initial-value: 0.5 }
    @property --_surf-l      { syntax: "<percentage>"; inherits: false; initial-value: 88% }
    @property --_c01         { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_col-l       { syntax: "<percentage>"; inherits: false; initial-value: 90% }
    @property --_col-c       { syntax: "<number>";     inherits: false; initial-value: 0.1 }
    @property --_k           { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_p3          { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_chrom-l     { syntax: "<percentage>"; inherits: false; initial-value: 88% }
    @property --_chrom-c     { syntax: "<number>";     inherits: false; initial-value: 0.018 }
    @property --_l           { syntax: "<percentage>"; inherits: false; initial-value: 88% }
    @property --_c           { syntax: "<number>";     inherits: false; initial-value: 0.018 }
    @property --_h           { syntax: "<number>";     inherits: false; initial-value: 220 }
    @property --_dark        { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-pos      { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-neg      { syntax: "<number>";     inherits: false; initial-value: 1 }
    @property --_fg-p3       { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-onpos    { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_fg-pole     { syntax: "<percentage>"; inherits: false; initial-value: 4% }
    @property --_fg-ramp-l   { syntax: "<percentage>"; inherits: false; initial-value: 90% }
    @property --_fg-ramp-c   { syntax: "<number>";     inherits: false; initial-value: 0.05 }
    @property --_fg-chrom-l  { syntax: "<percentage>"; inherits: false; initial-value: 4% }
    @property --_fg-chrom-c  { syntax: "<number>";     inherits: false; initial-value: 0.02 }
    @property --_fg-l        { syntax: "<percentage>"; inherits: false; initial-value: 4% }
    @property --_fg-c        { syntax: "<number>";     inherits: false; initial-value: 0.02 }
    @property --_surf-dark   { syntax: "<number>";     inherits: false; initial-value: 0 }


    /* ════════════════════════════════════════════════════════════════
       The formula — runs on every element, computes --_bg + color
       ════════════════════════════════════════════════════════════════ */
    @layer core.color {

      :root {
        --hue: 38;
        --cfg-color-muted-l: 96%;
        --cfg-color-muted-c: 0.025;
        --cfg-color-vivid-l: 35%;
        --cfg-color-vivid-c: 0.180;
        --cfg-color-surf-chroma: 0.005;
        --cfg-fg-tint: 0.012;
      }

      /* ── Light/dark theme blocks ────────────────────────────────
         These set the values that --bg's surface band consumes.
         The math itself doesn't change between themes — only the
         range it operates within. */
      @media (prefers-color-scheme: dark) {
        :root:not([data-ui-theme="light"]):not([data-ui-theme="dark"]),
        [data-ui-theme="system"] {
          --cfg-color-top-l: 33;
          --cfg-color-base-step: 2.5;
          --cfg-color-surf-chroma: 0.010;
          --cfg-color-surf-mid: 33.5;
          --cfg-color-surf-rng: 27.5;
        }
      }
      [data-ui-theme="light"] {
        --cfg-color-top-l: 88;
        --cfg-color-base-step: 4;
        --cfg-color-surf-chroma: 0.018;
        --cfg-color-surf-mid: 60.5;
        --cfg-color-surf-rng: 55;
      }
      [data-ui-theme="dark"] {
        --cfg-color-top-l: 33;
        --cfg-color-base-step: 2.5;
        --cfg-color-surf-chroma: 0.010;
        --cfg-color-surf-mid: 33.5;
        --cfg-color-surf-rng: 27.5;
      }

      :where(*) {
        /* ── Hue resolution ───────────────────────────────────────
           --hue-lock wins if set; otherwise --hue + --hue-shift. */
        --_h: var(--hue-lock, calc(var(--hue) + var(--hue-shift)));

        /* ── Surface depth math ───────────────────────────────────
           --depth steps the lightness down with a curve that softens
           near the perceptual midpoint. */
        --_naive:  calc(var(--cfg-color-top-l) - var(--depth) * var(--cfg-color-base-step));
        --_t:      calc((var(--_naive) - var(--cfg-color-surf-mid)) / var(--cfg-color-surf-rng));
        --_surf-l: calc((var(--_naive) - var(--depth) * var(--cfg-color-base-step) * var(--cfg-color-curve-k) * var(--_t) * var(--_t)) * 1%);

        /* ── --bg intensity scalars ───────────────────────────────
           Three bands isolated by clamp(). Each is 0..1, with the
           transition fixed at the band boundaries. */
        --_c01: clamp(0, var(--bg), 1);                          /* muted → vivid */
        --_k:   clamp(0, calc(var(--bg) + 1), 1);                /* surface → chromatic */
        --_p3:  clamp(0, calc(var(--bg) - 3), 1);                /* vivid → P3 */

        /* ── --bg chromatic ramp ──────────────────────────────────
           Lerp between muted and vivid endpoints. */
        --_col-l: calc(var(--cfg-color-muted-l) + var(--_c01) * (var(--cfg-color-vivid-l) - var(--cfg-color-muted-l)));
        --_col-c: calc(var(--cfg-color-muted-c) + var(--_c01) * (var(--cfg-color-vivid-c) - var(--cfg-color-muted-c)));

        /* ── --bg chromatic-mode result (with state shifts) ───────
           This is what the formula produces in the [-1, 1] range.
           --l-shift/--c-shift apply here so hover/active states
           compose naturally. */
        --_chrom-l: calc(var(--_surf-l) * (1 - var(--_k)) + var(--_col-l) * var(--_k) + var(--l-shift) * 100%);
        --_chrom-c: calc(var(--cfg-color-surf-chroma) * (1 - var(--_k)) + var(--_col-c) * var(--_k) + var(--c-shift));

        /* ── --bg final lightness/chroma ──────────────────────────
           Lerp from chromatic-mode toward the P3 endpoint. At
           --bg <= 3, --_p3 is 0 and chromatic wins. At --bg = 4,
           P3 endpoint wins exactly. */
        --_l: calc(var(--_chrom-l) * (1 - var(--_p3)) + var(--cfg-color-p3-l) * var(--_p3));
        --_c: calc(var(--_chrom-c) * (1 - var(--_p3)) + var(--cfg-color-p3-c) * var(--_p3));

        --_dark: clamp(0, calc((60 - var(--cfg-color-top-l)) / 30), 1);
        --_bg: oklch(clamp(4%, var(--_l), 97%) var(--_c) var(--_h) / var(--cfg-color-alpha));


        /* ── --fg intensity scalars ───────────────────────────────
           Same three-band structure as --bg, applied to text color. */
        --_fg-pos: clamp(0, var(--fg), 1);                       /* chromatic ramp magnitude */
        --_fg-neg: clamp(0, calc(-1 * var(--fg)), 1);            /* contrast-ink magnitude */
        --_fg-p3:  clamp(0, calc(var(--fg) - 3), 1);             /* chromatic → P3 */
        --_fg-onpos: clamp(0, calc(var(--_fg-pos) * 1000000), 1);  /* "is fg > 0?" hard switch */

        /* ── --fg contrast-ink branch ─────────────────────────────
           When fg < 0, pick dark or light ink based on surface
           lightness. This branch never enters P3 — contrast ink is
           inherently neutral. */
        --_surf-dark: clamp(0, calc((50% - var(--_l)) / 1% * 20), 1);
        --_fg-pole: calc(4% * (1 - var(--_surf-dark)) + 97% * var(--_surf-dark));

        /* ── --fg chromatic-ramp branch ───────────────────────────
           When fg > 0, map intensity onto the muted-to-vivid ramp,
           same endpoints as --bg. */
        --_fg-ramp-l: calc(var(--cfg-color-muted-l) + var(--_fg-pos) * (var(--cfg-color-vivid-l) - var(--cfg-color-muted-l)));
        --_fg-ramp-c: calc(var(--cfg-color-muted-c) + var(--_fg-pos) * (var(--cfg-color-vivid-c) - var(--cfg-color-muted-c)));

        /* ── --fg chromatic-mode result (intermediate) ────────────
           --_fg-onpos hard-switches between contrast-ink and
           chromatic-ramp. This is the "what color is the text in
           the [-1, 1] range" answer. */
        --_fg-chrom-l: calc(
          (clamp(4%, var(--_l), 97%) * (1 - var(--_fg-neg)) + var(--_fg-pole) * var(--_fg-neg)) * (1 - var(--_fg-onpos))
            + var(--_fg-ramp-l) * var(--_fg-onpos)
        );
        --_fg-chrom-c: calc(
          (var(--_c) * (1 - var(--_fg-neg)) + var(--cfg-fg-tint) * var(--_fg-neg)) * (1 - var(--_fg-onpos))
            + var(--_fg-ramp-c) * var(--_fg-onpos)
        );

        /* ── --fg final lightness/chroma ──────────────────────────
           Lerp the chromatic-mode result toward the P3 endpoint.
           At --fg <= 3, --_fg-p3 is 0 and chromatic wins. At --fg = 4,
           P3 endpoint wins. Note: --_fg-p3 is 0 for any --fg <= 3,
           which means contrast-ink (negative --fg) is never affected
           by the P3 lerp — its result already has --_fg-p3 = 0. */
        --_fg-l: calc(var(--_fg-chrom-l) * (1 - var(--_fg-p3)) + var(--cfg-color-p3-l) * var(--_fg-p3));
        --_fg-c: calc(var(--_fg-chrom-c) * (1 - var(--_fg-p3)) + var(--cfg-color-p3-c) * var(--_fg-p3));

        color: oklch(clamp(4%, var(--_fg-l), 97%) var(--_fg-c) var(--_h) / 1);


        /* ── Border helpers ───────────────────────────────────────
           --border: quiet (low-chroma, theme-aware luminance shift)
           --Border: louder (more chroma, slight hue rotation) */
        --border: oklch(from var(--_bg) calc(l + (var(--_dark) * 2 - 1) * 0.14) calc(c * 0.3) h);
        --Border: oklch(from var(--_bg) calc(l + (var(--_dark) * 2 - 1) * 0.22) clamp(0.08, calc(c + 0.12), 0.18) calc(h + 8));
      }


      /* ── Paint resolution ───────────────────────────────────────
         Default: every element renders --_bg at alpha=--_k. At --bg
         of -1 (default), --_k is 0, so unscoped elements stay
         transparent. Surfaces force opaque paint. */
      :where(*) {
        background-color: oklch(from var(--_bg) l c h / var(--_k));
      }
      :where(body, .surface) {
        background-color: var(--_bg);
      }


      /* ── Surface depth cascade ──────────────────────────────────
         A .surface containing nested .surfaces lifts its depth, which
         the formula uses to step lightness down. Body sits at depth 4
         so any top-level surface visually pops forward. */
      :where(body)                             { --depth: 4 }
      .surface:has(.surface)                   { --depth: 1 }
      .surface:has(.surface .surface)          { --depth: 2 }
      .surface:has(.surface .surface .surface) { --depth: 3 }
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
       core.type — the fluid type formula
       --cfg-type-min/max plus the viewport-clamped font-size, with
       derived line-height and letter-spacing.
       ════════════════════════════════════════════════════════════ */
    @layer core.type {
      :root {
        --cfg-type-min: 0.8rem;
        --cfg-type-max: 1rem;
      }
      :where(*) {
        --_t-min: calc(var(--cfg-type-min) * pow(var(--cfg-type-min-ratio), var(--type)));
        --_t-max: calc(var(--cfg-type-max) * pow(var(--cfg-type-max-ratio), var(--type)));
        font-size: calc(
          clamp(
            var(--_t-min),
            calc(var(--_t-min) + (var(--_t-max) - var(--_t-min)) * (100vi - var(--cfg-fluid-min-vp)) / (var(--cfg-fluid-max-vp) - var(--cfg-fluid-min-vp))),
            var(--_t-max)
          ) * var(--cfg-type-scale)
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
    /* ════════════════════════════════════════════════════════════════
       theme — project-level visual decisions
       The "vibe" of the page. Theme blocks (light/dark), state classes
       that nudge the color formula, font families, etc.
       State classes are uniform across all components.
       ════════════════════════════════════════════════════════════ */
    @layer theme {
      /* ── Light/dark theme values ──────────────────────────────
         The MATH lives in core.color. These rules only set which
         VALUES the math operates on for each theme.

         Default behavior: when no data-ui-theme attribute is set
         (or it's "system"), follow the OS preference via
         prefers-color-scheme. Explicit attributes override. */

      @media (prefers-color-scheme: dark) {
        :root:not([data-ui-theme="light"]):not([data-ui-theme="dark"]),
        [data-ui-theme="system"] {
          --cfg-color-top-l: 33;
          --cfg-color-base-step: 2.5;
          --cfg-color-curve-k: 0.6;
          --cfg-color-surf-chroma: 0.010;
          --cfg-color-surf-mid: 33.5;
          --cfg-color-surf-rng: 27.5;
        }
      }
      @media (prefers-color-scheme: light) {
        [data-ui-theme="system"] {
          --cfg-color-top-l: 88;
          --cfg-color-base-step: 4;
          --cfg-color-curve-k: 0.6;
          --cfg-color-surf-chroma: 0.018;
          --cfg-color-surf-mid: 60.5;
          --cfg-color-surf-rng: 55;
        }
      }
      [data-ui-theme="light"] {
        --cfg-color-top-l: 88;
        --cfg-color-base-step: 4;
        --cfg-color-curve-k: 0.6;
        --cfg-color-surf-chroma: 0.018;
        --cfg-color-surf-mid: 60.5;
        --cfg-color-surf-rng: 55;
      }
      [data-ui-theme="dark"] {
        --cfg-color-top-l: 33;
        --cfg-color-base-step: 2.5;
        --cfg-color-curve-k: 0.6;
        --cfg-color-surf-chroma: 0.010;
        --cfg-color-surf-mid: 33.5;
        --cfg-color-surf-rng: 27.5;
      }


      /* ── State classes ────────────────────────────────────────
         Uniform across every component. The pointer helper adds
         these via JS; CSS reacts through the formula. */
      .hover    { --l-shift: 0.04;  --c-shift: 0.02 }
      .active   { --l-shift: -0.04; --c-shift: -0.10 }
      .disabled { --fg: -0.35; cursor: not-allowed }


      /* ── Motion presets ───────────────────────────────────────
         --cfg-motion is a multiplier consumed by transition-duration
         calcs throughout the system. 0 disables motion; "debug" slows
         everything 10× for inspection. The OS/browser preference
         (prefers-reduced-motion: reduce) is sovereign — it overrides
         any explicit button choice. The button is for users who don't
         have that preference set. */
      [data-ui-motion="off"]   { --cfg-motion: 0 }
      [data-ui-motion="on"]    { --cfg-motion: 1 }
      [data-ui-motion="debug"] { --cfg-motion: 10 }
      @media (prefers-reduced-motion: reduce) {
        :root, [data-ui-motion] { --cfg-motion: 0 }
      }

      /* Timer-hand rotation reflects current motion state. The natural
         hand position in the SVG points at 1:30 (-45° from horizontal).
         Rotation values transform that to: 12 (off), 3 (on), 9 (debug).
         The transition uses --cfg-motion itself so when motion is off,
         the hand snaps; when debug, it sweeps slowly. */
      /* Timer-hand transition. The actual rotation comes from a
         monotonically-increasing signal counter on the SVG line —
         each click advances clockwise without wraparound concerns.
         Duration ties to --cfg-motion: snappy in 'on', slow in
         'debug', instant in 'off'. */
      .timer-hand {
        transform-box: view-box;
        transform-origin: 12px 14px;
        transition: rotate calc(var(--cfg-motion) * 0.25s) ease-out;
      }


      /* ── Type size presets ────────────────────────────────────
         Drive type via the --cfg-type-scale multiplier rather than
         resetting the base range. One value to reason about, one
         value to animate. Transition is tied to --cfg-motion so it
         respects the motion preset. */
      body {
        transition: --cfg-type-scale calc(var(--cfg-motion) * 0.2s) ease-out;
      }
      [data-ui-type="sm"] { --cfg-type-scale: 0.875 }
      [data-ui-type="md"] { --cfg-type-scale: 1     }
      [data-ui-type="lg"] { --cfg-type-scale: 1.125 }


      /* ── Scrollbars ───────────────────────────────────────────
         Track invisible (transparent over the surface). Thumb is
         the chromatic foreground at --fg: 0.5 — same color the fg
         formula would produce if an element had --fg: 0.5. We can't
         literally set --fg here (it would tint text on every element),
         so the formula is reproduced inline against the current
         surface (--_bg) and page hue (--_h). */
      * {
        scrollbar-width: thin;
        scrollbar-color: oklch(from var(--_bg)
          calc(var(--cfg-color-muted-l) + 0.5 * (var(--cfg-color-vivid-l) - var(--cfg-color-muted-l)))
          calc(var(--cfg-color-muted-c) + 0.5 * (var(--cfg-color-vivid-c) - var(--cfg-color-muted-c)))
          var(--_h)
        ) transparent;
      }
      ::-webkit-scrollbar { inline-size: 8px; block-size: 8px }
      ::-webkit-scrollbar-track { background: transparent }
      ::-webkit-scrollbar-thumb {
        background: oklch(from var(--_bg)
          calc(var(--cfg-color-muted-l) + 0.5 * (var(--cfg-color-vivid-l) - var(--cfg-color-muted-l)))
          calc(var(--cfg-color-muted-c) + 0.5 * (var(--cfg-color-vivid-c) - var(--cfg-color-muted-c)))
          var(--_h)
        );
        border-radius: 999px;
      }


      /* ── Syntax highlighting ──────────────────────────────────
         Live code tokens at --fg: 0.5 (mid-vivid chromatic) — the
         only chromatic value safe in both light and dark themes.
         Differentiated by --hue-shift in 12° steps within ±36° of
         the page hue. Tight tonal palette stays cohesive with the
         brand.

         Comments use negative --fg (contrast ink), the proper
         mode for dim text — theme-safe across light/dark via the
         formula's contrast branch.

         The CSS Custom Highlight API only supports color,
         background-color, text-decoration, text-shadow on
         ::highlight(). Differentiation here is color only. */
      ::highlight(css-comment),
      ::highlight(html-comment),
      ::highlight(python-comment),
      ::highlight(javascript-comment)    { --fg: -0.4; --hue-shift:   0 }

      ::highlight(css-string),
      ::highlight(html-value),
      ::highlight(python-string),
      ::highlight(javascript-string)     { --fg: 0.5; --hue-shift: -36 }

      ::highlight(css-number),
      ::highlight(css-unit),
      ::highlight(python-number),
      ::highlight(javascript-number)     { --fg: 0.5; --hue-shift: -24 }

      ::highlight(css-punctuation),
      ::highlight(html-bracket),
      ::highlight(python-operator),
      ::highlight(python-punctuation),
      ::highlight(javascript-operator),
      ::highlight(javascript-punctuation) { --fg: 0.5; --hue-shift: -12 }

      ::highlight(css-property),
      ::highlight(css-var-name),
      ::highlight(css-selector),
      ::highlight(html-tag),
      ::highlight(html-attribute),
      ::highlight(html-doctype),
      ::highlight(html-entity)           { --fg: 0.5; --hue-shift:  12 }

      ::highlight(python-function),
      ::highlight(python-class),
      ::highlight(python-builtin),
      ::highlight(javascript-function),
      ::highlight(javascript-class),
      ::highlight(javascript-builtin)    { --fg: 0.5; --hue-shift:  24 }

      ::highlight(css-atrule),
      ::highlight(python-keyword),
      ::highlight(python-decorator),
      ::highlight(javascript-keyword),
      ::highlight(javascript-decorator)  { --fg: 0.5; --hue-shift:  36 }

      /* Comments — contrast-ink (negative fg) branch of the formula.
         Theme-safe: dark text on light surfaces, light text on dark
         surfaces. Hue-shift adds a faint chromatic tint via
         --cfg-fg-tint. */
      ::highlight(css-comment),
      ::highlight(html-comment),
      ::highlight(python-comment),
      ::highlight(javascript-comment) {
        color: oklch(from var(--_bg)
          calc(
            l * (1 - clamp(0, -1 * var(--fg), 1))
            + (4% * clamp(0, calc((50% - l) / 1% * 20), 1)
               + 97% * (1 - clamp(0, calc((50% - l) / 1% * 20), 1)))
              * clamp(0, -1 * var(--fg), 1)
          )
          calc(c * (1 - clamp(0, -1 * var(--fg), 1)) + var(--cfg-fg-tint) * clamp(0, -1 * var(--fg), 1))
          calc(h + var(--hue-shift))
        );
      }

      /* Live code tokens — chromatic ramp (positive fg) branch.
         --fg: 0.5 sits at mid-vivid: visible against both light
         and dark surfaces. Hue shifts ±12° to ±36° spread the
         categories around the page hue without leaving the family. */
      ::highlight(css-string),
      ::highlight(css-atrule),
      ::highlight(css-var-name),
      ::highlight(css-unit),
      ::highlight(css-number),
      ::highlight(css-property),
      ::highlight(css-selector),
      ::highlight(css-punctuation),
      ::highlight(html-doctype),
      ::highlight(html-entity),
      ::highlight(html-value),
      ::highlight(html-tag),
      ::highlight(html-attribute),
      ::highlight(html-bracket),
      ::highlight(python-string),
      ::highlight(python-decorator),
      ::highlight(python-function),
      ::highlight(python-class),
      ::highlight(python-keyword),
      ::highlight(python-builtin),
      ::highlight(python-number),
      ::highlight(python-operator),
      ::highlight(python-punctuation),
      ::highlight(javascript-string),
      ::highlight(javascript-decorator),
      ::highlight(javascript-function),
      ::highlight(javascript-class),
      ::highlight(javascript-keyword),
      ::highlight(javascript-builtin),
      ::highlight(javascript-number),
      ::highlight(javascript-operator),
      ::highlight(javascript-punctuation) {
        color: oklch(from var(--_bg)
          calc(var(--cfg-color-muted-l) + var(--fg) * (var(--cfg-color-vivid-l) - var(--cfg-color-muted-l)))
          calc(var(--cfg-color-muted-c) + var(--fg) * (var(--cfg-color-vivid-c) - var(--cfg-color-muted-c)))
          calc(var(--_h) + var(--hue-shift))
        );
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### layout.app

    ```css
    @layer layout.app {
        body.app {
            display: grid;
            grid-template:
                "h h h" auto
                "n m a" 1fr
                "f f f" auto /
                auto 1fr auto;
            height: 100svh;
            overflow: hidden;

            > #header { grid-area: h; }
            > #footer { grid-area: f; }
            > #nav    { grid-area: n; overflow-y: auto; scrollbar-gutter: stable; }
            > #main   { grid-area: m; overflow-y: auto; scrollbar-gutter: stable; min-height: 0; }
            > #aside  { grid-area: a; overflow-y: auto; scrollbar-gutter: stable; }
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### layout.drawers

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
    ## layout.compose

    Honestly a wear layer, these do not alwas work well with grid / flex interaperability (need to clean up some day)

    ```css
    /* ════════════════════════════════════════════════════════════════
       layout.composition — stateless layout primitives
       ════════════════════════════════════════════════════════════ */

    @layer layout.composition {
      .column { display: flex; flex-direction: column; gap: var(--gap) }
      .row    { display: flex; flex-direction: row; flex-wrap: wrap; gap: var(--gap); align-items: center }

      .split {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--gap);
      }

      .spread {
        display: flex; flex-direction: row; flex-wrap: wrap;
        justify-content: space-between; align-items: center; gap: var(--gap);
      }
      .spread-column {
        display: flex; flex-direction: column;
        justify-content: space-between; gap: var(--gap);
      }

      .lcr {
        display: grid; grid-template-columns: 1fr auto 1fr;
        align-items: center; gap: var(--gap);

        & > :first-child  { justify-self: start }
        & > :nth-child(2) { justify-self: center }
        & > :last-child   { justify-self: end }
      }

      .tmb {
        display: grid; grid-template-rows: 1fr auto 1fr;
        justify-items: center; gap: var(--gap);

        & > :first-child  { align-self: start }
        & > :nth-child(2) { align-self: center }
        & > :last-child   { align-self: end }
      }

      /* ── .flank — leading/trailing fixed, the other grows ──── */
      .flank, .flank-start, .flank-end {
        display: flex; flex-direction: row; align-items: center; gap: var(--gap);
      }
      .flank, .flank-start {
        & > :first-child { flex: 0 0 auto }
        & > :last-child  { flex: 1 1 auto; min-inline-size: 0 }
      }
      .flank-end {
        & > :first-child { flex: 1 1 auto; min-inline-size: 0 }
        & > :last-child  { flex: 0 0 auto }
      }

      .frame {
        aspect-ratio: 16 / 9;
        overflow: hidden;

        & > * { inline-size: 100%; block-size: 100%; object-fit: cover }
      }

      .grid {
        display: grid; gap: var(--gap);
        grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--grid-min, 16rem)), 1fr));
      }

      .stack {
        display: grid;
        grid-template-areas: "stack";

        & > * { grid-area: stack }
      }

      /* ── .hud ─────────────────────────────────────────────────
         A .stack with 9 directional anchor slots. Children are
         full-bleed over a single cell, sized to content, anchored
         by justify-self / align-self. Siblings are geometrically
         independent — a giant ↖ panel cannot push a centered •
         child off-axis.

         Container is hit-test transparent (pointer-events: none);
         children opt back in. Decorative children (e.g. a centered
         reticle whose bounding box exceeds its visual) should set
         pointer-events: none again to avoid blocking passthrough.

         Slots: ↖ ↑ ↗ / ← • → / ↙ ↓ ↘
         ──────────────────────────────────────────────────────── */
      .hud {
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

        /* When .column or .row groups multiple items into one slot,
           mirror the slot's horizontal anchor on the inner cross-axis
           so grouped chips don't flag-fly. */
        & > .↖.column, & > .←.column, & > .↙.column { align-items: flex-start }
        & > .↑.column, & > .•.column, & > .↓.column { align-items: center }
        & > .↗.column, & > .→.column, & > .↘.column { align-items: flex-end }
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
    ## Components Simple
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Rule
    > element = `<hr>` or `<hr class="vr">`
    Native `<hr>` for horizontal dividers. Add `.vr` to flip orientation for vertical dividers in flex/inline rows. Vertical sized in em so it scales with the parent's font.
    use: `<hr>` between sections in a column; `<hr class="vr">` between items in a toolbar or status row.

    ```css
    @layer component.simple {
        :where(hr) {
            block-size: 1px;
            inline-size: 100%;
            margin: 0;
            background: var(--border);
            border: 0;

            &.vr {
                inline-size: 1px;
                block-size: 1.5em;
                flex-shrink: 0;
            }
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tab bar
    > class = ".tab-bar"
    Connected underline tab strip. The active item shows a 2px accent border that reads as the tab indicator. Each child carries `data-label` matching its visible text; a hidden ghost in `::before` reserves the bold-weight cell width so switching the active tab doesn't shift layout.

    Mark the active item with `aria-current="page"` (for nav links) or `aria-pressed="true"` (for toggle buttons). Both selectors are styled.

    use: top-level page nav, settings panel section switcher, any "one of N" view selector.

    ```css
    @layer component.simple {
        :where(.tab-bar) {
            display: inline-flex;
            align-self: end;
            align-items: end;

            & > * {
                --type: -1;
                --fg: -0.5;
                font: inherit;
                text-decoration: none;
                background: transparent;
                border: 0;
                padding: 0.5rem 0.9rem;
                border-block-end: 2px solid transparent;
                cursor: pointer;
                display: inline-grid;
                place-items: center;
                transition: color, border-color;
                transition-duration: calc(var(--cfg-motion) * 0.12s);
                transition-timing-function: ease-out;

                /* Hidden bold ghost reserves the cell width so weight
                   changes on activation don't shift layout. */
                &::before {
                    content: attr(data-label);
                    grid-area: 1 / 1;
                    font-weight: 600;
                    visibility: hidden;
                }
                /* Visible label stacks in the same cell as the ghost. */
                & > span {
                    grid-area: 1 / 1;
                }
                &[aria-current="page"],
                &[aria-pressed="true"] {
                    --fg: 0.5;
                    border-block-end-color: currentColor;
                    font-weight: 600;
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
    ### Chip
    > class = ".chip"
    Info-display pill. Stateless. May contain inner action buttons (add, dismiss).
    use: filter terms, status indicators, read-only tags.

    ```css
    @layer component.simple {
        :where(.chip) {
            --type: -1;
            display: inline-flex;
            align-items: center;
            gap: 0.4ch;
            padding: 0.25em 0.85em;
            border: 1px solid var(--border);
            border-radius: 999px;
            font: inherit;
            line-height: 1;

            & .btn {
                min-inline-size: unset;
                block-size: 1.25em;
                inline-size: 1.25em;
                aspect-ratio: 1;
                padding: 0;
                border: 0;
                background: transparent;
                font-weight: 400;
                margin-inline-end: -0.35em;

                & > svg {
                    inline-size: 1em;
                    block-size: 1em;
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
    ### Tag
    > class = ".tag"
    Toggleable on/off marker via `aria-pressed`. Click to flip. Active translate on press.
    use: filter toggles, multi-select chips, persistent boolean settings.

    ```css
    @layer component.simple {
        :where(.tag) {
            --type: -1;
            --fg: -0.6;
            cursor: pointer;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
            display: inline-flex;
            align-items: center;
            gap: 0.4ch;
            padding: 0.25em 0.7em;
            border: 1px solid var(--border);
            border-radius: 0.4em;
            font: inherit;
            font-weight: 600;
            line-height: 1;
            transition: background-color, color, border-color, translate;
            transition-duration: calc(var(--cfg-motion) * 0.08s);
            transition-timing-function: ease-out;

            &[aria-pressed="true"] {
                --bg: 0.3;
                --fg: 0.9;
                border-color: var(--Border);
            }
            &.active { translate: 0 1px }
            &.disabled { --fg: -0.35 }
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
    ### Button
    > class = ".btn"
    Clickable action, no persistent state. Press for active translate.
    use: any tap target shaped like a button — actions, submits, dismiss buttons inside chips.

    ```css
    @layer component.simple {
        :where(.btn) {
            --type: -1;
            cursor: pointer;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5em;
            min-inline-size: 12ch;
            padding: 0.4em 1em;
            border: 1px solid var(--border);
            border-radius: var(--cfg-radius);
            font: inherit;
            font-weight: 600;
            line-height: 1;
            transition: background-color, color, border-color, translate;
            transition-duration: calc(var(--cfg-motion) * 0.08s);
            transition-timing-function: ease-out;

            &.active {
                translate: 0 1px;
                --fg: -0.6;
            }
            &:focus-visible {
                outline: 2px solid var(--Border);
                outline-offset: 2px;
            }
            & > svg {
                inline-size: 1.25em;
                block-size: 1.25em;
                pointer-events: none;
                flex-shrink: 0;
            }
            /* Icon-only auto-detection: a button with no accessible text content
               must carry aria-label, so we use that as the signal. Pure :has(> svg)
               would also match icon+text buttons because text nodes don't break
               :only-child. */
            &[aria-label]:has(> svg) {
                min-inline-size: unset;
                padding: 0.4em;
                aspect-ratio: 1;
            }
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tap
    > class = ".tap"
    Behavior marker for non-button-shaped tappable things. Hover emphasis without click cursor. No padding, no border — just the interaction signals.
    use: data table rows, clickable cards, list items.

    ```css
    @layer component.simple {
        :where(.tap) {
            user-select: none;
            -webkit-tap-highlight-color: transparent;

            &.hover, &.active { background-color: var(--_bg) }
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
        :where(.nowrap)   { white-space: nowrap }
        :where(.truncate) {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Responsive show/hide. Matches viewport ranges; flips display
           to `revert-layer` so the element gets its natural display value
           back (block/inline/grid/etc.) without the consumer specifying. */
        :where(.mobile, .tablet, .desktop) { display: none }
        @media (         width <   480px) { :where(.mobile)  { display: revert-layer } }
        @media (480px <= width <  1024px) { :where(.tablet)  { display: revert-layer } }
        @media (         width >= 1024px) { :where(.desktop) { display: revert-layer } }

        /* Print mode adjustments — generic enough to live here. */
        @media print {
            :where(body) { min-height: 0 }
        }
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
