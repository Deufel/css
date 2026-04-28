# CSS System
# Layers

The toolbox CSS uses cascade layers to make every rule's role explicit. The order is fixed; the meaning of each layer is fixed; deciding where a new rule goes should be a 10-second decision.

```css
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

# Color Layer in Detail

A formula-driven CSS color system. You set numeric inputs; the system computes every visible color so contrast, theme, and surface depth always work.

## Public API

Set these on any element via inline `style` or class. All tokens cascade unless noted.

| Token             | Range     | Default  | Effect                                                       |
| ----------------- | --------- | -------- | ------------------------------------------------------------ |
| `--bg`            | `-1`…`1`  | `-1`     | Background. `-1` = surface mode (no chromatic paint). `0`…`1` = muted to vivid chromatic, theme-independent. |
| `--hue`           | `0`…`360` | inherits | Absolute hue override for a subtree (a section, card, or component that should reflow to a new hue). |
| `--hue-shift`     | number    | `0`      | Additive offset from the inherited hue. Use for sibling rotation (categorical charts, accents). |
| `--fg-contrast`   | `0`…`1`   | `1`      | Text ink strength. `1` = full contrast (black/white auto-flip). `0` = matches background (invisible). |
| `--fg-chroma`     | `0`…`0.4` | `0`      | Tint retained in text. Use `0.08`–`0.15` for tinted captions/links. |
| `--fg-hue`        | `0`…`360` | inherits | Hue override for text only.                                  |
| `--l-shift`       | number    | `0`      | State-only lightness offset (used by `.hover`/`.active`).    |
| `--c-shift`       | number    | `0`      | State-only chroma offset.                                    |
| `--cfg-color-hue` | `0`…`360` | `220`    | **Global** hue. Set once at `:root`. For subtree changes, use `--hue` instead. |

Classes:

| Class                       | Effect                                                       |
| --------------------------- | ------------------------------------------------------------ |
| `.surface`                  | Paints a real background; auto-nests up to depth 4 (deeper surfaces are lighter/more prominent). |
| `.suc` `.inf` `.wrn` `.dgr` | Set `--hue` to `145` / `240` / `75` / `25`.                  |
| `.hover` `.active`          | State classes toggled via the pointer-events script (below). Each composes `--l-shift`, `--c-shift`, `--fg-contrast`. **Use these, not `:hover`/`:active`** — pseudos break on iOS. |

Attributes:

| Attribute       | Values                  | Effect                                                       |
| --------------- | ----------------------- | ------------------------------------------------------------ |
| `data-ui-theme` | `light` `dark` `system` | Forces theme on element + subtree. Default follows `prefers-color-scheme`. |

Computed outputs (read-only — never assign):

- `var(--_bg)` — resolved background color
- `var(--border)` — quiet themed border
- `var(--Border)` — louder themed border (note capital B)

## The `--bg` ramp — practical guidance

Most of your work uses `.surface` and inherits everything. Reach for `--bg` only when you want chromatic paint.

| Range          | Use for                                                      | Notes                                                        |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `-1` (default) | Plain text on inherited surface; transparent decorations.    | You never type this.                                         |
| `0.01`–`0.05`  | Subtle buttons, badges, hovered list rows.                   | A button at `--bg: 0.02` is almost always nicer than `--bg: 0.5`. |
| `0.1`–`0.3`    | Standard buttons, pills, tags, callouts.                     | Clear chromatic identity without shouting.                   |
| `0.3`–`0.4`    | Strong buttons, primary CTAs, semantic toasts.               | Already sufficient for almost any component.                 |
| `0.4`–`1.0`    | Dense data viz only — heatmaps, choropleth maps, intensity grids. | "Inky." Inappropriate for UI controls; the eye reads it as a value, not a state. |

Rule of thumb: if you're styling a control and reach above `0.4`, you probably want a different design, not a louder color.

## Patterns

**Surfaces are containers; text is content.** Put `.surface` (or `--bg`) on a wrapper, text inside as children. Don't put `.surface` or `--bg` directly on a `<p>` or `<h2>`.

```html
<div class="surface">
  <h2>Title</h2>
  <p>Body text inherits the surface's resolved background.</p>
