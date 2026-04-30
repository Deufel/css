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

