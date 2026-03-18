# CSS 

## Reference


A CSS design system that derives surfaces, type, borders, shadows, and
interaction states from two inputs: a color and a number. No classes for
color. No tokens for surfaces. Set a custom property, the engine computes
the rest.
```
    ┌──────────────────────────────────────────────────────────┐
    │  <div style="--bg: 5">                                   │
    │  <div style="--bg: 5; --border: 2">                      │
    │  <button style="--bg: 14; --interactive: 2">             │
    │  <h2 style="--type: 2.7">                                │
    │  <div style="--bg: 3; --shadow: 4">                      │
    │                                                          │
    │  That's the entire API.                                  │
    └──────────────────────────────────────────────────────────┘
```
Browser support: Safari 17.4+, Chrome 111+, Firefox 128+.


---


## Architecture

### Layer order

    @layer reset, engine, typography, components, demo;

Everything the engine computes lives in `engine`. Typography and
components consume engine outputs but never fight them on specificity.

### The auto-trigger mechanism

The engine uses `:where([style*="--bg:"])` to detect when you set a
property inline. This is both the value assignment and the activation —
no data attributes, no sentinel values, no JS.

`:where()` keeps specificity at (0,0,0). The colon in the substring
match (`"--bg:"` not `"--bg"`) prevents false-positives against
`--bg-base` or similar.

**Trade-off:** won't trigger from `--bg` set in a CSS class. Surface
levels are per-instance (inline), so this is the correct boundary. For
class-driven surfaces, duplicate the background math in the class rule
(as `body` does).

### Inheritance model

    ┌─────────────────────────────────────────────────────────┐
    │  INHERITS (cascade down the tree)                       │
    │    --color          seed color (oklch)                  │
    │    --_dark          0–1 spectrum                        │
    │    --_motion        0 or 1                              │
    │    --_bg            computed background color           │
    │    --cfg-*          all config tokens                   │
    │                                                         │
    │  DOES NOT INHERIT (per-element only)                    │
    │    --bg             surface level                       │
    │    --border         border level                        │
    │    --interactive    hover shift amount                  │
    │    --shadow         elevation level                     │
    │    --type           type scale step                     │
    │    --contrast       text contrast fraction              │
    └─────────────────────────────────────────────────────────┘

This split is deliberate. `--color` and `--_dark` flow down so entire
subtrees re-derive when you change the seed. `--bg` does NOT inherit so
a child surface doesn't accidentally adopt its parent's level.


---


## Variable reference

### Inputs (you set these)

| Variable         | Type       | Default                 | Purpose                            |
|------------------|------------|-------------------------|------------------------------------|
| `--color`        | `<color>`  | `oklch(0.5 0.2 85)`     | Seed. Everything derives from this |
| `--_dark`        | `<number>` | `0`                     | 0 = light, 1 = dark, fractional OK |
| `--bg`           | `<number>` | `0`                     | Surface level (0–20 typical)       |
| `--border`       | `<number>` | `0`                     | Border contrast level (1–8 typical)|
| `--interactive`  | `<number>` | `0`                     | Hover shift in bg levels           |
| `--shadow`       | `<number>` | `0`                     | Elevation (1–10 typical)           |
| `--type`         | `<number>` | `0`                     | Type scale step, fractional OK     |
| `--contrast`     | `<number>` | `0.85`                  | Text contrast fraction (0–1)       |

### Outputs (engine computes these)

| Variable      | Contains                          | Used by                     |
|---------------|-----------------------------------|-----------------------------|
| `--_bg`       | Computed background color (oklch) | border, contrast, shadow    |
| `--_bg-base`  | Lightness anchor for surface 0    | background, interactive     |
| `--_bg-step`  | Lightness increment per level     | background, interactive     |
| `--_t-min`    | Min font-size at current step     | type clamp                  |
| `--_t-max`    | Max font-size at current step     | type clamp                  |
| `--_b-eff`    | Effective border level on hover   | border interactive states   |

### Configuration

