document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('login-button');
    const loginPopup = document.getElementById('login-popup');
    const closeButton = document.getElementById('close-login-popup');
    
    // Function to prevent scrolling
    function preventScroll(e) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
    
    // Function to disable page scrolling
    function disableScroll() {
        // Save current scroll position
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
        
        // Apply styles to prevent scrolling
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollTop}px`;
        document.body.style.left = `-${scrollLeft}px`;
        document.body.style.width = '100%';
        
        // Store scroll position for restoration
        document.body.setAttribute('data-scroll-top', scrollTop);
        document.body.setAttribute('data-scroll-left', scrollLeft);
    }
    
    // Function to enable page scrolling
    function enableScroll() {
        // Get stored scroll position
        const scrollTop = parseInt(document.body.getAttribute('data-scroll-top') || '0');
        const scrollLeft = parseInt(document.body.getAttribute('data-scroll-left') || '0');
        
        // Remove styles
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.width = '';
        
        // Restore scroll position
        window.scrollTo(scrollLeft, scrollTop);
        
        // Clean up attributes
        document.body.removeAttribute('data-scroll-top');
        document.body.removeAttribute('data-scroll-left');
    }
    
    // Open popup when login button is clicked
    if (loginButton && loginPopup) {
        loginButton.addEventListener('click', function(e) {
            e.preventDefault();
            disableScroll();
            loginPopup.classList.remove('hidden');
            
            // Add animation class
            setTimeout(() => {
                const modalContent = loginPopup.querySelector('.bg-white');
                if (modalContent) {
                    modalContent.style.transform = 'scale(1)';
                    modalContent.style.opacity = '1';
                }
            }, 10);
        });
    }
    
    // Close popup when close button is clicked
    if (closeButton && loginPopup) {
        closeButton.addEventListener('click', function(e) {
            e.preventDefault();
            closePopup();
        });
    }
    
    // Close popup when clicking outside the modal content
    if (loginPopup) {
        loginPopup.addEventListener('click', function(e) {
            // Check if the click is on the backdrop (not on the modal content)
            if (e.target === loginPopup || e.target.classList.contains('backdrop-blur-sm')) {
                closePopup();
            }
        });
    }
    
    // Close popup when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && loginPopup && !loginPopup.classList.contains('hidden')) {
            closePopup();
        }
    });
    
    function closePopup() {
        const modalContent = loginPopup.querySelector('.bg-white');
        if (modalContent) {
            modalContent.style.transform = 'scale(0.95)';
            modalContent.style.opacity = '0';
        }
        
        setTimeout(() => {
            loginPopup.classList.add('hidden');
            enableScroll();
        }, 200);
    }
}); 