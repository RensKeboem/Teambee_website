// Form handling functionality - Combined login, forgot password, and registration validation
document.addEventListener('DOMContentLoaded', function() {
    
    // === TRANSLATED MESSAGES ===
    const messages = {
        nl: {
            enterEmailFirst: 'Voer eerst je e-mailadres in.',
            enterValidEmail: 'Voer een geldig e-mailadres in.',
            enterEmailAndPassword: 'Voer een geldig e-mailadres en wachtwoord in.',
            networkError: 'Netwerkfout. Controleer je verbinding en probeer opnieuw.',
            fillAllFields: 'Vul alle velden correct in.',
            passwordsNotMatch: 'Wachtwoorden komen niet overeen',
            resetting: 'Bezig met resetten...',
            sending: 'Versturen...',
            resetPassword: 'Wachtwoord Resetten'
        },
        en: {
            enterEmailFirst: 'Please enter your email address first.',
            enterValidEmail: 'Please enter a valid email address.',
            enterEmailAndPassword: 'Please enter a valid email address and password.',
            networkError: 'Network error. Please check your connection and try again.',
            fillAllFields: 'Please fill in all fields correctly.',
            passwordsNotMatch: 'Passwords do not match',
            resetting: 'Resetting...',
            sending: 'Sending...',
            resetPassword: 'Reset Password'
        }
    };
    
    // Create translation function using shared utility
    const getMessage = TeambeeUtils.createTranslationFunction(messages);
    
    // === LOGIN FORM HANDLING ===
    const formPrefixes = ['main', 'popup'];
    
    formPrefixes.forEach(function(prefix) {
        const loginForm = document.getElementById(`${prefix}-login-form`);
        
        if (!loginForm) return;
        
        const submitButton = loginForm.querySelector(`#${prefix}-login-submit-btn`);
        const buttonText = loginForm.querySelector(`#${prefix}-login-button-text`);
        const buttonLoading = loginForm.querySelector(`#${prefix}-login-button-loading`);
        const errorContainer = loginForm.querySelector(`#${prefix}-login-error`);
        const passwordInput = loginForm.querySelector(`#${prefix}-password`);
        const emailInput = loginForm.querySelector(`#${prefix}-email`);
        const forgotPasswordBtn = document.getElementById(`${prefix}-forgot-password-btn`);
        const infoDiv = document.getElementById(`${prefix}-login-info`);
        
        // Login form validation
        function validateLoginForm() {
            const email = emailInput ? emailInput.value.trim() : '';
            const password = passwordInput ? passwordInput.value.trim() : '';
            const isEmailValid = TeambeeUtils.validateEmail(email);
            const isPasswordValid = password.length > 0;
            const isFormValid = isEmailValid && isPasswordValid;
            
            // Update submit button state
            if (submitButton) {
                submitButton.disabled = !isFormValid;
                if (isFormValid) {
                    submitButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
                    submitButton.classList.add('bg-[#3D2E7C]', 'hover:bg-[#3D2E7C]/90');
                } else {
                    submitButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
                    submitButton.classList.remove('hover:bg-[#3D2E7C]/90');
                }
            }
            
            // Update email field styling
            if (emailInput) {
                emailInput.classList.remove('border-red-300', 'focus-visible:ring-red-500', 'focus-visible:border-red-500');
                if (email && !isEmailValid) {
                    emailInput.classList.add('border-red-300', 'focus-visible:ring-red-500', 'focus-visible:border-red-500');
                } else {
                    emailInput.classList.add('border-gray-300', 'focus-visible:ring-[#3D2E7C]', 'focus-visible:border-[#3D2E7C]');
                }
            }
            
            return isFormValid;
        }
        
        // Add real-time validation listeners
        if (emailInput) {
            emailInput.addEventListener('input', function() {
                TeambeeUtils.hideMessage(errorContainer);
                validateLoginForm();
            });
            
            emailInput.addEventListener('blur', function() {
                const email = emailInput.value.trim();
                if (email && !TeambeeUtils.validateEmail(email)) {
                    TeambeeUtils.showMessage(errorContainer, getMessage('enterValidEmail'));
                }
            });
        }
        
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                TeambeeUtils.hideMessage(errorContainer);
                validateLoginForm();
            });
        }
        
        // Initial form validation
        validateLoginForm();
        
        // Login form submission
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (!validateLoginForm()) {
                TeambeeUtils.showMessage(errorContainer, getMessage('enterEmailAndPassword'));
                return;
            }
            
            // Show loading state
            if (submitButton) submitButton.disabled = true;
            if (buttonText) buttonText.classList.add('hidden');
            if (buttonLoading) buttonLoading.classList.remove('hidden');
            TeambeeUtils.hideMessage(errorContainer);
            
            try {
                const formData = new FormData(loginForm);
                
                // Detect language from current page URL and build the correct login URL
                const currentPath = window.location.pathname;
                const isEnglish = currentPath.startsWith('/en');
                const loginUrl = isEnglish ? '/en/login' : '/login';
                
                const response = await fetch(loginUrl, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                
                if (result.success) {
                    window.location.href = result.redirect_url;
                } else {
                    if (passwordInput) passwordInput.value = '';
                    TeambeeUtils.showMessage(errorContainer, result.message);
                    if (passwordInput) passwordInput.focus();
                    validateLoginForm();
                }
                            } catch (error) {
                if (passwordInput) passwordInput.value = '';
                TeambeeUtils.showMessage(errorContainer, getMessage('networkError'));
                if (passwordInput) passwordInput.focus();
                validateLoginForm();
            } finally {
                if (buttonText) buttonText.classList.remove('hidden');
                if (buttonLoading) buttonLoading.classList.add('hidden');
                validateLoginForm();
            }
        });
        
        // === FORGOT PASSWORD HANDLING ===
        if (forgotPasswordBtn) {
            forgotPasswordBtn.addEventListener('click', function(e) {
                e.preventDefault();
                
                TeambeeUtils.hideMessage(errorContainer);
                TeambeeUtils.hideMessage(infoDiv);
                
                const email = emailInput ? emailInput.value.trim() : '';
                
                if (!email) {
                    TeambeeUtils.showMessage(errorContainer, getMessage('enterEmailFirst'));
                    if (emailInput) emailInput.focus();
                    return;
                }
                
                if (!TeambeeUtils.validateEmail(email)) {
                    TeambeeUtils.showMessage(errorContainer, getMessage('enterValidEmail'));
                    if (emailInput) emailInput.focus();
                    return;
                }
                
                // Show loading state
                forgotPasswordBtn.disabled = true;
                const originalText = forgotPasswordBtn.textContent;
                forgotPasswordBtn.textContent = getMessage('sending');
                
                // Detect language from current page URL and build the correct action URL
                const currentPath = window.location.pathname;
                const isEnglish = currentPath.startsWith('/en');
                const actionUrl = isEnglish ? '/en/forgot-password' : '/forgot-password';
                
                fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: `email=${encodeURIComponent(email)}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        TeambeeUtils.showMessage(infoDiv, data.message);
                        if (emailInput) emailInput.value = '';
                        if (passwordInput) passwordInput.value = '';
                    } else {
                        TeambeeUtils.showMessage(errorContainer, data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    TeambeeUtils.showMessage(errorContainer, getMessage('networkError'));
                })
                .finally(() => {
                    forgotPasswordBtn.disabled = false;
                    forgotPasswordBtn.textContent = originalText;
                });
            });
        }
    });
    
    // === REGISTRATION VALIDATION ===
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const errorMsg = document.getElementById('password-mismatch-error');
    
    if (passwordField && confirmPasswordField && errorMsg) {
        function validatePasswords() {
            if (confirmPasswordField.value && passwordField.value !== confirmPasswordField.value) {
                confirmPasswordField.setCustomValidity(getMessage('passwordsNotMatch'));
                errorMsg.classList.remove('hidden');
                confirmPasswordField.classList.add('border-red-500');
            } else {
                confirmPasswordField.setCustomValidity('');
                errorMsg.classList.add('hidden');
                confirmPasswordField.classList.remove('border-red-500');
            }
        }
        
        // Real-time validation
        confirmPasswordField.addEventListener('input', validatePasswords);
        passwordField.addEventListener('input', validatePasswords);
        
        // Validation on blur
        confirmPasswordField.addEventListener('blur', function() {
            if (this.value && passwordField.value !== this.value) {
                errorMsg.classList.remove('hidden');
                this.classList.add('border-red-500');
            }
        });
        
        // Remove error styling on focus
        confirmPasswordField.addEventListener('focus', function() {
            this.classList.remove('border-red-500');
            if (this.value === passwordField.value) {
                errorMsg.classList.add('hidden');
            }
        });
    }
    
    // === PASSWORD RESET VALIDATION ===
    const resetSubmitButton = document.getElementById('reset-password-submit-btn');
    const resetForm = document.getElementById('reset-password-form');
    const resetErrorContainer = document.getElementById('reset-error');
    const resetSuccessContainer = document.getElementById('reset-success');
    
    if (resetSubmitButton && passwordField && confirmPasswordField && errorMsg) {
        function validateResetForm() {
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
                errorMsg.classList.remove('hidden');
                confirmPasswordField.classList.add('border-red-500');
                isValid = false;
            } else {
                confirmPasswordField.setCustomValidity('');
                errorMsg.classList.add('hidden');
                confirmPasswordField.classList.remove('border-red-500');
            }
            
            // Check if both fields are filled
            if (!password || !confirmPassword) {
                isValid = false;
            }
            
            // Update submit button state
            if (isValid) {
                resetSubmitButton.disabled = false;
                resetSubmitButton.classList.remove('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
                resetSubmitButton.classList.add('bg-[#3D2E7C]', 'hover:bg-[#3D2E7C]/90');
            } else {
                resetSubmitButton.disabled = true;
                resetSubmitButton.classList.add('disabled:bg-gray-400', 'disabled:cursor-not-allowed');
                resetSubmitButton.classList.remove('hover:bg-[#3D2E7C]/90');
            }
            
            return isValid;
        }
        
        // Initial validation
        validateResetForm();
        
        // Add real-time validation listeners
        passwordField.addEventListener('input', validateResetForm);
        confirmPasswordField.addEventListener('input', validateResetForm);
        
        // Enhanced blur validation
        confirmPasswordField.addEventListener('blur', function() {
            if (this.value && passwordField.value !== this.value) {
                errorMsg.classList.remove('hidden');
                this.classList.add('border-red-500');
            }
            validateResetForm();
        });
        
        // Enhanced focus handling
        confirmPasswordField.addEventListener('focus', function() {
            this.classList.remove('border-red-500');
            if (this.value === passwordField.value) {
                errorMsg.classList.add('hidden');
            }
        });
        
        // Form submission handling
        if (resetForm) {
            resetForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                if (!validateResetForm()) {
                    TeambeeUtils.showMessage(resetErrorContainer, getMessage('fillAllFields'));
                    return;
                }
                
                // Show loading state
                resetSubmitButton.disabled = true;
                resetSubmitButton.textContent = resetSubmitButton.dataset.loadingText || getMessage('resetting');
                TeambeeUtils.hideMessage(resetErrorContainer);
                TeambeeUtils.hideMessage(resetSuccessContainer);
                
                try {
                    const formData = new FormData(resetForm);
                    
                    const response = await fetch(window.location.pathname, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        TeambeeUtils.showMessage(resetSuccessContainer, result.message);
                        resetForm.reset();
                        
                        // Redirect after a short delay to show success message
                        if (result.redirect) {
                            setTimeout(() => {
                                window.location.href = result.redirect;
                            }, 2000);
                        }
                    } else {
                        TeambeeUtils.showMessage(resetErrorContainer, result.message);
                        
                        // Clear password fields and focus on first field when there's an error
                        if (passwordField) passwordField.value = '';
                        if (confirmPasswordField) confirmPasswordField.value = '';
                        if (passwordField) passwordField.focus();
                    }
                } catch (error) {
                    console.error('Error:', error);
                    TeambeeUtils.showMessage(resetErrorContainer, getMessage('networkError'));
                } finally {
                    resetSubmitButton.textContent = resetSubmitButton.dataset.defaultText || getMessage('resetPassword');
                    validateResetForm(); // Re-validate to restore button state
                }
            });
        }
    }
}); 