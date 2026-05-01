# colorNtype — Quick Start

A color system in two axes and three hue tokens. No tokens to memorize, no light/dark variants to maintain.

## The whole API

```css
.surface          /* structural container — flips with theme */
--bg: 0…1         /* chromatic background — theme-stable */
--fg: -1…1        /* ink — negative is contrast, positive is chromatic */
--hue: 0…360      /* page-level hue, cascades freely */
--hue-shift: N    /* relative offset on inherited --hue */
--hue-lock: 0…360 /* absolute pin, overrides --hue and --hue-shift */
--border          /* quiet border on the current surface */
--Border          /* loud border on the current surface */
```

That's it. Six tokens, one class, two borders.

## Surfaces hold content

`.surface` is the structural container. Cards, panels, modals, sections — anything that holds content goes on a surface. Surfaces auto-nest via `:has()` so deeper containers get progressively brighter, drawing focus to the most-nested content. They flip with theme automatically.

```html
<main class="surface">
  <article class="surface">
    <h2>Title</h2>
    <p>Body text — picks up theme-correct ink for free.</p>
  </article>
</main>
```

Most of your UI is surfaces. If something holds content, give it `.surface`.

## Chromatic `--bg` for semantic color

When you want a *colored* element — a status badge, a brand button, a callout — set `--bg: 0…1` directly. Don't add `.surface`. Chromatic elements are theme-stable: a green badge stays green in both light and dark mode.

```html
<span style="--bg: 0.55; --hue-lock: 145">LIVE</span>
<button style="--bg: 0.5">Continue</button>
```

**Pick one role per element.** A thing is either a surface (structural, theme-tracking) or a chromatic accent (semantic color, theme-stable). Never both. If you want a "colored card with content," make a `.surface` containing a chromatic child.

## `--fg` for ink

One axis covers all ink intent. Negative values produce *contrast* against the surface — readable in both themes automatically. Positive values produce *chromatic* ink — same color in both themes, useful for chart lines, deliberate accents, branded text.

```css
--fg: -1     /* max contrast — body text, default */
--fg: -0.6   /* secondary text, subdued */
--fg: -0.3   /* hints, captions */
--fg: 0      /* invisible (= surface color) */
--fg: 0.55   /* mid-chromatic — chart line, callout */
--fg: 0.85   /* deep chromatic — accent icon, badge text */
```

## Hue: three tokens, three roles

```css
--hue: 220        /* set on :root or any subtree → cascades down */
--hue-shift: 30   /* nudge: parent hue + 30°, stacks with parents */
--hue-lock: 145   /* pin: this subtree is hue 145, ignore cascade */
```

Use `--hue` to brand the whole page or a subtree. Use `--hue-shift` to make a section subtly different from its parent. Use `--hue-lock` for semantic colors (success, warning, danger) that must be specific hues regardless of context.

## Borders

`--border` and `--Border` are pre-resolved against the current surface — capital is louder, lowercase is quieter.

```css
border: 1px solid var(--border);  /* subtle */
border: 1px solid var(--Border);  /* prominent */
```

## A complete card component

```html
<article class="surface" style="border: 1px solid var(--border)">
  <h3>Quarterly results</h3>
  <p style="--fg: -0.7">Revenue beat expectations on solid customer growth.</p>
  <div style="display: flex; gap: 0.5rem">
    <button style="--bg: 0.55">Continue</button>
    <button class="surface" style="border: 1px solid var(--border)">Cancel</button>
    <span style="--bg: 0.55; --hue-lock: 145">LIVE</span>
  </div>
</article>
```

The card flips with theme. The "Continue" button stays its brand color. The "Cancel" button is a structural surface that flips. The "LIVE" badge stays green forever. The body text reads correctly against any background.

No tokens. No theme variants. No coordination.
