// Popup and Dropdown Utilities - Combined login popup and language dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // === UTILITY FUNCTIONS ===
    
    // Scroll prevention utilities
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
    
    // Generic dropdown handler
    function setupDropdown(buttonId, menuId) {
        const button = document.getElementById(buttonId);
        const menu = document.getElementById(menuId);
        
        if (!button || !menu) return;
        
        // Toggle dropdown when button is clicked
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            menu.classList.toggle('hidden');
            button.setAttribute('aria-expanded', !menu.classList.contains('hidden'));
            
            // Add visible class for smoother animation
            if (!menu.classList.contains('hidden')) {
                menu.classList.add('visible');
            } else {
                menu.classList.remove('visible');
            }
        });
        
        // Prevent clicks inside dropdown from closing it
        menu.addEventListener('click', function(event) {
            // Only stop propagation if it's not a link
            if (!event.target.matches('a')) {
                event.stopPropagation();
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function() {
            if (!menu.classList.contains('hidden')) {
                menu.classList.add('hidden');
                menu.classList.remove('visible');
                button.setAttribute('aria-expanded', 'false');
            }
        });
        
        // Add keyboard accessibility
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && !menu.classList.contains('hidden')) {
                menu.classList.add('hidden');
                menu.classList.remove('visible');
                button.setAttribute('aria-expanded', 'false');
                button.focus();
            }
        });
    }
    
    // Generic popup handler
    function setupPopup(openButtonId, popupId, closeButtonId) {
        const openButton = document.getElementById(openButtonId);
        const popup = document.getElementById(popupId);
        const closeButton = document.getElementById(closeButtonId);
        
        if (!openButton || !popup) return;
        
        function closePopup() {
            const modalContent = popup.querySelector('.bg-white');
            if (modalContent) {
                modalContent.style.transform = 'scale(0.95)';
                modalContent.style.opacity = '0';
            }
            
            setTimeout(() => {
                popup.classList.add('hidden');
                enableScroll();
            }, 200);
        }
        
        // Open popup
        openButton.addEventListener('click', function(e) {
            e.preventDefault();
            disableScroll();
            popup.classList.remove('hidden');
            
            setTimeout(() => {
                const modalContent = popup.querySelector('.bg-white');
                if (modalContent) {
                    modalContent.style.transform = 'scale(1)';
                    modalContent.style.opacity = '1';
                }
            }, 10);
        });
        
        // Close popup with close button
        if (closeButton) {
            closeButton.addEventListener('click', function(e) {
                e.preventDefault();
                closePopup();
            });
        }
        
        // Close popup when clicking outside
        popup.addEventListener('click', function(e) {
            if (e.target === popup || e.target.classList.contains('backdrop-blur-sm')) {
                closePopup();
            }
        });
        
        // Close popup when pressing Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && popup && !popup.classList.contains('hidden')) {
                closePopup();
            }
        });
    }
    
    // === CLUB LANGUAGE DROPDOWN ===
    
    function setupClubLanguageDropdown() {
        const button = document.getElementById('club-language-dropdown-button');
        const menu = document.getElementById('club-language-dropdown-menu');
        const hiddenInput = document.getElementById('language');
        const displaySpan = document.getElementById('language-display');
        const languageOptions = menu ? menu.querySelectorAll('.language-option') : [];
        
        if (!button || !menu || !hiddenInput || !displaySpan) return;
        
        // Set up basic dropdown functionality
        setupDropdown('club-language-dropdown-button', 'club-language-dropdown-menu');
        
        // Handle language option selection
        languageOptions.forEach(option => {
            option.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const value = this.getAttribute('data-value');
                const text = this.textContent.trim();
                
                // Update hidden input value
                hiddenInput.value = value;
                
                // Update display text
                displaySpan.textContent = text;
                
                // Close dropdown
                menu.classList.add('hidden');
                menu.classList.remove('visible');
                button.setAttribute('aria-expanded', 'false');
                
                // Update selection styling
                languageOptions.forEach(opt => {
                    opt.classList.remove('text-[#3D2E7C]', 'font-semibold', 'bg-gray-50');
                    opt.classList.add('text-gray-700');
                });
                this.classList.remove('text-gray-700');
                this.classList.add('text-[#3D2E7C]', 'font-semibold', 'bg-gray-50');
            });
        });
        
        // Set initial selection styling for default value (Dutch/nl)
        if (languageOptions.length > 0) {
            const defaultOption = Array.from(languageOptions).find(opt => 
                opt.getAttribute('data-value') === hiddenInput.value
            );
            if (defaultOption) {
                defaultOption.classList.remove('text-gray-700');
                defaultOption.classList.add('text-[#3D2E7C]', 'font-semibold', 'bg-gray-50');
            }
        }
    }
    
    // === SPECIFIC IMPLEMENTATIONS ===
    
    // Language dropdown
    setupDropdown('language-dropdown-button', 'language-dropdown-menu');
    
    // Login popup
    setupPopup('login-button', 'login-popup', 'close-login-popup');
    
    // User dropdown (if exists)
    setupDropdown('user-dropdown-button', 'user-dropdown-menu');
    
    // Club language dropdown (for create club form)
    setupClubLanguageDropdown();
    
}); 