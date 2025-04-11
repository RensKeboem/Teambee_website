// Contact highlight functionality
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll to contact section with highlighting animation
    const scrollButtons = document.querySelectorAll('[data-scroll-to="contact"]');
    const contactSection = document.getElementById('contact');
    let isButtonScroll = false;
    
    // Create an Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && isButtonScroll) {
                // When contact section is fully in view and scroll was initiated by button
                const contactInfo = entry.target.querySelector('.contact-info');
                if (contactInfo) {
                    // Add animation to all elements within contact-info
                    const contactElements = contactInfo.querySelectorAll('*');
                    contactElements.forEach(element => {
                        element.classList.add('scale-contact');
                        setTimeout(() => {
                            element.classList.remove('scale-contact');
                        }, 2000);
                    });
                }
                // Reset the flag after animation
                setTimeout(() => {
                    isButtonScroll = false;
                }, 2000);
            }
        });
    }, {
        threshold: 0.8 // Trigger when 80% of the section is visible
    });
    
    // Start observing the contact section
    if (contactSection) {
        observer.observe(contactSection);
    }
    
    // Add event listeners to all buttons that scroll to contact
    scrollButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('data-scroll-to');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                // Set flag to indicate button-initiated scroll
                isButtonScroll = true;
                
                // Calculate the offset to account for the fixed header
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}); 