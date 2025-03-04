from fasthtml.common import *

# Define default theme settings
DEFAULT_THEME = {
    'theme_color_scheme': 'light',
    'theme_hue': 210,
    'theme_rotate': 0,
    'theme_chroma': 0.89,
    'theme_button_radius': '--radius-2',
    'theme_typography_scale': 'medium',
    'theme_border_color_step': 4,
    'theme_border_radius': '--radius-2',
    'theme_border_width': 1,
    'theme_primary_color_step': 8,
}

# Radius mapping for border and button radius
RADIUS_MAP = {
    0: '--radius-1',
    1: '--radius-2',
    2: '--radius-3',
    3: '--radius-4',
    4: '--radius-round'
}

# Typography scales for small, medium, and large
TYPOGRAPHY_SCALES = {
    'small': {
        '--font-size-h1': '2.5rem',
        '--font-size-h2': '1.75rem',
        '--font-size-h3': '1.25rem',
        '--font-size-h4': '1.1rem',
        '--font-size-h5': '1rem',
        '--font-size-h6': '0.875rem',
        '--font-size-lg': '1.1rem',
        '--font-size-md': '0.875rem',
        '--font-size-sm': '0.75rem',
        '--font-size-xs': '0.625rem',
    },
    'medium': {
        '--font-size-h1': '3.5rem',
        '--font-size-h2': '2rem',
        '--font-size-h3': '1.5rem',
        '--font-size-h4': '1.25rem',
        '--font-size-h5': '1.1rem',
        '--font-size-h6': '1rem',
        '--font-size-lg': '1.25rem',
        '--font-size-md': '1rem',
        '--font-size-sm': '0.875rem',
        '--font-size-xs': '0.75rem',
    },
    'large': {
        '--font-size-h1': '4.5rem',
        '--font-size-h2': '2.5rem',
        '--font-size-h3': '1.75rem',
        '--font-size-h4': '1.5rem',
        '--font-size-h5': '1.25rem',
        '--font-size-h6': '1.1rem',
        '--font-size-lg': '1.5rem',
        '--font-size-md': '1.1rem',
        '--font-size-sm': '1rem',
        '--font-size-xs': '0.875rem',
    }
}

# Initialize FastHTML app
app, rt = fast_app(
    exts='head-support',
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='https://deufel.github.io/css/css/main.css'),
        HighlightJS(langs=['css']),
        Link(rel='stylesheet',
             href='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/tokyo-night-dark.min.css')
    )
)

def css_preview(session):
    """Generate the CSS preview card"""
    return Div(cls="card outlined margin")(
        Hgroup(
            P("Live CSS", cls="overline"),
            H2("Current Theme CSS"),
            P("This shows the current CSS being applied to the page"),
        ),
        Pre(style="max-width: none; width: 100%;")(
            Code(id="css-preview", hx_get="/theme-css", hx_trigger="theme-update from:body", 
                 hx_swap="innerHTML", style="overflow: hidden;")(
                generate_theme_css(session),
            )
        ),
        Script("""
        (function() {
            hljs.highlightElement(document.querySelector('#css-preview'));
            let highlightTimeout;
            function debouncedHighlight() {
                clearTimeout(highlightTimeout);
                highlightTimeout = setTimeout(() => {
                    const codeElement = document.querySelector('#css-preview');
                    if (codeElement) hljs.highlightElement(codeElement);
                }, 50);
            }
            htmx.on('#css-preview', 'htmx:afterSwap', debouncedHighlight);
        })();
        """)
    )

def generate_theme_css(session):
    """Generate CSS based on session theme values"""
    css = [':root {']
    css.append(f'color-scheme: {session["theme_color_scheme"]};')
    css.append(f'--palette-hue: {session["theme_hue"]};')
    css.append(f'--palette-hue-rotate-by: {session["theme_rotate"]};')
    css.append(f'--palette-chroma: {session["theme_chroma"]};')
    css.append(f'--button-border-radius: var({session["theme_button_radius"]});')
    
    # Add typography variables based on selected scale
    scale = session.get('theme_typography_scale', 'medium')
    for var, value in TYPOGRAPHY_SCALES[scale].items():
        css.append(f'{var}: {value};')
    
    # Add border variables
    css.append(f'--border-color: var(--color-{session["theme_border_color_step"]});')
    css.append(f'--border-radius: var({session["theme_border_radius"]});')
    css.append(f'--border-width: {session["theme_border_width"]}px;')
    
    # Add primary color
    css.append(f'--primary: var(--color-{session["theme_primary_color_step"]});')
    
    css.append('}')
    return '\n'.join(css)

