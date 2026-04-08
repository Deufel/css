import marimo

__generated_with = "0.22.5"
app = marimo.App(width="full")

with app.setup:
    import os

    from py_sse.app import create_app, create_relay, create_signer, static, set_cookie, serve, signals
    from py_sse.mserver import serve_background, stop_background, ServerState, dev_alive
    from py_sse.ngrok import start_tunnel, stop_tunnel, TunnelState
    from html_tags import pretty, to_html, Html, Head, Body, Style, Link, Meta, Header, Nav, Main, Aside, Footer, Div, H1, H2, H3, P, A, Span, Button, Ul, Li, Dialog, Title, Small, Fragment, Hr, Input, Fieldset, Legend, Label, H5, H4, H6, Code, Section, Strong, Br, Table, Thead, Tbody, Tr, Td, Th, Script, Tag, Kbd

    from html_tags.extras import Datastar, ScopedCSS, Favicon, FontImport, MeCSS, Pointer






    HERE = os.path.dirname(os.path.abspath(__file__))
    app = create_app()
    static(app, "/static", os.path.join(HERE, "static"))

    relay = create_relay()
    signer = create_signer()

    #coolfont??
    font = FontImport(url="https://fonts.googleapis.com/css2?family=Josefin+Slab:ital,wght@0,100..700;1,100..700&display=swap")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo


    return (mo,)


@app.cell
def _():
    state = serve_background(app, host="127.0.0.1", port=8000)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Navigation
    """)
    return


@app.cell
def _():


    nav_links = [
        ("Buttons",     "#buttons"),
        ("Surface",     "#surface"),
        ("Calendar",    "#calendar"),
        ("Reflow",      "#reflow"),
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
    return (nav,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Aside
    """)
    return


@app.cell
def _():
    def check_item(title, description):
        return Div(cls="stack", style="--space: 0;")(
            H5(title),
            P(description, style="--contrast: 0.6;"),
        )

    aside = Aside(id="aside", cls="surface stack", style="padding: 1rem; --space: 1; min-width: 180px;")(
                Div(cls="surface vh")(Div(cls="surface vh")),
                H3("Aside"), 
                Hr(), 
                Code(data_text="`theme:` + $_themes[$_theme]"),
                Code(data_text=" `size:` + $_sizes[$_size]"),
                Code(data_text=" `motion:` + $_motions[$_motion]")

                  ) 
    return (aside,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Header
    """)
    return


@app.cell
def _(icon_font, icon_moon, icon_timer):
    header = Header(id="header", cls="surface split")(
        Style('''
        me { padding: 0.25rem; align-items: center; }
        me > hr { width: stretch; }
        '''),
        H4("Design System Check"),
        Div(cls="row")(
            A(href="https://github.com/Deufel/css")("github"),
            Hr(),
            Button({"data-on:click":"$_motion= ($_motion+ 1) % $_motions.length"}, icon_timer, cls="btn"),
            Button({"data-on:click":"$_theme = ($_theme + 1) % $_themes.length"}, icon_moon, cls="btn"),
            Button({"data-on:click":"$_size = ($_size  + 1) % $_sizes.length"},  icon_font, cls="btn"),
        ),
    )
    return (header,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Footer
    """)
    return


@app.cell
def _():
    footer = Footer(id="footer", cls="surface split", style="padding: 0.5rem 1.5rem; align-items: center;")(
        Small("Design System Check", style="--contrast: 0.4;"),
        Small("Classes: layout + color roles · Inline: --type --space --contrast · Components: scoped CSS", style="--contrast: 0.4;"),
    )
    return (footer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Helpers
    pannel, section
    """)
    return


@app.cell
def _():
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





    return panel, section


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##  Buttons
    """)
    return


@app.cell
def _(icon_cancel, icon_font, icon_moon, icon_save, icon_user_plus, section):
    sec_buttons = section("buttons",
        "test: btn.pri, btn.sec",
        "Buttons",
        "The button has no color opinion by default. Color role classes compose onto it. Hover should lighten, active should darken. Disabled drops contrast & opacity.",
        Div(cls="grid")(
             Div(cls="row")(
                Button("disabled",  cls="btn pri", disabled=True), 
                Button("at rest",  cls="btn pri "), 
                Button("hover ",  cls="btn pri hover"), 
                Button("active",  cls="btn pri active"), 
            ),
             Div(cls="row")(
                Button("disabled",  cls="btn sec", disabled=True), 
                Button("at rest",  cls="btn sec"), 
                Button("hover ",  cls="btn sec hover"), 
                Button("active",  cls="btn sec active"), 
            ),
             Div(cls="row")(
                Button(cls="btn sec", disabled=True)(icon_moon),
                Button(cls="btn sec")(icon_moon), 
                Button(cls="btn sec hover")(icon_moon),  
                Button(cls="btn sec active")(icon_moon),   
             ),
             Div(cls="row")(
                Button(cls="btn pri", disabled=True)(icon_moon),
                Button(cls="btn pri")(icon_moon), 
                Button(cls="btn pri hover")(icon_moon),  
                Button(cls="btn pri active")(icon_moon),   
             ),
             Div(cls="row")(
                Button(cls="btn pri")(icon_save),
                Button(cls="btn pri")(icon_user_plus), 
                Button(cls="btn sec")(icon_cancel),  
                Button(cls="btn sec")(icon_font),   
             ),
        )
    )
    return (sec_buttons,)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Demo
    ### Calendar
    """)
    return


@app.cell
def _():
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

    return (month,)


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
                month("April 2026",  2, 30, today=7),   # Apr 1 = Wednesday (offset 2)
                month("May 2026",    4, 31),              # May 1 = Friday (offset 4)
                month("June 2026",   0, 30),              # Jun 1 = Monday (offset 0)
            ),
        ),
    )
    return (sec_calendar,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Color Change
    """)
    return


