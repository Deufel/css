╔═══════════════════════════════════════════════════════════════════╗
║              THE colorNtype MENTAL MODEL                          ║
║                                                                   ║
║   Every element is one of two things:                             ║
╚═══════════════════════════════════════════════════════════════════╝


   ┌─────────────────────────────┐      ┌─────────────────────────────┐
   │       SURFACE               │      │       CONTENT               │
   │   (paints a background)     │      │   (sits on a surface)       │
   ├─────────────────────────────┤      ├─────────────────────────────┤
   │                             │      │                             │
   │  How to make one:           │      │  How to make one:           │
   │                             │      │                             │
   │   .surface                  │      │   (the default)             │
   │     auto-nests, theme-      │      │     transparent background  │
   │     aware, no chroma        │      │                             │
   │                             │      │  How it knows the bg:       │
   │   --bg: 0 … 1               │      │                             │
   │     explicit chromatic      │      │   reads inherited --_bg     │
   │     paint, theme-stable     │      │   from nearest surface      │
   │                             │      │                             │
   │  What it sets:              │      │  What it can declare:       │
   │                             │      │                             │
   │   --_bg ───────────────────────────► --fg-contrast (0…1)         │
   │   (resolved bg color)       │      │   --fg-chroma   (0…0.4)     │
   │                             │      │                             │
   │  What it can decorate with: │      │  What it gets back:         │
   │                             │      │                             │
   │   var(--border)  quiet      │      │   color (auto-flips         │
   │   var(--Border)  loud       │      │     against --_bg)          │
   │                             │      │                             │
   └─────────────────────────────┘      └─────────────────────────────┘
                │                                      ▲
                │                                      │
                │     --_bg cascades down the tree     │
                └──────────────────────────────────────┘
                            (inheritance)


╔═══════════════════════════════════════════════════════════════════╗
║   WHAT CHANGES WITH THEME (light ↔ dark)                          ║
╚═══════════════════════════════════════════════════════════════════╝

   .surface  ─────────► flips        (the canvas itself inverts)
   --bg: 0…1 ─────────► STABLE       (a 0.4 green is the same green
                                      in both themes — by design)
   --border  ─────────► flips        (must contrast its surrounding)
   --Border  ─────────► flips        (same reason)
   --fg-contrast ────► STABLE input, flipped output
                       (formula re-resolves against new --_bg)


╔═══════════════════════════════════════════════════════════════════╗
║   THE ONE FORMULA                                                 ║
╚═══════════════════════════════════════════════════════════════════╝

   inputs ──────────────────► formula ────────────────► outputs
   ──────                     ───────                   ───────

   --bg          (canvas)       │                       --_bg
   --hue                        │                       color
   --hue-shift                  ├──── one math ────►    --border
   --fg-contrast (ink)          │     pass              --Border
   --fg-chroma                  │                       fill (svg)
   theme                        │                       stroke (svg)


╔═══════════════════════════════════════════════════════════════════╗
║   WHY THIS IS THE WHOLE SYSTEM                                    ║
╚═══════════════════════════════════════════════════════════════════╝

   You change ONE input on a parent…
   ────────────────────────────────

      <div style="--hue: 145">          ← change this
        <div class="surface">           ← surface re-resolves
          <h2>Title</h2>                ← contrast re-resolves
          <button class="btn pri">Go    ← button re-resolves
          </button>                       border re-resolves
        </div>
      </div>

   …and EVERYTHING below it updates, because every output is a
   function of the same inputs through the same formula.

   No coordination. No tokens to keep in sync. No light/dark pairs
   to maintain. The surface declares the canvas, the content
   declares its contrast, the formula does the rest.
