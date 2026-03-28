// Global approach easier

document.addEventListener('pointerdown', (e) => {
  const el = e.target.closest('button:not([disabled])');
  if (!el) return;
  if (!el.classList.contains('ripple')) el.classList.add('ripple');

  const r = el.getBoundingClientRect();
  const x = ((e.clientX - r.left) / r.width  * 100).toFixed(1);
  const y = ((e.clientY - r.top)  / r.height * 100).toFixed(1);

  const span = document.createElement('span');
  span.style.setProperty('--_rp-x', `${x}%`);
  span.style.setProperty('--_rp-y', `${y}%`);
  span.className = 'ripple-burst';
  el.appendChild(span);
  span.addEventListener('animationend', () => span.remove(), { once: true });
});


// Opt in approach  <button data-on:mousedown="ripple(evt)">
//
// window.ripple = (e) => {
//   const el = e.currentTarget;
//   const r = el.getBoundingClientRect();
//   const x = ((e.clientX - r.left) / r.width  * 100).toFixed(1);
//   const y = ((e.clientY - r.top)  / r.height * 100).toFixed(1);

//   const span = document.createElement('span');
//   span.style.setProperty('--_rp-x', `${x}%`);
//   span.style.setProperty('--_rp-y', `${y}%`);
//   span.className = 'ripple-burst';
//   el.appendChild(span);
//   span.addEventListener('animationend', () => span.remove(), { once: true });
// }
