function handlePopoverAttributes() {
  const mobilePopoverElements = document.querySelectorAll('[data-layout="mobile-popover"]');

  if (window.innerWidth > 768) {
    mobilePopoverElements.forEach(element => {
      element.removeAttribute('popover');
      element.style.position = 'static';
      element.style.transform = 'none';
      element.style.opacity = '1';
      element.style.width = 'auto';
    });
  } else {
    mobilePopoverElements.forEach(element => {
      element.setAttribute('popover', 'auto');
      element.removeAttribute('style');
    });
  }
}

// Ensure it runs after the DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  handlePopoverAttributes();
  window.addEventListener('resize', handlePopoverAttributes);
});
