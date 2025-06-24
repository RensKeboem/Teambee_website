// Forgot password functionality
document.addEventListener('DOMContentLoaded', function() {
    // Handle both login forms (main page and popup) with their specific prefixes
    const formPrefixes = ['main', 'popup'];
    
    formPrefixes.forEach(function(prefix) {
        const forgotPasswordBtn = document.getElementById(`${prefix}-forgot-password-btn`);
        const emailInput = document.getElementById(`${prefix}-email`);
        const errorDiv = document.getElementById(`${prefix}-login-error`);
        const infoDiv = document.getElementById(`${prefix}-login-info`);
        
        if (!forgotPasswordBtn) return; // Skip if button doesn't exist
        
        forgotPasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Clear previous messages
            hideMessage(errorDiv);
            hideMessage(infoDiv);
            
            // Get email value
            const email = emailInput ? emailInput.value.trim() : '';
            
            // Validate email input
            if (!email) {
                showMessage(errorDiv, 'Please enter your email address first.');
                if (emailInput) {
                    emailInput.focus();
                }
                return;
            }
            
            // Basic email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showMessage(errorDiv, 'Please enter a valid email address.');
                if (emailInput) {
                    emailInput.focus();
                }
                return;
            }
            
            // Disable button and show loading state
            forgotPasswordBtn.disabled = true;
            const originalText = forgotPasswordBtn.textContent;
            forgotPasswordBtn.textContent = 'Sending...';
            
            // Send AJAX request
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
                    // Clear the form
                    if (emailInput) emailInput.value = '';
                    const passwordInput = document.getElementById(`${prefix}-password`);
                    if (passwordInput) passwordInput.value = '';
                } else {
                    showMessage(errorDiv, data.message || 'Failed to send reset email. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage(errorDiv, 'An error occurred. Please try again later.');
            })
            .finally(() => {
                // Re-enable button and restore text
                forgotPasswordBtn.disabled = false;
                forgotPasswordBtn.textContent = originalText;
            });
        });
    });
});

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