// Popup and Dropdown Utilities - Combined login popup and language dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // === UTILITY FUNCTIONS ===
    

    
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
                TeambeeUtils.enableScroll();
            }, 200);
        }
        
        // Open popup
        openButton.addEventListener('click', function(e) {
            e.preventDefault();
            TeambeeUtils.disableScroll();
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
    
    // === CONTACT POPUP HANDLER ===
    
    function setupContactPopup() {
        const contactPopup = document.getElementById('contact-popup');
        const contactForm = document.getElementById('contact-form');
        const closeContactBtn = document.getElementById('close-contact-popup');
        
        // Contact form button IDs (only buttons that should open the popup)
        const contactButtons = [
            { id: 'main-contact-us-button', type: 'ongoing' },
            { id: 'popup-contact-us-button', type: 'ongoing' },
            { id: 'services-cta-button', type: 'services' }
        ];
        
        if (!contactPopup) return;
        
        // Contact form translations
        const translations = {
            en: {
                contact_title: "Contact Us",
                contact_subtitle: "Fill out the form below and we'll get back to you as soon as possible.",
                services_title: "Request Information",
                services_subtitle: "Tell us about your club and we'll show you how Teambee can help you grow."
            },
            nl: {
                contact_title: "Neem Contact Op",
                contact_subtitle: "Vul onderstaand formulier in en we nemen zo snel mogelijk contact met je op.",
                services_title: "Informatie Aanvragen",
                services_subtitle: "Vertel ons over je club en we laten je zien hoe Teambee je kan helpen groeien."
            }
        };
        
        // Get current language
        // Translated messages for contact form
        const contactMessages = {
            nl: {
                networkError: 'Netwerkfout. Controleer je verbinding en probeer opnieuw.'
            },
            en: {
                networkError: 'Network error. Please check your connection and try again.'
            }
        };
        
        // Create translation function using shared utility
        const getContactMessage = TeambeeUtils.createTranslationFunction(contactMessages);
        
        // Show contact popup with form type
        function showContactPopup(formType = 'ongoing', fromPopup = false) {
            const lang = TeambeeUtils.getCurrentLanguage();
            const trans = translations[lang];
            const formTypeInput = document.getElementById('form_type');
            const contactFormTitle = document.getElementById('contact-form-title');
            const contactFormSubtitle = document.getElementById('contact-form-subtitle');
            
            if (formType === 'services') {
                if (contactFormTitle) contactFormTitle.textContent = trans.services_title;
                if (contactFormSubtitle) contactFormSubtitle.textContent = trans.services_subtitle;
                if (formTypeInput) formTypeInput.value = 'services';
            } else {
                if (contactFormTitle) contactFormTitle.textContent = trans.contact_title;
                if (contactFormSubtitle) contactFormSubtitle.textContent = trans.contact_subtitle;
                if (formTypeInput) formTypeInput.value = 'ongoing';
            }
            
            // Only disable scroll if not coming from another popup
            if (!fromPopup) {
                TeambeeUtils.disableScroll();
            }
            contactPopup.classList.remove('hidden');
            
            setTimeout(() => {
                const modalContent = contactPopup.querySelector('.bg-white');
                if (modalContent) {
                    modalContent.style.transform = 'scale(1)';
                    modalContent.style.opacity = '1';
                }
            }, 10);
            
            // Focus first input and setup validation
            setTimeout(() => {
                const firstInput = contactForm?.querySelector('input[type="text"]');
                if (firstInput) firstInput.focus();
                addValidationListeners();
            }, 100);
        }
        
        // Hide contact popup with cleanup
        function hideContactPopup() {
            const modalContent = contactPopup.querySelector('.bg-white');
            if (modalContent) {
                modalContent.style.transform = 'scale(0.95)';
                modalContent.style.opacity = '0';
            }
            
            setTimeout(() => {
                contactPopup.classList.add('hidden');
                TeambeeUtils.enableScroll();
                
                // Reset form and validation state
                if (contactForm) {
                    contactForm.reset();
                    const errorDiv = document.getElementById('contact-error');
                    const successDiv = document.getElementById('contact-success');
                    if (errorDiv) errorDiv.classList.add('hidden');
                    if (successDiv) successDiv.classList.add('hidden');
                    setTimeout(validateForm, 10);
                }
            }, 200);
        }
        
        // Form validation
        function validateForm() {
            const inputs = {
                firstName: document.getElementById('contact_first_name'),
                lastName: document.getElementById('contact_last_name'),
                clubName: document.getElementById('contact_club_name'),
                email: document.getElementById('contact_email'),
                phone: document.getElementById('contact_phone')
            };
            const submitBtn = document.getElementById('contact-submit-btn');
            
            if (!Object.values(inputs).every(Boolean) || !submitBtn) return;
            
            const values = Object.fromEntries(
                Object.entries(inputs).map(([key, input]) => [key, input.value.trim()])
            );
            
            const isEmailValid = TeambeeUtils.validateEmail(values.email);
            const isFormValid = Object.values(values).every(Boolean) && isEmailValid;
            
            // Update submit button state
            submitBtn.disabled = !isFormValid;
            if (isFormValid) {
                submitBtn.classList.remove('bg-gray-400', 'cursor-not-allowed');
                submitBtn.classList.add('bg-[#3D2E7C]', 'hover:bg-[#3D2E7C]/90');
            } else {
                submitBtn.classList.add('bg-gray-400', 'cursor-not-allowed');
                submitBtn.classList.remove('bg-[#3D2E7C]', 'hover:bg-[#3D2E7C]/90');
            }
            
            // Email field visual feedback
            if (values.email && !isEmailValid) {
                inputs.email.classList.add('border-red-500');
                inputs.email.classList.remove('border-gray-300');
            } else {
                inputs.email.classList.remove('border-red-500');
                inputs.email.classList.add('border-gray-300');
            }
        }
        
        // Add validation listeners
        function addValidationListeners() {
            const inputIds = ['contact_first_name', 'contact_last_name', 'contact_club_name', 'contact_email', 'contact_phone'];
            inputIds.forEach(inputId => {
                const input = document.getElementById(inputId);
                if (input) {
                    input.addEventListener('input', validateForm);
                    input.addEventListener('blur', validateForm);
                }
            });
            validateForm();
        }
        
        // Setup multiple trigger buttons
        contactButtons.forEach(({ id, type }) => {
            const button = document.getElementById(id);
            if (button) {
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    
                    // Special handling for contact button in login popup
                    if (id === 'popup-contact-us-button') {
                        const loginPopup = document.getElementById('login-popup');
                        if (loginPopup && !loginPopup.classList.contains('hidden')) {
                            // Close login popup first
                            const loginModalContent = loginPopup.querySelector('.bg-white');
                            if (loginModalContent) {
                                loginModalContent.style.transform = 'scale(0.95)';
                                loginModalContent.style.opacity = '0';
                            }
                            
                            setTimeout(() => {
                                loginPopup.classList.add('hidden');
                                // Then open contact popup (fromPopup = true to preserve scroll position)
                                showContactPopup(type, true);
                            }, 200);
                            return;
                        }
                    }
                    
                    showContactPopup(type);
                });
            }
        });
        
        // Setup close button using existing logic
        if (closeContactBtn) {
            closeContactBtn.addEventListener('click', function(e) {
                e.preventDefault();
                hideContactPopup();
            });
        }
        
        // Close popup when clicking outside
        contactPopup.addEventListener('click', function(e) {
            if (e.target === contactPopup || e.target.classList.contains('backdrop-blur-sm')) {
                hideContactPopup();
            }
        });
        
        // Close popup when pressing Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && contactPopup && !contactPopup.classList.contains('hidden')) {
                hideContactPopup();
            }
        });
        
        // Handle form submission
        if (contactForm) {
            contactForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const submitBtn = document.getElementById('contact-submit-btn');
                const buttonText = document.getElementById('contact-button-text');
                const buttonLoading = document.getElementById('contact-button-loading');
                const errorDiv = document.getElementById('contact-error');
                const successDiv = document.getElementById('contact-success');
                
                if (!submitBtn || !buttonText || !buttonLoading) return;
                
                // Hide previous messages
                if (errorDiv) errorDiv.classList.add('hidden');
                if (successDiv) successDiv.classList.add('hidden');
                
                // Show loading state
                submitBtn.disabled = true;
                buttonText.classList.add('hidden');
                buttonLoading.classList.remove('hidden');
                
                try {
                    const formData = new FormData(contactForm);
                    
                    // Detect language from current page URL and build the correct contact URL
                    const isEnglish = TeambeeUtils.getCurrentLanguage() === 'en';
                    const contactUrl = isEnglish ? '/en/contact' : '/contact';
                    
                    const response = await fetch(contactUrl, {
                        method: 'POST',
                        headers: { 'X-Requested-With': 'XMLHttpRequest' },
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        if (successDiv) {
                            successDiv.textContent = result.message;
                            successDiv.classList.remove('hidden');
                        }
                        setTimeout(hideContactPopup, 3000);
                    } else {
                        if (errorDiv) {
                            errorDiv.textContent = result.message;
                            errorDiv.classList.remove('hidden');
                        }
                    }
                } catch (error) {
                    console.error('Contact form error:', error);
                    if (errorDiv) {
                        // Use a generic error message - the server will provide translated messages for specific errors
                        errorDiv.textContent = getContactMessage('networkError');
                        errorDiv.classList.remove('hidden');
                    }
                } finally {
                    buttonText.classList.remove('hidden');
                    buttonLoading.classList.add('hidden');
                    validateForm();
                }
            });
        }
    }
    
    // === HERO SERVICES SCROLL HANDLER ===
    
    function setupHeroServicesScroll() {
        const heroServicesButton = document.getElementById('hero-services-button');
        const servicesSection = document.getElementById('services');
        
        if (!heroServicesButton || !servicesSection) return;
        
        heroServicesButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get header height for offset
            const headerHeight = document.querySelector('header')?.offsetHeight || 0;
            const targetPosition = servicesSection.getBoundingClientRect().top + window.pageYOffset - headerHeight;
            
            // Smooth scroll to services section
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        });
    }
    
    // === SPECIFIC IMPLEMENTATIONS ===
    
    // Language dropdown
    setupDropdown('language-dropdown-button', 'language-dropdown-menu');
    
    // Login popup
    setupPopup('login-button', 'login-popup', 'close-login-popup');
    
    // Contact popup with multiple trigger buttons
    setupContactPopup();
    
    // User dropdown (if exists)
    setupDropdown('user-dropdown-button', 'user-dropdown-menu');
    
    // Club language dropdown (for create club form)
    setupClubLanguageDropdown();
    
    // Hero services button scroll functionality
    setupHeroServicesScroll();
    
}); 