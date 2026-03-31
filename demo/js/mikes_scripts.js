    /**
     * highlight.js
     * Multi-language syntax highlighting via the CSS Custom Highlight API.
     * No dependencies, no DOM mutation.
     *
     * Supported languages: css, html
     * Declare on the <pre> element: <pre class="css"> or <pre class="html">
     * Defaults to CSS if neither class is present.
     *
     * Usage:
     *   <script type="module" src="highlight.js"></script>
     *
     * Re-highlight after dynamic DOM changes:
     *   import { highlightAll } from './highlight.js';
     *   highlightAll();
     */

    const CSS_TOKENS = [
      ['css-punctuation', /[{}();]/g],
      ['css-number',      /\b\d*\.?\d+\b/g],
      ['css-value',       /(?<=:)[^;{}]+/g],
      ['css-string',      /"[^"]*"|'[^']*'/g],
      ['css-unit',        /\b\d*\.?\d+(?:px|rem|em|%|vw|vh|svh|svw|dvh|dvw|ch|ex|fr|deg|rad|turn|ms|s)\b/g],
      ['css-property',    /(?:^|(?<=[{;])\s*)[\w-]+(?=\s*:)/gm],
      ['css-var-name',    /--[\w-]+/g],
      ['css-selector',    /^[ \t]*([^{};@/][^{};]*?)(?=\s*\{)/gm],
      ['css-atrule',      /@[\w-]+/g],
      ['css-comment',     /\/\*[\s\S]*?\*\//g],
    ];

    const HTML_TOKENS = [
      ['html-bracket',   /<\/?|\/?>|>/g],
      ['html-value',     /(?<==)\s*"[^"]*"|(?<==)\s*'[^']*'/g],
      ['html-attribute', /\b[\w-]+(?=\s*=|\s*(?:\/?>))/g],
      ['html-tag',       /(?<=<\/?)\s*[\w-]+/g],
      ['html-entity',    /&[#\w]+;/g],
      ['html-doctype',   /<!DOCTYPE[^>]*>/gi],
      ['html-comment',   /<!--[\s\S]*?-->/g],
    ];

    const ALL_TOKENS = [...CSS_TOKENS, ...HTML_TOKENS];

    function getLang(el) {
      if (el.classList.contains('html') || el.dataset.highlight === 'html') return 'html';
      return 'css';
    }

    export function highlightAll(root = document) {
      if (!CSS?.highlights) return;
      for (const [name] of ALL_TOKENS) CSS.highlights.delete(name);

      const cssBlocks = [], htmlBlocks = [];
      root.querySelectorAll('pre, .pattern-block, .code-block, .install-block, [data-highlight]').forEach(el => {
        const code = el.querySelector('code') ?? el;
        const node = code.firstChild;
        if (node?.nodeType !== Node.TEXT_NODE) return;
        const block = { src: node.textContent, textNode: node };
        if (getLang(el) === 'html') htmlBlocks.push(block);
        else cssBlocks.push(block);
      });

      applyTokens(CSS_TOKENS, cssBlocks);
      applyTokens(HTML_TOKENS, htmlBlocks);
    }

    function applyTokens(tokens, blocks) {
      if (!blocks.length) return;
      for (const [name, pattern] of tokens) {
        const highlight = new Highlight();
        for (const { src, textNode } of blocks) {
          const re = new RegExp(pattern.source, pattern.flags);
          for (const match of src.matchAll(re)) {
            const range = new Range();
            range.setStart(textNode, match.index);
            range.setEnd(textNode, match.index + match[0].length);
            highlight.add(range);
          }
        }
        if (highlight.size > 0) CSS.highlights.set(name, highlight);
      }
    }

    window._hl = highlightAll;

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => highlightAll());
    else highlightAll();

    