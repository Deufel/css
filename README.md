# Design System

This is a work in progress just kind of a testing ground at the moment.
CSS layers meet Datastar reactivity.

## What It Does

This system styles your web pages. It uses CSS layers and Datastar for reactive components. No build step. No framework bloat.

## Files

```
css/
  reset.css          # Fixes browser quirks
  theme.css          # Colors and tokens
  composition.css    # Layout tools
  utility.css        # Helper classes  
  block.css          # Component base
  exception.css      # Variants and sizes
  
```

## Install

Add these in order:

```html
<link rel="stylesheet" href="css/reset.css">
<link rel="stylesheet" href="css/theme.css">
<link rel="stylesheet" href="css/composition.css">
<link rel="stylesheet" href="css/utility.css">
<link rel="stylesheet" href="css/block.css">
<link rel="stylesheet" href="css/exception.css">
```

Add Datastar:

```html
<script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.7/bundles/datastar.js"></script>
```

## Three-Letter Attributes

Style components with short attributes:

```html
<button class="btn" var="pri" sz="lg">Click</button>
```

**var** = variant (pri, sec, out, gho)  
**sz** = size (xs, sm, md, lg, xl)  
**st** = state (def, lod, dis, err, suc, wrn, inf)

These are CSS hooks. Not Datastar attributes.

## Make It Reactive

Use Datastar to control attributes:

```html
<button class="btn"
        var="pri"
        sz="md"
        data-signals="{v: 'pri', s: 'md'}"
        data-attr:var="$v"
        data-attr:sz="$s"
        data-on:click="$v = 'sec'">
  Toggle
</button>
```

The `$v` signal controls the `var` attribute. Click changes it. CSS reacts.

## Components

**Buttons:**
```html
<button class="btn" var="pri" sz="md">Primary</button>
<button class="btn" var="sec" sz="lg">Secondary</button>
<button class="btn" var="out" sz="sm">Outline</button>
```

**Badges:**
```html
<span class="badge" var="pri">Primary</span>
<span class="badge" var="suc">Success</span>
<span class="badge" var="err">Error</span>
```

**Cards:**
```html
<div class="card">
  <h3>Title</h3>
  <p>Content here.</p>
</div>
```

**Inputs:**
```html
<input class="input" st="def" type="text">
<input class="input" st="err" type="text">
<input class="input" st="suc" type="text">
```

## Layout

Stack things:
```html
<div class="--flex:stack">
  <div>One</div>
  <div>Two</div>
</div>
```

Wrap things:
```html
<div class="--flex:cluster">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
</div>
```

Grid things:
```html
<div class="--grid:auto-fit" style="--min-col: 250px;">
  <div>Item</div>
  <div>Item</div>
</div>
```

## Rules

- Static markup gets static attributes
- Dynamic markup gets Datastar signals
- Signals control attributes
- Attributes control styles
- Keep `data-*` for Datastar only
- Keep regular attributes for styling

## License

MIT. Use it.