| Variable                | Default      | Controls                     |
|-------------------------|--------------|------------------------------|
| `--cfg-fluid-min-vp`    | `22.5rem`    | Fluid type/space lower bound |
| `--cfg-fluid-max-vp`    | `77.5rem`    | Fluid type/space upper bound |
| `--cfg-type-min`        | `1.125rem`   | Base font-size (narrow)      |
| `--cfg-type-max`        | `1.25rem`    | Base font-size (wide)        |
| `--cfg-type-min-ratio`  | `1.2`        | Scale ratio (narrow)         |
| `--cfg-type-max-ratio`  | `1.25`       | Scale ratio (wide)           |
| `--cfg-type-scale`      | `1`          | Global type multiplier       |
| `--cfg-space-scale`     | `1`          | Global space multiplier      |
| `--cfg-border-radius`   | `0.375rem`   | Default border-radius        |

### Environment overrides

| Attribute / media query              | Effect                    |
|--------------------------------------|---------------------------|
| `prefers-color-scheme: dark`         | `--_dark: 1`              |
| `prefers-reduced-motion: reduce`     | `--_motion: 0`            |
| `html[data-ui-scheme="dark"]`        | `--_dark: 1`              |
| `html[data-ui-scheme="light"]`       | `--_dark: 0`              |
| `html[data-ui-motion="none"]`        | `--_motion: 0`            |
| `html[data-ui-density="compact"]`    | `--cfg-space-scale: 0.75` |
| `html[data-ui-density="comfortable"]`| `--cfg-space-scale: 1.25` |
| `html[data-ui-size="small"]`         | `--cfg-type-scale: 0.85`  |
| `html[data-ui-size="large"]`         | `--cfg-type-scale: 1.15`  |


---


## Processing pipelines

### Background + contrast

    --color ──┐
    --_dark ──┤
    --bg ─────┤
              ▼
    ┌──────────────────────────────────────────────┐
    │  BACKGROUND                                  │
    │                                              │
    │  base-L = 95% − _dark × 75%                  │
    │  step-L = −3% + _dark × 7%                   │
    │                                              │
    │  L = clamp(10%, base-L + bg × step-L, 99%)   │
    │  C = min(0.02 + bg² × 0.004, seed-C)         │
    │  H = seed-H + bg × 0.4                       │
    │                                              │
    │  output: --_bg = oklch(L C H)                │
    │          background: --_bg                   │
    └────────────────┬─────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │  CONTRAST (auto text color)             │
    │                                         │
    │  from --_bg:                            │
    │    target = (L < 0.6) ? 1 : 0           │
    │    text-L = L + (target − L) × contrast │
    │                                         │
    │  output: color = oklch(text-L C H)      │
    └─────────────────────────────────────────┘

The `(0.6 − l) × 999` trick is a CSS-only conditional. When background
lightness is below 0.6 the result clamps to 1 (white target); above 0.6
it clamps to 0 (black target). The `--contrast` fraction (default 0.85)
controls how far toward the target the text travels. Set to 0.4 for
muted text, 0.95 for maximum sharpness.

**Lightness behavior across --_dark:**

    --_dark:  0.0    0.3    0.5    0.7    1.0
    base-L:   95%    72.5%  57.5%  42.5%  20%
    step-L:   −3%    −0.9%  +0.5%  +1.9%  +4%

    At --_dark: 0 (light mode), each bg level darkens by 3%.
    At --_dark: 1 (dark mode), each bg level lightens by 4%.
    The crossover near --_dark: 0.43 is where step-L ≈ 0
    and all surfaces collapse to a single tone.

**Chroma behavior:**

    bg:  0  →  C = 0.020  (nearly achromatic)
    bg:  5  →  C = 0.120  (moderate saturation)
    bg: 10  →  C = 0.420  (capped at seed chroma)

    Quadratic ramp (bg² × 0.004) means low levels stay neutral
    while high levels approach the seed's full chroma. The min()
    ensures the border never exceeds what the seed color provides.


### Border

    --_bg ────┐
    --border ─┤
              ▼
    ┌─────────────────────────────────────────┐
    │  BORDER                                 │
    │                                         │
    │  from --_bg:                            │
    │    target = (L < 0.6) ? 1 : 0           │
    │    border-L = L + (target − L)          │
    │                     × border × 0.1      │
    │    border-C = min(C + border × 0.012,   │
    │                                  0.15)  │
    │    border-H = H + border × 0.3          │
    │                                         │
    │  output: border-color = oklch(...)      │
    └─────────────────────────────────────────┘

The lightness formula is identical to contrast text but scaled by
`border × 0.1` instead of `--contrast`. So `--border: 3` moves 30% of
the way toward the contrast pole — a partial step rather than the full
swing that text takes.