@app.cell
def _(section):
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ── Toggle Group (scoped component demo) ──
    """)
    return


@app.cell
def _(section):
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
    return (sec_toggle,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ── Contrast Scale ──
    """)
    return


@app.cell
def _(section):
    sec_contrast = section("contrast",
        "test: --contrast as a continuous dial",
        "Contrast Scale",
        "--contrast is not on/off — it's a continuous value from 0 to 1. The color engine computes the optimal text color at every point.",
        Div(cls="surface row", style="padding: 1rem; border-radius: var(--cfg-radius);")(
            Style("me > div { padding: 0.75rem 1rem; border-radius: var(--cfg-radius); flex: 1; min-width: 5rem; text-align: center; }"),
            *[Div(str(v), style=f"--contrast: {v};") for v in [0.1, 0.2, 0.3, 0.5, 0.7, 0.85, 1.0]],
        ),
    )
    return (sec_contrast,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ── Layout Compositions ──
    """)
    return


@app.cell
def _(panel, section):
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
    return (sec_layouts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ── System Summary ──
    """)
    return


@app.cell
def _(section):
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Page
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## head
    """)
    return


@app.cell
def _():
    head = Head( 
        Title("Test Page"),  
        Datastar(),  
        MeCSS(), 
        Pointer(), 
        Favicon("🤖"), 
        Link(rel="stylesheet", href="./static/style.css") 
    )
    return (head,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Main
    """)
    return


@app.cell
def _(
    sec_buttons,
    sec_calendar,
    sec_contrast,
    sec_layouts,
    sec_reflow,
    sec_toggle,
):
    main = Div(id="main", cls="stack", style="padding: 1.5rem; max-width=800px;")(
        sec_buttons,
        sec_calendar,
        sec_reflow,
        sec_toggle,
        sec_contrast,
        sec_layouts,
    )
    return (main,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Body
    """)
    return


@app.cell
def _(aside, footer, header, main, nav):
    body = Body(
        {   "data-signals:_theme"     : "0", 
            "data-signals:_themes"    : "['light', 'dark', null]", # values in css 
            "data-attr:data-ui-theme" : "$_themes[$_theme]", 

            "data-signals:_size"      : "1", 
            "data-signals:_sizes"     : "['sm', 'md', 'lg']",      # Values set in css
            "data-attr:data-ui-size"  : "$_sizes[$_size]",

            "data-signals:_motion"      : "1", 
            "data-signals:_motions"     : "['off', 'on', 'debug']", # values set in css
            "data-attr:data-ui-motion"  : "$_motions[$_motion]"

        },
        cls="app",
    )(
        header,
        nav,
        aside,
        main,
        footer,
    )
    return (body,)


@app.cell
def _(page):
    print(pretty(page))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## page
    """)
    return


@app.cell
def _(body, head):
    page = Html(lang="en")(head, body)
    return (page,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Scratch work
    """)
    return


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Icons
    """)
    return


@app.cell
def _():
    from html_tags import html_to_tag

    icon_cancel = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x-icon lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>''')
    icon_font = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-alarge-small-icon lucide-a-large-small"><path d="m15 16 2.536-7.328a1.02 1.02 1 0 1 1.928 0L22 16"/><path d="M15.697 14h5.606"/><path d="m2 16 4.039-9.69a.5.5 0 0 1 .923 0L11 16"/><path d="M3.304 13h6.392"/></svg>''')
    icon_moon = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon-icon lucide-moon"><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/></svg>''')
    icon_save = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-save-icon lucide-save"><path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7"/><path d="M7 3v4a1 1 0 0 0 1 1h7"/></svg>''')
    icon_user_plus = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user-plus-icon lucide-user-plus"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" x2="19" y1="8" y2="14"/><line x1="22" x2="16" y1="11" y2="11"/></svg>''')
    icon_timer = html_to_tag('''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-timer-icon lucide-timer"><line x1="10" x2="14" y1="2" y2="2"/><line x1="12" x2="15" y1="14" y2="11"/><circle cx="12" cy="14" r="8"/></svg>''')
    return (
        icon_cancel,
        icon_font,
        icon_moon,
        icon_save,
        icon_timer,
        icon_user_plus,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Toolbox
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
