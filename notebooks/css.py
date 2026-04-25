import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")

with app.setup:

    from pathlib import Path


@app.cell
def _():
    import marimo as mo


    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # CSS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Layers
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css
    @layer  reset.fix,       /* CSS WC Mistakes and artifacts */
        reset.opinion,       /* Project level decisions live here */
        core.color,          /* The Core Color API all color math here. no color set directly after this consume api */
        core.type,           /* enables `--type: (-inf, inf)` basicaly a font but scales apppropraitly across all screen sizes */
        core.space,          /* final api not finalized yet but essentially the dame thing as the type for for spacing */
        theme,               /* Project level themeing for things like Pri, sec, semantic colors border radius ect */
        layout.page,         /* Opinionated layout for all my projects an application shell that works on all screen sizes WIP */
        layout.composition,  /* Layout primatives Compose well with layout page */
        component.base,      /* restyling default components that responde to the theme */
        component.simple,    /* `normal` components like breadcrumbs, pagation, chip, button ect ect.. use discression */
        component.complex,   /* more complex components like a calendar or a datatable */
        utility.layout,      /* currently this is my dynamic layout query with fallback trick idk what else fits here..*/
        utility.exceptions,  /* Left as a buffer no plan to ever use this layer */
        utility.important;   /* The only use case for this layer is that you MUST override an inline style avoid like the plauge */
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2A reset.fix
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css
    @layer reset.fix {
        *,*::before,*::after { box-sizing: border-box; margin: 0; background-repeat: no-repeat }
        :root { interpolate-size: allow-keywords }
        :where(html) {
            color-scheme: light dark; line-height: 1.1; -moz-text-size-adjust: none;
            -webkit-text-size-adjust: none; text-size-adjust: none }
        :where(body,figure,blockquote,dl,dd,p) { margin-block-end: 0 }
        :where(img,picture,svg) { max-width: 100%; display: block; height: auto }
        :where(table,thead,tbody,tfoot,tr) { isolation: isolate }  /* INVESTIGAVE */
        :where(input,button,textarea,select) { font: inherit }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2B reset.opinion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css
    @layer reset.opinion {
        :where(body) { overflow-wrap: break-word }
        :where(html) { scrollbar-width: thin }
        :where(p) { text-wrap: pretty }
        :where(h1,h2,h3,h4,h5,h6) { text-wrap: balance }
        :where(img,picture,video,canvas,svg) { height: auto }
        :where(svg) { color: currentColor }
        :where(button,[role="button"],summary,label[for],input[type="file"]::file-selector-button) { cursor: pointer; user-select: none; -webkit-user-select: none }
        :where(:disabled,[aria-disabled="true"]) { cursor: not-allowed }
        :where(table) { border-collapse: collapse }
        :where(fieldset) { border: 0; padding: 0; margin: 0; min-inline-size: 0 }
        :where(legend) { padding: 0 }
        :where(textarea) { resize: vertical }
        :where(textarea:not([rows])) { min-block-size: 10em }
        :where(abbr[title]) { cursor: help; text-decoration: underline dotted }
        :where(summary) { list-style: none }
        :where(a) { text-decoration: none }
        :where(input):autofill { box-shadow: inset 0 0 0 1000px var(--bg, transparent) }
        :where(ul,ol): where([role="list"]) { list-style:none; padding: 0 }
        :where([hidden]) { display: none }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3A core.color

    ```css
    /* ─── Public API ─────────────────────────────────────
       Structural (cascade-driven):
         .surface                  opt-in to paint a surface; auto-nests
         --color      -1..1        -1 = surface, 0..1 = muted..vivid
         --hue        number       absolute hue override
         --hue-shift  number       additive offset from --cfg-color-hue
         --contrast   0..1         text ink strength
         --contrast-hue number     explicit Hue change for text(remember contrast is used to set `color only`)
         --contrast-chroma 0..0.4  add some chroma retention to let color-text keep some color (or else goes to white/black)

       Stateful (component-driven, non-inheriting):
         compose with the shifts; (--{hue, c, l}-shift)

       Computed outputs:
         var(--bg)                 background color
         var(--border)             quiet accent (neighbor of --bg)
         var(--Border)             loud accent (stronger neighbor)

       Semantic hue conveniences: .suc .inf .wrn .dgr
       ────────────────────────────────────────────────── */

    /* ---------- Config properties ---------- */
    @property --cfg-color-hue          { syntax: "<number>";     inherits: true; initial-value: 120 }
    @property --cfg-color-alpha        { syntax: "<number>";     inherits: true; initial-value: 1 }
    @property --cfg-color-top-l        { syntax: "<number>";     inherits: true; initial-value: 88 }
    @property --cfg-color-base-step    { syntax: "<number>";     inherits: true; initial-value: 4 }
    @property --cfg-color-curve-k      { syntax: "<number>";     inherits: true; initial-value: 0.6 }
    @property --cfg-color-surf-mid     { syntax: "<number>";     inherits: true; initial-value: 60.5 }
    @property --cfg-color-surf-rng     { syntax: "<number>";     inherits: true; initial-value: 55 }
    @property --cfg-color-surf-chroma  { syntax: "<number>";     inherits: true; initial-value: 0.018 }
    @property --cfg-color-muted-l      { syntax: "<percentage>"; inherits: true; initial-value: 90% }
    @property --cfg-color-muted-c      { syntax: "<number>";     inherits: true; initial-value: 0.05 }
    @property --cfg-color-vivid-l      { syntax: "<percentage>"; inherits: true; initial-value: 20% }
    @property --cfg-color-vivid-c      { syntax: "<number>";     inherits: true; initial-value: 0.3 }

    /* ---------- Public API ---------- */
    @property --depth       { syntax: "<number>"; inherits: false; initial-value: 0 }
    @property --color       { syntax: "<number>"; inherits: true;  initial-value: -1 }
    /* --hue intentionally has syntax "*" and no initial-value so that
       var(--hue, calc(--cfg-color-hue + --hue-shift)) falls through
       to the fallback until something explicitly sets --hue. Do NOT
       "fix" this to <number> — it will break --hue-shift entirely. */
    @property --hue       { syntax: "*";        inherits: true }
    @property --hue-shift { syntax: "<number>"; inherits: true; initial-value: 0 }
    @property --l-shift   { syntax: "<number>"; inherits: true; initial-value: 0 }
    @property --c-shift   { syntax: "<number>"; inherits: true; initial-value: 0 }

    /* these are used to set a background aware text color */
    @property --contrast    { syntax: "<number>"; inherits: true; initial-value: 1 }
    @property --contrast-hue    { syntax: "*"; inherits: true }
    @property --contrast-chroma { syntax: "*"; inherits: true ; initial-value:0 }

    /* Helper colors */
    @property --border { syntax: "<color>"; inherits: true; initial-value: red }
    @property --Border { syntax: "<color>"; inherits: true; initial-value: blue}

    /* ---------- Private intermediates ---------- */

    @property --_naive   { syntax: "<number>";     inherits: false; initial-value: 88 }
    @property --_t       { syntax: "<number>";     inherits: false; initial-value: 0.5 }
    @property --_surf-l  { syntax: "<percentage>"; inherits: false; initial-value: 88% }
    @property --_c01     { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_col-l   { syntax: "<percentage>"; inherits: false; initial-value: 90% }
    @property --_col-c   { syntax: "<number>";     inherits: false; initial-value: 0.1 }
    @property --_k       { syntax: "<number>";     inherits: false; initial-value: 0 }
    @property --_l       { syntax: "<percentage>"; inherits: false; initial-value: 88% }
    @property --_c       { syntax: "<number>";     inherits: false; initial-value: 0.018 }
    @property --_h       { syntax: "<number>";     inherits: false; initial-value: 220 }

    @layer core.color {

        /* ---------- Theme detection (moved in from theme layer) ---------- */
        @media (prefers-color-scheme: dark) {
            :root:not([data-ui-theme="light"]):not([data-ui-theme="dark"]),
            [data-ui-theme="system"] {
                --cfg-color-top-l: 33;
                --cfg-color-base-step: 2.5;
                --cfg-color-surf-chroma: 0.010;
                --cfg-color-surf-mid: 33.5;
                --cfg-color-surf-rng: 27.5
            }
        }
        @media (prefers-color-scheme: light) {
            [data-ui-theme="system"] {
                --cfg-color-top-l: 88;
                --cfg-color-base-step: 4;
                --cfg-color-surf-chroma: 0.018;
                --cfg-color-surf-mid: 60.5;
                --cfg-color-surf-rng: 55
            }
        }
        [data-ui-theme="light"] {
            --cfg-color-top-l: 88;
            --cfg-color-base-step: 4;
            --cfg-color-curve-k: 0.6;
            --cfg-color-surf-chroma: 0.018;
            --cfg-color-surf-mid: 60.5;
            --cfg-color-surf-rng: 55
        }
        [data-ui-theme="dark"] {
            --cfg-color-top-l: 33;
            --cfg-color-base-step: 2.5;
            --cfg-color-curve-k: 0.6;
            --cfg-color-surf-chroma: 0.010;
            --cfg-color-surf-mid: 33.5;
            --cfg-color-surf-rng: 27.5
        }

        /* Semantic hue conveniences — only set --hue. */
        .suc { --hue: 145 }
        .inf { --hue: 240 }
        .wrn { --hue: 75 }
        .dgr { --hue: 25 }

        /* ---------- The formula ---------- */
        :where(*) {
            --_naive:  calc(var(--cfg-color-top-l) - var(--depth) * var(--cfg-color-base-step));
            --_t:      calc((var(--_naive) - var(--cfg-color-surf-mid)) / var(--cfg-color-surf-rng));
            --_surf-l: calc((var(--_naive) - var(--depth) * var(--cfg-color-base-step) * var(--cfg-color-curve-k) * var(--_t) * var(--_t)) * 1%);
            --_c01:    clamp(0, var(--color), 1);
            --_col-l:  calc(var(--cfg-color-muted-l) + var(--_c01) * (var(--cfg-color-vivid-l) - var(--cfg-color-muted-l)));
            --_col-c:  calc(var(--cfg-color-muted-c) + var(--_c01) * (var(--cfg-color-vivid-c) - var(--cfg-color-muted-c)));
            --_k:      clamp(0, calc(var(--color) + 1), 1);
            --_l:      calc(var(--_surf-l) * (1 - var(--_k)) + var(--_col-l) * var(--_k));
            --_c:      calc(var(--cfg-color-surf-chroma) * (1 - var(--_k)) + var(--_col-c) * var(--_k));
            --_h:      var(--hue, calc(var(--cfg-color-hue) + var(--hue-shift)));
            --bg: oklch(
                clamp(4%, calc(var(--_l) + var(--l-shift) * 100%), 97%)     /*Lightness 0-1   */
                /* calc(var(--_c) + var(--c-shift))                            Chroma    0-.4  */
       /*            calc(var(--_c) + var(--c-shift) * pow(var(--_l) / 100%, 2)) /*Chroma    0-.4  */
                calc(var(--_c) + var(--c-shift) * (var(--_l) / 100%))

                var(--_h)                                                   /*Hue       0-360 */
                / var(--cfg-color-alpha)                                    /*Alpha     0-1   */
            );
            --border: oklch(from var(--bg) calc(l - 0.14) calc(c * 0.7) h);
            --Border: oklch(from var(--bg) calc(l - 0.28) clamp(0.08, calc(c * 1.4), 0.22) calc(h + 8));
            color: oklch(from var(--bg)
                calc(l + (clamp(0, calc((0.5 - l) * 999), 1) - l) * var(--contrast))
                calc(c * (1 - var(--contrast)) + var(--contrast-chroma))
                var(--contrast-hue, h)
            );
        }

        :where(*) { background-color: oklch(from var(--bg) l c h / var(--_k)) }
        :where(body, .surface, .btn) { background-color: var(--bg) }
        .surface:has(.surface)                                    { --depth: 1 }
        .surface:has(.surface .surface)                           { --depth: 2 }
        .surface:has(.surface .surface .surface)                  { --depth: 3 }
        .surface:has(.surface .surface .surface .surface)         { --depth: 4 }
    }


    @layer theme {

        ::selection       { background: var(--Border); color: var(--bg) }
        :focus-visible    { outline: 2px solid var(--Border); outline-offset: 2px }
        .shadow { filter: drop-shadow(0 6px 12px oklch(from var(--bg) 20% 0.08 h / 0.4)) }
        .glow { filter: drop-shadow(0 0 12px oklch(from var(--bg) 70% 0.2 h / 0.6)) }

        /* script takes care of active and hover on btn classes easier then using mcss and the pointer api */
        .hover  {
            --l-shift:  0.04;
            --contrast: calc(var(--contrast, 1) + 0.15) ;
            --c-shift: 0.02;
        }
        .active {
            --l-shift: -0.04;
            --contrast: max(calc(var(--contrast, 1) - 0.2), .4);
            --c-shift: -0.1;
        }
        .disabled { cursor: not-allowed; opacity: 0.45 }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3B core.type
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css

    @property --cfg-fluid-min-vp { syntax: "<length>"; inherits: true; initial-value: 320px }
    @property --cfg-fluid-max-vp { syntax: "<length>"; inherits: true; initial-value: 1280px }
    @property --type { syntax: "<number>"; inherits: false; initial-value: 0 }
    @property --cfg-type-scale { syntax: "<number>"; inherits: true; initial-value: 1 }
    @property --cfg-type-min-ratio { syntax: "<number>"; inherits: true; initial-value: 1.2 }
    @property --cfg-type-max-ratio { syntax: "<number>"; inherits: true; initial-value: 1.28 }

    :root { --cfg-fluid-min-vp: 320px; --cfg-fluid-max-vp: 1280px }
    :root { --cfg-type-min: 0.85rem; --cfg-type-max: 1.0625rem }

    @layer core.type {
        :where(*) {
            --_t-min: calc(var(--cfg-type-min) * pow(var(--cfg-type-min-ratio),var(--type)));
            --_t-max: calc(var(--cfg-type-max) * pow(var(--cfg-type-max-ratio),var(--type)));
            font-size: calc( clamp(var(--_t-min),calc(var(--_t-min) + (var(--_t-max) - var(--_t-min)) * (100vi - var(--cfg-fluid-min-vp)) / (var(--cfg-fluid-max-vp) - var(--cfg-fluid-min-vp))),var(--_t-max) ) * var(--cfg-type-scale) );
            letter-spacing: calc(0.01em - var(--type) * 0.01em);
            line-height: calc(1.5 - var(--type) * 0.075)
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3C core.space
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css
        /* ============================================
           CORE.SPACE

           NOTE: @property initial-values for <length> MUST be
           computationally independent — no rem, em, %, vw, etc.
           Use px in @property, then set the "real" default in a rule.
           ============================================ */

        @property --space { syntax: "<number>"; inherits: false; initial-value: 0 }
        @property --s     { syntax: "<length>"; inherits: false; initial-value: 0px }

        @property --cfg-space-base  { syntax: "<length>"; inherits: true; initial-value: 8px }
        @property --cfg-space-ratio { syntax: "<number>"; inherits: true; initial-value: 1.5 }
        @property --cfg-space-scale { syntax: "<number>"; inherits: true; initial-value: 1 }

        /* Real defaults (rem-based) set here, not in @property */
        :where(html) {
            --cfg-space-base: 0.5rem;
        }

        :where(*) {
            --s: calc(
                var(--cfg-space-base) *
                pow(var(--cfg-space-ratio), var(--space)) *
                clamp(0.75, 100vi / 80rem, 1) *
                var(--cfg-space-scale)
            );
        }

        :where(.m)  { margin:  var(--s) }
        :where(.p)  { padding: var(--s) }
        :where(.mx) { margin-inline:  var(--s) }
        :where(.my) { margin-block:   var(--s) }
        :where(.px) { padding-inline: var(--s) }
        :where(.py) { padding-block:  var(--s) }

        [data-ui-space="sm"] { --cfg-space-scale: 0.875 }
        [data-ui-space="md"] { --cfg-space-scale: 1 }
        [data-ui-space="lg"] { --cfg-space-scale: 1.2 }
    ```

    ```old css

    /* ============================================
       CORE.SPACE — localized, non-inheriting
       Public API: --space (input), --s (output)
       ============================================ */

    /* Space configs — co-located with the layer that uses them */
    @property --cfg-space-scale     { syntax: "<number>"; inherits: true;  initial-value: 1 }
    @property --cfg-space-min-ratio { syntax: "<number>"; inherits: true;  initial-value: 1.5 }
    @property --cfg-space-max-ratio { syntax: "<number>"; inherits: true;  initial-value: 1.6 }
    @property --cfg-space-min       { syntax: "<length>"; inherits: true;  initial-value: 0.25rem }
    @property --cfg-space-max       { syntax: "<length>"; inherits: true;  initial-value: 0.5rem }

    /* Public API — does NOT inherit. Each element decides its own spacing. */
    @property --space { syntax: "<number>"; inherits: false; initial-value: 0 }
    @property --s     { syntax: "<length>"; inherits: false; initial-value: 0.5rem }

    /* Private intermediates — also non-inheriting so they don't leak */
    @property --_s-min { syntax: "<length>"; inherits: false; initial-value: 0.25rem }
    @property --_s-max { syntax: "<length>"; inherits: false; initial-value: 0.5rem }

    @layer core.space {
        :where(*) {
            --_s-min: calc(var(--cfg-space-min) * pow(var(--cfg-space-min-ratio), var(--space)));
            --_s-max: calc(var(--cfg-space-max) * pow(var(--cfg-space-max-ratio), var(--space)));
            --s: calc(
                clamp(
                    var(--_s-min),
                    calc(var(--_s-min) + (var(--_s-max) - var(--_s-min)) * (100vi - var(--cfg-fluid-min-vp)) / (var(--cfg-fluid-max-vp) - var(--cfg-fluid-min-vp))),
                    var(--_s-max)
                ) * var(--cfg-space-scale)
            )
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 theme
    Q1: should this layer exist? ? (it is not even have anything that can go in a layer...
    A1: yes this is basically the noramilization that needs to use the core or interact with it this layer makes sense Keep it

    If the things can go into the core, or normalize put it there first if it is purly a layout theme then iti  goes here.

    > reminder: --custom properties go on root (or can be scoped on whatever) ,
    > [data-ui-motion="off"]
    > @properties Must go top layer

    Consider nameign all --cfg-theme for matching the other --cfg-color, --cfg-space..


    ```css
    @property --cfg-radius   { syntax: "<length>"; inherits: true; initial-value: 8px }
    @property --cfg-motion   { syntax: "<number>"; inherits: true; initial-value: 1 }

    :root {
        --font-heading: "Iowan Old Style","Palatino Linotype","URW Palladio L",P052,serif;
        --font-body: Avenir,Montserrat,Corbel,"URW Gothic",source-sans-pro,sans-serif;
        --font-mono: ui-monospace,"SF Mono",Monaco,Menlo,Consolas,monospace;
        --font-kbd: "Courier New","Nimbus Mono PS",monospace
    }

    /* MOTION */
    @media (prefers-reduced-motion:reduce) { :root { --cfg-motion: 0 } }
    [data-ui-motion="off"] { --cfg-motion: 0 }
    [data-ui-motion="on"] { --cfg-motion: 1 }
    [data-ui-motion="debug"] { --cfg-motion: 10 }

    /* TYPE */
    [data-ui-size="sm"] { --cfg-type-scale: 0.875; --cfg-space-scale: 0.875 }
    [data-ui-size="md"] { --cfg-type-scale: 1; --cfg-space-scale: 1 }
    [data-ui-size="lg"] { --cfg-type-scale: 1.25; --cfg-space-scale: 1.1 }


    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5A layout.page
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css
    @property --cfg-layout-radius   { syntax: "<length>"; inherits: true; initial-value: 4px; }
    @property --cfg-layout-page-gap { syntax: "<length>"; inherits: true; initial-value: 6px; }

    :where(html) {
        --cfg-layout-radius: clamp(0px, calc(100vi - 100%) * 1e5, 0.5rem);
        --cfg-layout-page-gap: clamp(0px, calc(100vi - 100%) * 1e5, 1rem);
    }

    @layer layout.page {
        body {
            font: 14px/1.5 ui-sans-serif, system-ui, sans-serif;
            background: var(--bg);

            /* The container context that drives the layout switch */
            container: app-shell / inline-size;

            /* WIDE LAYOUT (default) — 3x3 grid with named areas.
            Columns are `auto 1fr auto` so the nav/aside tracks
            size to their explicit widths, and collapse to zero
            when those dialogs leave the grid (position: fixed).
            gap: 0 + explicit margins on #main avoids phantom gap
            around collapsed tracks in narrow mode. */
            display: grid;
            grid-template:
                "header header header" auto
                "nav    main   aside"  1fr
                "footer footer footer" auto /
                auto    1fr    auto;
            gap: 0;
            height: 100svh;
            overflow: hidden;  /* body never scrolls; #main does */
        }

        /* Only #main scrolls; header/footer stay pinned */
        #main {
            overflow-y: auto;
            min-height: 0;   /* critical in grid — lets child scroll */
        }
        #header, #footer {
            min-height: 0;
        }

      /* ---------------------------------------------------------
         GRID-MODE DIALOG RESET
         ---------------------------------------------------------
         <dialog> comes with UA styles we need to neutralize so
         it renders like a plain block in its grid slot:
           - position: absolute → static
           - display: none (when !open) → block (always visible in grid)
           - border, margin, etc. → ours
         --------------------------------------------------------- */
        #nav, #aside {
            position: static;
            display: block;  /* overrides dialog's display:none */
            max-width: none;
            max-height: none;
            /* Explicit widths let the `auto` columns size to these
            in wide mode, and collapse to 0 when position: fixed */
            width: var(--drawer-width);
            height: auto;
            margin: 0;
            padding: 1rem;
            border: 1px solid var(--border);
            border-radius: var(--cfg-layout-radius);
            background: var(--bg);
            color: inherit;
            overflow-y: auto;
        }

        #nav {
            grid-area: nav;
            margin-right: var(--cfg-layout-page-gap);   /* gap against #main — leaves with the drawer */
        }
        #aside {
            grid-area: aside;
            margin-left: var(--cfg-layout-page-gap);    /* gap against #main — leaves with the drawer */
        }

      /* Regular grid areas */
        #main{
            padding: 1rem;
            border: 1px solid var(--border);
            border-radius: var(--cfg-layout-radius);
            background: var(--bg);
        }
        #header {
            grid-area: header;
            margin-bottom: var(--cfg-layout-page-gap);  /* gap below header — always wanted */
        }
        #main    {
            grid-area: main;
            background: var(--bg);
        }
        #footer  {
            grid-area: footer;
            margin-top: var(--cfg-layout-page-gap);     /* gap above footer — always wanted */
        }

      /* ---------------------------------------------------------
         NARROW LAYOUT — container query switches everything
         ---------------------------------------------------------
         Below 900px of container width:
           - Grid collapses to single column DONT THINK WE NEED THIS
           - #nav / #aside removed from grid, positioned as fixed drawers KEEP IMPORTANT
           - Triggers become visible USE UTILITY.LAYOUT BETTER
         --------------------------------------------------------- */
        @container app-shell (width < 1024px) {
            /* The drawers: fixed, off-screen by default, slide in when open */
            #nav, #aside {
                position: fixed;
                /* Reset all inset sides, then set the one we want per drawer.
                Dialog UA style is `inset: 0` + `margin: auto` which would
                fight our positioning, so we null it explicitly. */
                inset: 0 auto 0 auto;
                margin: 0;
                width: min(85vw, 320px);
                max-width: 85vw;
                height: 100svh;
                border-radius: 0;
                border: 0;
                background: var(--bg);
                padding: 1.5rem 1rem;
                overflow-y: auto;

                /* Animation setup — transition discrete props */
                transition:
                    translate calc(var(--cfg-motion) * 0.25s) ease-out,
                    opacity   calc(var(--cfg-motion) * 0.25s) ease-out,
                    display   calc(var(--cfg-motion) * 0.25s) allow-discrete,
                    overlay   calc(var(--cfg-motion) * 0.25s) allow-discrete;
                translate: 0 0;
                opacity: 1;
            }

            #nav {
                left: 0;
                border-right: 1px solid var(--Border);
            }
            #aside {
                left: auto;
                right: 0;
                border-left: 1px solid var(--Border);
            }

            /* Closed state */
            #nav:not([open]) {
                display: none;
                translate: -100% 0;
                opacity: 0;
            }
            #aside:not([open]) {
                display: none;
                translate: 100% 0;
                opacity: 0;
            }

            /* Starting state when opening — what we animate FROM */
            @starting-style {
                #nav[open] {
                    translate: -100% 0;
                    opacity: 0;
                }
                #aside[open] {
                    translate: 100% 0;
                    opacity: 0;
                }
            }

            /* Backdrop only appears in modal mode (top layer) */
            #nav::backdrop,
            #aside::backdrop {
                background: oklch(0% 0 0 / 0.5);
                transition:
                    background-color calc(var(--cfg-motion) * 0.25s) ease-out,
                    display          calc(var(--cfg-motion) * 0.25s) allow-discrete,
                    overlay          calc(var(--cfg-motion) * 0.25s) allow-discrete;
            }
            #nav:not([open])::backdrop,
            #aside:not([open])::backdrop {
                background: oklch(0% 0 0 / 0);
            }
            @starting-style {
                #nav[open]::backdrop,
                #aside[open]::backdrop {
                      background: oklch(0% 0 0 / 0);
                }
            }
        } /* end of @container query */
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5B layout.composition
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css
    @layer layout.composition {
        .stack {
            display: flex;
            flex-direction: column;
            gap: var(--s,0.75rem)
        }

        .row {
            display: flex;
            flex-wrap: wrap;
            gap: var(--s,0.5rem)
        }

        .split {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: var(--s,0.5rem)
        }

        .cluster {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            gap: var(--s,0.5rem)
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit,minmax(var(--_col,15rem),1fr));
            gap: var(--s,1rem)
        }

        .flank {
            display: flex;
            flex-wrap: wrap;
            gap: var(--s,1rem)
        }

        .flank >:first-child {
            flex: 1 1 var(--_flank,auto)
        }

        .flank >:last-child {
            flex: 999 1 0
        }

        .flank-end {
            display: flex;
            flex-wrap: wrap;
            gap: var(--s,1rem)
        }

        .flank-end >:first-child {
            flex: 999 1 0
        }

        .flank-end >:last-child {
            flex: 1 1 var(--_flank,auto)
        }

        .span {
            grid-column: 1 / -1
        }

        .wrap {
            flex-wrap: wrap
        }

        .nowrap {
            flex-wrap: nowrap
        }


        .right { margin-inline-start: auto; text-align: end }
        .fab-row { position: fixed; inset-block-end: 1rem; inset-inline-end: 1rem; display: flex; gap: 0.5rem; }

        .grid-2x2,.grid-3x3,.grid-overlap{display:grid;height:100%}
        .grid-2x2{grid-template:1fr 1fr/1fr 1fr}
        .grid-3x3{grid-template:1fr 1fr 1fr/1fr 1fr 1fr}
        .grid-overlap{grid-template:1fr/1fr}
        .grid-overlap>*{grid-area:1/1/-1/-1}
        .↖{grid-area:1/1;justify-self:start;align-self:start}
        .↗{grid-area:1/-2;justify-self:end;align-self:start}
        .↙{grid-area:-2/1;justify-self:start;align-self:end}
        .↘{grid-area:-2/-2;justify-self:end;align-self:end}
        .grid-3x3>.↑,.grid-overlap>.↑{grid-area:1/2;justify-self:center;align-self:start}
        .grid-3x3>.←,.grid-overlap>.←{grid-area:2/1;justify-self:start;align-self:center}
        .grid-3x3>.→,.grid-overlap>.→{grid-area:2/-2;justify-self:end;align-self:center}
        .grid-3x3>.↓,.grid-overlap>.↓{grid-area:-2/2;justify-self:center;align-self:end}

    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6A Component.base
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css
    @layer component.base {
        h1 {
            --type: 2;
        }

        p {
            --contrast: 1;
            font-family: var(--font-body)
        }

        small {
            --type: -1.5;
            --contrast: 0.6;
            font-family: var(--font-body);
            text-transform: uppercase
        }

        code {
            --type: -0.5;
            --contrast: 0.8;
            font-family: var(--font-mono)
        }

        figcaption {
            --type: -0.5;
            --contrast: 0.7
        }

        blockquote {
            --contrast: 0.75
        }

        address {
            --contrast: 0.75
        }

        cite {
            --contrast: 0.7
        }

        mark {
            --contrast: 1
        }

        :where(.badge) {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.15em 0.6em;
            border-radius: 99px;
        }

        :where(hr) {
            border-color: var(--border)
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6B Component Simple
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tag

    ```css
    @layer component.simple{
        .tag {
            --type:-2;
            display: inline-flex; align-items: center;
            padding-inline: 0.6em; padding-block: 0.15em;
            border-radius: 999px; border: 1px solid var(--border);
            white-space: nowrap;
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Button

    ```css
    @layer component.simple {
        :where(.btn) {
            --type: -1;
            --contrast: 0.85;

            -webkit-tap-highlight-color: transparent;
            min-width: 12ch;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5em;
            padding: 0.35em 1em;
            margin: 5px;
            border: 1px solid var(--border);
            border-radius: var(--cfg-radius);
            font-family: var(--font-mono);
            font-weight: 600;
            cursor: pointer;
            transition: background-color, color, border-color;
            transition-duration: calc(var(--cfg-motion) * 0.12s);
            transition-timing-function: ease-out;

            /* SVG sizing inside any .btn — text-only buttons won't hit this,
               combo and icon-only both will. Keeps icons proportional to
               the current --type instead of hardcoded px. */
            & > svg {
                inline-size: 1.25em;
                block-size: 1.25em;
                pointer-events: none;
                flex-shrink: 0;
            }

            /* Combo: svg + text. Tighten left padding so the icon has
               room to breathe from the button edge without pushing the
               label off-center. gap: 0.5em (inherited) handles icon↔text. */
            &:has(> svg):not(:has(> svg:only-child)) {
                padding-inline-start: 0.75em;
            }

            /* Icon-only: square, no min-width. */
            &:has(> svg:only-child) {
                min-width: unset;
                padding: 0.25em;
                block-size: calc(2.5 * 1em);
                aspect-ratio: 1;
            }

            /* Touch-device overrides — nested inside .btn since you asked.
               `pointer: coarse` catches phones/tablets where the primary
               input is a finger, regardless of viewport width. More reliable
               than width media queries for this. */
            @media (pointer: coarse) {
                min-block-size: 44px;
                padding-block: 0.6em;

                &:has(> svg:only-child) {
                    /* 48px keeps us comfortably above the 44px floor even
                       when rendered at small --type values. */
                    block-size: 48px;
                    inline-size: 48px;
                }

                /* Give combo buttons a bit more horizontal room on touch */
                &:has(> svg):not(:has(> svg:only-child)) {
                    padding-inline: 1em 1.25em;
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
    ```OLD BUTTON

    @property --_btn-t    { syntax: "<time>";   inherits: false; initial-value: 0.12s }
    @property --_btn-jump { syntax: "<length>"; inherits: false; initial-value: -0.1em }

    @layer component.simple {
        :where(button, .btn) {
            --_btn-t: 0.12s;
            --_btn-jump: -0.1em;
            --type: -1;
            --contrast: 0.85;

            -webkit-tap-highlight-color: transparent;
            min-width: 12ch;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5em;
            padding: 0.35em 1em;
            border: 1px solid var(--Button);
            border-radius: var(--cfg-radius);
            font-family: var(--font-mono);
            font-weight: 600;
            cursor: pointer;
            contain: layout;

            box-shadow: calc(-1 * var(--_btn-jump)) calc(-1 * var(--_btn-jump)) 0 var(--Border);
            transform: translateX(var(--_btn-jump)) translateY(var(--_btn-jump));
            transition: calc(var(--cfg-motion) * var(--_btn-t)) ease-out;

            &:has(> svg:only-child) {
                min-width: unset;
                padding: 0.25em;
                height: calc(2.5 * 1em);
                aspect-ratio: 1;
                svg { pointer-events: none }
            }

            &.hover  { --lighten: 0.2; --contrast: 1 }
            &.active {
                --lighten: -0.05;
                --contrast: 0.6;
                transform: translateX(0) translateY(0);
                box-shadow: 0 0 0 var(--Border)
            }
            &:focus-visible { outline: 2px solid var(--Border); outline-offset: var(--_btn-jump) }
            &.disabled { cursor: not-allowed; opacity: 0.45 }
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Card
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```css
    @layer componet.simple {

        .card {
            box-shadow: inset 0 1px 0 oklch(from var(--bg) calc(l + 0.1) c h);
            border-radius: var(--cfg-radius);
            border: 1px solid var(--border);
        }

        .Card {
            box-shadow: inset 0 1px 0 oklch(from var(--bg) calc(l + 0.1) c h);
            border-radius: var(--cfg-radius);
            border: 1px solid var(--Border);
        }

    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6C component.complex
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### resume header specifics

    ```css
    @layer component.complex {
        #header {
            display: flex;
            flex-direction: column;
            gap: var(--s);
            padding: var(--s);
        }

        .header-top { align-items: center }

        .blurb {
            --type: 0;
            --contrast: 0.8;
            max-inline-size: 65ch;
            line-height: 1.4;
            margin: 0;
        }

        .contact {
            --type: -0.5;
            --contrast: 0.7;
            display: inline-flex;
            align-items: center;
            gap: 0.4em;
            font-family: var(--font-body);

            > svg {
                inline-size: 1em;
                block-size: 1em;
                opacity: 0.7;
            }
        }
    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### resume timeline

    ```css
    @layer component.complex {
        /* ============================================================
           TIMELINE — horizontal time-block bar.

           Markup contract:
             <div class="timeline" style="--start: 2011; --end: 2026">
                 <div class="tl-track">
                     <span class="tl-block" style="--from: 2011; --to: 2015; --hue-shift: 0">
                         B.S. EE
                     </span>
                     <span class="tl-block" style="--from: 2015; --to: 2021; --hue-shift: 30">
                         S&C Electric
                     </span>
                     ...
                 </div>
                 <div class="tl-ticks">
                     <span>2011</span><span>2015</span><span>2020</span><span>2026</span>
                 </div>
             </div>

           Each block sets its own --from/--to. The track uses CSS Grid
           with --span fr units to size segments proportionally.

           Why grid + fr: alternatives are positioned absolute (fragile,
           requires container width) or flex with calc'd flex-basis
           (clamps weirdly). Grid fr units are made for exactly this.
           ============================================================ */

        .timeline {
            --tl-height: 2.25rem;
            --tl-radius: calc(var(--cfg-radius) / 2);
            --tl-tick-color: oklch(from var(--bg) calc(l + 0.05) c h / 0.4);

            display: flex;
            flex-direction: column;
            gap: calc(var(--s) / 3);
            inline-size: 100%;
            font-family: var(--font-body);

            /* The bar itself: grid with --span-total fr columns, where
               --span-total = --end - --start. Each block spans
               (--to - --from) fr units. */
            > .tl-track {
                display: grid;
                grid-template-columns: repeat(
                    calc(var(--end) - var(--start)),
                    1fr
                );
                block-size: var(--tl-height);
                gap: 2px;                    /* hairline between segments */
                border-radius: var(--tl-radius);
                overflow: hidden;            /* clips segment corners to bar */
                background: var(--tl-tick-color);  /* shows through gaps */
            }

            /* A segment. --color: 0.5 takes it out of "surface" territory
               into the muted-vivid color zone, where --hue-shift actually
               changes its appearance. --contrast: 0 lets the color system
               pick a readable text color against the segment's background. */
            .tl-block {
                --color: 0.5;
                --contrast: 0;

                /* Span proportional to its duration */
                grid-column: span calc(var(--to) - var(--from));

                display: flex;
                align-items: center;
                justify-content: center;
                padding-inline: 0.5em;
                font-size: 0.75em;
                font-weight: 600;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                cursor: default;
                transition: filter calc(var(--cfg-motion) * 0.15s) ease-out;

                /* Subtle hover lift — useful if you wire tooltips later */
                &:hover {
                    filter: brightness(1.1);
                }
            }

            /* Quiet "gap" segment — for unaccounted-for time. */
            .tl-block.tl-gap {
                --color: -0.3;
                --contrast: 0.4;
                font-style: italic;
            }

            /* Year tick row underneath. Positioned with the same grid math
               so labels align to segment boundaries. */
            > .tl-ticks {
                display: grid;
                grid-template-columns: repeat(
                    calc(var(--end) - var(--start)),
                    1fr
                );
                font-size: 0.7em;
                --contrast: 0.55;
                font-family: var(--font-mono);
                font-variant-numeric: tabular-nums;
            }

            /* Each tick spans from its --at year to the next year boundary,
               rendered with the year label at its starting edge. */
            .tl-ticks > span {
                grid-column: calc(var(--at) - var(--start) + 1);
                justify-self: start;
                transform: translateX(-50%);   /* center over its boundary */
                white-space: nowrap;
            }

            /* First and last tick: don't translate off-edge */
            .tl-ticks > span:first-child { transform: none }
            .tl-ticks > span:last-child  { transform: translateX(-100%) }
        }
    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### resume aside

    ```css
    @layer component.complex {
        .aside {
            --space: -1;                            /* was 0 — denser whole component */
            width: minmax(18rem, 25%);
            display: flex;
            flex-direction: column;
            gap: calc(var(--s) * 2);                /* was *3 — pull sections closer */
            padding: var(--s);
            font-family: var(--font-body);

            > section {
                display: flex;
                flex-direction: column;
                gap: calc(var(--s) * 0.75);

                > h2 {
                    --type: 0;
                    --contrast: 1;
                    margin: 0;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    padding-block-end: calc(var(--s) / 3);
                    border-block-end: 1px solid var(--Border);
                }
            }

            /* ── EDUCATION ──────────────────────────────────────────
               Two-column row: left = degree+school stacked,
               right = date+location stacked. No wrapping. */
            .edu {
                display: flex;
                flex-direction: column;
                gap: calc(var(--s) / 6);

                > header {
                    display: grid;
                    grid-template-columns: 1fr auto;
                    column-gap: var(--s);
                    align-items: start;
                }

                .edu-degree {
                    --type: 0;
                    margin: 0;
                    line-height: 1.25;
                    font-weight: 600;
                }
                .edu-school {
                    --type: -0.5;
                    --contrast: 0.75;
                    font-weight: 500;
                }

                .edu-meta-group {
                    display: flex;
                    flex-direction: column;
                    align-items: flex-end;
                    gap: 0;
                }

                .edu-meta {
                    --type: -1;
                    --contrast: 0.6;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.3em;
                    white-space: nowrap;
                    line-height: 1.4;

                    > svg {
                        inline-size: 0.9em;
                        block-size: 0.9em;
                        flex-shrink: 0;
                        opacity: 0.7;
                    }
                }

                > ul {
                    margin: 0;
                    margin-block-start: calc(var(--s) / 3);
                    padding-inline-start: 1em;
                    display: flex;
                    flex-direction: column;
                    gap: calc(var(--s) / 6);
                }
                > ul > li {
                    --type: -1;
                    --contrast: 0.8;
                    line-height: 1.35;
                }
            }

            /* ── PROFICIENCY / LANGUAGES ────────────────────────────
               Label left, dots right. min-width on dot rail prevents
               it from collapsing in narrow drawers. */
            .prof {
                list-style: none;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                gap: calc(var(--s) / 3);

                > li {
                    display: grid;
                    grid-template-columns: 1fr auto;
                    align-items: center;
                    gap: var(--s);

                    > span:first-child {
                        --type: -0.5;
                        font-weight: 600;
                    }
                }
            }

            .prof-dots {
                display: inline-flex;
                gap: 0.25em;
                list-style: none;
                margin: 0;
                padding: 0;

                > i {
                    inline-size: 0.5em;
                    block-size: 0.5em;
                    border-radius: 50%;
                    background: oklch(from var(--bg) calc(l - 0.04) calc(c * 0.4) h);
                }
            }
            .prof-dots[data-level="1"] > i:nth-child(-n+1),
            .prof-dots[data-level="2"] > i:nth-child(-n+2),
            .prof-dots[data-level="3"] > i:nth-child(-n+3),
            .prof-dots[data-level="4"] > i:nth-child(-n+4),
            .prof-dots[data-level="5"] > i:nth-child(-n+5),
            .prof-dots[data-level="6"] > i:nth-child(-n+6) {
                background: var(--Border);
            }

            /* ── STACK GROUPS ───────────────────────────────────────
               Tighter pills, smaller subheads. */
            .stack-grp {
                display: flex;
                flex-direction: column;
                gap: calc(var(--s) / 3);

                > h3 {
                    --type: -0.5;
                    --contrast: 0.85;
                    margin: 0;
                    font-weight: 700;
                }

                > .tags {
                    display: flex;
                    flex-wrap: wrap;
                    gap: calc(var(--s) / 3);
                }

                .tag {
                    --type: -2;
                    padding-inline: 0.55em;
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
    ### resume experience

    ```css
    @layer component.complex {
        /* Experience entry — resume/CV job block.
           Structure:
             .xp
               > header   (title+company on left, meta on right)
                   > .xp-title   (role + org)
                   > .xp-meta    (dates + location, right-aligned)
               > p            (summary)
               > ul           (bullets, optional)
               > .xp-tags     (skill pills, right-aligned)

           Composes with .surface for auto-nested background. */
        .xp {
            --space: 1;                 /* drives padding/gap via --s */

            display: flex;
            flex-direction: column;
            gap: var(--s);
            padding: var(--s);
            border-radius: var(--cfg-radius);
        }

        /* Header row: role block + meta block, space-between */
        .xp > header {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: var(--s);
        }

        .xp-title      { display: flex; flex-direction: column; gap: 0 }
        .xp-title > h3 { --type: 2; margin: 0; line-height: 1.1 }
        .xp-title > *:not(h3) { --contrast: 0.7 }   /* company name, subtitle */

        .xp-meta {
            display: flex;
            flex-direction: column;
            gap: 0;
            text-align: end;
            margin-inline-start: auto;  /* hard-right when header wraps */
        }
        .xp-meta > * { --type: -1; --contrast: 0.7 }

        /* Body text */
        .xp > p {
            --type: 0;
            line-height: 1.35;          /* tighter than default, readable */
            margin: 0;
        }

        /* Bullets — reset the list, space items with --s/2 */
        .xp > ul {
            margin: 0;
            padding-inline-start: 1.25em;
            display: flex;
            flex-direction: column;
            gap: calc(var(--s) / 2);
        }
        .xp > ul > li { --contrast: 0.85 }

        /* Skill tag row — right-aligned, tags inherit from component vars
           instead of being set per-span. Flip --xp-tag-color if you ever
           want the whole row quieter/louder in a single spot. */
        .xp-tags {
            --xp-tag-hue-shift: 15;
            --xp-tag-color: -0.1;

            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: calc(var(--s) / 2);
        }
        .xp-tags > .tag {
            --hue-shift: var(--xp-tag-hue-shift);
            --color: var(--xp-tag-color);
        }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### resume notes

    ```css
    @layer component.complex {
        /* Notes — scratchpad component. Originally built for a #nav drawer,
           now lives in a popover anchored to a FAB. Composes with .surface
           for auto-nested background, .popover for positioning/animation,
           and the existing --s / --border / --cfg-radius tokens.

           Two contexts handled in one rule:
             1. Bare .notes (drawer / dialog)        → fills container
             2. .notes.popover (FAB-anchored popup)  → bounded width, 5-row
                                                       textarea, surface bg
        */
        .notes {
            display: flex;
            flex-direction: column;
            gap: var(--s);
            block-size: 100%;       /* fill the drawer */
            min-block-size: 0;      /* allow the textarea middle to shrink */

            /* ── Header row: title + close button ─────────────────── */
            > header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: var(--s);

                h3 {
                    --type: 1;
                    margin: 0;
                }
            }

            /* ── Close button: borderless, no min-width ───────────── */
            .close {
                border-color: transparent;
                margin: 0;
            }

            /* ── Textarea: composes with .surface for auto bg ─────── */
            > textarea {
                flex: 1 1 auto;
                min-block-size: 0;
                inline-size: 100%;
                padding: var(--s);
                border: 0;
                border-radius: var(--cfg-radius);
                resize: none;
                font-family: var(--font-body);

                /* Caret tinted off the current --bg, --color: 0.4 equivalent.
                   Stays hue-aware with the rest of the system. */
                caret-color: oklch(from var(--bg) 65% 0.18 h);

                &::placeholder {
                    --contrast: 0.45;
                    color: currentColor;
                }

                &:focus-visible {
                    outline: 2px solid var(--border);
                    outline-offset: -2px;   /* inside — no border to sit beside */
                }
            }

            /* ══ Popover variant ═══════════════════════════════════════
               When .notes is also a .popover, override the drawer-style
               "fill container" behavior with a bounded geometry suitable
               for a FAB-anchored popup. */
            &.popover {
                --depth: 1;
                background: var(--bg);
                border: 1px solid var(--border);

                /* Fixed, intentional width — not driven by content */
                inline-size: min(95vw, 28rem);
                min-width: unset;
                max-width: unset;

                /* Drop the "fill the drawer" behavior */
                block-size: auto;

                > textarea {
                    flex: 0 0 auto;
                    inline-size: 100%;        /* fill the popover, don't size to content */
                    block-size: calc(5lh + 2 * var(--s));  /* explicit 5-line height */

                    /* Drop field-sizing — we want a fixed box, not a content-driven one */
                    field-sizing: normal;
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
    ### Popover - auto align
        [] test add timing to motion styles
        [] test auto layout

    ```css

    @layer component.simple {
      [popover].popover {
        position: fixed;
        inset: auto;
        margin: 0;
        border: 1px solid var(--border);
        min-width: clamp(10rem, 40vw, 18rem);
        max-width: min(90vw, 24rem);
        max-height: 80vh;
        overflow: auto;

        background: var(--bg);
        color: inherit;                          /* let --contrast cascade do its job */
        border-radius: var(--cfg-radius);
        box-shadow: 0 8px 24px oklch(from var(--bg) 10% 0.05 h / 0.3);
        padding: var(--s);

        opacity: 1;
        transform: scale(1);
        position-area: block-start inline-end;
        position-try-order: most-block-size;
        position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline;
        position-visibility: anchors-visible;

        transition:
          opacity   calc(var(--cfg-motion) * 0.18s) ease-out,
          transform calc(var(--cfg-motion) * 0.18s) ease-out,
          display   calc(var(--cfg-motion) * 0.18s) allow-discrete,
          overlay   calc(var(--cfg-motion) * 0.18s) allow-discrete;
      }

      [popover].popover:not(:popover-open) {
        opacity: 0;
        transform: scale(0.95);
      }

      [popover].popover.below-start { position-area: block-end inline-start; }
      [popover].popover.below-end   { position-area: block-end inline-end; }
      [popover].popover.above-start { position-area: block-start inline-start; }
      [popover].popover.above-end   { position-area: block-start inline-end; }
    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dialog
    ```css
    @layer component.complex {
        :where(dialog.modal) {
            border: 1px solid var(--border);
            border-radius: var(--cfg-radius);
            padding: 0;
            max-width: min(90vw,32rem);
            max-height: 85vh;
            overflow: auto;
            opacity: 1;
            transform: translateY(0);
            transition: opacity calc(var(--cfg-motion) * 0.25s) ease-out,transform calc(var(--cfg-motion) * 0.25s) ease-out,display calc(var(--cfg-motion) * 0.25s) allow-discrete,overlay calc(var(--cfg-motion) * 0.25s) allow-discrete;
            &:not([open]) {
                opacity: 0;
                transform: translateY(calc(var(--cfg-motion) * 0.5rem))
            }

            @starting-style {
                opacity: 0;
                transform: translateY(calc(var(--cfg-motion) * -0.5rem))
            }

            &::backdrop {
                background: transparent
            }
        }
    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7A utility.layout

    ```css

    @layer utility.layout {
        :where(.nowrap) { white-space: nowrap; }
        :where(.truncate) { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        :where(.mobile,.tablet,.desktop) { display: none }
        @media (         width <   480px) { :where(.mobile)  { display:revert-layer } }
        @media (480px <= width <  1024px) { :where(.tablet)  { display:revert-layer } }
        @media (         width >= 1024px) { :where(.desktop) { display:revert-layer } }

        @media print { :where(body) { min-height: 0 } } /* does this actualy do anything ? */
    }

    @layer utility.exceptions {
        :is(.vh) { inline-size: 0; block-size: 0; overflow: hidden; }
    }

    @layer utility.important {
        :where([hidden]) { display: none !important }
        @media print { :where(.np) { display: none !important } }
    }


    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## * Highlight js
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```noexport css
      /* highlight.css
      * Syntax highlight colors using OKLCH relative to --cfg-hue.
      *
      * Scheme: warm/cool split
      *   - Declarative tokens (keyword, function, class, decorator) → warm (+30 to +75°)
      *   - Data tokens (string, number, builtin) → cool (-30 to -60°)
      *   - Structural tokens (comment, operator, punctuation) → same as base hue
      *
      * Colors derive from var(--bg) on the originating <pre> so they follow the
      * current theme (lightness) and page hue automatically. Comments use alpha
      * to dim further without changing lightness.
      */

      /* ─── Python ──────────────────────────────────────────────────────────── */

      ::highlight(python-keyword)     { color: oklch(from var(--bg) 70% 0.19 calc(h + 45));  font-weight: 600; }
      ::highlight(python-string)      { color: oklch(from var(--bg) 70% 0.14 calc(h - 60)); }
      ::highlight(python-comment)     { color: oklch(from var(--bg) 55% 0.02 h / 0.6); font-style: italic; }
      ::highlight(python-number)      { color: oklch(from var(--bg) 73% 0.16 calc(h - 45)); }
      ::highlight(python-decorator)   { color: oklch(from var(--bg) 73% 0.17 calc(h + 60)); }
      ::highlight(python-function)    { color: oklch(from var(--bg) 70% 0.18 calc(h + 30));  font-weight: 600; }
      ::highlight(python-class)       { color: oklch(from var(--bg) 70% 0.16 calc(h + 75));  font-weight: 600; }
      ::highlight(python-builtin)     { color: oklch(from var(--bg) 68% 0.13 calc(h - 30)); }
      ::highlight(python-operator)    { color: oklch(from var(--bg) 60% 0.03 h); }
      ::highlight(python-punctuation) { color: oklch(from var(--bg) 55% 0.02 h); }

      /* ─── CSS ─────────────────────────────────────────────────────────────── */

      ::highlight(css-comment)        { color: oklch(from var(--bg) 55% 0.02 h / 0.6); font-style: italic; }
      ::highlight(css-string)         { color: oklch(from var(--bg) 70% 0.14 calc(h - 60)); }
      ::highlight(css-atrule)         { color: oklch(from var(--bg) 70% 0.19 calc(h + 45));  font-weight: 600; }
      ::highlight(css-var-name)       { color: oklch(from var(--bg) 73% 0.17 calc(h + 60)); }
      ::highlight(css-unit)           { color: oklch(from var(--bg) 68% 0.13 calc(h - 30)); }
      ::highlight(css-number)         { color: oklch(from var(--bg) 73% 0.16 calc(h - 45)); }
      ::highlight(css-property)       { color: oklch(from var(--bg) 70% 0.18 calc(h + 30)); }
      ::highlight(css-selector)       { color: oklch(from var(--bg) 70% 0.16 calc(h + 75));  font-weight: 600; }
      ::highlight(css-punctuation)    { color: oklch(from var(--bg) 55% 0.02 h); }

      /* ─── HTML ────────────────────────────────────────────────────────────── */

      ::highlight(html-comment)       { color: oklch(from var(--bg) 55% 0.02 h / 0.6); font-style: italic; }
      ::highlight(html-doctype)       { color: oklch(from var(--bg) 60% 0.03 h / 0.7); font-style: italic; }
      ::highlight(html-entity)        { color: oklch(from var(--bg) 73% 0.16 calc(h - 45)); }
      ::highlight(html-value)         { color: oklch(from var(--bg) 70% 0.14 calc(h - 60)); }
      ::highlight(html-tag)           { color: oklch(from var(--bg) 70% 0.18 calc(h + 30));  font-weight: 600; }
      ::highlight(html-attribute)     { color: oklch(from var(--bg) 73% 0.17 calc(h + 60)); }
      ::highlight(html-bracket)       { color: oklch(from var(--bg) 55% 0.02 h); }



    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```no export css
    .test_1 {
        --hue: 140;
        --color: .6;
        --contrast: 0;
        background-color: inherit;
    }
    .test_2 {
        --hue: 45;
        --color: .6;
        --contrast: 0;
        background-color: transparent;
    }
    .test_3 {
        --color: .6;
        --contrast: 0;
        background-color: inherit;
    }
    .test_4 {
        --color: .6;
        --contrast: 0;
        background-color: transparent;
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # HTML
    """)
    return


@app.cell
def _():
    from html_tags import html_doc, head, body, link, meta, Datastar, MeCSS, Pointer, html_to_tag
    from html_tags import h1, span, div, header, body, main, nav, aside, footer, link, a, svg, button 

    return (
        Datastar,
        MeCSS,
        Pointer,
        a,
        aside,
        body,
        button,
        div,
        footer,
        h1,
        head,
        header,
        html_doc,
        html_to_tag,
        link,
        main,
        nav,
    )


@app.cell
def _(html_to_tag):
    # Some icons
    home = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M4 20h16v2H4zm16-10h2v10h-2zM2 10h2v10H2zm2-2h2v2H4zm2-2h2v2H6zm2-2h2v2H8zm2-2h4v2h-4zm4 2h2v2h-2zm2 2h2v2h-2zm2 2h2v2h-2zM8 14h2v6H8zm2-2h4v2h-4zm4 2h2v6h-2z"/></svg>''')
    cal = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M5 4h14v2H5zm0 16h14v2H5zM3 10h2v10H3zm0-4h2v2H3zm16 0h2v2h-2zm0 4h2v10h-2zM3 8h18v2H3zm12-6h2v2h-2zM7 2h2v2H7zm0 10h2v2H7zm0 4h2v2H7zm4-4h2v2h-2zm0 4h2v2h-2zm4-4h2v2h-2z"/></svg>''')
    icon = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48"><g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"><path fill="#2f88ff" fill-rule="evenodd" stroke="#000" d="M17 14L44 24V44H17L17 14Z" clip-rule="evenodd"/><path stroke="#000" d="M17 14L4 24L4 44H17"/><path stroke="#fff" d="M35 44V32L26 29L26 44"/><path stroke="#000" d="M44 44H17"/></g></svg>''')
    return cal, home, icon


@app.cell
def _(
    Datastar,
    MeCSS,
    Pointer,
    a,
    aside,
    body,
    button,
    cal,
    div,
    footer,
    h1,
    head,
    header,
    home,
    html_doc,
    icon,
    link,
    main,
    nav,
):
    page = html_doc( 
            head(
                Datastar(), 
                MeCSS(), 
                Pointer(),
                link(rel="stylesheet", href="css.css")
            ), 
            body(cls = "surface")(
                header(id="header", cls="split")(
                    div(cls="flank")(
                        icon,
                        h1(cls="nowrap")("Demo Page")
                    ),
                    div(
                        button(cls="surface btn")("dark")
                       )
                ),
                nav(id = "nav", cls="stack")(

                    a(href="")(home, "home"),
                    a(href="")(cal, "home"),
                ),
                main(id = "main", cls = "surface")(
                    div(cls="cluster")(
                        div(cls="surface", style="--hue: 3")(
                            button(cls="btn")("button"),
                            button(cls="btn")(home),
                            button(cls="btn")("button"),
                        ) 
                    )
                ),
                aside(id = "aside", style = "--depth:3")("Aside with depth setting"),
                footer(id = "footer", cls="surface", style="--hue: 29")("Footer")
            )
        )


    write_html(page, "notebooks/index.html")
    return


@app.function
def write_html(html: str, path: str | Path) -> Path:
    from pathlib import Path
    p = Path(path)
    p.write_text(html, encoding="utf-8")
    return p


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
