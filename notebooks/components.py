import marimo

__generated_with = "0.22.4"
app = marimo.App(width="full")

with app.setup:
    import os
    from py_sse import create_app, create_relay, create_signer, start_tunnel, static, stop_background, stop_tunnel, set_cookie, serve_background, serve, signals, ServerState

    from html_tags import pretty, to_html, Html, Head, Body, Style, Link, Meta, Header, Nav, Main, Aside, Footer, Div, H1, H2, H3, P, A, Span, Button, Ul, Li, Dialog, Title, Small, Fragment, Hr, Input, Fieldset, Legend, Label, H5, H4, H6, Code, Section, Strong, Br, Table, Thead, Tbody, Tr, Td, Th, Script, Tag

    from html_tags.extras import Datastar, ScopedCSS, Favicon, FontImport

    from py_sse.ngrok import start_tunnel, stop_tunnel




    HERE = os.path.dirname(os.path.abspath(__file__))
    app = create_app()
    static(app, "/static", os.path.join(HERE, "static"))

    relay = create_relay()
    signer = create_signer()

    font = FontImport(url="https://fonts.googleapis.com/css2?family=Josefin+Slab:ital,wght@0,100..700;1,100..700&display=swap")

    head = Head(Title("Test Page"),  Datastar(),  ScopedCSS(),  Favicon("🎾"), FontImport(), font, Link(rel="stylesheet", href="./static/style.css") )


@app.cell
def _():
    import marimo as mo


    return (mo,)


@app.cell
def _():
    state  = serve_background(app, port=8000)
    return


