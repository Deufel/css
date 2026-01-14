# CUBE CSS Design System

A scalable, progressive enhancement CSS system following the CUBE methodology.

## Philosophy

This system embraces CSS's cascade and progressive nature. It's designed to hint the browser with flexible rules rather than micro-manage with strict ones. Most styling is done at a high level, with each layer adding specificity only when needed.

## File Structure

```bash
.
├── 0_reset.css            # Browser reset/normalize
├── 1_props.css            # Design tokens (numbers, raw values)
├── 2_theme-default.css    # Theme layer (maps props to t-shirt sizes)
├── 3_composition.css      # Skeletal layout primitives
├── 4_utility.css          # Single-purpose classes
├── 5_block.css            # Component styles
├── 6_exception.css        # State variations
└── 7_transitions.css      # View transitions (optional)
```

## Installation

Add layer declaration first to establish hierarchy:

```html
<style>
  @layer reset, props, theme, composition, utility, block, exception;
</style>
<link rel="stylesheet" href="css/0_reset.css">
<link rel="stylesheet" href="css/1_props.css">
<link rel="stylesheet" data-attr:href="$prst_theme">
<link rel="stylesheet" href="css/3_composition.css">
<link rel="stylesheet" href="css/4_utility.css">
<link rel="stylesheet" href="css/5_block.css">
<link rel="stylesheet" href="css/6_exception.css">
<!-- Optional: -->
<link rel="stylesheet" href="css/7_transitions.css">
```

**Note:** Theme is loaded via Datastar signal for persistence. Use your backend to track user preferences in production.

## CUBE Methodology

### Composition (Skeletal Layouts)

Composition provides flexible, content-agnostic layout systems. These are skeletal structures that work with any content.

#### Flow
Consistent vertical rhythm between siblings:
```html
<article class="flow">
  <h2>Heading</h2>
  <p>Paragraph one</p>
  <p>Paragraph two</p>
</article>
```

Customize spacing:
```html
<article class="flow" style="--flow-space: var(--space-sm)">
  <!-- Tighter spacing -->
</article>
```

#### Stack
Vertical flex layout:
```html
<div class="stack">
  <header>Header</header>
  <main>Content</main>
  <footer>Footer</footer>
</div>
```

Custom gap:
```html
<div class="stack" style="--stack-space: var(--space-lg)">
  <!-- Larger gaps -->
</div>
```

#### Cluster
Horizontal wrapping layout:
```html
<nav class="cluster">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
</nav>
```

#### Sidebar
Content with fixed-width sidebar:
```html
<div class="sidebar">
  <aside>Sidebar content</aside>
  <main>Main content</main>
</div>
```

Sidebar on right:
```html
<div class="sidebar" data-direction="end">
  <main>Main content</main>
  <aside>Sidebar content</aside>
</div>
```

Custom width:
```html
<div class="sidebar" style="--sidebar-width: 300px; --sidebar-content-min: 60%">
  <!-- Wider sidebar, main content needs more space to stay inline -->
</div>
```

#### Switcher
Switches from horizontal to stacked below threshold:
```html
<div class="switcher">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

Custom threshold:
```html
<div class="switcher" style="--switcher-threshold: 40rem">
  <!-- Stays horizontal longer -->
</div>
```

#### Grid Layouts

**Auto-fit:** Fills available space
```html
<div class="grid" data-layout="auto-fit" style="--grid-min: 250px">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>
```

**Auto-fill:** Creates empty tracks
```html
<div class="grid" data-layout="auto-fill" style="--grid-min: 200px">
  <!-- Empty tracks created even with fewer items -->
</div>
```

**LCR (Left-Center-Right):** Hero grid layout
```html
<header class="grid" data-layout="lcr">
  <div>Logo</div>
  <nav>Navigation</nav>
  <div>Actions</div>
</header>
```

**TMB (Top-Middle-Bottom):** Vertical centering
```html
<section class="grid" data-layout="tmb">
  <div>Header</div>
  <div>Centered content</div>
  <div>Footer</div>
</section>
```

**Overlap:** Stacked layers
```html
<div class="grid" data-layout="overlap">
  <img src="bg.jpg" alt="">
  <div class="content">Overlaid content</div>
</div>
```

**Fullpage:** Holy grail layout
```html
<div class="grid" data-layout="fullpage">
  <!-- Creates 3x3 grid for app-like layouts -->
  <header>Header</header>
  <nav>Sidebar</nav>
  <main>Main</main>
  <aside>Aside</aside>
  <footer>Footer</footer>
</div>
```

#### Wrapper
Centered max-width container:
```html
<div class="wrapper">
  <h1>Centered content</h1>
  <p>Max width with padding</p>
</div>
```

Custom width:
```html
<div class="wrapper" style="--wrapper-max: 90rem">
  <!-- Wider container -->
</div>
```

#### Region
Full-width section with internal wrapper:
```html
<section class="region">
  <div class="wrapper">
    <h2>Section title</h2>
    <p>Content</p>
  </div>
