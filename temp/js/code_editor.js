document.querySelectorAll('.code-editor').forEach(editor => {
  const textarea = editor.querySelector('textarea');
  const code     = editor.querySelector('code');

  textarea.addEventListener('input', () => {
    code.textContent = textarea.value;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  });

  // seed initial content
  const tmpl = editor.querySelector('template');
  if (tmpl) {
    textarea.value   = tmpl.innerHTML.trim();
    code.textContent = textarea.value;
    textarea.dispatchEvent(new Event('input'));
  }
});