</div>
```

**Surfaces auto-nest.** Don't manage depth.

```html
<div class="surface">                  <!-- depth 0 -->
  <div class="surface">                <!-- depth 1, lighter -->
    <div class="surface">              <!-- depth 2, lighter still -->
      <p>Most prominent layer.</p>
    </div>
  </div>
</div>
```

**Hue cascades.** Set `--hue` (or `--hue-shift`) on any parent to recolor the subtree.

```html
<aside style="--hue: 280">
  <button class="surface" style="--bg: 0.2">Purple by inheritance</button>
</aside>
```

**Categorical color via sibling `--hue-shift`.**

```html
<g style="--bg: 0.5">
  <rect style="--hue-shift: 0"   .../>
  <rect style="--hue-shift: 60"  .../>
  <rect style="--hue-shift: 120" .../>
</g>
```

## SVG

The same primitives work in SVG. The bridge:

| Slot                   | HTML               | SVG                            |
| ---------------------- | ------------------ | ------------------------------ |
| `--bg` paints          | `background-color` | shape `fill`                   |
| `--fg-contrast` paints | `color` (text)     | text `fill` via `currentColor` |
| `--bg: -1` renders as  | transparent        | **opaque, in surface color**   |

**Pattern: group + shape + text.** Put `--bg` on a `<g>`, both children inherit it. The shape paints itself with `--_bg`; the text computes contrast against the same `--_bg`.

```html
<svg viewBox="0 0 200 60">
  <g style="--bg: 0.5; --hue: 145">
    <rect width="200" height="60" rx="8"/>
    <text x="100" y="38" text-anchor="middle">+12%</text>
  </g>
</svg>
```

**Pitfalls:**

1. **Text outside the colored group computes contrast against the page**, not the shape behind it. Always wrap shape and text in the same `<g>` with `--bg`.
2. **`--bg: -1` in SVG is opaque** (paints the inherited surface color). For genuinely transparent SVG fills, use `fill="none"` directly.

**Escape hatch:** inline `style` overrides the system's CSS for `fill`/`stroke`. Use when you need a specific color the system doesn't anticipate (e.g., gridlines that should always be a quiet edge):

```html
<line x1="0" y1="50" x2="100" y2="50" style="stroke: var(--border)"/>
```

## Theme and state

Theme is a single attribute. Colors recompute; no markup changes.

```html
<html data-ui-theme="dark">     <!-- forced -->
<section data-ui-theme="light"> <!-- subtree override -->
```

`--bg` is theme-independent by design — a heatmap cell at `--bg: 0.7` reads as the same vivid chroma in both themes. Surfaces and borders adapt to theme; chromatic paint does not.

State on interactive elements uses `.hover` / `.active` classes toggled by the pointer-events helper, not CSS pseudos. Pseudos don't generalize across mouse, touch, and stylus (especially on iOS, where `:hover` sticks after a tap). Include the helper script once per page:

```html
<script src="https://cdn.jsdelivr.net/gh/Deufel/toolbox@latest/js/pointer_events.js"></script>
```

Then style the classes. The system ships defaults; override per component if needed:

```css
.btn.hover  { --l-shift: 0.04;  --c-shift: 0.02 }
.btn.active { --l-shift: -0.04; --c-shift: -0.06 }
```

## Don't

- Don't assign `--depth`, `--_bg`, or any `--_*` token. They're private.
- Don't set `--cfg-*` config tokens outside `:root` or theme blocks. Set once.
- Don't use `:hover` / `:active` pseudos. Use `.hover` / `.active` classes (see Theme and state).
- Don't pair colors manually for light/dark. The system has one set of color math; theme is a single config flip.
- Don't transition the resolved color. Transition the numeric inputs (`--bg`, `--hue`, `--fg-contrast`); the formula re-resolves each frame.


