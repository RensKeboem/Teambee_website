document.addEventListener('DOMContentLoaded', function() {
    // Handle both login forms (main page and popup) with their specific prefixes
    const formPrefixes = ['main', 'popup'];
    
    formPrefixes.forEach(function(prefix) {
        const loginForm = document.getElementById(`${prefix}-login-form`);
        
        if (!loginForm) return; // Skip if form doesn't exist
        
        const submitButton = loginForm.querySelector(`#${prefix}-login-submit-btn`);
        const buttonText = loginForm.querySelector(`#${prefix}-login-button-text`);
        const buttonLoading = loginForm.querySelector(`#${prefix}-login-button-loading`);
        const errorContainer = loginForm.querySelector(`#${prefix}-login-error`);
        const passwordInput = loginForm.querySelector(`#${prefix}-password`);
        const emailInput = loginForm.querySelector(`#${prefix}-email`);
        
        // Email validation regex
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        // Function to validate form and update button state
        function validateForm() {
            const email = emailInput ? emailInput.value.trim() : '';
            const password = passwordInput ? passwordInput.value.trim() : '';
            const isEmailValid = email && emailRegex.test(email);
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
                hideError();
                validateForm();
            });
            
            emailInput.addEventListener('blur', function() {
                const email = emailInput.value.trim();
                if (email && !emailRegex.test(email)) {
                    showError('Please enter a valid email address.');
                }
            });
        }
        
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                hideError();
                validateForm();
            });
        }
        
        // Initial form validation
        validateForm();
        
        // Add event listener to this specific form
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Validate form before submission
            if (!validateForm()) {
                showError('Please enter a valid email address and password.');
                return;
            }
            
            // Show loading state
            if (submitButton) submitButton.disabled = true;
            if (buttonText) buttonText.classList.add('hidden');
            if (buttonLoading) buttonLoading.classList.remove('hidden');
            hideError();
            
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
                    // Redirect on success
                    window.location.href = result.redirect_url;
                } else {
                    // Clear password field and show error message
                    if (passwordInput) passwordInput.value = '';
                    showError(result.message);
                    // Focus back to password field
                    if (passwordInput) passwordInput.focus();
                    // Re-validate form after clearing password
                    validateForm();
                }
            } catch (error) {
                // Clear password field on any error
                if (passwordInput) passwordInput.value = '';
                showError('An unexpected error occurred. Please try again.');
                if (passwordInput) passwordInput.focus();
                // Re-validate form after clearing password
                validateForm();
            } finally {
                // Reset button state (but keep it disabled if form is invalid)
                if (buttonText) buttonText.classList.remove('hidden');
                if (buttonLoading) buttonLoading.classList.add('hidden');
                validateForm(); // This will properly set the button state
            }
        });
        
        function showError(message) {
            if (errorContainer) {
                errorContainer.textContent = message;
                errorContainer.classList.remove('hidden');
            }
        }
        
        function hideError() {
            if (errorContainer) {
                errorContainer.classList.add('hidden');
            }
        }
    });
}); 