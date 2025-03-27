// Handles the honeycomb parallax scrolling effect

// Throttle function to limit how often the scroll handler fires
function throttle(callback, delay = 15) {
  let isThrottled = false;
  
  return function() {
    if (isThrottled) return;
    
    isThrottled = true;
    const context = this;
    const args = arguments;
    
    callback.apply(context, args);
    
    setTimeout(() => {
      isThrottled = false;
    }, delay);
  };
}

// Parallax effect function
function updateParallax() {
  try {
    const scrolled = window.pageYOffset;
    const honeycomb = document.querySelector('.parallax');
    
    if (honeycomb) {
      honeycomb.style.transform = `translate3d(0, ${-scrolled * 0.4}px, 0)`;
    }
  } catch (error) {
    console.error('Error in parallax effect:', error);
  }
}

// Apply throttling to the scroll event handler
const throttledParallax = throttle(updateParallax);

// Initialize parallax effect
function initParallax() {
  // Run once on page load
  updateParallax();
  
  // Add scroll event listener with throttled function
  window.addEventListener('scroll', throttledParallax, { passive: true });
  
  // Handle resize events
  window.addEventListener('resize', throttledParallax, { passive: true });
}

// Run initialization when DOM is fully loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initParallax);
} else {
  initParallax();
}