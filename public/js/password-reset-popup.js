// Password reset popup functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // Password reset popup elements
    const passwordResetPopup = document.getElementById('password-reset-popup');
    const passwordResetForm = document.getElementById('reset-password-form');
    const closePasswordResetBtn = document.getElementById('close-password-reset-popup');
    const submitButton = document.getElementById('reset-password-submit-btn');
    const passwordField = document.getElementById('reset-new-password');
    const confirmPasswordField = document.getElementById('reset-confirm-password');
    const errorMsg = document.getElementById('reset-password-mismatch-error');
    const tokenField = document.getElementById('reset-token');
    
    // Translation messages
    const messages = {
        nl: {
            passwordsNotMatch: 'Wachtwoorden komen niet overeen',
            networkError: 'Er is een fout opgetreden. Probeer het opnieuw.',
            resetting: 'Opnieuw instellen...',
            allFieldsRequired: 'Alle velden zijn verplicht',
            passwordTooShort: 'Wachtwoord moet minimaal 8 tekens bevatten'
        },
        en: {
            passwordsNotMatch: 'Passwords do not match',
            networkError: 'An error occurred. Please try again.',
            resetting: 'Resetting...',
            allFieldsRequired: 'All fields are required',
            passwordTooShort: 'Password must be at least 8 characters long'
        }
    };
    
    function getMessage(key) {
        const lang = TeambeeUtils.getCurrentLanguage();
        return messages[lang]?.[key] || messages.en[key] || key;
    }
    
    function openPasswordResetPopup(token) {
        if (!passwordResetPopup || !tokenField) return;
        
        // Set the token
        tokenField.value = token;
        
        // Close any other open popups/dropdowns
        TeambeeUtils.closeAllDropdowns();
        
        // Show popup
        TeambeeUtils.disableScroll();
        passwordResetPopup.classList.remove('hidden');
        
        setTimeout(() => {
            const modalContent = passwordResetPopup.querySelector('.bg-white');
            if (modalContent) {
                modalContent.style.transform = 'scale(1)';
                modalContent.style.opacity = '1';
            }
        }, 10);
        
        // Focus on password field
        setTimeout(() => {
            if (passwordField) passwordField.focus();
        }, 100);
    }
    
    function closePasswordResetPopup() {
        if (!passwordResetPopup) return;
        
        const modalContent = passwordResetPopup.querySelector('.bg-white');
        if (modalContent) {
            modalContent.style.transform = 'scale(0.95)';
            modalContent.style.opacity = '0';
        }
        
        setTimeout(() => {
            passwordResetPopup.classList.add('hidden');
            TeambeeUtils.enableScroll();
            
            // Clear form
            if (passwordResetForm) passwordResetForm.reset();
            if (tokenField) tokenField.value = '';
            
            // Hide messages
            TeambeeUtils.hideMessage(document.getElementById('reset-popup-error'));
            TeambeeUtils.hideMessage(document.getElementById('reset-popup-success'));
            
            // Reset validation
            if (errorMsg) errorMsg.classList.add('hidden');
            if (confirmPasswordField) confirmPasswordField.classList.remove('border-red-500');
        }, 200);
    }
    
    // Check if there's a reset_token in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const resetToken = urlParams.get('reset_token');
    
    if (resetToken) {
        // Remove the token from URL for security
        const newUrl = window.location.pathname + (window.location.pathname.endsWith('/') ? '' : '/');
        window.history.replaceState({}, document.title, newUrl);
        
        // Open the password reset popup
        openPasswordResetPopup(resetToken);
    }
    
    // Close button handler
    if (closePasswordResetBtn) {
        closePasswordResetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            closePasswordResetPopup();
        });
    }
    
    // Close popup when clicking outside
    if (passwordResetPopup) {
        passwordResetPopup.addEventListener('click', function(e) {
            if (e.target === passwordResetPopup || e.target.classList.contains('backdrop-blur-sm')) {
                closePasswordResetPopup();
            }
        });
    }
    
    // Close popup when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && passwordResetPopup && !passwordResetPopup.classList.contains('hidden')) {
            closePasswordResetPopup();
        }
    });
    
    // Form validation
    function validatePasswordResetForm() {
        if (!passwordField || !confirmPasswordField || !submitButton) return false;
        
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        let isValid = true;
        
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
        
        // Check if both fields are filled
        if (!password || !confirmPassword) {
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
    if (passwordField && confirmPasswordField) {
        passwordField.addEventListener('input', validatePasswordResetForm);
        confirmPasswordField.addEventListener('input', validatePasswordResetForm);
        
        // Initial validation
        validatePasswordResetForm();
    }
    
    // Form submission handler
    if (passwordResetForm) {
        passwordResetForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!validatePasswordResetForm()) {
                TeambeeUtils.showMessage(document.getElementById('reset-popup-error'), getMessage('allFieldsRequired'));
                return;
            }
            
            const token = tokenField ? tokenField.value : '';
            if (!token) {
                TeambeeUtils.showMessage(document.getElementById('reset-popup-error'), 'Invalid reset token');
                return;
            }
            
            // Show loading state
            submitButton.disabled = true;
            submitButton.textContent = submitButton.dataset.loadingText || getMessage('resetting');
            TeambeeUtils.hideMessage(document.getElementById('reset-popup-error'));
            TeambeeUtils.hideMessage(document.getElementById('reset-popup-success'));
            
            try {
                const formData = new FormData(passwordResetForm);
                formData.append('token', token);
                
                // Detect current page language and use appropriate endpoint
                const currentLang = TeambeeUtils.getCurrentLanguage();
                const resetUrl = currentLang === 'en' ? `/en/reset-password/${token}` : `/reset-password/${token}`;
                
                const response = await fetch(resetUrl, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const result = await response.json();
                
                if (result.success) {
                    TeambeeUtils.showMessage(document.getElementById('reset-popup-success'), result.message);
                    
                    // Clear form
                    passwordResetForm.reset();
                    
                    // Close popup after a short delay
                    setTimeout(() => {
                        closePasswordResetPopup();
                        
                        // Show success message on main page if available
                        const mainSuccessContainer = document.querySelector('.success-notification');
                        if (mainSuccessContainer && result.message) {
                            // You can implement a main page notification here if needed
                        }
                    }, 2000);
                } else {
                    TeambeeUtils.showMessage(document.getElementById('reset-popup-error'), result.message);
                    
                    // Clear password fields and focus on first field
                    if (passwordField) passwordField.value = '';
                    if (confirmPasswordField) confirmPasswordField.value = '';
                    if (passwordField) passwordField.focus();
                }
            } catch (error) {
                console.error('Error:', error);
                TeambeeUtils.showMessage(document.getElementById('reset-popup-error'), getMessage('networkError'));
            } finally {
                submitButton.textContent = submitButton.dataset.defaultText || 'Reset Password';
                validatePasswordResetForm(); // Re-validate to restore button state
            }
        });
    }
}); 