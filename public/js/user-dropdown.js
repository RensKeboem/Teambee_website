// User dropdown and popup functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Translated messages for user dashboard forms
    const userMessages = {
        nl: {
            passwordsNotMatch: 'Wachtwoorden komen niet overeen',
            networkError: 'Er is een fout opgetreden. Probeer het opnieuw.',
            sending: 'Versturen...',
            updating: 'Bijwerken...',
            allFieldsRequired: 'Alle velden zijn verplicht',
            passwordTooShort: 'Wachtwoord moet minimaal 8 tekens bevatten',
            authenticationRequired: 'Authenticatie vereist',
            authServiceUnavailable: 'Authenticatieservice niet beschikbaar',
            invalidCredentials: 'Ongeldig huidige wachtwoord',
            passwordUpdated: 'Wachtwoord succesvol bijgewerkt',
            emailRequired: 'E-mailadres is verplicht',
            validEmailRequired: 'Voer een geldig e-mailadres in',
            onlyClubUsersInvite: 'Alleen clubgebruikers kunnen uitnodigen',
            invitationSent: 'Uitnodiging succesvol verzonden',
            userAlreadyExists: 'Een gebruiker met dit e-mailadres bestaat al'
        },
        en: {
            passwordsNotMatch: 'Passwords do not match',
            networkError: 'An error occurred. Please try again.',
            sending: 'Sending...',
            updating: 'Updating...',
            allFieldsRequired: 'All fields are required',
            passwordTooShort: 'Password must be at least 8 characters long',
            authenticationRequired: 'Authentication required',
            authServiceUnavailable: 'Authentication service unavailable',
            invalidCredentials: 'Invalid current password',
            passwordUpdated: 'Password updated successfully',
            emailRequired: 'Email address is required',
            validEmailRequired: 'Please enter a valid email address',
            onlyClubUsersInvite: 'Only club users can send invitations',
            invitationSent: 'Invitation sent successfully',
            userAlreadyExists: 'A user with this email address already exists'
        }
    };
    
    // Utility function to close other dropdowns
    function closeOtherDropdowns(excludeMenuId) {
        const dropdownMenus = [
            { menuId: 'user-dropdown-menu', buttonId: 'user-dropdown-button' },
            { menuId: 'language-dropdown-menu', buttonId: 'language-dropdown-button' }
        ];
        
        dropdownMenus.forEach(({ menuId, buttonId }) => {
            if (menuId !== excludeMenuId) {
                const menu = document.getElementById(menuId);
                const button = document.getElementById(buttonId);
                
                if (menu && !menu.classList.contains('hidden')) {
                    menu.classList.add('hidden');
                    menu.classList.remove('visible');
                    if (button) {
                        button.setAttribute('aria-expanded', 'false');
                    }
                }
            }
        });
    }
    
    // Create translation function using shared utility
    const getUserMessage = TeambeeUtils.createTranslationFunction(userMessages);
    
    // Utility function to update button state (DRY principle)
    function updateButtonState(button, isValid) {
        if (!button) return;
        
        button.disabled = !isValid;
        
        if (isValid) {
            button.classList.remove('opacity-50', 'cursor-not-allowed', 'bg-gray-400');
            button.classList.add('hover:bg-[#3D2E7C]/90', 'bg-[#3D2E7C]');
        } else {
            button.classList.add('opacity-50', 'cursor-not-allowed', 'bg-gray-400');
            button.classList.remove('hover:bg-[#3D2E7C]/90', 'bg-[#3D2E7C]');
        }
    }
    
    // Function to translate common server error messages
    function translateServerMessage(serverMessage) {
        if (!serverMessage) return null;
        
        // More maintainable approach: map specific known server messages to translation keys
        // This avoids duplication and focuses on actual server responses
        const serverMessageToTranslationKey = {
            // Authentication & Password errors
            'Current password is incorrect': 'invalidCredentials',
            'Invalid current password': 'invalidCredentials',
            'Password updated successfully': 'passwordUpdated',
            'New password must be at least 8 characters long': 'passwordTooShort',
            'New passwords do not match': 'passwordsNotMatch',
            'Authentication required': 'authenticationRequired',
            'Authentication service unavailable': 'authServiceUnavailable',
            'User not found': 'authenticationRequired',
            
            // Form validation errors
            'All fields are required': 'allFieldsRequired',
            'Email address is required': 'emailRequired',
            'Please enter a valid email address': 'validEmailRequired',
            
            // User invitation errors
            'Only club users can invite new users': 'onlyClubUsersInvite',
            'A user with this email already exists': 'userAlreadyExists',
            'Failed to send invitation email': 'networkError'
        };
        
        // Direct lookup first (most common case)
        const translationKey = serverMessageToTranslationKey[serverMessage];
        if (translationKey) {
            return getUserMessage(translationKey);
        }
        
        // Fallback: check for partial matches (for variations in server messages)
        const lowerMessage = serverMessage.toLowerCase();
        for (const [pattern, key] of Object.entries(serverMessageToTranslationKey)) {
            if (lowerMessage.includes(pattern.toLowerCase())) {
                return getUserMessage(key);
            }
        }
        
        return null; // No translation found, use original message
    }
    const button = document.getElementById('user-dropdown-button');
    const menu = document.getElementById('user-dropdown-menu');
    
    // Dropdown functionality with exclusive behavior
    if (button && menu) {
        // Toggle dropdown when button is clicked
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            
            // Close other dropdowns first
            closeOtherDropdowns('user-dropdown-menu');
            
            // Then toggle this dropdown
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
    

    
    // Setup popup triggers using the utility function
    if (passwordUpdateOption && passwordUpdatePopup) {
        passwordUpdateOption.addEventListener('click', function(e) {
            e.preventDefault();
            openPopup(passwordUpdatePopup);
        });
    }
    
    if (inviteUserOption && inviteUserPopup) {
        inviteUserOption.addEventListener('click', function(e) {
            e.preventDefault();
            openPopup(inviteUserPopup);
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
    
    // Utility function for popup management
    function openPopup(popup) {
        if (!popup) return;
        
        TeambeeUtils.closeAllDropdowns();
        TeambeeUtils.disableScroll();
        popup.classList.remove('hidden');
        
        setTimeout(() => {
            const modalContent = popup.querySelector('.bg-white');
            if (modalContent) {
                modalContent.style.transform = 'scale(1)';
                modalContent.style.opacity = '1';
            }
        }, 10);
    }
    
    function closePopup(popup) {
        if (!popup) return;
        
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
            if (!currentPasswordInput || !newPasswordInput || !confirmPasswordInput || !submitButton) return;
            
            const values = {
                current: currentPasswordInput.value.trim(),
                new: newPasswordInput.value,
                confirm: confirmPasswordInput.value
            };
            
            // Validation rules
            const isFieldsComplete = Object.values(values).every(val => val);
            const isPasswordLongEnough = !values.new || values.new.length >= 8;
            const isPasswordsMatch = !values.confirm || values.new === values.confirm;
            
            const isValid = isFieldsComplete && isPasswordLongEnough && isPasswordsMatch;
            
            // Handle password match visual feedback
            if (values.confirm && !isPasswordsMatch) {
                confirmPasswordInput.setCustomValidity(getUserMessage('passwordsNotMatch'));
                confirmPasswordInput.classList.add('border-red-300');
            } else {
                confirmPasswordInput.setCustomValidity('');
                confirmPasswordInput.classList.remove('border-red-300');
            }
            
            // Update submit button state
            updateButtonState(submitButton, isValid);
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
                
                // Detect current language and use appropriate endpoint
                const isEnglish = TeambeeUtils.getCurrentLanguage() === 'en';
                const updatePasswordUrl = isEnglish ? '/en/dashboard/update-password' : '/dashboard/update-password';
                
                const response = await fetch(updatePasswordUrl, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const result = await response.json();
                
                if (result.success) {
                    const successMessage = translateServerMessage(result.message) || getUserMessage('passwordUpdated') || result.message;
                    TeambeeUtils.showMessage(document.getElementById('password-update-success'), successMessage);
                    passwordUpdateForm.reset();
                    validatePasswordForm(); // Reset validation state
                    
                    // Auto-close popup after 3 seconds
                    setTimeout(() => closePopup(passwordUpdatePopup), 3000);
                } else {
                    const errorMessage = translateServerMessage(result.message) || result.message;
                    TeambeeUtils.showMessage(document.getElementById('password-update-error'), errorMessage);
                }
            } catch (error) {
                console.error('Password update error:', error);
                TeambeeUtils.showMessage(document.getElementById('password-update-error'), getUserMessage('networkError'));
            } finally {
                updateButtonState(submitButton, true); // Re-enable button
                submitButton.textContent = submitButton.dataset.defaultText || 'Update Password';
            }
        });
    }
    
    // User invitation form handling
    const inviteForm = document.getElementById('invite-form');
    if (inviteForm) {
        const submitButton = inviteForm.querySelector('#invite-submit-btn');
        const emailInput = inviteForm.querySelector('#invite_email');
        
        // Real-time form validation
        function validateInviteForm() {
            if (!submitButton || !emailInput) return;
            
            const email = emailInput.value.trim();
            const isValid = email && TeambeeUtils.validateEmail(email);
            
            updateButtonState(submitButton, isValid);
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
                
                // Detect current language and use appropriate endpoint
                const isEnglish = TeambeeUtils.getCurrentLanguage() === 'en';
                const inviteUserUrl = isEnglish ? '/en/dashboard/invite-user' : '/dashboard/invite-user';
                
                const response = await fetch(inviteUserUrl, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const result = await response.json();
                
                if (result.success) {
                    const successMessage = translateServerMessage(result.message) || getUserMessage('invitationSent') || result.message;
                    TeambeeUtils.showMessage(document.getElementById('invite-success'), successMessage);
                    inviteForm.reset();
                    validateInviteForm(); // Reset validation state
                } else {
                    const errorMessage = translateServerMessage(result.message) || result.message;
                    TeambeeUtils.showMessage(document.getElementById('invite-error'), errorMessage);
                }
            } catch (error) {
                console.error('Invite user error:', error);
                TeambeeUtils.showMessage(document.getElementById('invite-error'), getUserMessage('networkError'));
            } finally {
                updateButtonState(submitButton, true); // Re-enable button
                submitButton.textContent = submitButton.dataset.defaultText || 'Send Invitation';
            }
        });
    }
}); 