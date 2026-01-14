# CUBE CSS Design System (WIP)

A minimal CSS design system using CSS layers, custom attributes, and CUBE methodology.

## Layer Order

```html
<style>@layer reset, props, theme, composition, utility, block, exception;</style>
```

## File Structure

```
├── 0_reset.css         # Normalize/reset
├── 1_props.css         # Raw design tokens (Open Props style)
├── 2_theme-*.css       # Semantic tokens with t-shirt sizes
├── 3_composition.css   # Layout primitives
├── 4_utility.css       # Single-purpose classes
├── 5_block.css         # Components (btn, card, badge, etc.)
└── 6_exception.css     # Block modifications
```

---

## Composition Layer

Layout primitives use `type:variant` syntax.

### Flex Layouts

| Class | Behavior |
|-------|----------|
| `flex:cluster` | Horizontal flex, wraps |
| `flex:stack` | Vertical flex |
| `flex:split-row` | Horizontal, children grow equally (`flex: 1`) |
| `flex:split-column` | Vertical, children grow equally |
| `flex:spread-row` | Horizontal, `justify-content: space-between` |
| `flex:spread-column` | Vertical, `justify-content: space-between` |
| `flex:flank-start` | Push children to start |
| `flex:flank-end` | Push children to end |

```html
<div class="flex:cluster gap:md">...</div>
<div class="flex:stack align:center gap:lg">...</div>
<div class="flex:split-row gap:sm">...</div>
<div class="flex:spread-row align:center">...</div>
```

### Grid Layouts

| Class | Behavior |
|-------|----------|
| `grid:lcr` | 3-column: left / center / right (`auto 1fr auto`) |
| `grid:tmb` | 3-row: top / middle / bottom (`auto 1fr auto` rows) |
| `grid:pancake` | Header / main / footer stack (`auto 1fr auto` rows) |
| `grid:hero-nested` | 3×3 grid (`auto 1fr auto / auto 1fr auto`) |
| `grid:hero-full` | 3×3 grid + `min-height: 100svh`, viewport fitting |
| `grid:auto-fit` | Responsive columns, uses `--grid-min` |
| `grid:auto-fill` | Like auto-fit but keeps empty tracks |

```html
<div class="grid:lcr gap:md">
  <div>Left</div>
  <div>Center</div>
  <div>Right</div>
</div>

<div class="grid:auto-fit gap:sm" style="--grid-min: 200px;">
  <div>Item</div>
  <div>Item</div>
</div>

<body class="grid:hero-full">
  <header>...</header>
  <nav>...</nav>
  <main>...</main>
  <aside>...</aside>
  <footer>...</footer>
</body>
```

### Frame (Aspect Ratio)

| Class | Aspect Ratio |
|-------|--------------|
| `frame` / `frame:square` | 1 / 1 |
| `frame:landscape` | 16 / 9 |
| `frame:portrait` | 9 / 16 |

```html
<div class="frame:landscape">
  <img src="..." alt="...">
</div>
```

---

## Utility Layer

Single-purpose modifiers that compose with layouts.

### Alignment

| Class | Property |
|-------|----------|
| `align:start` | `align-items: flex-start` |
| `align:end` | `align-items: flex-end` |
| `align:center` | `align-items: center` |
| `align:stretch` | `align-items: stretch` |
| `align:baseline` | `align-items: baseline` |

| Class | Property |
|-------|----------|
| `justify:start` | `justify-content: flex-start` |
| `justify:end` | `justify-content: flex-end` |
| `justify:center` | `justify-content: center` |
| `justify:between` | `justify-content: space-between` |
| `justify:around` | `justify-content: space-around` |
| `justify:evenly` | `justify-content: space-evenly` |

### Gap

| Class | Value |
|-------|-------|
| `gap:xs` | `var(--space-xs)` |
| `gap:sm` | `var(--space-sm)` |
| `gap:md` | `var(--space-md)` |
| `gap:lg` | `var(--space-lg)` |
| `gap:xl` | `var(--space-xl)` |

### Wrap

| Class | Property |
|-------|----------|
| `wrap` | `flex-wrap: wrap` |
| `nowrap` | `flex-wrap: nowrap` |

### Spacing

| Class | Property |
|-------|----------|
| `p:xs` ... `p:xl` | `padding: var(--space-*)` |
| `m:xs` ... `m:xl` | `margin: var(--space-*)` |

### Text Size

| Class | Property |
|-------|----------|
| `text:xs` ... `text:xl` | `font-size: var(--text-*)` |

---

## Block Layer

Components use class + attribute API.

### Attribute API

| Attribute | Purpose | Values |
|-----------|---------|--------|
| `var` | Variant | `pri`, `sec`, `out`, `gho` |
| `sz` | Size | `xs`, `sm`, `md`, `lg`, `xl` |
| `st` | State | `def`, `lod`, `dis`, `err`, `suc`, `wrn`, `inf` |

### Button

```html
<button class="btn" var="pri" sz="md">Primary</button>
<button class="btn" var="sec" sz="lg">Secondary</button>
<button class="btn" var="out" sz="sm">Outline</button>
<button class="btn" var="gho" sz="md">Ghost</button>
<button class="btn" var="pri" st="lod">Loading...</button>
<button class="btn" var="pri" st="dis" disabled>Disabled</button>
```

### Badge

```html
<span class="badge" var="pri">Primary</span>
<span class="badge" var="suc">Success</span>
<span class="badge" var="err">Error</span>
<span class="badge" var="wrn">Warning</span>
```

### Card

```html
<div class="card" var="pri">
  <h3>Title</h3>
  <p>Content</p>
</div>
```

### Icon Button

```html
<button class="icon-btn" sz="md" var="gho">
  <svg>...</svg>
</button>
```

---

## Exception Layer

Modifications to blocks for edge cases.

---

## Theme Switching

Themes are swappable CSS files. Only load one at a time.

```html
<link rel="stylesheet" href="../css/2_theme-default.css">
```

With Datastar persistence:

```html
<link rel="stylesheet" data-attr:href="$prst_theme">
```

---

## Rules

- Do **not** use `!important` — this breaks layer cascade
- Keep `data-*` attributes for Datastar only
- Keep `var`, `sz`, `st` attributes for styling

