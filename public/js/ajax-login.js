document.addEventListener('DOMContentLoaded', function() {
    // Handle all login forms (both popup and main page)
    const loginForms = document.querySelectorAll('form[id="login-form"]');
    
    loginForms.forEach(function(loginForm, index) {
        const submitButton = loginForm.querySelector('#login-submit-btn');
        const buttonText = loginForm.querySelector('#login-button-text');
        const buttonLoading = loginForm.querySelector('#login-button-loading');
        const errorContainer = loginForm.querySelector('#login-error');
        const passwordInput = loginForm.querySelector('#password');
        
        // Add event listener to this specific form
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
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
                }
            } catch (error) {
                // Clear password field on any error
                if (passwordInput) passwordInput.value = '';
                showError('An unexpected error occurred. Please try again.');
                if (passwordInput) passwordInput.focus();
            } finally {
                // Reset button state
                if (submitButton) submitButton.disabled = false;
                if (buttonText) buttonText.classList.remove('hidden');
                if (buttonLoading) buttonLoading.classList.add('hidden');
            }
        });
        
        // Hide error when user starts typing in this form
        const emailInput = loginForm.querySelector('#email');
        
        if (emailInput) {
            emailInput.addEventListener('input', hideError);
        }
        
        if (passwordInput) {
            passwordInput.addEventListener('input', hideError);
        }
        
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