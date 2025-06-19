document.addEventListener('DOMContentLoaded', function() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const errorMsg = document.getElementById('password-mismatch-error');
    
    function validatePasswords() {
        if (confirmPassword.value && password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity('Passwords do not match');
            errorMsg.classList.remove('hidden');
            confirmPassword.classList.add('border-red-500');
        } else {
            confirmPassword.setCustomValidity('');
            errorMsg.classList.add('hidden');
            confirmPassword.classList.remove('border-red-500');
        }
    }
    
    // Validate on input
    confirmPassword.addEventListener('input', validatePasswords);
    password.addEventListener('input', validatePasswords);
    
    // Validate on blur (when user leaves the field)
    confirmPassword.addEventListener('blur', function() {
        if (this.value && password.value !== this.value) {
            errorMsg.classList.remove('hidden');
            this.classList.add('border-red-500');
        }
    });
    
    // Remove error styling on focus
    confirmPassword.addEventListener('focus', function() {
        this.classList.remove('border-red-500');
        if (this.value === password.value) {
            errorMsg.classList.add('hidden');
        }
    });
}); 