Chroma blooms slightly with level (capped at 0.15) so borders aren't
flat grey. Hue drifts at 0.3°/level, matching the drift direction of
`--bg`.


### Border + interactive composition

    --border ──────┐
    --interactive ─┤
                   ▼
    ┌──────────────────────────────────────────┐
    │  INTERACTIVE BORDER                      │
    │                                          │
    │  rest:   effective = border              │
    │  hover:  effective = border + int × 0.5  │
    │  active: effective = border + int × 1.0  │
    │                                          │
    │  Same L/C/H formula as above,            │
    │  substituting effective for border.      │
    └──────────────────────────────────────────┘

This is independent of the background's interactive shift. On hover, the
background moves by `--interactive` levels AND the border intensifies by
`interactive × 0.5` — they react simultaneously but at different rates.


### Interactive (background)

    --bg ──────────┐
    --interactive ─┤
    --color ───────┤
    --_dark ───────┤
                   ▼
    ┌─────────────────────────────────────────┐
    │  INTERACTIVE BACKGROUND                 │
    │                                         │
    │  hover:  level = bg + interactive       │
    │  active: level = bg + interactive × 2   │
    │                                         │
    │  Recomputes --_bg using the shifted     │
    │  level through the full background      │
    │  formula (same L/C/H math).             │
    │                                         │
    │  Text contrast auto-updates because     │
    │  it reads from --_bg.                   │
    └─────────────────────────────────────────┘

The hover state literally recomputes the background at a higher surface
level. This means it doesn't just change lightness — chroma and hue
shift too, exactly as if you'd set a higher `--bg` value.


### Shadow

    --color ──┐
    --shadow ─┤
              ▼
    ┌─────────────────────────────────────────┐
    │  SHADOW                                 │
    │                                         │
    │  offset-y = shadow × 1px                │
    │  blur     = shadow × 3px                │
    │  spread   = shadow × 1px                │
    │                                         │
    │  color = oklch(                         │
    │    from --color:                        │
    │      L = 30%                            │
    │      C = seed-C × 0.5                   │
    │      H = seed-H                         │
    │      α = 0.15 + shadow × 0.04           │
    │  )                                      │
    └─────────────────────────────────────────┘

Shadow derives from `--color` (not `--_bg`), so the shadow hue matches
the seed. Lightness is fixed at 30%, chroma is halved — dark and
slightly chromatic, never flat grey.


### Type

    --type ───────────┐
    --cfg-type-* ─────┤
    viewport width ───┤
                      ▼
    ┌─────────────────────────────────────────┐
    │  TYPE                                   │
    │                                         │
    │  min = cfg-type-min × ratio-min ^ step  │
    │  max = cfg-type-max × ratio-max ^ step  │
    │                                         │
    │  font-size = clamp(min, fluid, max)     │
    │              × cfg-type-scale           │
    │                                         │
    │  letter-spacing = 0.01em − step × 0.01  │
    │  line-height    = 1.5 − step × 0.075    │
    └─────────────────────────────────────────┘

`pow()` is computed inline — no pre-baked tokens. `--type: 2.7` gives a
size between step 2 and step 3. Negative steps work. Letter-spacing
tightens as size increases; line-height compresses for headings.

Triggers: `[style*="--type:"]`, plus `h1`–`h6`, `small`, `.small`,
`.xs` via `:where()`.


### Space tokens

Pre-baked fluid tokens on `:root`. Not driven by `--bg` or `--color`:

    --space--1    (0.36rem → 0.45rem)
    --space-0     (0.50rem → 0.75rem)
    --space-1     (0.70rem → 1.24rem)
    --space-2     (0.98rem → 2.04rem)
    --space-3     (1.37rem → 3.37rem)
    --space-4     (1.92rem → 5.56rem)
    --space-5     (2.69rem → 9.17rem)

Used via `--_gap` on layout primitives.


---


## Composability

Every property is orthogonal. Any combination works because each reads
only its own inputs:

    ┌──────────────────────────────────────────────────┐
    │  style="--bg: 3;                                 │
    │         --border: 2;                             │
    │         --shadow: 4;                             │
    │         --interactive: 2"                        │
    │                                                  │
    │   --bg: 3           → background + text color    │
    │   --border: 2       → border from --_bg          │
    │   --shadow: 4       → shadow from --color        │
    │   --interactive: 2  → hover shifts bg by +2      │
    │                       hover intensifies border   │
    │                                                  │
    │  On hover, FOUR things change simultaneously:    │
    │    1. background recomputes at level 5           │
    │    2. text contrast re-derives from new --_bg    │
    │    3. border intensifies (eff = 2 + 2×0.5 = 3)   │
    │    4. shadow stays constant (not interactive)    │
    └──────────────────────────────────────────────────┘

