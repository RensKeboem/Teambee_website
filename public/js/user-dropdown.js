// User dropdown and popup functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Translated messages for user dashboard forms
    const userMessages = {
        nl: {
            passwordsNotMatch: 'Wachtwoorden komen niet overeen',
            networkError: 'Er is een fout opgetreden. Probeer het opnieuw.',
            sending: 'Versturen...',
            updating: 'Bijwerken...'
        },
        en: {
            passwordsNotMatch: 'Passwords do not match',
            networkError: 'An error occurred. Please try again.',
            sending: 'Sending...',
            updating: 'Updating...'
        }
    };
    
    // Create translation function using shared utility
    const getUserMessage = TeambeeUtils.createTranslationFunction(userMessages);
    const button = document.getElementById('user-dropdown-button');
    const menu = document.getElementById('user-dropdown-menu');
    
    // Dropdown functionality (based on language-dropdown.js)
    if (button && menu) {
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
    
    // Popup functionality (based on login-popup.js)
    const passwordUpdateOption = document.getElementById('update-password-option');
    const inviteUserOption = document.getElementById('invite-user-option');
    const passwordUpdatePopup = document.getElementById('password-update-popup');
    const inviteUserPopup = document.getElementById('user-invite-popup');
    const closePasswordButton = document.getElementById('close-password-popup');
    const closeInviteButton = document.getElementById('close-invite-popup');
    

    
    // Open password update popup
    if (passwordUpdateOption && passwordUpdatePopup) {
        passwordUpdateOption.addEventListener('click', function(e) {
            e.preventDefault();
            // Close dropdown first
            if (menu) {
                menu.classList.add('hidden');
                menu.classList.remove('visible');
                button.setAttribute('aria-expanded', 'false');
            }
            
            TeambeeUtils.disableScroll();
            passwordUpdatePopup.classList.remove('hidden');
            
            setTimeout(() => {
                const modalContent = passwordUpdatePopup.querySelector('.bg-white');
                if (modalContent) {
                    modalContent.style.transform = 'scale(1)';
                    modalContent.style.opacity = '1';
                }
            }, 10);
        });
    }
    
    // Open invite user popup
    if (inviteUserOption && inviteUserPopup) {
        inviteUserOption.addEventListener('click', function(e) {
            e.preventDefault();
            // Close dropdown first
            if (menu) {
                menu.classList.add('hidden');
                menu.classList.remove('visible');
                button.setAttribute('aria-expanded', 'false');
            }
            
            TeambeeUtils.disableScroll();
            inviteUserPopup.classList.remove('hidden');
            
            setTimeout(() => {
                const modalContent = inviteUserPopup.querySelector('.bg-white');
                if (modalContent) {
                    modalContent.style.transform = 'scale(1)';
                    modalContent.style.opacity = '1';
                }
            }, 10);
        });
    }
    
    // Close password popup
    if (closePasswordButton && passwordUpdatePopup) {
        closePasswordButton.addEventListener('click', function(e) {
            e.preventDefault();
            closePopup(passwordUpdatePopup);
        });
    }
    
    // Close invite popup
    if (closeInviteButton && inviteUserPopup) {
        closeInviteButton.addEventListener('click', function(e) {
            e.preventDefault();
            closePopup(inviteUserPopup);
        });
    }
    
    // Close popups when clicking outside
    [passwordUpdatePopup, inviteUserPopup].forEach(popup => {
        if (popup) {
            popup.addEventListener('click', function(e) {
                if (e.target === popup || e.target.classList.contains('backdrop-blur-sm')) {
                    closePopup(popup);
                }
            });
        }
    });
    
    // Close popups when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (passwordUpdatePopup && !passwordUpdatePopup.classList.contains('hidden')) {
                closePopup(passwordUpdatePopup);
            }
            if (inviteUserPopup && !inviteUserPopup.classList.contains('hidden')) {
                closePopup(inviteUserPopup);
            }
        }
    });
    
    function closePopup(popup) {
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
    
    // Form handling (integrated from dashboard-forms.js)
    // Password update form handling
    const passwordUpdateForm = document.getElementById('password-update-form');
    if (passwordUpdateForm) {
        const submitButton = passwordUpdateForm.querySelector('#password-update-btn');
        const currentPasswordInput = passwordUpdateForm.querySelector('#current_password');
        const newPasswordInput = passwordUpdateForm.querySelector('#new_password');
        const confirmPasswordInput = passwordUpdateForm.querySelector('#confirm_new_password');
        
        // Real-time form validation
        function validatePasswordForm() {
            const currentPassword = currentPasswordInput.value.trim();
            const newPassword = newPasswordInput.value;
            const confirmPassword = confirmPasswordInput.value;
            
            let isValid = true;
            
            // Check if all fields are filled
            if (!currentPassword || !newPassword || !confirmPassword) {
                isValid = false;
            }
            
            // Check new password length
            if (newPassword && newPassword.length < 8) {
                isValid = false;
            }
            
            // Check password match
            if (confirmPassword && newPassword !== confirmPassword) {
                confirmPasswordInput.setCustomValidity(getUserMessage('passwordsNotMatch'));
                confirmPasswordInput.classList.add('border-red-300');
                isValid = false;
            } else {
                confirmPasswordInput.setCustomValidity('');
                confirmPasswordInput.classList.remove('border-red-300');
            }
            
            // Update button state
            if (isValid) {
                submitButton.disabled = false;
                submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
                submitButton.classList.add('hover:bg-[#3D2E7C]/90');
            } else {
                submitButton.disabled = true;
                submitButton.classList.add('opacity-50', 'cursor-not-allowed');
                submitButton.classList.remove('hover:bg-[#3D2E7C]/90');
            }
        }
        
        // Initial validation
        validatePasswordForm();
        
        // Add event listeners for real-time validation
        currentPasswordInput.addEventListener('input', validatePasswordForm);
        newPasswordInput.addEventListener('input', validatePasswordForm);
        confirmPasswordInput.addEventListener('input', validatePasswordForm);
        
        passwordUpdateForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Validate passwords match
            if (newPasswordInput.value !== confirmPasswordInput.value) {
                TeambeeUtils.showMessage(document.getElementById('password-update-error'), getUserMessage('passwordsNotMatch'));
                return;
            }
            
            // Show loading state
            submitButton.disabled = true;
            submitButton.textContent = submitButton.dataset.updatingText || getUserMessage('updating');
            TeambeeUtils.hideMessage(document.getElementById('password-update-error'));
            TeambeeUtils.hideMessage(document.getElementById('password-update-success'));
            
            try {
                const formData = new FormData(passwordUpdateForm);
                
                const response = await fetch('/dashboard/update-password', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const result = await response.json();
                
                if (result.success) {
                    TeambeeUtils.showMessage(document.getElementById('password-update-success'), result.message);
                    passwordUpdateForm.reset();
                    // Auto-close popup after 3 seconds
                    setTimeout(() => {
                        const passwordUpdatePopup = document.getElementById('password-update-popup');
                        if (passwordUpdatePopup && !passwordUpdatePopup.classList.contains('hidden')) {
                            closePopup(passwordUpdatePopup);
                        }
                    }, 3000);
                } else {
                    TeambeeUtils.showMessage(document.getElementById('password-update-error'), result.message);
                }
            } catch (error) {
                TeambeeUtils.showMessage(document.getElementById('password-update-error'), getUserMessage('networkError'));
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = submitButton.dataset.defaultText || 'Update Password';
            }
        });
    }
    
    // User invitation form handling
    const inviteForm = document.getElementById('invite-form');
    if (inviteForm) {
        const submitButton = inviteForm.querySelector('#invite-btn');
        const emailInput = inviteForm.querySelector('#invite_email');
        
        // Real-time form validation
        function validateInviteForm() {
            if (!submitButton || !emailInput) return;
            
            const email = emailInput.value.trim();
            const isValid = email && TeambeeUtils.validateEmail(email);
            
            // Update button state
            if (isValid) {
                submitButton.disabled = false;
                submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
                submitButton.classList.add('hover:bg-[#94C46F]/90');
            } else {
                submitButton.disabled = true;
                submitButton.classList.add('opacity-50', 'cursor-not-allowed');
                submitButton.classList.remove('hover:bg-[#94C46F]/90');
            }
        }
        
        // Initial validation
        validateInviteForm();
        
        // Add event listener for real-time validation
        emailInput.addEventListener('input', validateInviteForm);
        
        inviteForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading state
            submitButton.disabled = true;
            submitButton.textContent = submitButton.dataset.sendingText || getUserMessage('sending');
            TeambeeUtils.hideMessage(document.getElementById('invite-error'));
            TeambeeUtils.hideMessage(document.getElementById('invite-success'));
            
            try {
                const formData = new FormData(inviteForm);
                
                const response = await fetch('/dashboard/invite-user', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const result = await response.json();
                
                if (result.success) {
                    TeambeeUtils.showMessage(document.getElementById('invite-success'), result.message);
                    inviteForm.reset();
                } else {
                    TeambeeUtils.showMessage(document.getElementById('invite-error'), result.message);
                }
            } catch (error) {
                TeambeeUtils.showMessage(document.getElementById('invite-error'), getUserMessage('networkError'));
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = submitButton.dataset.defaultText || 'Send Invitation';
            }
        });
    }
}); 