@app.cell
def _():


    # ══════════════════════════════════════════════════════════════════════════
    # Nav
    # ══════════════════════════════════════════════════════════════════════════
    nav_links = [
        ("Typography",  "#typography"),
        ("Buttons",     "#buttons"),
        ("Color Roles", "#color-roles"),
        ("Surface",     "#surface"),
        ("Spacing",     "#spacing"),
        ("Calendar",    "#calendar"),
        ("Reflow",      "#reflow"),
        ("Badges",      "#badges"),
        ("Contrast",    "#contrast"),
    ]

    nav = Nav(id="nav", cls="surface stack", style="padding: 1rem; --space: 1; min-width: 12rem;")(
        Style("""
            me a { display: block; padding: 0.35em 0.75em; border-radius: var(--cfg-radius); --contrast: 0.7; }
            me a:hover { --_l-shift: 0.03; --contrast: 0.9; }
        """),
        Small("Tests"),
        *[A(label, href=href) for label, href in nav_links],
    )


    # ══════════════════════════════════════════════════════════════════════════
    # Aside — quick checks + live config controls
    # ══════════════════════════════════════════════════════════════════════════
    def check_item(title, description):
        return Div(cls="stack", style="--space: 0;")(
            H5(title),
            P(description, style="--contrast: 0.6;"),
        )

    aside = Aside(id="aside", cls="surface stack", style="padding: 1rem; --space: 1; max-width: 180px;")(
        Small("Quick checks"),
        check_item("Expect", "Background gets lighter per .surface nesting (light mode) or darker (dark mode)"),
        Hr(),
        check_item("Expect", "Text color auto-flips dark↔light for readability on any bg"),
        Hr(),
        check_item("Expect", "Buttons hover → lighter, active → darker"),
        Hr(),
        check_item("Expect", "Calendar day cells visually distinct from month bg from outer bg"),
        Hr(),
        check_item("Expect", "Reflow cards: each subtree has its own complete color world"),
        Hr(),
        Div(cls="stack", style="--space: -1;")(
            Small("Status colors"),
            Span("suc", cls="badge suc"),
            Span("err", cls="badge err"),
            Span("wrn", cls="badge wrn"),
            Span("inf", cls="badge inf"),
        ),
    )


    # ══════════════════════════════════════════════════════════════════════════
    # Header
    # ══════════════════════════════════════════════════════════════════════════
    header = Header(id="header", cls="surface split", style="padding: 0.75rem 1.5rem;")(
        Style("me { align-items: center; }"),
        H4("Design System Check"),
        Div(cls="row", style="--space: -1;")(
            Small("--cfg-hue: 220"),
            Small("Public API: --type · --space · --contrast"),
        ),
    )


    # ══════════════════════════════════════════════════════════════════════════
    # Footer
    # ══════════════════════════════════════════════════════════════════════════
    footer = Footer(id="footer", cls="surface split", style="padding: 0.5rem 1.5rem; align-items: center;")(
        Small("Design System Check", style="--contrast: 0.4;"),
        Small("Classes: layout + color roles · Inline: --type --space --contrast · Components: scoped CSS", style="--contrast: 0.4;"),
    )


    # ══════════════════════════════════════════════════════════════════════════
    # Main — test sections
    # ══════════════════════════════════════════════════════════════════════════

    # ── Helper: section wrapper ──
    def section(id, label, title, description, *children):
        return Section(id=id, cls="stack", style="--space: 1;")(
            Div(
                Small(label),
                H2(title),
                P(description),
            ),
            *children,
        )

    # ── Helper: surface panel ──
    def panel(*children, **kwargs):
        style = kwargs.get("style", "")
        cls = kwargs.get("cls", "surface stack")
        return Div(cls=cls, style=f"padding: 1rem; border-radius: var(--cfg-radius); {style}")(*children)


    # ── Typography ──
    sec_typography = section("typography",
        "test: typography scale",
        "Typography",
        "Each heading sets --type in component.base. The fluid engine computes font-size automatically. Resize the viewport to see the scale respond.",
        panel(
            Style("me p { --contrast: 0.5; }"),
            H1("h1 — --type: 2.5"), P("Expect: largest heading, serif, weight 400"), Hr(),
            H2("h2 — --type: 1.5"), P("Expect: second largest, serif, weight 400"), Hr(),
            H3("h3 — --type: 0.8"), P("Expect: medium, serif, weight 500"), Hr(),
            H4("h4 — --type: 0.4"), P("Expect: small heading, serif, weight 600"), Hr(),
            H5("h5 — --type: 0.2"), P("Expect: near body size, serif, weight 600"), Hr(),
            H6("h6 — --type: 0"),   P("Expect: body size, serif, weight 700"), Hr(),
            P("p — --type: 0 (body text)"),
            Small("small — --type: -1.5, uppercase"),
            P(Code("code — --type: -0.5, monospace"), style="--type: -0.5;"),
            style="--space: 0;",
        ),
        panel(
            P('Custom: style="--type: 1.2" — any element, any step. This text is between h3 and h2.', style="--type: 1.2;"),
        ),
    )

    return aside, footer, header, nav, panel, sec_typography, section


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##  Buttons
    """)
    return


@app.cell
def _(icon, section):
    sec_buttons = section("buttons",
        "test: btn, btn.pri, btn.sec",
        "Buttons",
        "The button has no color opinion by default. Color role classes compose onto it. Hover should lighten, active should darken. Disabled drops contrast.",
        Div(cls="split")(
            Div(cls="row", style="--cfg-dark:0")(
                Button("btn pri",  cls="btn pri"), 
                Button("btn pri",  cls="btn sec"), 
                Button("btn sec",  cls="btn pri", disabled=1), 
                Button("btn sec",  cls="btn sec", disabled=1), 
            ),
             Div(cls="row", style="--cfg-dark:1")(
                Button("disabled",  cls="btn sec disabled"), 
                Button("at rest",  cls="btn sec"), 
                Button("hover ",  cls="btn sec hover"), 
                Button("active",  cls="btn sec active"), 
            ),
             Div(cls="row", style="--cfg-dark:1")(
                Button(cls="btn sec disabled")(icon),
                Button(cls="btn sec")(icon), 
                Button(cls="btn sec hover")(icon),  
                Button(cls="btn sec active")(icon),   
             )
        )
    )


    return (sec_buttons,)


@app.cell
def _():
    from html_tags import html_to_tag

    svg_str = '''<svg xmlns="http://www.w3.org/2000/svg" width="stretch" height="stretch" viewBox="0 0 48 48"><circle cx="24.039" cy="23.76" r="21.5" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M32.611 10.373v8.131l-7.057 4.1l.017-8.163zM15.389 34.977l4-6.928l.59 9.578l4-6.928" stroke-width="2"/></svg>'''

    icon = html_to_tag(svg_str)

    return (icon,)


@app.cell
def _(panel, section):

    # ── Color Roles on Divs ──
    def color_div(name, hue_label):
        return Div(cls=name, style="padding: 1rem; border-radius: var(--cfg-radius);")(
            Strong(name), Br(), f"hue: {hue_label}",
        )

    sec_color_roles = section("color-roles",
        "test: color role classes on arbitrary elements",
        "Color Roles on Divs",
        "Color classes work on any element. Text color auto-computes for contrast. These divs have zero custom CSS — just the class name.",
        Div(cls="grid", style="--_col: 8rem;")(
            color_div("pri", "base"),
            color_div("sec", "+120"),
            color_div("ter", "+240"),
            color_div("suc", "145"),
            color_div("err", "25"),
            color_div("wrn", "85"),
            color_div("inf", "250"),
        ),
    )


    # ── Surface Depth ──
    sec_surface = section("surface",
        "test: .surface leapfrog",
        "Surface Auto-Depth",
        "Nest .surface elements and the parity system auto-increments depth. No numbers to manage. Each level gets 2.5% lighter (light mode) or darker (dark mode).",
        panel(
            P(Strong("Surface 1"), " — first nested .surface"),
            panel(
                P(Strong("Surface 2"), " — auto-incremented"),
                panel(
                    P(Strong("Surface 3"), " — and again"),
                    panel(P(Strong("Surface 4"), " — and deeper still")),
                ),
            ),
        ),
    )


    # ── Spacing ──
    def spacing_demo(space_val, label):
        return panel(
            Style("me > .stack > div { padding: 0.5rem 0.75rem; border-radius: var(--cfg-radius); border: 1px dashed var(--border); }"),
            Small(label),
            Div(cls="stack")(Div("Item A"), Div("Item B"), Div("Item C")),
            style=f"--space: {space_val};",
        )

    sec_spacing = section("spacing",
        "test: --space on layout classes",
        "Spacing Scale",
        "Layout classes consume --space for their gap. Set it on the container and children flow accordingly.",
        spacing_demo(2, "--space: 2 (wide gaps)"),
        spacing_demo(-1, "--space: -1 (tight gaps)"),
    )


    # ── Badges ──
    sec_badges = section("badges",
        "test: badge + color roles",
        "Badges",
        "Same color role classes, different element. Zero extra CSS needed.",
        Div(cls="row", style="--space: 0;")(
            *[Span(name, cls=f"badge {name}") for name in ["pri", "sec", "ter", "suc", "err", "wrn", "inf"]]
        ),
    )


    # ── Calendar ──
    DAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    def day_cell(n, today=False):
        cls = "surface day today" if today else "surface day"
        return Div(str(n), cls=cls)

    def month(name, start_offset, num_days, today=None):
        """start_offset: 0=Monday, 1=Tuesday, etc."""
        return Div(cls="surface stack", style="padding: 0.75rem; border-radius: var(--cfg-radius); --space: 0;")(
            H4(name, style="text-align: center;"),
            Div(cls="month-grid")(
                *[Small(d) for d in DAYS],
                *[Span() for _ in range(start_offset)],
                *[day_cell(d, today=(d == today)) for d in range(1, num_days + 1)],
            ),
        )

    return month, sec_badges, sec_color_roles, sec_spacing, sec_surface


@app.cell
def _(month, section):
    sec_calendar = section("calendar",
        "test: .surface 3 levels deep + scoped component",
        "3-Month Calendar",
        "The outer container is a .surface. Each month is a .surface. Each day cell is a .surface. Three levels of auto-depth.",
        Div(cls="surface", style="padding: 1rem; border-radius: var(--cfg-radius);")(
            Style("""
                me { container-type: inline-size; }
                me .cal-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--_s, 0.75rem); }
                @container (max-width: 50rem) { me .cal-grid { grid-template-columns: 1fr; } }
                me .month-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; text-align: center; }
                me .month-grid small { padding: 0.25em 0; --contrast: 0.5; }
                me .day { padding: 0.35em 0.25em; border-radius: calc(var(--cfg-radius) * 0.5); }
                me .day.today { --_color-l: var(--cfg-color-l); --_color-c: var(--cfg-color-chroma); --contrast: 1; font-weight: 600; }
            """),
            Div(cls="cal-grid")(
                month("April 2026",  2, 30, today=4),   # Apr 1 = Wednesday (offset 2)
                month("May 2026",    4, 31),              # May 1 = Friday (offset 4)
                month("June 2026",   0, 30),              # Jun 1 = Monday (offset 0)
            ),
        ),
    )

    return (sec_calendar,)


@app.cell
def _(section):
    # ── Subtree Color Reflow ──
    def reflow_card(hue, label, color_name):
        return Div(style=f"--cfg-hue: {hue};")(
            Style("me { border-radius: var(--cfg-radius); overflow: hidden; border: 1px solid var(--border); }"),
            Div(cls="surface stack", style="padding: 1rem; --space: 0;")(
                H4(f"--cfg-hue: {hue}"),
                P(f"{color_name} family", style="--contrast: 0.6;"),
                Div(cls="row", style="--space: -1;")(
                    Button("Action", cls="btn pri"),
                    Button("Save", cls="btn sec"),
                    Button("Back", cls="btn"),
                ),
                Div(cls="surface", style="padding: 0.5rem; border-radius: calc(var(--cfg-radius) * 0.5); margin-top: 0.5rem;")(
                    P("Nested surface", style="--contrast: 0.6;"),
                ),
            ),
        )

    sec_reflow = section("reflow",
        "test: subtree color reflow — change one variable, everything updates",
        "Subtree Color Reflow",
        "Each card sets --cfg-hue on itself. Every child — surfaces, buttons, badges, borders — recomputes automatically.",
        Div(cls="grid", style="--_col: 14rem;")(
            reflow_card(350, "--cfg-hue: 350", "Rose"),
            reflow_card(281, "--cfg-hue: 281", "Purple"),
            reflow_card(60,  "--cfg-hue: 60",  "Amber"),
        ),
    )

    return (sec_reflow,)


@app.cell
def _(panel, section):
    # ── Toggle Group (scoped component demo) ──
    sec_toggle = section("toggle",
        "test: scoped CSS component — toggle group",
        "Scoped Component: Toggle Group",
        "Defined entirely in a <style> block using me scoping. Composes with the global button primitive.",
        Div(
            Style("""
                me { display: inline-flex; }
                me button { --contrast: 0.5; --_color-c: var(--cfg-surf-chroma); border: 1px solid var(--border); }
                me button:has(+ button) { border-start-end-radius: 0; border-end-end-radius: 0; }
                me button + button { border-start-start-radius: 0; border-end-start-radius: 0; border-inline-start: 1px solid var(--border); }
                me button:hover { --contrast: 0.75; }
                me button[aria-pressed="true"] { --_color-l: var(--cfg-color-l); --_color-c: var(--cfg-color-chroma); --contrast: 1; }
                me button[aria-pressed="true"] + button,
                me button + button[aria-pressed="true"] { border-inline-start-color: transparent; }
            """),
            Button("Day",   **{"aria-pressed": "true"}),
            Button("Week",  **{"aria-pressed": "false"}),
            Button("Month", **{"aria-pressed": "false"}),
        ),
    )


    # ── Contrast Scale ──
    sec_contrast = section("contrast",
        "test: --contrast as a continuous dial",
        "Contrast Scale",
        "--contrast is not on/off — it's a continuous value from 0 to 1. The color engine computes the optimal text color at every point.",
        Div(cls="surface row", style="padding: 1rem; border-radius: var(--cfg-radius);")(
            Style("me > div { padding: 0.75rem 1rem; border-radius: var(--cfg-radius); flex: 1; min-width: 5rem; text-align: center; }"),
            *[Div(str(v), style=f"--contrast: {v};") for v in [0.1, 0.2, 0.3, 0.5, 0.7, 0.85, 1.0]],
        ),
    )


    # ── Layout Compositions ──
    sec_layouts = section("layouts",
        "test: layout classes",
        "Layout Compositions",
        "Layout classes declare flow context. .stack = vertical, .row = horizontal wrap, .split = space-between, .cluster = centered wrap, .grid = auto-fit columns.",
        panel(
            Style("me .demo-box { padding: 0.5rem 1rem; border: 1px dashed var(--border); border-radius: calc(var(--cfg-radius) * 0.5); --contrast: 0.6; }"),
            Small(".stack"),
            Div(cls="stack")(Div("A", cls="demo-box"), Div("B", cls="demo-box"), Div("C", cls="demo-box")),
            Hr(),
            Small(".row"),
            Div(cls="row")(*[Div(x, cls="demo-box") for x in "ABCDE"]),
            Hr(),
            Small(".split"),
            Div(cls="split")(Div("Left", cls="demo-box"), Div("Right", cls="demo-box")),
            Hr(),
            Small(".cluster"),
            Div(cls="cluster")(*[Div(x, cls="demo-box") for x in "ABCDE"]),
            Hr(),
            Small('.grid (--_col: 8rem)'),
            Div(cls="grid", style="--_col: 8rem;")(*[Div(str(i), cls="demo-box") for i in range(1, 7)]),
        ),
    )


    # ── System Summary ──
    sec_summary = section("summary",
        "reference",
        "System Summary",
        "",
        Div(cls="surface", style="padding: 1rem; border-radius: var(--cfg-radius);")(
            Style("""
                me table { width: 100%; }
                me th, me td { padding: 0.4em 0.75em; text-align: left; border-bottom: 1px solid var(--border); }
                me code { padding: 0.1em 0.3em; border-radius: 0.2em; }
            """),
            Table(
                Thead(Tr(Th("Layer"), Th("Mechanism"), Th("Examples"))),
                Tbody(
                    Tr(Td("Config"),     Td(Code("--cfg-*"), " on :root"),     Td("--cfg-hue, --cfg-dark, --cfg-radius")),
                    Tr(Td("Public API"), Td("Inline style"),                   Td("--type, --space, --contrast")),
                    Tr(Td("Layout"),     Td("Classes"),                        Td(".stack .row .cluster .grid .surface")),
                    Tr(Td("Color"),      Td("Classes"),                        Td(".pri .sec .ter .suc .err .wrn .inf")),
                    Tr(Td("Components"), Td("Scoped CSS"),                     Td("Style(\"me button { ... }\")")),
                    Tr(Td("Internals"),  Td(Code("--_*")),                     Td("--_color-l, --_l, --_bg, --_depth")),
                ),
            ),
        ),
    )

    return sec_contrast, sec_layouts, sec_summary, sec_toggle


@app.cell
def _(
    aside,
    btnJs,
    footer,
    header,
    nav,
    sec_badges,
    sec_buttons,
    sec_calendar,
    sec_color_roles,
    sec_contrast,
    sec_layouts,
    sec_reflow,
    sec_spacing,
    sec_summary,
    sec_surface,
    sec_toggle,
    sec_typography,
):
    # ══════════════════════════════════════════════════════════════════════════
    # Main assembly
    # ══════════════════════════════════════════════════════════════════════════
    main = Div(id="main", cls="stack", style="padding: 1.5rem; --space: 3;")(
        sec_typography,
        sec_buttons,
        sec_color_roles,
        sec_surface,
        sec_spacing,
        sec_badges,
        sec_calendar,
        sec_reflow,
        sec_toggle,
        sec_contrast,
        sec_layouts,
        sec_summary,
    )


    # ══════════════════════════════════════════════════════════════════════════
    # Body — Datastar bindings for live config
    # ══════════════════════════════════════════════════════════════════════════
    body = Body(
        {
            "data-store": "{"
                "'hue': 220, "
                "'dark': 0, "
                "'surfChroma': 0.015, "
                "'colorChroma': 0.14, "
                "'motion': 1"
            "}",
            "data-style": "{"
                "'--cfg-hue': '' + $hue, "
                "'--cfg-dark': '' + $dark, "
                "'--cfg-surf-chroma': '' + $surfChroma, "
                "'--cfg-color-chroma': '' + $colorChroma, "
                "'--cfg-motion': '' + $motion"
            "}",
        },
        cls="app",
    )(
        header,
        nav,
        aside,
        main,
        footer,
        btnJs,
    )


    # ══════════════════════════════════════════════════════════════════════════
    # Page
    # ══════════════════════════════════════════════════════════════════════════
    page = Html(lang="en")(head, body)
    return (page,)


@app.function
# ── Dialog Fragment ──
def dialog():
    return Dialog({"data-on:close":"$dialogOpen = false"}, id="my-dialog")(
        Div(cls="stack level unmute", style="--space: 1; padding: var(--_s);")(
            H3("Dialog Title"),
            P("This dialog dims the page through the color system — ",
              "no backdrop opacity, just contrast muting. Every ",
              "surface recalculates through OKLCH."),
            Button({"data-on:click":"el.closest('dialog').close()"}, "Close")
            )
        )


@app.cell
def _(page):
    @app.get("/")
    async def home(req):
        return page

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Theme Controls
    """)
    return