### Dependency graph

    --color ─────────────────┬──────────────────────┐
    --_dark ────────┐        │                      │
                    ▼        ▼                      ▼
    --bg ────→ [BACKGROUND] ──→ --_bg ──→ [BORDER] [SHADOW]
                    │              │          ▲
                    │              ▼          │
                    │         [CONTRAST]      │
                    │              │          │
    --interactive ──┴──────────────┴──────────┘
                    │
                    ▼
               [HOVER/ACTIVE]
               recomputes --_bg
               intensifies border

    --type ────→ [TYPE] (independent, reads only config)

Key: `--_bg` is the central hub. Background computes it, then contrast,
border, and interactive states all read from it. Shadow is the one
exception — it reads `--color` directly.


### Subtree re-derivation

    <div style="--color: oklch(0.5 0.2 265)">
      <!-- everything inside re-derives:
           backgrounds shift to blue hues,
           borders pick up blue chroma,
           shadows tint blue,
           text contrast still works -->
    </div>

Setting `--color` on any element triggers the background rule (via
`[style*="--color:"]`), and because `--color` inherits, all descendants
re-derive too.


---


## Layout primitives

    .stack   flex column, gap: --_gap (default --space-1)
    .row     flex row, wrapping, gap: --_gap (default --space-0)
    .grid    auto-fit grid, min col: --_col (default 15rem)

Override gap: `style="--_gap: var(--space-3)"`.
Override column min: `style="--_col: 8rem"`.


---


## Typography layer

### Heading map

    h1  →  --type: 4     font-heading
    h2  →  --type: 3     font-heading
    h3  →  --type: 2     font-heading
    h4  →  --type: 1     font-heading
    body → --type: 0     font-body

### Font stacks

    --font-body:    Charter, 'Bitstream Charter', Cambria, serif
    --font-heading: 'Iowan Old Style', 'Palatino Linotype', P052, serif
    --font-mono:    'Dank Mono', Inconsolata, 'Fira Mono', ui-monospace

### Utilities

    .muted   color at 40% contrast (vs 85% default)
    .small   --type: -1
    .xs      --type: -1.5

### Heading color

Headings use an inlined `--background(18)` accent — the seed color at
surface level 18. This gives headings a chromatic tint that tracks the
seed without being a separate design token.


---


## Registered properties

All `@property` declarations, with rationale:

    --color           <color>    inherits    seed for everything
    --_dark           <number>   inherits    enables transition/animation
    --_motion         <integer>  inherits    motion preference flag
    --_bg             <color>    inherits    computed bg, flows to children
    --bg              <number>   no inherit  per-element surface level
    --type            <number>   no inherit  per-element type step
    --border          <number>   no inherit  per-element border level
    --interactive     <number>   no inherit  per-element hover shift
    --shadow          <number>   no inherit  per-element elevation
    --contrast        <number>   no inherit  per-element text contrast
    --cfg-type-scale  <number>   inherits    global type multiplier
    --cfg-space-scale <number>   inherits    global space multiplier

Registering `--_dark` as `<number>` (not `<integer>`) is what makes the
continuous spectrum work. CSS can interpolate `--_dark` from 0 to 1 in
a transition — every surface, border, and contrast value animates along
with it.


---


## Quick recipes

**Card:**
```html
<div style="--bg: 2; --border: 1; --shadow: 2; --interactive: 2">
```

**Primary button:**
```html
<button style="--bg: 16; --interactive: 2; --shadow: 3">
```

**Secondary button:**
```html
<button style="--bg: 2; --interactive: 2; --border: 1">
```

**Muted annotation:**
```html
<p class="muted" style="--type: -0.5">
```

**Hue override for a section:**
```html
<section style="--color: oklch(0.5 0.2 265)">
  <!-- everything inside shifts to blue -->
</section>
```

**Dark mode toggle (JS):**
```js
document.documentElement.style.setProperty('--_dark', 1);
// or animate it:
document.documentElement.animate(
  { '--_dark': [0, 1] },
  { duration: 300, fill: 'forwards' }
);
```

**Compact density:**
```html
<html data-ui-density="compact">
```

