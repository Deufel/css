# Design System

This is a work in progress just kind of a testing ground at the moment.
CSS layers meet Datastar reactivity.

## What It Does

This system styles your web pages. It uses CSS layers and Datastar for reactive components. No build step. No framework bloat.

## Files

```
css/
  reset.css          # Fixes browser quirks
  props.css          # CSS Custom Props
  theme.css          # Theme
  composition.css    # Layout 
  utility.css        # single purpopse 
  block.css          # Component base
  exception.css      # Variants and sizes
```

## To "install" just add to your page headers. in the correctly layer order

Add a layer declaration first: 
 - this establishes the layer hierarchy
 - Do not use important this has weird behaviour with layers You should not need important this is a sign your using CUBE incorrectly.
 - reset is very basic
 - props is basically Open Props
 - theme is where the Custom Props are applied to the design system;
  * Ideally the Custom Props are the same not matter what and all you would need to change the design system would be the theme layer More on this next* 

```html 
<style>@layer reset, props, theme, composition, utility, block, exception;</style>
<link rel="stylesheet" href="../css/reset.css">
<link rel="stylesheet" data-attr:href="$prst_theme">
<!-- and import the rest since of the css here -->
```

Notice the theme is loaded in via a `$prst_theme` this is a datastar signal that is used to keep the users theme in local storage; It is probably a bettter idea to use your backend and track the users theme in your database. We will use persist for the purpose of being able to test this easily locally. 
    ** NOTE: data-persist is a datastar_pro attribute ** 



```html
<script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.7/bundles/datastar.js"></script>
```

## API

Components all follow generally the same API;
```html
<button class="btn" var="pri" sz="lg" st="lod">Click</button>
```
these html attributes are out of spec I do understand this. Maybe later I will make this a rocket library to comply with html spec:


**var** = variant (pri, sec, out, gho)  
**sz** = size (xs, sm, md, lg, xl)  
**st** = state (def, lod, dis, err, suc, wrn, inf)

These are CSS hooks. Not Datastar attributes.

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
- Keep `data-*` for Datastar only
- Keep regular attributes for styling

## License

MIT. 