@app.function
def ToggleGroup(signal, options, default=None):
    """options: list of (value, label) tuples or just strings"""
    if default is None:
        default = options[0] if isinstance(options[0], str) else options[0][0]
    opts = [(o, o) if isinstance(o, str) else o for o in options]
    return Div(
        {"data-signals": f"{{{signal}: '{default}'}}"},
        *[Button(
            {"data-attr:aria-pressed": f"String(${signal}==='{v}')",
             "data-on:pointerdown": f"${signal}='{v}'"},
            aria_pressed=str(v == default).lower()
        )(label) for v, label in opts],
        cls="toggle-group"
    )


@app.function
def ThemeControls():
    return Div(
        Style('''
        me input {width:100%; display: block}
        '''),
        ToggleGroup("palette", [
            ("mono", "Mono"), ("comp", "Complementary"),
            ("triad", "Triadic"), ("analog", "Analogous")
        ], default="comp"),

        ToggleGroup("scheme", ["light", "dark"], default="dark"),

        Label("Hue ", Span(**{"data-text": "$hue"}),
              Input(type="range", min="0", max="360", step="1", value="250",
                    **{"data-bind": "hue"})),

        Label("Surface Chroma ", Span(**{"data-text": "$surfaceChroma"}),
              Input(type="range", min="0", max="0.15", step="0.005", value="0.03",
                    **{"data-bind": "surfaceChroma"})),

        Label("Color Chroma ", Span(**{"data-text": "$colorChroma"}),
              Input(type="range", min="0", max="0.4", step="0.005", value="0.15",
                    **{"data-bind": "colorChroma"})),

        Label("Dark ", Span(**{"data-text": "$dark"}),
              Input(type="range", min="0", max="1", step="0.01", value="1",
                    **{"data-bind": "dark"})),

        Label("UI Scale ", Span(**{"data-text": "$uiScale"}),
              Input(type="range", min="0.75", max="1.5", step="0.05", value="1",
                    **{"data-bind": "uiScale"})),
    )


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Utls
    """)
    return


@app.cell
def _():
    btnJs = Script('''window.btnStates ??= (() => {
        const slot = cls => {
            let cur = null
            return el => { cur?.classList.remove(cls); (cur = el)?.classList.add(cls) }
        }

        const active = slot('active')
        const hover  = slot('hover')
        const B  = e => e.target.closest?.('.btn')
        const kb = e => e.key === ' ' || e.key === 'Enter'
        const guard = (el, fn) => el && !el.disabled && fn(el)

        document.addEventListener('pointerdown',   e => guard(B(e), active),           {passive:true})
        document.addEventListener('pointerup',     () => active(null),                 {passive:true})
        document.addEventListener('pointercancel', () => active(null),                 {passive:true})
        document.addEventListener('pointerenter',  e => guard(B(e), hover),            {passive:true, capture:true})
        document.addEventListener('pointerleave',  e => { hover(null); if(B(e)===document.activeElement?.closest('.btn')) active(null) }, {passive:true, capture:true})
        document.addEventListener('keydown',       e => kb(e) && guard(document.activeElement?.closest('.btn'), active))
        document.addEventListener('keyup',         e => kb(e) && active(null))

        const scan = root => root.querySelectorAll?.('.btn')
            .forEach(el => el.classList.toggle('disabled', !!el.disabled))

        new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(scan)))
            .observe(document.body, {childList:true, subtree:true})

        scan(document)
    })()
    ''')
    return (btnJs,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
