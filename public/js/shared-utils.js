// Shared utility functions for Teambee application
window.TeambeeUtils = (function() {
    'use strict';
    
    // === LANGUAGE UTILITIES ===
    function getCurrentLanguage() {
        return window.location.pathname.startsWith('/en') ? 'en' : 'nl';
    }
    
    // === VALIDATION UTILITIES ===
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    function validateEmail(email) {
        return email && emailRegex.test(email);
    }
    
    // === SCROLL UTILITIES ===
    function preventScroll(e) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
    
    function disableScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
        
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollTop}px`;
        document.body.style.left = `-${scrollLeft}px`;
        document.body.style.width = '100%';
        
        document.body.setAttribute('data-scroll-top', scrollTop);
        document.body.setAttribute('data-scroll-left', scrollLeft);
    }
    
    function enableScroll() {
        const scrollTop = parseInt(document.body.getAttribute('data-scroll-top') || '0');
        const scrollLeft = parseInt(document.body.getAttribute('data-scroll-left') || '0');
        
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.width = '';
        
        window.scrollTo(scrollLeft, scrollTop);
        
        document.body.removeAttribute('data-scroll-top');
        document.body.removeAttribute('data-scroll-left');
    }
    
    // === MESSAGE UTILITIES ===
    function showMessage(element, message) {
        if (element) {
            element.textContent = message;
            element.classList.remove('hidden');
        }
    }
    
    function hideMessage(element) {
        if (element) {
            element.classList.add('hidden');
            element.textContent = '';
        }
    }
    
    // === TRANSLATION UTILITIES ===
    function createTranslationFunction(messages) {
        return function(key) {
            const lang = getCurrentLanguage();
            return messages[lang][key] || messages.en[key];
        };
    }
    
    // === DROPDOWN UTILITIES ===
    function closeAllDropdowns() {
        const dropdownMenus = [
            { menuId: 'user-dropdown-menu', buttonId: 'user-dropdown-button' },
            { menuId: 'language-dropdown-menu', buttonId: 'language-dropdown-button' }
        ];
        
        dropdownMenus.forEach(({ menuId, buttonId }) => {
            const menu = document.getElementById(menuId);
            const button = document.getElementById(buttonId);
            
            if (menu && !menu.classList.contains('hidden')) {
                menu.classList.add('hidden');
                menu.classList.remove('visible');
                if (button) {
                    button.setAttribute('aria-expanded', 'false');
                }
            }
        });
    }
    
    // === SUCCESS NOTIFICATION UTILITIES ===
    function initSuccessNotification() {
        const notification = document.getElementById('success-notification');
        const closeBtn = document.getElementById('close-success-notification');
        
        // Function to smoothly hide notification
        function hideNotification() {
            if (notification) {
                // Add transition if not already present
                if (!notification.style.transition) {
                    notification.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
                }
                
                // Start fade out animation
                notification.style.opacity = '0';
                notification.style.transform = 'translateY(-20px)';
                
                // Actually hide the element after animation completes
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 500); // Match transition duration
            }
        }
        
        if (notification) {
            // Check if notification is visible (either display: block or not display: none)
            const isVisible = notification.style.display === 'block' || 
                             (notification.style.display !== 'none' && !notification.classList.contains('hidden'));
            
            // Set initial state for animation
            if (isVisible) {
                notification.style.opacity = '1';
                notification.style.transform = 'translateY(0)';
                notification.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
                
                // Auto-hide after 5 seconds with smooth animation
                setTimeout(() => {
                    hideNotification();
                }, 5000);
            }
            
            // Setup close button with smooth animation
            if (closeBtn) {
                closeBtn.addEventListener('click', function() {
                    hideNotification();
                });
            }
        }
    }
    
    // Public API
    return {
        getCurrentLanguage,
        validateEmail,
        preventScroll,
        disableScroll,
        enableScroll,
        showMessage,
        hideMessage,
        createTranslationFunction,
        closeAllDropdowns,
        initSuccessNotification
    };
})(); 