// Form handling functionality - Combined login, forgot password, and registration validation
document.addEventListener('DOMContentLoaded', function() {
    
    // === UTILITY FUNCTIONS ===
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
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
    
    function validateEmail(email) {
        return email && emailRegex.test(email);
    }
    
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
            const isEmailValid = validateEmail(email);
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
                hideMessage(errorContainer);
                validateLoginForm();
            });
            
            emailInput.addEventListener('blur', function() {
                const email = emailInput.value.trim();
                if (email && !validateEmail(email)) {
                    showMessage(errorContainer, 'Please enter a valid email address.');
                }
            });
        }
        
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                hideMessage(errorContainer);
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
                showMessage(errorContainer, 'Please enter a valid email address and password.');
                return;
            }
            
            // Show loading state
            if (submitButton) submitButton.disabled = true;
            if (buttonText) buttonText.classList.add('hidden');
            if (buttonLoading) buttonLoading.classList.remove('hidden');
            hideMessage(errorContainer);
            
            try {
                const formData = new FormData(loginForm);
                
                const response = await fetch('/login', {
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
                    showMessage(errorContainer, result.message);
                    if (passwordInput) passwordInput.focus();
                    validateLoginForm();
                }
            } catch (error) {
                if (passwordInput) passwordInput.value = '';
                showMessage(errorContainer, 'An unexpected error occurred. Please try again.');
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
                
                hideMessage(errorContainer);
                hideMessage(infoDiv);
                
                const email = emailInput ? emailInput.value.trim() : '';
                
                if (!email) {
                    showMessage(errorContainer, 'Please enter your email address first.');
                    if (emailInput) emailInput.focus();
                    return;
                }
                
                if (!validateEmail(email)) {
                    showMessage(errorContainer, 'Please enter a valid email address.');
                    if (emailInput) emailInput.focus();
                    return;
                }
                
                // Show loading state
                forgotPasswordBtn.disabled = true;
                const originalText = forgotPasswordBtn.textContent;
                forgotPasswordBtn.textContent = 'Sending...';
                
                fetch('/forgot-password', {
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
                        showMessage(infoDiv, data.message || 'Password reset link has been sent to your email address.');
                        if (emailInput) emailInput.value = '';
                        if (passwordInput) passwordInput.value = '';
                    } else {
                        showMessage(errorContainer, data.message || 'Failed to send reset email. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage(errorContainer, 'An error occurred. Please try again later.');
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
                confirmPasswordField.setCustomValidity('Passwords do not match');
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
}); 