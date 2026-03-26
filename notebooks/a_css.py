import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium", css_file="mmm.css")

with app.setup:
    # std lib
    import re, textwrap, logging, sys
    from pathlib import Path
    from dataclasses import dataclass, field

    # other
    from html_tags import setup_svg, setup_tags, HTML, Fragment, to_html, html_to_tag
    setup_tags(), setup_svg()

    # notebook settings
    DEFAULT_CSS_PATH = "output.css"


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This should be a nice way to use css and should overtime get better and better, and allow multiple people to work on asingle project because the convention is obvious and easy to catch on with.

    Naming conventions;
    ```css
    /*

    PREFIX       RULE
    --cfg-*      Core calc params. Set once.
    data-ui-*    User prefs. HTML attributes.
    --*          Public. Set freely. Core eats.
    --_*         Private. Don't touch. Ever.

    */
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # CSS
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 0 @Properties
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Registered properties
    ```css
    /* must be on root ie. can not be in a layer */

    /* public: the five knobs */
    @property --hue       { syntax: "<number>";  inherits: true;  initial-value: 250; }
    @property --surface   { syntax: "<number>";  inherits: true;  initial-value: 0; }
    @property --type      { syntax: "<number>";  inherits: false; initial-value: 0; }

    /* config */
    @property --chroma         { syntax: "<number>";  inherits: true;  initial-value: 0.02; }
    @property --cfg-dark       { syntax: "<number>";  inherits: true;  initial-value: 0; }
    @property --cfg-motion     { syntax: "<number>"; inherits: true;  initial-value: 1; }
    @property --cfg-type-scale { syntax: "<number>";  inherits: true;  initial-value: 1; }

    /* private: contrast */
    @property --_contrast  { syntax: "<number>";  inherits: true;  initial-value: 0.01; }
    @property --_hue-shift { syntax: "<number>";  inherits: true;  initial-value: 1; }

    /* private: leapfrog state */
    @property --_depth-a  { syntax: "<integer>"; inherits: true;  initial-value: 0; }
    @property --_depth-b  { syntax: "<integer>"; inherits: true;  initial-value: 0; }
    @property --_parity   { syntax: "<integer>"; inherits: true;  initial-value: 0; }
    @property --_bg       { syntax: "<color>";   inherits: true;  initial-value: oklch(95% 0.02 250); }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1 Layer Definition
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1 Layer order
    ```css
    @layer reset.fix,          /* FIX CSS Working group admitted mistakes */
           reset.opinion,      /* Project Specific Global Resets  */
           core.config,        /* --cfg variable that set the math in the core "engine" and data-ui settings */
           core.color,         /* Complex but user friendly color engine bg & contrast conrtol everything */
           core.type,          /* --type fluid system */
           core.spacing,       /* -- fluid spacing & fixed */
           theme,              /* theme should be quite minimal... */
           layout.page,        /* Page Level Layout decisions...RULE-only target by id here */
           layout.composition, /* how components will fill out */
           component.complex,  /* Components that are complex... */
           component.simple,   /* Classic layout building blocks... */
           utility;            /* Use this — don't use !important anywhere... */
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2 Reset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2a Reset.fix
    [these should not be controvosial](https://wiki.csswg.org/ideas/mistakes/)
    ```css
    @layer reset.fixes {
        *, *::before, *::after { box-sizing: border-box; margin: 0; background-repeat: no-repeat; }
        :root { interpolate-size: allow-keywords; }
        :where(html) { color-scheme: light dark; line-height: 1.5; -moz-text-size-adjust: none; -webkit-text-size-adjust: none; text-size-adjust: none; }
        :where(body, figure, blockquote, dl, dd, p) { margin-block-end: 0; }
        :where(img, picture, svg) { max-width: 100%; display: block; height: auto; }
        :where(table, thead, tbody, tfoot, tr) { isolation: isolate; }
        :where(input, button, textarea, select) { font: inherit; }
    }
    ```

    2b Reset.opinion
    change these for your project
    ```css
    @layer reset.opinion {
        :where(html) { scrollbar-width: thin; }
        :where(p) { text-wrap: pretty; }
        :where(h1, h2, h3, h4, h5, h6) { text-wrap: balance; }
        :where(body) { overflow-wrap: break-word; }             /* Prevent long strings from blowing out layouts */
        :where(img, picture, video, canvas, svg) { height: auto; }                  /* Preserve aspect ratios — height: auto is the missing piece */
        :where(svg) { color: currentColor; }                     /* SVG inherits text color by default — use color not fill for stroke compadibility */
        :where(button, [role="button"], summary, label[for],  input[type="file"]::file-selector-button) { cursor: pointer; } /* Cursor affordance for interactive elements */
        :where(:disabled, [aria-disabled="true"]) { cursor: not-allowed; }          /* Disable cursor on disabled elements */
        :where(table) { border-collapse: collapse; }            /* Universal table opinion — almost no one wants separated borders */
        :where(fieldset) { border: 0; padding: 0; margin: 0; min-inline-size: 0; }  /* Strip fieldset chrome — you'll restyle in components */
        :where(legend) { padding: 0; }                          /* Strip fieldset chrome — you'll restyle in components */
        :where(textarea) { resize: vertical; }                  /* Sensible textarea resize constraint */
        :where(textarea:not([rows])) { min-block-size: 10em; }  /* Sensible textarea resize constraint */
        :where(abbr[title]) { cursor: help; text-decoration: underline dotted; }   /* Abbreviation affordance */
        :where(summary) { list-style: none; }                   /* only if you want full control */
        :where(a) {text-decoration: none; }                     /* No underline on links */

        :where(input) { autofill:shadow-[inset_0_0_0px_1000px_var(--bg_color)]  } /* [todo: autofill black magic not sure about] */

        /* Remove list semantics reset — use the :where([role="list"]) pattern
           so VoiceOver doesn't strip semantics when you remove list-style in CSS */
        :where(ul, ol):where([role="list"]) { list-style: none; padding: 0; }

        /* Hidden attribute should always mean hidden  */
        :where([hidden]) { display: none; }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3 Core
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3a core.config
    ```css
    @layer core.config {

      :root {
        --cfg-dark: 0;
        --cfg-motion: 1;

        /* surface curve: two numbers drive light ↔ dark */
        --_surf-base: calc(95% - var(--cfg-dark) * 82%);
        --_surf-step: calc(-2.5% + var(--cfg-dark) * 6.5%);

        /* type */
        --cfg-fluid-min-vp:  22.5rem;
        --cfg-fluid-max-vp:  77.5rem;
        --cfg-type-min:       1.125rem;
        --cfg-type-max:       1.25rem;
        --cfg-type-min-ratio: 1.2;
        --cfg-type-max-ratio: 1.25;

        /* shape */
        --cfg-radius: 0.375rem;
      }

      @media (prefers-color-scheme: dark)     { :root { --cfg-dark: 1; } }
      @media (prefers-reduced-motion: reduce) { :root { --cfg-motion: 0; } }

      html[data-ui-scheme="dark"]  { --cfg-dark: 1; }
      html[data-ui-scheme="light"] { --cfg-dark: 0; }
      html[data-ui-motion="none"]  { --cfg-motion: 0; }


    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3b. core.color

    ```css
    @layer core.color {

      :where(*) {
        --_bg: oklch(
          clamp(10%, calc(var(--_surf-base) + var(--surface) * var(--_surf-step)), 99%)
          var(--chroma)
          var(--hue)
        );
        background: var(--_bg);
        color: oklch(from var(--_bg)
          calc(l + (clamp(0, calc((0.5 - l) * 999), 1) - l) * var(--contrast))
          calc(c * (1 - var(--contrast)))
          h
        );
      }

      /* ── fill: vibrant bg, auto-contrast text ──
         Bypasses the surface staircase.
         Lands at a fixed mid-lightness with real chroma.
         --hue and --chroma still work. Text still derives. */

      .fill {
        --_bg: oklch(
          calc(65% - var(--cfg-dark) * 15%)
          max(var(--chroma), 0.12)
          var(--hue)
        );
        background: var(--_bg);
      }


      /* ── leapfrog: parity 0 ── */

      @container style(--_parity: 0) {
        .surface {
          --_depth-b: calc(var(--_depth-a) + 1);
          --surface: var(--_depth-b);
          --_parity: 1;
        }
        .well {
          --_depth-b: calc(var(--_depth-a) - 1);
          --surface: var(--_depth-b);
          --_parity: 1;
        }
      }

      /* ── leapfrog: parity 1 ── */

      @container style(--_parity: 1) {
        .surface {
          --_depth-a: calc(var(--_depth-b) + 1);
          --surface: var(--_depth-a);
          --_parity: 0;
        }
        .well {
          --_depth-a: calc(var(--_depth-b) - 1);
          --surface: var(--_depth-a);
          --_parity: 0;
        }
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3c. core.type

    ```css
    @layer core.type {
      body,
      :where(h1, h2, h3, h4, h5, h6, small, .icon-btn),
      :where([style*="--type:"]) {
        --_t-min: calc(var(--cfg-type-min) * pow(var(--cfg-type-min-ratio), var(--type)));
        --_t-max: calc(var(--cfg-type-max) * pow(var(--cfg-type-max-ratio), var(--type)));
        font-size: calc(
          clamp(var(--_t-min),
            calc(var(--_t-min) + (var(--_t-max) - var(--_t-min)) *
              (100vi - var(--cfg-fluid-min-vp)) /
              (var(--cfg-fluid-max-vp) - var(--cfg-fluid-min-vp))),
            var(--_t-max)
          ) * var(--cfg-type-scale)
        );
        letter-spacing: calc(0.01em - var(--type) * 0.01em);
        line-height: calc(1.5 - var(--type) * 0.075);
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3d. core.space

    ```css
    @layer core.spacing {
      :root {
        --space-0: clamp(0.5rem, 0.409rem + 0.364vi, 0.75rem);
        --space-1: clamp(0.7rem, 0.473rem + 0.909vi, 1.238rem);
        --space-2: clamp(0.98rem, 0.48rem + 2vi, 2.042rem);
        --space-3: clamp(1.372rem, 0.382rem + 3.959vi, 3.369rem);
      }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4 Theme
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4 Theme

    ```css
    @layer theme {
      :root {

          /* Open Props Fonts */
        --font-system-ui: system-ui, sans-serif;
        --font-transitional: Charter, Bitstream Charter, Sitka Text, Cambria, serif;
        --font-old-style: Iowan Old Style, Palatino Linotype, URW Palladio L, P052, serif;
        --font-humanist: Seravek, Gill Sans Nova, Ubuntu, Calibri, DejaVu Sans, source-sans-pro, sans-serif;
        --font-geometric-humanist: Avenir, Montserrat, Corbel, URW Gothic, source-sans-pro, sans-serif;
        --font-classical-humanist: Optima, Candara, Noto Sans, source-sans-pro, sans-serif;
        --font-neo-grotesque: Inter, Roboto, Helvetica Neue, Arial Nova, Nimbus Sans, Arial, sans-serif;
        --font-monospace-slab-serif: Nimbus Mono PS, Courier New, monospace;
        --font-monospace-code: Dank Mono, Operator Mono, Inconsolata, Fira Mono, ui-monospace, SF Mono,Monaco, Droid Sans Mono, Source Code Pro, Cascadia Code,Menlo, Consolas, DejaVu Sans Mono, monospace;
        --font-industrial: Bahnschrift, DIN Alternate, Franklin Gothic Medium, Nimbus Sans Narrow, sans-serif-condensed, sans-serif;
        --font-rounded-sans: ui-rounded, Hiragino Maru Gothic ProN, Quicksand, Comfortaa, Manjari, Arial Rounded MT, Arial Rounded MT Bold, Calibri, source-sans-pro, sans-serif;
        --font-slab-serif: Rockwell, Rockwell Nova, Roboto Slab, DejaVu Serif, Sitka Small, serif;
        --font-antique: Superclarendon, Bookman Old Style, URW Bookman, URW Bookman L, Georgia Pro, Georgia, serif;
        --font-didone: Didot, Bodoni MT, Noto Serif Display, URW Palladio L, P052, Sylfaen, serif;
        --font-handwritten: Segoe Print, Bradley Hand, Chilanka, TSCu_Comic, casual, cursive;


          /* Theme */
        --font-body:    var(--font-geometric-humanist);
        --font-heading: var(--font-didone);
        --font-mono:    var(--font-monospace-code)
      }

      body  {               font-family: var(--font-body); }
      h1    { --type:  2.0; font-family: var(--font-heading); }
      h2    { --type:  1.4; font-family: var(--font-heading); }
      h3    { --type:  1.2; font-family: var(--font-heading); }
      h4    { --type:  1.0; font-family: var(--font-heading); }
      p     { --type:  0.8; font-family: var(--font-body); }
      small { --type: -2.0; font-family: var(--font-heading); text-transform: uppercase }
      code  { --type: -0.8; font-family: var(--font-mono) }
      pre   { --type: -0.8; font-family: var(--font-mono) }

    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5 Layout
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5a. Layout.page
    [] dashboard
    [] landing
    Q: Drawers here or Components?
    ```css
    @layer layout.page{
        :where(body.dashboard) {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            overscroll-behavior: none;
            display: grid;
            grid-template:
                "header   header  header" auto
                "nav      main    aside"  1fr
                "footer   footer  footer" auto
                / auto    1fr     auto;
            height: 100svh;
            padding: 0;
            margin: 0;

            dialog::backdrop {
                background-color: light-dark(
                    rgba(0, 0, 0, 0.7),
                    rgba(0, 0, 0, 0.8)
                );
            }

            #header {
                grid-area: header;
            }
            #main {
                grid-area: main;
            }
            #nav {
                grid-area: nav;
            }
            #aside {
                grid-area: aside;
            }
            #footer {
                grid-area: footer;
            }
        }
    }

    ```

    5b. Layout.composition

    ```css
    @layer composition {
      /* containers */
      .stack { display: flex; flex-direction: column; gap: var(--_gap, .75rem); }
      .row   { display: flex; flex-wrap: wrap; gap: var(--_gap, .5rem); }
      .split { display: flex; flex-wrap: wrap; justify-content: space-between; gap: var(--_gap, .5rem); }
      .grid  { display: grid; grid-template-columns: repeat(auto-fit, minmax(var(--_col, 15rem), 1fr)); gap: var(--_gap, 1rem); }
      .flank { display: flex; flex-wrap: wrap; gap: var(--_gap, 1rem); }
      .flank > :first-child { flex: 1 1 var(--_flank, auto); }
      .flank > :last-child { flex: 999 1 0; }
      .flank-end { display: flex; flex-wrap: wrap; gap: var(--_gap, 1rem); }
      .flank-end > :first-child { flex: 999 1 0; }
      .flank-end > :last-child { flex: 1 1 var(--_flank, auto); }
      /* modifiers */
      .span { grid-column: 1 / -1; }
      .wrap { flex-wrap: wrap; } .nowrap { flex-wrap: nowrap; }
      /* alignment */
      .ai-start { align-items: flex-start; } .ai-center { align-items: center; } .ai-end { align-items: flex-end; } .ai-baseline { align-items: baseline; } .ai-stretch { align-items: stretch; }
      .jc-start { justify-content: flex-start; } .jc-center { justify-content: center; } .jc-end { justify-content: flex-end; } .jc-between { justify-content: space-between; } .jc-around { justify-content: space-around; } .jc-evenly { justify-content: space-evenly; }
      .as-start { align-self: flex-start; } .as-center { align-self: center; } .as-end { align-self: flex-end; } .as-baseline { align-self: baseline; } .as-stretch { align-self: stretch; }
    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 6 Components
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6a. Components.complex

    ### Data Table
    ```css
    @layer components.complex {
       .datatable { }
    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6b. Components.simple

    ### Card
    ```css
    @layer components.simple {
       .card {
        padding: var(--space-1);
        border-radius: var(--cfg-radius);
      }
    ```

    ### Icon Button
    ```css
    /* ICON BUTTON */
    @layer components.simple {
      .icon-btn {
        /* ─── knobs ─── */
        --type:        0;
        --_ib-color:   inherit;
        --_ib-bg:      transparent;
        --_ib-radius:  100vw;
        --_ib-opacity: 1;
        --_ib-cursor:  pointer;
        --_ib-em:      2.5em;

        /* ─── override ripple knobs ─── */
        --_rp-size:    130%;

        /* ─── layout ─── */
        align-items: center;
        aspect-ratio: 1;
        display: inline-flex;
        justify-content: center;
        padding: 0;
        border: 0;

        /* ─── driven by knobs ─── */
        background-color: var(--_ib-bg);
        border-radius:    var(--_ib-radius);
        color:            var(--_ib-color);
        cursor:           var(--_ib-cursor);
        inline-size:      var(--_ib-em);
        opacity:          var(--_ib-opacity);

        & > svg { inline-size: 1em; block-size: 1em; }

        /* ─── states ─── */
        &[disabled] {
          --_ib-color:   light-dark(rgb(0 0 0 / .3), rgb(255 255 255 / .26));
          --_ib-cursor:  not-allowed;
          --_ib-opacity: .64;
        }

        &.dormant { --_ib-color: var(--border-color); --_ib-opacity: .8; }
        &.active  { --_ib-color: var(--color-7); }
        &.small   { --type: -1; }
      }
    }
    ```

    ### Badge
    ```css
    @layer components.simple {
      .badge {
        display: inline-block;
        padding: 0.15em 0.6em;
        border-radius: 999px;
        --type: -2;
      }
    }
    ```

    ### Divider
    ```css
    @layer components.simple {
      .divider {
        border: none;
        border-block-start: 1px solid oklch(from var(--_bg) calc(l + 0.08) c h);
      }
    }
    ```

    ### Popover auto align
    ```css
    @layer components.simple {
      [popover].popover { position: fixed; inset: auto; margin: 0; border: none; min-width: clamp(10rem, 40vw, 18rem); max-width: min(90vw, 24rem); max-height: 80vh; overflow: auto; --_bg: --surface(1); background: var(--_bg); color: --contrast(0.7); border-radius: 0.5rem; box-shadow: --shadow(5); padding: --space(1); opacity: 1; transform: scale(1); position-area: self-block-start self-inline-end; position-try-order: most-block-size; position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline; position-visibility: anchors-visible; transition: opacity calc(var(--_motion) * 0.18s) ease-out, transform calc(var(--_motion) * 0.18s) ease-out, display calc(var(--_motion) * 0.18s) allow-discrete, overlay calc(var(--_motion) * 0.18s) allow-discrete; }
      [popover].popover:not(:popover-open) { opacity: 0; transform: scale(0.95); }
      [popover].popover.below-start { position-area: self-block-end self-inline-start; }
      [popover].popover.below-end { position-area: self-block-end self-inline-end; }
      [popover].popover.above-start { position-area: self-block-start self-inline-start; }
      [popover].popover.above-end { position-area: self-block-start self-inline-end; }
    }
    ```

    ## 6c. components.utls
    ```css

    /* ─── ripple primitive ─── */
    @layer components.utls {
      .ripple {
        --_rp-size:     150%;
        --_rp-bg:       oklch(0.6 0 0 / 0.2);
        --_rp-speed:    calc(0.2s * var(--cfg-motion));
        --_rp-ease:     ease-out;
        --_rp-scale:    0.01;
        --_rp-z:        -1px;

        --isLTR: 1;
        --isRTL: -1;

        position: relative;
        transform-style: preserve-3d;

        &:dir(rtl) {
          --isLTR: -1;
          --isRTL: 1;
        }

        &:not([disabled]) {
          &:hover   { --_rp-scale: 1; }
          &:active  { --_rp-scale: 1.1; }

          &::before {
            background-color: var(--_rp-bg);
            block-size:       var(--_rp-size);
            clip-path:        circle(50%);
            content:          "\";
            inline-size:      var(--_rp-size);
            inset-block-start:  50%;
            inset-inline-start: 50%;
            position:         absolute;
            transform-origin: center center;
            transform:
              translateX(calc(var(--isRTL) * 50%))
              translateY(-50%)
              translateZ(var(--_rp-z))
              scale(var(--_rp-scale));
            transition: transform var(--_rp-speed) var(--_rp-ease);
            will-change: transform;
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
    # 7 Utility
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7a. utility.layout
    single purpose utilities
    ```css
    @layer utility.layout {
      :where(.mobile, .tablet, .desktop) { display: none; }
      @media (width < 768px)           { :where(.mobile)  { display: revert-layer; } }
      @media (768px <= width < 1024px) { :where(.tablet)  { display: revert-layer; } }
      @media (width >= 1024px)         { :where(.desktop) { display: revert-layer; } }
    }
    ```

    ## 7b. utility.exceptions
    Ideally this is empty but in time crunch you can use
    ```css
    @layer utility.exceptions {
      :where(.vh) { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0; }
    }
    ```


    ## 7b. utility.important
    Use this only when you need to be sure to beat inline styles
    ```css
    @layer utility.important {
      :where([hidden]) { display: none !important; }
      @media print { :where(.np) { display: none !important; } }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Component Testing
    """)
    return


@app.cell
def _(
    Body,
    Head,
    Html,
    Iframe,
    Meta,
    Style,
    extract_lang_blocks,
    extract_md_blocks,
    read_file,
):
    def create_isolated_component(*content):
        """Create a component in an isolated iframe, CSS extracted live from this notebook."""
        import base64

        # Same pattern as the export pipeline — always fresh from source
        _source = read_file()
        _md_blocks = extract_md_blocks(_source)
        _css = "\n".join(extract_lang_blocks(_md_blocks, "css"))

        document = Html(
            Head(
                Meta(charset="utf-8"),
                Meta(name="viewport", content="width=device-width, initial-scale=1"),
                Style(_css)
            ),
            Body(*content)
        )

        html_string = to_html(document)
        encoded_html = base64.b64encode(html_string.encode("utf-8")).decode("utf-8")
        data_url = f"data:text/html;base64,{encoded_html}"

        return Iframe(
            src=data_url,
            style="""
    display: block;
      inline-size: 100%;
      block-size: 100cqb;
      border: none;
      margin-block:-1rem;
      width: 100%
      height: 100%
                """
        
        )

    return (create_isolated_component,)


@app.cell
def _():
    icon_ski = html_to_tag("""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cable-car-icon lucide-cable-car"><path d="M10 3h.01"/><path d="M14 2h.01"/><path d="m2 9 20-5"/><path d="M12 12V6.5"/><rect width="16" height="10" x="4" y="12" rx="3"/><path d="M9 12v5"/><path d="M15 12v5"/><path d="M4 17h16"/></svg>""")
    return (icon_ski,)


@app.cell
def _(
    A,
    Aside,
    Body,
    Button,
    Div,
    H1,
    H2,
    Header,
    Li,
    Main,
    Nav,
    Section,
    Small,
    Strong,
    Ul,
    create_isolated_component,
    icon_ski,
):
    HTML(
        create_isolated_component(
            Body(cls="dashboard", style="height=100svh, --color: red")(
                Header(cls="split", id="header")(
                    H1("Logo"),
                    Div(
                        Button("Login"),
                        Button("Sign Up")
                    )
                      ),
                Nav(id="nav")(
                    Ul(
                        Li(A("Demo1")),
                        Li(A("Demo2")),
                        Li(A("Demo3")),
                    )
                ),
                Main(id="main", cls="surface")(
                    Section(
                        H2("Components.simple"),
                        Button("im a button", cls="surface"),
                        Button(cls="icon-button")(icon_ski)
                    )
                ),
                Aside(id="aside")(
                    Ul(style=" list-style: none; padding: 0; margin: 1rem;}")(
                        Li(Strong(Small("on this page"))),
                        Li(Small("Definitions")),
                        Li(Small("Examples")),
                        Li(Small("Code"))
                    )
                )
            )
        )
    )
    return


@app.cell
def _(Button, Svg):
    to_html(Button(cls="icon-button")(
                           Svg("""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cable-car-icon lucide-cable-car"><path d="M10 3h.01"/><path d="M14 2h.01"/><path d="m2 9 20-5"/><path d="M12 12V6.5"/><rect width="16" height="10" x="4" y="12" rx="3"/><path d="M9 12v5"/><path d="M15 12v5"/><path d="M4 17h16"/></svg>""")
                        ))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # III Export your css
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Export functions
    """)
    return


@app.cell
def _():
    def read_file(path: str = __file__) -> str:
        return Path(path).read_text()
    
    def extract_md_blocks(source: str) -> list[str]:
        pattern = r'mo\.md\(r"""\n(.*?)"""'
        return re.findall(pattern, source, flags=re.DOTALL)
    
    def extract_lang_blocks(blocks: list[str], lang: str) -> list[str]:
        pattern = rf'```{lang}\n(.*?)```'
        result = []
        for block in blocks:
            result.extend(re.findall(pattern, block, flags=re.DOTALL))
        return result
    
    def write_file(blocks: list[str], path: str) -> None:
        _path = Path(path)
        _path.parent.mkdir(parents=True, exist_ok=True)
        _path.write_text("\n".join(blocks))
    
    def get_css() -> str:
        """Extract and return all CSS blocks from this notebook."""
        return "\n".join(extract_lang_blocks(extract_md_blocks(read_file()), "css"))

    def export_css(path: str | None = None) -> str:
        """Write CSS to path (creates dirs). Returns the path used."""
        _path = path or _DEFAULT_CSS_PATH
        write_file([get_css()], _path)
        return _path

    def download_css(filename: str | None = None) -> str:
        """Save CSS to the user's Downloads folder. Returns the path used."""
        _filename = filename or Path(_DEFAULT_CSS_PATH).name
        _path = Path.home() / "Downloads" / _filename
        write_file([get_css()], str(_path))
        return str(_path)

    

    return extract_lang_blocks, extract_md_blocks, read_file, write_file


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## CSS Check
    """)
    return


@app.cell
def _():
    SKIP = {
        ".venv",
        "docs/wasm",
    }

    @dataclass
    class Issue:
        file: str
        line: int
        level: str
        msg: str

    def find_root(start: Path = None, marker: str = "pyproject.toml") -> Path:
        p = (start or Path.cwd()).resolve()
        for parent in [p, *p.parents]:
            if (parent / marker).exists():
                return parent
        raise FileNotFoundError(f"No {marker} found in {p} or any parent directory")

    def should_skip(path: Path, root: Path) -> bool:
        rel = str(path.relative_to(root))
        return any(rel.startswith(s) for s in SKIP)

    def lint_css(path: Path) -> list[Issue]:
        issues = []
        lines = path.read_text().splitlines()

        for i, ln in enumerate(lines, 1):
            if re.search(r'var\(--_[\w-]+\)(?!.*,)', ln):
                issues.append(Issue(path.name, i, "warn", "private knob with no fallback"))
            if re.search(r'(?<!-)#[0-9a-fA-F]{3,8}\b', ln):
                issues.append(Issue(path.name, i, "warn", "raw hex color — use token?"))
            if re.search(r'\b\d+px\b', ln) and '--cfg' not in ln:
                issues.append(Issue(path.name, i, "warn", "px unit — intentional?"))
            if re.search(r'transition.*\d+(\.\d+)?s', ln) and '--cfg-motion' not in ln:
                issues.append(Issue(path.name, i, "error", "timing without --cfg-motion multiplier"))

        return issues

    return SKIP, find_root, lint_css, should_skip


@app.cell
def _(SKIP, find_root, lint_css, should_skip):
    def check_css():
        root = find_root()
        print(f"Project root: {root}\n")

        if sys.argv[1:]:
            paths = [Path(p) for p in sys.argv[1:]]
        else:
            paths = sorted(p for p in root.rglob("*.css") if not should_skip(p, root))

        total = 0
        for p in paths:
            issues = lint_css(p)
            if not issues:
                continue
            rel = p.relative_to(root)
            print(f"{rel}")
            for iss in issues:
                icon = "❌" if iss.level == "error" else "⚠️"
                print(f"  {icon} :{iss.line} — {iss.msg}")
            print()
            total += len(issues)

        scanned = len(list(p for p in root.rglob("*.css") if not should_skip(p, root)))
        print(f"{total} issue{'s' * (total != 1)} found across {scanned} CSS files")
        print(f"Skipped: {', '.join(sorted(SKIP))}")
        return 

    return (check_css,)


@app.cell
def _(check_css):
    check_css()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Export Marimo ui elements
    """)
    return


@app.cell
def _(mo):
    export_btn   = mo.ui.run_button(label="Export")
    download_btn = mo.ui.run_button(label="Download CSS")
    export_path  = mo.ui.text(value="static/style.css", placeholder="output.css")
    return export_btn, export_path


@app.cell
def ui_sidebar(
    export_btn,
    export_path,
    extract_lang_blocks,
    extract_md_blocks,
    mo,
    read_file,
    write_file,
):
    _source = read_file()
    _css_content = "\n".join(extract_lang_blocks(extract_md_blocks(_source), "css"))

    _DEFAULT_CSS_PATH = "output.css"
    _resolved_path = export_path.value.strip() or _DEFAULT_CSS_PATH

    if export_btn.value:
        write_file([_css_content], _resolved_path)
        _msg = mo.md(f"✅ CSS exported to `{_resolved_path}`")
    else:
        _msg = mo.md("")

    _export_ui = mo.hstack([export_path, export_btn])
    _download_ui = mo.download(
        data=_css_content.encode(),
        filename=Path(_resolved_path).name,
        mimetype="text/css",
        label="Download CSS"
    )

    ui_footer = mo.vstack([_msg, _export_ui, _download_ui], justify="end")

    mo.sidebar(
        mo.vstack([
            mo.outline(label="Table of contents"),
            mo.Html("<div style='flex: 1'></div>"),
            ui_footer,
        ])
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
