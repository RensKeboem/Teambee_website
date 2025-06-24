// Scroll Animation Script for Teambee
document.addEventListener('DOMContentLoaded', function() {
    
    // Elements to animate
    const animatedElements = [
        // Section titles and subtitles
        '.animate-section-title',
        '.animate-section-subtitle',
        
        // Cards and features
        '.animate-card',
        
        // Lists and other elements
        '.animate-list-item',
        
        // Use specific animation groups for staggered animations
        '.animate-stagger-container .animate-stagger-item'
    ];
    
    // Combined selector for all animated elements
    const selector = animatedElements.join(', ');
    
    // Get all elements to animate
    const elements = document.querySelectorAll(selector);
    
    // Set initial styles (hidden)
    elements.forEach(function(element) {
        // Don't apply to stagger items - they'll be handled by their container
        if (!element.classList.contains('animate-stagger-item')) {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        }
    });
    
    // Handle staggered containers separately
    const staggerContainers = document.querySelectorAll('.animate-stagger-container');
    
    staggerContainers.forEach(function(container) {
        const items = container.querySelectorAll('.animate-stagger-item');
        
        items.forEach(function(item, index) {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            // Add delay based on index for staggered effect
            item.dataset.staggerDelay = index * 0.05; // 50ms between items
        });
    });
    
    // Check if element is in viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.95 &&
            rect.bottom >= 0
        );
    }
    
    // Animate elements when they enter viewport
    function animateOnScroll() {
        elements.forEach(function(element) {
            if (isInViewport(element)) {
                if (element.classList.contains('animate-stagger-item')) {
                    // Apply staggered delay
                    const delay = element.dataset.staggerDelay || 0;
                    setTimeout(function() {
                        element.style.opacity = '1';
                        element.style.transform = 'translateY(0)';
                    }, delay * 1000);
                } else {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }
            }
        });
    }
    
    // Run on initial load
    animateOnScroll();
    
    // Add scroll listener
    window.addEventListener('scroll', animateOnScroll);
}); 