# Routes

@rt("/theme-css")
def get(session):
    return Code(generate_theme_css(session))

@rt("/theme")
def post(session, color_scheme:int=None, hue:int=None, rotate:int=None,
         chroma:float=None, button_radius:int=None, typography_scale:int=None,
         border_color_step:int=None, border_radius:int=None, border_width:int=None,
         primary_color_step:int=None):
    """Handle theme updates"""
    # Map numeric inputs to corresponding values
    if color_scheme is not None:
        scheme_map = {0: 'light', 1: 'dark'}
        color_scheme = scheme_map.get(color_scheme)
    if button_radius is not None:
        button_radius = RADIUS_MAP.get(button_radius)
    if border_radius is not None:
        border_radius = RADIUS_MAP.get(border_radius)

    # Validate and update session
    if color_scheme and color_scheme in ['light', 'dark']:
        session['theme_color_scheme'] = color_scheme
    if hue is not None and 0 <= hue <= 360:
        session['theme_hue'] = hue
    if rotate is not None and -20 <= rotate <= 20:
        session['theme_rotate'] = rotate
    if chroma is not None and 0 <= chroma <= 1:
        session['theme_chroma'] = chroma
    if button_radius is not None:
        session['theme_button_radius'] = button_radius
    if typography_scale is not None and 0 <= typography_scale <= 2:
        session['theme_typography_scale'] = ['small', 'medium', 'large'][typography_scale]
    if border_color_step is not None and 1 <= border_color_step <= 12:
        session['theme_border_color_step'] = border_color_step
    if border_radius is not None and 0 <= border_radius <= 4:
        session['theme_border_radius'] = border_radius
    if border_width is not None and 0 <= border_width <= 5:
        session['theme_border_width'] = border_width
    if primary_color_step is not None and 1 <= primary_color_step <= 12:
        session['theme_primary_color_step'] = primary_color_step

    # Generate updated CSS
    css = [':root {']
    if 'theme_color_scheme' in session:
        css.append(f'color-scheme: {session["theme_color_scheme"]};')
    if 'theme_hue' in session:
        css.append(f'--palette-hue: {session["theme_hue"]};')
    if 'theme_rotate' in session:
        css.append(f'--palette-hue-rotate-by: {session["theme_rotate"]};')
    if 'theme_chroma' in session:
        css.append(f'--palette-chroma: {session["theme_chroma"]};')
    if 'theme_button_radius' in session:
        css.append(f'--button-border-radius: var({session["theme_button_radius"]});')
    if 'theme_typography_scale' in session:
        scale = session['theme_typography_scale']
        for var, value in TYPOGRAPHY_SCALES[scale].items():
            css.append(f'{var}: {value};')
    if 'theme_border_color_step' in session:
        css.append(f'--border-color: var(--color-{session["theme_border_color_step"]});')
    if 'theme_border_radius' in session:
        css.append(f'--border-radius: var({session["theme_border_radius"]});')
    if 'theme_border_width' in session:
        css.append(f'--border-width: {session["theme_border_width"]}px;')
    if 'theme_primary_color_step' in session:
        css.append(f'--primary: var(--color-{session["theme_primary_color_step"]});')
    css.append('}')
    css_text = '\n'.join(css)

    return (
        Style(css_text, hx_head="re-eval"),
        Script("htmx.trigger(document.body, 'theme-update');")
    )

