// Registration popup functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // Registration popup elements
    const registrationPopup = document.getElementById('registration-popup');
    const registrationForm = document.getElementById('registration-form');
    const closeRegistrationBtn = document.getElementById('close-registration-popup');
    const submitButton = document.getElementById('registration-submit-btn');
    const emailField = document.getElementById('registration-email');
    const passwordField = document.getElementById('registration-password');
    const confirmPasswordField = document.getElementById('registration-confirm-password');
    const errorMsg = document.getElementById('registration-password-mismatch-error');
    const tokenField = document.getElementById('registration-token');
    const clubSubtitle = document.getElementById('registration-club-subtitle');
    
    // Translation messages
    const messages = {
        nl: {
            passwordsNotMatch: 'Wachtwoorden komen niet overeen',
            networkError: 'Er is een fout opgetreden. Probeer het opnieuw.',
            creating: 'Account aanmaken...',
            allFieldsRequired: 'Alle velden zijn verplicht',
            passwordTooShort: 'Wachtwoord moet minimaal 8 tekens bevatten',
            emailRequired: 'Email is verplicht',
            validEmailRequired: 'Geldig emailadres is verplicht',
            createAccountFor: 'Maak je account aan voor'
        },
        en: {
            passwordsNotMatch: 'Passwords do not match',
            networkError: 'An error occurred. Please try again.',
            creating: 'Creating Account...',
            allFieldsRequired: 'All fields are required',
            passwordTooShort: 'Password must be at least 8 characters long',
            emailRequired: 'Email is required',
            validEmailRequired: 'Valid email address is required',
            createAccountFor: 'Create your account for'
        }
    };
    
    function getMessage(key) {
        const lang = TeambeeUtils.getCurrentLanguage();
        return messages[lang]?.[key] || messages.en[key] || key;
    }
    
    function openRegistrationPopup(token, clubName, prefilledEmail) {
        if (!registrationPopup || !tokenField) return;
        
        // Set the token
        tokenField.value = token;
        
        // Update subtitle with club name
        if (clubSubtitle && clubName) {
            clubSubtitle.textContent = `${getMessage('createAccountFor')} ${clubName}`;
        }
        
        // Prefill email if provided
        if (emailField && prefilledEmail) {
            emailField.value = prefilledEmail;
        }
        
        // Close any other open popups/dropdowns
        TeambeeUtils.closeAllDropdowns();
        
        // Show popup
        TeambeeUtils.disableScroll();
        registrationPopup.classList.remove('hidden');
        
        setTimeout(() => {
            const modalContent = registrationPopup.querySelector('.bg-white');
            if (modalContent) {
                modalContent.style.transform = 'scale(1)';
                modalContent.style.opacity = '1';
            }
        }, 10);
        
        // Focus on email field or password field if email is pre-filled
        setTimeout(() => {
            if (prefilledEmail && passwordField) {
                passwordField.focus();
            } else if (emailField) {
                emailField.focus();
            }
        }, 100);
    }
    
    function closeRegistrationPopup() {
        if (!registrationPopup) return;
        
        const modalContent = registrationPopup.querySelector('.bg-white');
        if (modalContent) {
            modalContent.style.transform = 'scale(0.95)';
            modalContent.style.opacity = '0';
        }
        
        setTimeout(() => {
            registrationPopup.classList.add('hidden');
            TeambeeUtils.enableScroll();
            
            // Clear form
            if (registrationForm) registrationForm.reset();
            if (tokenField) tokenField.value = '';
            
            // Hide messages
            TeambeeUtils.hideMessage(document.getElementById('registration-popup-error'));
            TeambeeUtils.hideMessage(document.getElementById('registration-popup-success'));
            
            // Reset validation
            if (errorMsg) errorMsg.classList.add('hidden');
            if (confirmPasswordField) confirmPasswordField.classList.remove('border-red-500');
            
            // Clear URL parameters
            const newUrl = window.location.pathname + (window.location.pathname.endsWith('/') ? '' : '/');
            window.history.replaceState({}, document.title, newUrl);
        }, 200);
    }
    
    // Check if there's a registration_token in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const registrationToken = urlParams.get('registration_token');
    const prefilledEmail = urlParams.get('email');
    
    if (registrationToken) {
        // Fetch club info for the token
        fetch(`/api/registration/${registrationToken}`, {
            method: 'GET'
        }).then(response => response.json())
        .then(data => {
            if (data.valid) {
                openRegistrationPopup(registrationToken, data.club_name, prefilledEmail);
            } else {
                console.error('Invalid registration token:', data.error);
                window.location.href = '/?error=invalid_token';
            }
        }).catch(error => {
            console.error('Error validating token:', error);
            window.location.href = '/?error=invalid_token';
        });
    }
    
    // Close button handler
    if (closeRegistrationBtn) {
        closeRegistrationBtn.addEventListener('click', function(e) {
            e.preventDefault();
            closeRegistrationPopup();
        });
    }
    
    // Close popup when clicking outside
    if (registrationPopup) {
        registrationPopup.addEventListener('click', function(e) {
            if (e.target === registrationPopup || e.target.classList.contains('backdrop-blur-sm')) {
                closeRegistrationPopup();
            }
        });
    }
    
    // Close popup when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && registrationPopup && !registrationPopup.classList.contains('hidden')) {
            closeRegistrationPopup();
        }
    });
    
    // Form validation
    function validateRegistrationForm() {
        if (!emailField || !passwordField || !confirmPasswordField || !submitButton) return false;
        
        const email = emailField.value.trim();
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        let isValid = true;
        
        // Check email
        if (!email) {
            isValid = false;
        } else if (!TeambeeUtils.validateEmail(email)) {
            isValid = false;
        }
        
        // Check password length
        if (password.length < 8) {
            isValid = false;
        }
        
        // Check if passwords match
        if (password && confirmPassword && password !== confirmPassword) {
            confirmPasswordField.setCustomValidity(getMessage('passwordsNotMatch'));
            if (errorMsg) errorMsg.classList.remove('hidden');
            confirmPasswordField.classList.add('border-red-500');
            isValid = false;
        } else {
            confirmPasswordField.setCustomValidity('');
            if (errorMsg) errorMsg.classList.add('hidden');
            confirmPasswordField.classList.remove('border-red-500');
        }
        
        // Check if all fields are filled
        if (!email || !password || !confirmPassword) {
            isValid = false;
        }
        
        // Update submit button state
        if (isValid) {
            submitButton.disabled = false;
            submitButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            submitButton.classList.add('bg-[#3D2E7C]', 'hover:bg-[#3D2E7C]/90');
        } else {
            submitButton.disabled = true;
            submitButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
            submitButton.classList.remove('hover:bg-[#3D2E7C]/90');
        }
        
        return isValid;
    }
    
    // Add validation listeners
    if (emailField && passwordField && confirmPasswordField) {
        emailField.addEventListener('input', validateRegistrationForm);
        passwordField.addEventListener('input', validateRegistrationForm);
        confirmPasswordField.addEventListener('input', validateRegistrationForm);
        
        // Initial validation
        validateRegistrationForm();
    }
    
    // Form submission handler
    if (registrationForm) {
        registrationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!validateRegistrationForm()) {
                TeambeeUtils.showMessage(document.getElementById('registration-popup-error'), getMessage('allFieldsRequired'));
                return;
            }
            
            const token = tokenField ? tokenField.value : '';
            if (!token) {
                TeambeeUtils.showMessage(document.getElementById('registration-popup-error'), 'Invalid registration token');
                return;
            }
            
            // Show loading state
            submitButton.disabled = true;
            submitButton.textContent = submitButton.dataset.loadingText || getMessage('creating');
            TeambeeUtils.hideMessage(document.getElementById('registration-popup-error'));
            TeambeeUtils.hideMessage(document.getElementById('registration-popup-success'));
            
            try {
                const formData = new FormData(registrationForm);
                formData.append('token', token);
                
                const response = await fetch(`/register/${token}`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const result = await response.json();
                
                if (result.success) {
                    TeambeeUtils.showMessage(document.getElementById('registration-popup-success'), result.message);
                    
                    // Clear form
                    registrationForm.reset();
                    
                    // Close popup after a short delay and redirect
                    setTimeout(() => {
                        closeRegistrationPopup();
                        
                        if (result.redirect) {
                            window.location.href = result.redirect;
                        }
                    }, 2000);
                } else {
                    TeambeeUtils.showMessage(document.getElementById('registration-popup-error'), result.message);
                    
                    // Clear password fields and focus on first field
                    if (passwordField) passwordField.value = '';
                    if (confirmPasswordField) confirmPasswordField.value = '';
                    if (passwordField) passwordField.focus();
                }
            } catch (error) {
                console.error('Error:', error);
                TeambeeUtils.showMessage(document.getElementById('registration-popup-error'), getMessage('networkError'));
            } finally {
                submitButton.textContent = submitButton.dataset.defaultText || 'Create Account';
                validateRegistrationForm(); // Re-validate to restore button state
            }
        });
    }
}); 