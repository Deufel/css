```
╔═══════════════════════════════════════════════════════════════════╗
║              THE colorNtype MENTAL MODEL                          ║
║                                                                   ║
║   The whole system, in two axes and three hue tokens.             ║
╚═══════════════════════════════════════════════════════════════════╝


   ┌─────────────────────────────────────────────────────────────┐
   │                  EVERY ELEMENT HAS TWO KNOBS                │
   │                                                             │
   │   --bg : -1  ←──── 0 ────→ +1     PAINT THE BACKGROUND      │
   │           (none)  (muted) (vivid)                           │
   │                                                             │
   │   --fg : -1  ←──── 0 ────→ +1     PAINT THE INK             │
   │       (contrast) (none)  (chromatic)                        │
   │                                                             │
   │  Both axes are continuous. Both work in HTML and SVG.       │
   └─────────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════════════════════════════════╗
║   THE TWO ROLES — MUTUALLY EXCLUSIVE                              ║
╚═══════════════════════════════════════════════════════════════════╝

   ┌──────────────────────────────┐    ┌──────────────────────────────┐
   │       .surface               │    │     CHROMATIC ACCENT         │
   │  (structural container)      │    │  (semantic colored element)  │
   ├──────────────────────────────┤    ├──────────────────────────────┤
   │                              │    │                              │
   │  Default --bg: -1            │    │  Set --bg: 0 … 1             │
   │     transparent, tracks      │    │     explicit chromatic       │
   │     parent                   │    │     paint                    │
   │                              │    │                              │
   │  Auto-depth via :has()       │    │  Theme-STABLE                │
   │     more nesting = brighter  │    │     same color in light      │
   │     surface (focus moves     │    │     and dark themes          │
   │     toward the most-nested   │    │                              │
   │     content)                 │    │  No structural role          │
   │                              │    │     no auto-depth            │
   │  Theme-FLIPS                 │    │     no theme tracking        │
   │     light surfaces in light  │    │                              │
   │     mode, dark surfaces in   │    │  Use for: chips, badges,     │
   │     dark mode                │    │     status cards, brand      │
   │                              │    │     callouts, swatches,      │
   │  Use for: cards, panels,     │    │     buttons, avatars         │
   │     modals, sections, the    │    │                              │
   │     page itself, anything    │    │  Examples:                   │
   │     holding content          │    │     <div                     │
   │                              │    │       style="--bg: 0.55      │
   │  Examples:                   │    │             --hue-lock: 145" │
   │     <div class="surface">    │    │     >LIVE</div>              │
   │       <h2>Title</h2>         │    │                              │
   │       <p>Body…</p>           │    │     <button                  │
   │     </div>                   │    │       style="--bg: 0.5">     │
   │                              │    │       Continue               │
   │                              │    │     </button>                │
   └──────────────────────────────┘    └──────────────────────────────┘

       Pick ONE per element. Never both. If you feel like you want
       both, you actually want a .surface CONTAINING a chromatic
       child element.


╔═══════════════════════════════════════════════════════════════════╗
║   THE THREE HUE TOKENS                                            ║
╚═══════════════════════════════════════════════════════════════════╝

      --hue           page-level default. Cascades freely.
                      Set on :root or any subtree as a default
                      for everything below.

      --hue-shift     relative offset. Adds to the inherited
                      --hue. Stacks with parent shifts.
                      Use for: subtle subtree variation.

      --hue-lock      absolute pin. Wins over --hue and
                      --hue-shift from above.
                      Use for: semantic colors (success/info/
                      warning/danger), brand-color elements,
                      anything that must be a specific hue
                      regardless of cascade.

   ┌─────────────────────────────────────────────────────────┐
   │  Resolution:                                            │
   │                                                         │
   │    --_h: var(--hue-lock,                                │
   │            calc(var(--hue) + var(--hue-shift)))         │
   │                                                         │
   │  If --hue-lock is set anywhere up the cascade,          │
   │  it wins. Otherwise: page hue + shifts.                 │
   └─────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════════════════════════════════╗
║   WHAT CHANGES WITH THEME (light ↔ dark)                          ║
╚═══════════════════════════════════════════════════════════════════╝

   .surface          ───►  FLIPS         (canvas inverts)

   --bg: 0…1         ───►  STABLE        (a 0.4 green stays
                                          green in both themes —
                                          by design)

   --fg: -1…0        ───►  FLIPS         (contrast pole derives
                                          from the surface, so
                                          ink lands correctly
                                          against either pole)

   --fg: 0…1         ───►  STABLE        (chromatic ink, same
                                          color in both themes,
                                          mirror of --bg)

   --hue / --hue-lock /
   --hue-shift       ───►  STABLE        (hue is theme-orthogonal)

   --border          ───►  FLIPS
   --Border          ───►  FLIPS


╔═══════════════════════════════════════════════════════════════════╗
║   THE FG AXIS — TWO MODES IN ONE NUMBER                           ║
╚═══════════════════════════════════════════════════════════════════╝

       --fg : -1 ────────── 0 ────────── +1
              │             │             │
              │             │             │
       max contrast    invisible      max chromatic
       (theme-aware)   (= surface)    (theme-stable)
              │                           │
              │                           │
       contextual ink                 brand ink
       (titles, body                  (highlights,
        text, default)                 chart lines,
                                       deliberate
                                       color)

       Negative half = contrast against the surface.
       Positive half = same color the surface would be at --bg = X.

       This means:  --fg: 0.4 produces the same color as --bg: 0.4
                    on a surface at the same hue.


╔═══════════════════════════════════════════════════════════════════╗
║   THE ONE FORMULA                                                 ║
╚═══════════════════════════════════════════════════════════════════╝

   inputs ────────────────────► formula ──────────────► outputs
   ──────                       ───────                 ───────

   --bg              (canvas)        │                  --_bg
   --fg              (ink)           │                  color
   --hue                             │                  fill (svg)
   --hue-lock                        ├──── one math ──► stroke (svg)
   --hue-shift                       │     pass         --border
   --depth (auto)                    │                  --Border
   theme (--cfg-color-*)             │
   chromatic config (--cfg-color-    │
     muted-l/c, vivid-l/c,           │
     surf-chroma, fg-tint)           │


╔═══════════════════════════════════════════════════════════════════╗
║   THE CASCADE IN ACTION                                           ║
╚═══════════════════════════════════════════════════════════════════╝

   Change ONE input on a parent…
   ─────────────────────────────

      <body style="--hue: 145">         ← change this
        <main class="surface">          ← surface re-resolves
          <article class="surface">     ← deeper surface re-resolves
            <h2>Title</h2>              ← --fg: -1 (default ink)
                                          re-resolves contrast
            <span style="--bg: 0.55">   ← chromatic accent ignores
              new                         hue cascade IF it has
            </span>                       --hue-lock; otherwise
                                          tints with --hue
            <button style="--bg: 0.5">  ← chromatic, picks up --hue
              Go
            </button>
          </article>
        </main>
      </body>

   …and EVERYTHING below updates because every output is a
   function of the same inputs through the same formula.

   No coordination. No tokens to keep in sync. No light/dark
   pairs to maintain.

   Surfaces declare the canvas.
   Chromatic --bg declares semantic color.
   --fg declares ink intent.
   The three hue tokens decide what hue to render in.
   The formula does the rest.


╔═══════════════════════════════════════════════════════════════════╗
║   THE PUBLIC API, IN ONE BLOCK                                    ║
╚═══════════════════════════════════════════════════════════════════╝

   Per-element:
   ──────────
      --bg          -1 … 1     surface intensity (HTML elements)
      --fg          -1 … 1     ink intensity
      --hue         0 … 360    page-level hue (cascades)
      --hue-shift   any        relative offset (cascades)
      --hue-lock    0 … 360    absolute pin (cascades, overrides)

   Class:
   ─────
      .surface                 declares structural container,
                               participates in depth cascade

   Designer config:
   ───────────────
      --cfg-color-muted-l       muted-end lightness  (--bg = 0)
      --cfg-color-muted-c       muted-end chroma     (--bg = 0)
      --cfg-color-vivid-l       vivid-end lightness  (--bg = 1)
      --cfg-color-vivid-c       vivid-end chroma     (--bg = 1)
      --cfg-color-surf-chroma   hue carry on neutral surfaces
      --cfg-fg-tint             hue carry on contrast ink

   That's it. Six numbers tune the chromatic identity.
   Two numbers per element say what color it wants to be.
   Three tokens decide which hue to use.
   One class makes a structural surface.
```
