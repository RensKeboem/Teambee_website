// UI Enhancements - Combined scroll animations, smooth scrolling, and parallax effects
document.addEventListener('DOMContentLoaded', function() {
    
    // === UTILITY FUNCTIONS ===
    
    // Throttle function to limit how often handlers fire
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
    
    // Check if element is in viewport
    function isInViewport(element, threshold = 0.95) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) * threshold &&
            rect.bottom >= 0
        );
    }
    
    // === SCROLL ANIMATIONS ===
    
    // Elements to animate
    const animatedElements = [
        '.animate-section-title',
        '.animate-section-subtitle',
        '.animate-card',
        '.animate-list-item',
        '.animate-stagger-container .animate-stagger-item'
    ];
    
    const selector = animatedElements.join(', ');
    const elements = document.querySelectorAll(selector);
    
    // Set initial styles (hidden)
    elements.forEach(function(element) {
        if (!element.classList.contains('animate-stagger-item')) {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        }
    });
    
    // Handle staggered containers
    const staggerContainers = document.querySelectorAll('.animate-stagger-container');
    
    staggerContainers.forEach(function(container) {
        const items = container.querySelectorAll('.animate-stagger-item');
        
        items.forEach(function(item, index) {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            item.dataset.staggerDelay = index * 0.05; // 50ms between items
        });
    });
    
    // Animate elements when they enter viewport
    function animateOnScroll() {
        elements.forEach(function(element) {
            if (isInViewport(element)) {
                if (element.classList.contains('animate-stagger-item')) {
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
    
    // === PARALLAX EFFECT ===
    
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
    
    // === SMOOTH SCROLLING ===
    
    const scrollButtons = document.querySelectorAll('[data-scroll-to]');
    let isButtonScroll = false;
    
    // Contact section highlighting animation
    const contactSection = document.getElementById('contact');
    const contactObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && isButtonScroll) {
                const contactInfo = entry.target.querySelector('.contact-info');
                if (contactInfo) {
                    const contactElements = contactInfo.querySelectorAll('*');
                    contactElements.forEach(element => {
                        element.classList.add('scale-contact');
                        setTimeout(() => {
                            element.classList.remove('scale-contact');
                        }, 2000);
                    });
                }
                setTimeout(() => {
                    isButtonScroll = false;
                }, 2000);
            }
        });
    }, {
        threshold: 0.8
    });
    
    // Start observing the contact section
    if (contactSection) {
        contactObserver.observe(contactSection);
    }
    
    // Add event listeners to scroll buttons
    scrollButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('data-scroll-to');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                isButtonScroll = targetId === 'contact';
                
                const headerHeight = document.querySelector('header')?.offsetHeight || 0;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // === COMBINED SCROLL HANDLER ===
    
    function handleScroll() {
        animateOnScroll();
        updateParallax();
    }
    
    // Apply throttling to the combined scroll handler
    const throttledScrollHandler = throttle(handleScroll);
    
    // === INITIALIZATION ===
    
    // Run once on page load
    animateOnScroll();
    updateParallax();
    
    // Initialize success notification if available
    if (typeof TeambeeUtils !== 'undefined' && TeambeeUtils.initSuccessNotification) {
        TeambeeUtils.initSuccessNotification();
    }
    
    // Add scroll event listener
    window.addEventListener('scroll', throttledScrollHandler, { passive: true });
    
    // Handle resize events
    window.addEventListener('resize', throttledScrollHandler, { passive: true });
    
}); 