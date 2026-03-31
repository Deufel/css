import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium", css_file="", auto_download=["html"])

with app.setup:
    # std lib
    import re, textwrap, logging, sys
    from pathlib import Path
    from dataclasses import dataclass, field

    # other
    from html_tags import setup_svg, setup_tags, HTML, Fragment, to_html, html_to_tag, pretty
    setup_tags(), setup_svg()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This should be a nice way to use css and should overtime get better and better, and allow multiple people to work on asingle project because the convention is obvious and easy to catch on with.
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
    /* ══════════════════════════════════════════════════════════════════════
       @property registrations
       ─────────────────────────────────────────────────────────────────
        > must be defined outside of all selectors
        > naming convention: [this is still very fluid]
           --[var]      developer-facing knobs, set freely on elements as you want
           --cfg-[var]  config — change at your own peril, used in color math
           --_[var]     internal intermediary, basically never touch
    ══════════════════════════════════════════════════════════════════════ */

    @property --type      { syntax: "<number>"; inherits: false; initial-value: 0; }
    @property --cfg-motion     { syntax: "<number>"; inherits: true; initial-value: 1; }
    @property --cfg-type-scale { syntax: "<number>"; inherits: true; initial-value: 1; }

    @property --hue          { syntax: "<number>"; inherits: true;  initial-value: 220; }
    @property --hue-shift    { syntax: "<number>"; inherits: true;  initial-value: 0; }
    @property --chroma-shift { syntax: "<number>"; inherits: true;  initial-value: 0; }
    @property --l-shift      { syntax: "<number>"; inherits: true;  initial-value: 0; }
    @property --depth        { syntax: "<number>"; inherits: true;  initial-value: 0; }
    @property --contrast     { syntax: "<number>"; inherits: true;  initial-value: 9; }

    @property --cfg-dark         { syntax: "<number>"; inherits: true; initial-value: 0; }
    @property --cfg-surf-chroma  { syntax: "<number>"; inherits: true; initial-value: 0.015; }
    @property --cfg-color-chroma { syntax: "<number>"; inherits: true; initial-value: 0.14; }
    @property --cfg-color-l      { syntax: "<percentage>"; inherits: true; initial-value: 68%; }
    @property --cfg-radius       { syntax: "<length>"; inherits: true; initial-value: 6px; }

    @property --_l      { syntax: "<percentage>"; inherits: true; initial-value: 87%; }
    @property --_c      { syntax: "<number>";  inherits: true; initial-value: 0.015; }
    @property --_bg     { syntax: "<color>";   inherits: true; initial-value: oklch(87% 0.015 220); }
    @property --_even   { syntax: "<integer>"; inherits: true; initial-value: 0; }
    @property --_odd    { syntax: "<integer>"; inherits: true; initial-value: 0; }
    @property --_parity { syntax: "<integer>"; inherits: true; initial-value: 0; }



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
           component.utls,    /* Component helpers ripple efect for example */
           utility.layout,    /* layout utls some media qs  */
           utility.exceptions, /* incase of emergency break glass  */
           utility.important;  /* Only use for when you actually NEED to overwrite an inline style.. */
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
    @layer reset.fix {
        *, *::before, *::after { box-sizing: border-box; margin: 0; background-repeat: no-repeat; }
        :root { interpolate-size: allow-keywords; }
        :where(html) { color-scheme: light dark; line-height: 1.5; -moz-text-size-adjust: none; -webkit-text-size-adjust: none; text-size-adjust: none; }
        :where(body, figure, blockquote, dl, dd, p) { margin-block-end: 0; }
        :where(img, picture, svg) { max-width: 100%; display: block; height: auto; }
        :where(table, thead, tbody, tfoot, tr) { isolation: isolate; }
        :where(input, button, textarea, select) { font: inherit; }
    }
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    2b Reset.opinion
    change these for your project
    ```css
    @layer reset.opinion {
        :where(body) { min-height: 100svh; }
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

        :where(input):autofill { box-shadow: inset 0 0 0 1000px var(--_bg); } /* [todo: autofill black magic not sure about] */
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
        /* color */
        --_surf-base: calc(87% - var(--cfg-dark) * 75%);
        --_l: var(--_surf-base);
        --_c: var(--cfg-surf-chroma);

        /* type */
        --cfg-fluid-min-vp:  22.5rem;
        --cfg-fluid-max-vp:  77.5rem;
        --cfg-type-min:       1.0625rem;
        --cfg-type-max:       1.1875rem;
        --cfg-type-min-ratio: 1.2;
        --cfg-type-max-ratio: 1.28;
        --cfg-type-scale: 1;

        --cfg-radius: 0.5rem;
      }

      @media (prefers-color-scheme: dark) { :root { --cfg-dark: 1; } }
      html[data-ui-scheme="dark"]  { --cfg-dark: 1; }
      html[data-ui-scheme="light"] { --cfg-dark: 0; }
    }

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3b. core.color

    ```css
    @layer core.color {

      /*.pri, .sec, .ter { --_l: var(--cfg-color-l); --_c: var(--cfg-color-chroma); }*/
      :is(button, .badge, .avatar, .btn):is(.pri, .sec, .ter),
      :is(.pri, .sec, .ter) :is(button, .badge, .avatar, .btn) {
        --_l: var(--cfg-color-l); --_c: var(--cfg-color-chroma);
      }

      .layer { --_l: calc(var(--_surf-base) + var(--depth) * 2.5%); }

      :where(*) {
        --_bg: oklch(
          clamp(10%, calc(var(--_l) + var(--l-shift) * 100%), 99%)
          calc(var(--_c) + var(--chroma-shift))
          calc(var(--hue) + var(--hue-shift))
        );
        --border: oklch(from var(--_bg) calc(l - 0.09 + var(--cfg-dark) * 0.20) var(--cfg-surf-chroma) h);
        --Border: oklch(from var(--_bg) calc(l - 0.09 + var(--cfg-dark) * 0.20) var(--cfg-color-chroma) h);
        background: var(--_bg);
        color: oklch(from var(--_bg)
          calc(l + (clamp(0, calc((0.5 - l) * 999), 1) - l) * var(--contrast))
          calc(c * (1 - var(--contrast))) h
        );
      }

      html[data-ui-color-palette="mono"]   { .sec { --chroma-shift:   0.03; }  .ter { --chroma-shift:    -0.03; } }
      html[data-ui-color-palette="comp"]   { .sec { --hue-shift:  180; }   .ter { --hue-shift:    0; --l-shift: 0.02; } }
      html[data-ui-color-palette="triad"]  { .sec { --hue-shift:  120; }   .ter { --hue-shift:  240; } }
      html[data-ui-color-palette="analog"] { .sec { --hue-shift:  -30; }   .ter { --hue-shift:   30; } }
      html[data-ui-color-palette="splitc"] { .sec { --hue-shift:  50; }   .ter { --hue-shift:  100; } }

      @container style(--_parity: 0) { .layer { --_odd:  calc(var(--_even) + 1); --depth: var(--_odd);  --_parity: 1; } }
      @container style(--_parity: 1) { .layer { --_even: calc(var(--_odd)  + 1); --depth: var(--_even); --_parity: 0; } }
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
      :where(h1, h2, h3, h4, h5, h6, small, .icon-btn, .btn),
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
    /* ═══════════════════════════════════════════
       core.spacing
       pow(ratio, --space). Fluid. Same curve shape as type.
       --space: 0 = ~0.5rem  |  1 = ~0.85rem  |  2 = ~1.3rem
                3 = ~2rem     | -1 = ~0.33rem  | -2 = ~0.22rem
       ═══════════════════════════════════════════ */

    @layer core.spacing {
      :where(*) {
        --_s-min: calc(var(--cfg-space-min) * pow(var(--cfg-space-min-ratio), var(--space)));
        --_s-max: calc(var(--cfg-space-max) * pow(var(--cfg-space-max-ratio), var(--space)));
        --_s: clamp(var(--_s-min),
          calc(var(--_s-min) + (var(--_s-max) - var(--_s-min)) *
            (100vi - var(--cfg-fluid-min-vp)) /
            (var(--cfg-fluid-max-vp) - var(--cfg-fluid-min-vp))),
          var(--_s-max)
        )  * var(--cfg-space-scale);
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
    cust to your pref

    ```css
    @layer theme {
      :root {
        --font-heading: Charter, 'Bitstream Charter', 'Sitka Text', Cambria, serif;
        --font-body:    Optima, Candara, 'Noto Sans', source-sans-pro, sans-serif;
        --font-mono:    'SF Mono', Menlo, ui-monospace, 'Cascadia Code', 'Source Code Pro', Consolas, monospace;
      }

      h1    { --type:  2.5; font-family: var(--font-heading); font-weight: 400; }
      h2    { --type:  1.5; font-family: var(--font-heading); font-weight: 400; }
      h3    { --type:  0.8; font-family: var(--font-heading); font-weight: 500; }
      h4    { --type:  0.4; font-family: var(--font-heading); font-weight: 600; }
      p     { --type:  0;   font-family: var(--font-body); }
      body  { --type:  0;   font-family: var(--font-body); --type: 0; }
      small { --type: -1.5; font-family: var(--font-body); text-transform: uppercase; letter-spacing: 0.06em; }
      code  { --type: -0.5; font-family: var(--font-mono); }
      pre   { --type: -0.5; font-family: var(--font-mono); }
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


@app.cell
def _(mo):
    mo.md(r"""
    5a. Layout.page
    [] dashboard
    [] landing
    Q: Drawers here or Components?
    ```css
    @layer layout.page {

      :where(body.blog) { display: flex; flex-direction: column; min-height: 100svh;
          & #main { felx: 1; }
      }

      :where(body.app) {
          position: fixed; /*not sure about this*/
          inset: 0;
          overflow: hidden;
          overscroll-behavior: none;
          display: grid;
          grid-template:
            "header  header  header" auto
            "nav     main    aside"  1fr
            "footer  footer  footer" auto
            / auto   1fr     auto;
          height: 100svh;

          & #header, #main, #aside { overflow-y:auto; scrollbar-gutter: stable;}

          & #header { grid-area: header; margin-bottom: var(--cfg-page-gap);}
          & #main   { grid-area: main; }
          & #nav    { grid-area: nav;    margin-right:  var(--cfg-page-pag);}
          & #aside  { grid-area: aside;  margin-left:   var(--cfg-page-gap);}
          & #footer { grid-area: footer; margin-top:    var(--cfg-page-gap);}

          & dialog::backdrop { background-color: oklch(0 0 0 / calc(0.7 + var(--cfg-dark) * 0.1)); }
      }
    }

    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    5b. Layout.composition

    ```css
    @layer layout.composition {
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


@app.cell
def _(mo):
    mo.md(r"""
    ## 6a. Components.complex

    ### Toggle Button Group
    ```css
    @layer component.complex {
      :where(.toggle-group) { display: inline-flex;
        button { --contrast: 0.5; --_c: var(--cfg-surf-chroma); border: 1px solid var(--border);
          &:has(+ button) { border-start-end-radius: 0;   border-end-end-radius: 0; }
          & + button      { border-start-start-radius: 0; border-end-start-radius: 0;
                            border-inline-start: 1px solid var(--border); }
          &:hover { --contrast: 0.75; }
          &[aria-pressed="true"] { --_l: var(--cfg-color-l); --_c: var(--cfg-color-chroma); --contrast: 1; }
          &[aria-pressed="true"] + button,
          & + button[aria-pressed="true"] { border-inline-start-color: transparent; }
        }
      }
    }

    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 6b. Components.simple

    ### Button
    ```css
    @layer component.simple {
      :where(button, .btn) {
        border: 1px solid var(--Border);
        border-radius: var(--cfg-radius);
        padding: 0.5em 1.25em;
        cursor: pointer;
        font: inherit;
      }

      :where(.pri, .sec, .ter):where(button, .btn) {
        &:hover  { --l-shift:  0.04; }
        &:active { --l-shift: -0.04; }
      }

      :where(button.ghost, .btn.ghost) {
        --_l: calc(var(--_surf-base) + (var(--depth) + 1) * 2.5%); /* manual surface step */
        --_c: var(--cfg-surf-chroma);
        --contrast: 0.8;
        border-color: var(--border);
        &:hover  { --contrast: 0.75; --_l: calc(var(--_surf-base) + (var(--depth) + 2) * 2.5%); }
        &:active { --contrast: 1;    --_l: calc(var(--_surf-base) + (var(--depth) + 3) * 2.5%); }
      }
    }
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Card
    ```css
      :where(.Card) {
        border-radius: var(--cfg-radius);
        border: 1px solid var(--Border);
        padding: --space:1;
        overflow: hidden;
      }

      :where(.card) {
        border-radius: var(--cfg-radius);
        border: 1px solid var(--border);
        padding: --space:1;
        overflow: hidden;
      }
    }
    ```
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Button
    ```css
    /* BUTTON */

    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Badge
    ```css
    @layer component.simple {
      :where(.badge) {
        display: inline-flex; align-items: center; justify-content: center;
        padding: 0.15em 0.6em; border-radius: 99px;
        font-size: 0.75em; font-weight: 600;
      }
    }
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Divider
    ```css
    @layer component.simple {
      .divider { border: none; border-block-start: 1px solid --border; }
      .Divider { border: none; border-block-start: 1px solid --Border; }
    }
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Popover auto align
    ```css
    @layer component.simple {
      [popover].popover { position: fixed; inset: auto; margin: 0; border: none; min-width: clamp(10rem, 40vw, 18rem); max-width: min(90vw, 24rem); max-height: 80vh; overflow: auto; --_bg: --surface(1); background: var(--_bg); color: --contrast(0.7); border-radius: 0.5rem; box-shadow: --shadow(5); padding: --space(1); opacity: 1; transform: scale(1); position-area: self-block-start self-inline-end; position-try-order: most-block-size; position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline; position-visibility: anchors-visible; transition: opacity calc(var(--cfg-motion) * 0.18s) ease-out, transform calc(var(--cfg-motion) * 0.18s) ease-out, display calc(var(--cfg-motion) * 0.18s) allow-discrete, overlay calc(var(--cfg-motion) * 0.18s) allow-discrete; }
      [popover].popover:not(:popover-open) { opacity: 0; transform: scale(0.95); }
      [popover].popover.below-start { position-area: self-block-end self-inline-start; }
      [popover].popover.below-end { position-area: self-block-end self-inline-end; }
      [popover].popover.above-start { position-area: self-block-start self-inline-start; }
      [popover].popover.above-end { position-area: self-block-start self-inline-end; }
    }
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6c. component.utls
    ```css

    /* ─── ripple primitive ─── */

    @layer component.utls {
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
            content:          " ";
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
def _():
    from marimo_css import get_css

    return


@app.cell
def _():
    import html as html_lib



    return


@app.cell
def _():
    DATASTAR_SRC = Path("vendor/ds.js").read_text()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Testing graning threaded server * Advanced *
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## App Demo
    """)
    return


@app.cell
def _():
    FILE_JS = """
    function dropHandler(e) {
        e.preventDefault();
        e.target.classList.remove('dragover');
        const file = (e.dataTransfer || e.target).files[0];
        if (!file || file.size > 5*1024*1024) return;
        const reader = new FileReader();
        reader.onload = () => {
            fetch('/upload', {method:'POST', headers:{'Content-Type':'application/json'},
                body:JSON.stringify({datastar:{fileName:file.name, fileType:file.type, fileData:reader.result.split(',')[1]}})});
        };
        reader.readAsDataURL(file);
    }
    """
    return


@app.cell
def _():
    ME_CSS = """// 🌘 CSS Scope Inline 1.1.0 (https://github.com/gnat/css-scope-inline)
    window.cssScopeCount ??= 1 // Let extra copies share the scope count.
    window.cssScope ??= new MutationObserver(mutations => { // Allow 1 observer.
    	document?.body?.querySelectorAll('style:not([ready])').forEach(node => { // Faster than walking MutationObserver results when recieving subtree (DOM swap, htmx, ajax, jquery).
    		var scope = 'me__'+(window.cssScopeCount++) // Ready. Make unique scope, example: .me__1234
    		node.parentNode.classList.add(scope)
    		node.textContent = node.textContent
    		.replace(/(?:^|\.|(\s|[^a-zA-Z0-9\-\_]))(me|this|self)(?![a-zA-Z\/])/g, '$1.'+scope) // Can use: me this self
    		.replace(/((@keyframes|animation:|animation-name:)[^{};]*)\.me__/g, '$1me__') // Optional. Removes need to escape names, ex: "\.me"
    		.replace(/(?:@media)\s(xs-|sm-|md-|lg-|xl-|sm|md|lg|xl|xx)/g, // Optional. Responsive design. Mobile First (above breakpoint): 🟢 None sm md lg xl xx 🏁  Desktop First (below breakpoint): 🏁 xs- sm- md- lg- xl- None 🟢 *- matches must be first!
    			(match, part1) => { return '@media '+({'sm':'(min-width: 640px)','md':'(min-width: 768px)', 'lg':'(min-width: 1024px)', 'xl':'(min-width: 1280px)', 'xx':'(min-width: 1536px)', 'xs-':'(max-width: 639px)', 'sm-':'(max-width: 767px)', 'md-':'(max-width: 1023px)', 'lg-':'(max-width: 1279px)', 'xl-':'(max-width: 1535px)'}[part1]) }
    		)
    		node.setAttribute('ready', '')
    	})
    }).observe(document.documentElement, {childList: true, subtree: true})"""
    return (ME_CSS,)


@app.cell
def _(
    A,
    Body,
    Button,
    Div,
    Footer,
    H2,
    Head,
    Header,
    Html,
    Img,
    Input,
    ME_CSS,
    Main,
    P,
    Script,
    Source,
    Span,
    Style,
    Video,
):
    import secrets, json, time, base64, tempfile, os, threading, apsw
    from py_sse import create_app, create_relay, serve_background, stop_background, patch_elements, body


    setup_tags()

    CHUNK_THRESHOLD = 10 * 1024 * 1024

    def _delayed_unlink(path, delay=5): threading.Timer(delay, os.unlink, args=(path,)).start()

    # ── Database ──────────────────────────────────────────────────

    db = apsw.Connection("chat.db")
    db.execute("""
        CREATE TABLE IF NOT EXISTS messages (id TEXT, user TEXT, text TEXT, ts REAL);
        CREATE TABLE IF NOT EXISTS files (id TEXT PRIMARY KEY, name TEXT, mime TEXT, size INTEGER, data BLOB, ts REAL);
        CREATE TABLE IF NOT EXISTS uploads (id TEXT PRIMARY KEY, name TEXT, mime TEXT, size INTEGER, received INTEGER DEFAULT 0, ts REAL, user TEXT, done INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS upload_chunks (uid TEXT, offset INTEGER, data BLOB, PRIMARY KEY (uid, offset))
    """)

    def _db(): return apsw.Connection("chat.db")

    def save_msg(id, user, text, ts): _db().execute("INSERT INTO messages VALUES (?,?,?,?)", (id, user, text, ts))

    def load_msgs():
        sql = """SELECT id, user, text,
                 strftime('%l:%M %p', ts, 'unixepoch', 'localtime') as sent,
                 CASE
                   WHEN unixepoch('now') - ts < 60 THEN 'just now'
                   WHEN unixepoch('now') - ts < 3600 THEN cast(((unixepoch('now') - ts) / 60) as int) || 'm ago'
                   WHEN unixepoch('now') - ts < 86400 THEN cast(((unixepoch('now') - ts) / 3600) as int) || 'h ago'
                   ELSE cast(((unixepoch('now') - ts) / 86400) as int) || 'd ago'
                 END as ago
                 FROM messages ORDER BY ts"""
        return [dict(id=r[0], user=r[1], text=r[2], sent=r[3], ago=r[4]) for r in _db().execute(sql)]

    def save_file(id, name, mime, data, ts): _db().execute("INSERT INTO files VALUES (?,?,?,?,?,?)", (id, name, mime, len(data), data, ts))

    def get_file_meta(fid):
        r = list(_db().execute("SELECT name, mime FROM files WHERE id=?", (fid,)))
        if r: return dict(name=r[0][0], mime=r[0][1], src="files")
        r = list(_db().execute("SELECT name, mime FROM uploads WHERE id=? AND done=1", (fid,)))
        if r: return dict(name=r[0][0], mime=r[0][1], src="uploads")
        return None

    def file_to_disk(fid):
        meta = get_file_meta(fid)
        if not meta: return None
        conn = _db()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix="_" + meta["name"])
        if meta["src"] == "files":
            row = list(conn.execute("SELECT rowid FROM files WHERE id=?", (fid,)))[0][0]
            blob = conn.blobopen("main", "files", "data", row, False)
            offset = 0
            while offset < blob.length():
                tmp.write(blob.read(min(65536, blob.length() - offset)))
                offset = tmp.tell()
            blob.close()
        else:
            for chunk in conn.execute("SELECT data FROM upload_chunks WHERE uid=? ORDER BY offset", (fid,)):
                tmp.write(chunk[0])
        tmp.close()
        meta["path"] = tmp.name
        return meta

    # ── App ───────────────────────────────────────────────────────

    app = create_app()
    relay = create_relay()
    NAMES = ["Fox", "Owl", "Bear", "Wolf", "Hawk"]

    @app.before
    async def inject_user(req):
        user = req["cookies"].get("user")
        if not user:
            user = secrets.choice(NAMES) + str(secrets.randbelow(100))
            req["set_cookie"] = ("user", user)
        req["user"] = user

    def render_messages():
        msgs = load_msgs()
        items = []
        for m in msgs:
            if m["text"].startswith("[file:"):
                parts = m["text"][6:-1].split(":", 1)
                fid, fname = parts[0], parts[1] if len(parts) > 1 else "file"
                meta = get_file_meta(fid)
                mime = meta["mime"] if meta else ""
                if mime.startswith("image/"): content = Img(src=f"/file/{fid}", style="max-width:300px;border-radius:0.5rem")
                elif mime.startswith("video/"): content = Video(Source(src=f"/file/{fid}", type=mime), controls=True, style="max-width:300px")
                else: content = A(fname, href=f"/file/{fid}", download=fname, target="_blank", style="color:#4af")
            else: content = Span(m["text"])
            items.append(Div(
                Span(m["user"], style="font-weight:bold"), " ", content,
                Span(f" · {m['sent']} · {m['ago']}", style="color:#666;font-size:0.8em")))
        return Div(*items, id="chat")

    # ── JS ────────────────────────────────────────────────────────

    CHUNK_JS = """
    function uint8ToB64(bytes) {
        const chunks = [];
        for (let i = 0; i < bytes.length; i += 8192) chunks.push(String.fromCharCode.apply(null, bytes.subarray(i, i + 8192)));
        return btoa(chunks.join(''));
    }
    async function uploadFile(input) {
        const file = input.files[0];
        if (!file) return;
        const prog = document.getElementById('upload-progress');
        if (file.size < %d) {
            prog.textContent = 'Uploading...';
            const reader = new FileReader();
            reader.onload = async () => {
                const b64 = reader.result.split(',')[1];
                await fetch('/upload/small', {method:'POST', headers:{'Content-Type':'application/json'},
                    body: JSON.stringify({fileName:file.name, fileType:file.type, fileData:b64})});
                prog.textContent = 'Done!';
                input.value = '';
            };
            reader.readAsDataURL(file);
        } else {
            const CHUNK = 1 * 1024 * 1024;
            const res = await fetch('/upload/init', {method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({datastar:{fileName:file.name, fileType:file.type, fileSize:file.size}})});
            const {uploadId: uid} = await res.json();
            if (!uid) return;
            let offset = 0;
            while (offset < file.size) {
                try {
                    const slice = file.slice(offset, offset + CHUNK);
                    const buf = await slice.arrayBuffer();
                    const b64 = uint8ToB64(new Uint8Array(buf));
                    await fetch('/upload/chunk/'+uid+'?offset='+offset, {method:'POST',
                        headers:{'Content-Type':'application/json'},
                        body: JSON.stringify({datastar:{chunk:b64}})});
                    offset += slice.size;
                    prog.textContent = Math.round(offset/file.size*100)+'%%';
                } catch(e) {
                    prog.textContent = 'Resuming...';
                    await new Promise(r => setTimeout(r, 2000));
                    try {
                        const sr = await fetch('/upload/status/'+uid);
                        const st = await sr.json();
                        offset = st.uploadOffset || offset;
                    } catch(e2) { await new Promise(r => setTimeout(r, 3000)); }
                }
            }
            prog.textContent = 'Done!';
            input.value = '';
        }
    }
    """ % CHUNK_THRESHOLD

    # ── Routes ────────────────────────────────────────────────────

    @app.get("/")
    async def home(req):
        user = req["user"]
        return to_html(Html(
            Head(Script(type="module", src="https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.8/bundles/datastar.js"),
                Script(ME_CSS), Script(CHUNK_JS)),
            Body(
                Style("""
                me {height:60vh; display: grid; grid-template-rows: auto 1fr auto;}
                me > main {scrollbar-gutter: stable; overflow-y:auto; display: flex; flex-direction: column-reverse;}
                """),
                Header(H2("Mini Chat"), P(f"You are: {user}")),
                Main(Div(id="chat", **{"data-init": "@get('/stream')"})),
                Footer(
                    Input(id="inp", placeholder="Type a message...", **{"data-bind:text": ""}),
                    Button({"data-on:click": "@post('/send')"}, "Send"),
                    Button({"data-on:click": "@post('/clear')"}, "Clear"),
                    Input(type="file", onchange="uploadFile(this)"),
                    Span(id="upload-progress")))))

    @app.get("/stream")
    async def stream(req):
        user = req["user"]
        yield patch_elements(render_messages())
        try:
            async for topic, data in relay.subscribe("chat.*"):
                yield patch_elements(render_messages())
        finally: pass

    @app.post("/send")
    async def send_msg(req):
        user = req["user"]
        raw = await body(req)
        text = json.loads(raw).get("datastar", json.loads(raw)).get("text", "").strip()
        if not text: return None
        save_msg(secrets.token_urlsafe(8), user, text, time.time())
        relay.publish("chat.message", user)
        return None

    @app.post("/clear")
    async def clear_chat(req):
        conn = _db()
        conn.execute("DELETE FROM messages")
        conn.execute("DELETE FROM files")
        conn.execute("DELETE FROM uploads")
        conn.execute("DELETE FROM upload_chunks")
        relay.publish("chat.clear", req["user"])
        return None

    @app.post("/upload/small")
    async def upload_small(req):
        raw = await body(req, max_size=CHUNK_THRESHOLD * 2)
        s = json.loads(raw)
        fdata = base64.b64decode(s.get("fileData", ""))
        if not fdata: return None
        fid = secrets.token_urlsafe(12)
        save_file(fid, s.get("fileName", "file"), s.get("fileType", "application/octet-stream"), fdata, time.time())
        save_msg(secrets.token_urlsafe(8), req["user"], f"[file:{fid}:{s.get('fileName','file')}]", time.time())
        relay.publish("chat.file", req["user"])
        return None

    @app.post("/upload/init")
    async def upload_init(req):
        raw = await body(req)
        s = json.loads(raw).get("datastar", json.loads(raw))
        name, mime, size = s.get("fileName", "file"), s.get("fileType", "application/octet-stream"), int(s.get("fileSize", 0))
        if size <= 0: return None
        uid = secrets.token_urlsafe(12)
        _db().execute("INSERT INTO uploads(id,name,mime,size,received,ts,user,done) VALUES (?,?,?,?,0,?,?,0)", (uid, name, mime, size, time.time(), req["user"]))
        return dict(uploadId=uid)

    @app.post("/upload/chunk/{uid}")
    async def upload_chunk(req):
        uid = req["params"]["uid"]
        offset = int(req["query"].get("offset", 0))
        raw = await body(req, max_size=8*1024*1024)
        chunk = base64.b64decode(json.loads(raw).get("datastar", json.loads(raw)).get("chunk", ""))
        if not chunk: return None
        conn = _db()
        r = list(conn.execute("SELECT size FROM uploads WHERE id=? AND done=0", (uid,)))
        if not r: return None
        conn.execute("INSERT OR REPLACE INTO upload_chunks VALUES (?,?,?)", (uid, offset, chunk))
        received = offset + len(chunk)
        conn.execute("UPDATE uploads SET received=? WHERE id=?", (received, uid))
        size = r[0][0]
        if received >= size:
            conn.execute("UPDATE uploads SET done=1 WHERE id=?", (uid,))
            name = list(conn.execute("SELECT name FROM uploads WHERE id=?", (uid,)))[0][0]
            save_msg(secrets.token_urlsafe(8), req["user"], f"[file:{uid}:{name}]", time.time())
            relay.publish("chat.file", req["user"])
        return dict(uploadOffset=received)

    @app.get("/upload/status/{uid}")
    async def upload_status(req):
        uid = req["params"]["uid"]
        r = list(_db().execute("SELECT received, size, done FROM uploads WHERE id=?", (uid,)))
        if not r: return None
        received, size, done = r[0]
        return dict(uploadId=uid, uploadOffset=received, uploadSize=size, uploadDone=bool(done))

    @app.get("/file/{fid}")
    async def serve_file(req):
        fid = req["params"]["fid"]
        f = file_to_disk(fid)
        if not f: return None
        proto = req["_proto"]
        proto.response_file(200, [("content-type", f["mime"]), ("content-disposition", f'inline; filename="{f["name"]}"')], f["path"])
        _delayed_unlink(f["path"])
        req["_sent"] = True


    return app, apsw, serve_background


@app.cell
def _(app, serve_background):

    state = serve_background(app, port=8000)
    input("pause")
    return


@app.cell
def _():
    return


@app.cell
def _(apsw):


    list(apsw.Connection("/Users/mikedeufel/code/pub/css/chat.db").execute("SELECT id, name, mime, size FROM files"))


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Ngrok Tunnel
    """)
    return


@app.cell
def _():
    from py_sse.ngrok import start_tunnel, stop_tunnel, load_env

    return


@app.cell
def _():

    # load_env()

    # state  = serve_background(app, port=8000)
    # tunnel = start_tunnel(8000)
    # print(tunnel.url)

    # input("pause")

    # stop_tunnel(tunnel)
    # stop_background(state)
    return


if __name__ == "__main__":
    app.run()
