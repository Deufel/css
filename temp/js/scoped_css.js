// 🌘 CSS Scope Inline 1.1.0 (https://github.com/gnat/css-scope-inline)
window.cssScopeCount ??= 1 // Let extra copies share the scope count.
window.cssScope ??= new MutationObserver(mutations => { // Allow 1 observer.
	document?.body?.querySelectorAll('style:not([ready])').forEach(node => { // Faster than walking MutationObserver results when recieving subtree (DOM swap, htmx, ajax, jquery).
		var scope = 'me__'+(window.cssScopeCount++) // Ready. Make unique scope, example: .me__1234
		node.parentNode.classList.add(scope)
		node.textContent = node.textContent
		.replace(/(?:^|\.|(\s|[^a-zA-Z0-9\-\_]))(me|this|self)(?![a-zA-Z\/])/g, '$1.'+scope) // Can use: me this self
		.replace(/((@keyframes|animation:|animation-name:)[^{};]*)\.me__/g, '$1me__') // Optional. Removes need to escape names, ex: "\.me"
		node.setAttribute('ready', '')
	})
}).observe(document.documentElement, {childList: true, subtree: true})