@rt("/")
def get(session):
    """Main theme configurator page"""
    # Set default theme values
    for key, value in DEFAULT_THEME.items():
        session.setdefault(key, value)
    initial_css = Style(generate_theme_css(session), hx_head='merge')

    theme_controls = Div(cls="card outlined margin")(
        Hgroup(
            P("Theme Controls", cls="overline"),
            H2("Theme"),
            P("Move the sliders to see the change in the Design System Components"),
        ),
        Div(cls="content")(
            # Theme Mode
            Div(
                Label(cls="range")(
                    Span(cls="label")("Theme Mode (Light ↔ Dark)"),
                    Input(
                        type='range', min=0, max=1, step=1,
                        value={'light': 0, 'dark': 1}[session['theme_color_scheme']],
                        name="color_scheme", hx_post="/theme", hx_trigger="change"
                    )
                )
            ),
            # Button Radius
            Div(
                Label(cls="range")(
                    Span(cls="label")("Button Radius (Sharp → Round)"),
                    Input(
                        type='range', min=0, max=4, step=1,
                        value=[k for k, v in RADIUS_MAP.items() if v == session['theme_button_radius']][0],
                        name="button_radius", hx_post="/theme", hx_trigger="change"
                    )
                )
            ),
            # Typography Scale
            Div(
                Label(cls="range")(
                    Span(cls="label")("Typography Scale (Small → Medium → Large)"),
                    Input(
                        type='range', min=0, max=2, step=1,
                        value={'small': 0, 'medium': 1, 'large': 2}[session['theme_typography_scale']],
                        name="typography_scale", hx_post="/theme", hx_trigger="change"
                    )
                )
            ),
            # Border Color Step
            Div(
                Label(cls="range")(
                    Span(cls="label")("Border Color Step [1,12]"),
                    Input(
                        type='range', min=1, max=12, step=1,
                        value=session['theme_border_color_step'],
                        name="border_color_step", hx_post="/theme", hx_trigger="change"
                    )
                )
            ),
            # Border Radius
            Div(
                Label(cls="range")(
                    Span(cls="label")("Border Radius (Sharp → Round)"),
                    Input(
                        type='range', min=0, max=4, step=1,
                        value=[k for k, v in RADIUS_MAP.items() if v == session['theme_border_radius']][0],
                        name="border_radius", hx_post="/theme", hx_trigger="change"
                    )
                )
            ),
            # Border Width
            Div(
                Label(cls="range")(
                    Span(cls="label")("Border Width (px) [0,5]"),
                    Input(
                        type='range', min=0, max=5, step=1,
                        value=session['theme_border_width'],
                        name="border_width", hx_post="/theme", hx_trigger="change"
                    )
                )
            ),
            # Primary Color Step
            Div(
                Label(cls="range")(
                    Span(cls="label")("Primary Color Step [1,12]"),
                    Input(
                        type='range', min=1, max=12, step=1,
                        value=session['theme_primary_color_step'],
                        name="primary_color_step", hx_post="/theme", hx_trigger="change"
                    )
                )
            ),
            # Hue
            Div(
                Label(cls="range")(
                    Span(cls="label")("Theme Hue [0, 360]"),
                    Input(type='range', min=0, max=360, value=session['theme_hue'], 
                          name="hue", hx_post="/theme", hx_trigger="change")
                )
            ),
            # Hue Rotation
            Div(
                Label(cls="range")(
                    Span(cls="label")("Color Palette Hue Step [-20, 20]"),
                    Input(type='range', min=-20, max=20, value=session['theme_rotate'], 
                          name="rotate", hx_post="/theme", hx_trigger="change")
                )
            ),
            # Chroma
            Div(
                Label(cls="range")(
                    Span(cls="label")("Chroma [0,1]"),
                    Input(type='range', min=0, max=1, value=session['theme_chroma'], step=0.01, 
                          name="chroma", hx_post="/theme", hx_trigger="change")
                )
            )
        ),
        Div(cls="actions")(
            Button(cls="button")("Default"),
            Button(cls="button outlined")("Outlined"),
            Button(cls="button tonal")("Tonal"),
            Button(cls="button filled")("Filled"),
            Button(cls="button elevated")("Elevated"),
        )
    )

    preview = (
        Div(cls="card outlined margin")(
            Hgroup(
                P("Color Palette"),
                H2("Theme Colors"),
            ),
            Div(cls="flex-wrap padding")(
                *[Div(
                    Style=f"""
                        width: var(--size-8);
                        height: var(--size-8);
                        background: var(--color-{i});
                        border-radius: var(--radius-2);
                        position: relative;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    """
                )(P(Style=f"color: lch(from var(--color-{i}) calc((50 - l) * infinity) 0 0 )")(i))
                for i in range(1, 13)]
            )
        ),
        css_preview(session)
    )

    return (
        Title("OpenProps UI Theme Previewer"),
        Div(cls="flex-center")(
            initial_css,
            Container(hx_ext="head-support")(
                theme_controls,
                preview,
            )
        )
    )

serve()