</section>
```

#### Cover
Vertically center content in viewport:
```html
<div class="cover">
  <header>Header</header>
  <div class="cover__centered">
    <h1>Centered content</h1>
  </div>
  <footer>Footer</footer>
</div>
```

### Utility (Single Purpose)

Utilities do one job well. Use them to fine-tune layouts without writing custom CSS.

#### Common Utilities

```html
<!-- Flexbox alignment -->
<div class="flex justify-between items-center">
  <span>Left</span>
  <span>Right</span>
</div>

<!-- Grid alignment -->
<div class="grid place-center">
  <div>Perfectly centered</div>
</div>

<!-- Spacing -->
<div class="stack gap-lg">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Sizing -->
<img class="w-full h-auto" src="image.jpg" alt="">

<!-- Shadows -->
<div class="shadow-3 rounded">Card with shadow</div>

<!-- Text -->
<p class="text-center text-balance">Balanced centered text</p>

<!-- Display -->
<nav class="flex flex-wrap gap-md">
  <a href="/">Link</a>
</nav>
```

### Block (Components)

Blocks are your components. By this point, most styling is done by global CSS, composition, and utilities, so blocks are minimal.

```html
<!-- Button component -->
<button class="btn" var="pri" sz="md">
  Click me
</button>

<!-- Card component -->
<article class="card">
  <img class="card__image" src="thumb.jpg" alt="">
  <div class="card__content flow">
    <h3>Title</h3>
    <p>Description text here</p>
  </div>
</article>

<!-- Badge component -->
<span class="badge" var="suc">Success</span>

<!-- Input component -->
<input class="input" st="def" type="text" placeholder="Enter text">
```

#### Component API

Most blocks use these HTML attributes for variants:

- **var** = variant (pri, sec, out, gho)
- **sz** = size (xs, sm, md, lg, xl)
- **st** = state (def, lod, dis, err, suc, wrn, inf)

These are CSS attribute selectors, not Datastar attributes.

### Exception (State Changes)

Exceptions handle state variations using data attributes. This keeps state changes clear and works with both CSS and JavaScript.

```html
<!-- Reversed card -->
<article class="card" data-state="reversed">
  <!-- Content order flipped via flexbox -->
</article>

<!-- Loading button -->
<button class="btn" var="pri" data-state="loading">
  Processing...
</button>

<!-- Disabled input -->
<input class="input" data-state="disabled" disabled>

<!-- Active navigation item -->
<a class="nav-link" data-state="active" href="/current">
  Current Page
</a>
```

## Spacing System

The theme layer maps numeric tokens to t-shirt sizes:

```css
--space-xs: 0.25rem   /* 4px */
--space-sm: 0.5rem    /* 8px */
--space-md: 1rem      /* 16px */
--space-lg: 1.5rem    /* 24px */
--space-xl: 2rem      /* 32px */
--space-2xl: 3rem     /* 48px */
--space-3xl: 4rem     /* 64px */
```

Swap themes to change spacing throughout your app without touching component code.

## Custom Properties

Compositions and utilities use CSS custom properties for customization:

```css
/* Composition */
--flow-space: var(--space-md)
--stack-space: var(--space-md)
--cluster-space: var(--space-md)
--grid-space: var(--space-md)
--grid-min: 20ch
--sidebar-width: 250px
--sidebar-content-min: 50%
--switcher-threshold: 30rem
--wrapper-max: 75rem
--wrapper-padding: var(--space-md)
--region-space: var(--space-lg)
--cover-height: 100svh
--cover-space: var(--space-md)
```

## Rules

1. **Let the cascade work** - Style at the highest level possible
2. **Composition is skeletal** - No colors, no decorative styles
3. **Utilities are single-purpose** - One job, done well
4. **Blocks are minimal** - Most work is already done
5. **Exceptions use data attributes** - Clear state management
6. **Never use !important** - If you need it, your layer is wrong
7. **Keep data-\* for Datastar** - Don't mix styling attributes with framework attributes

## Theme Switching

```javascript
// Datastar signal (client-side)
<script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.7/bundles/datastar.js"></script>

<div data-signals="{ prst_theme: '/css/2_theme-default.css' }">
  <link rel="stylesheet" data-attr:href="$prst_theme">
</div>
```

For production, track theme preference on backend and serve appropriate theme file.

## Container Queries

The `body` element has `container-type: inline-size` set up. Use container queries for responsive components:

```css
@container (min-width: 40rem) {
  .my-component {
    /* Styles for wider containers */
  }
}
```

## Browser Support

- Modern browsers (last 2 versions)
- `light-dark()` requires recent browser (fallback to light theme)
- View transitions are progressive enhancement
- Container queries require modern browser

## License

MIT

## Resources

- [CUBE CSS](https://cube.fyi)
- [Every Layout](https://every-layout.dev)
- [Open Props](https://open-props.style)
