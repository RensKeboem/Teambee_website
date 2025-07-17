document.addEventListener('DOMContentLoaded', function() {
    // Handle URL parameters for success/error messages
    const urlParams = new URLSearchParams(window.location.search);
    const successParam = urlParams.get('success');
    const errorParam = urlParams.get('error');
    
    const successDiv = document.getElementById('club-success');
    const errorDiv = document.getElementById('club-error');
    
    if (successParam === 'club_created') {
        successDiv.innerHTML = `
            <strong>Success!</strong> Club created successfully.<br>
            <div class="mt-2 text-xs text-gray-600">
                You can now send registration invitations from the Clubs tab using the "Send Invitation" button.
            </div>
        `;
        successDiv.classList.remove('hidden');
        
        // Clear form
        const nameField = document.getElementById('name');
        const systemPrefixField = document.getElementById('system_prefix');
        const languageField = document.getElementById('language');
        const languageDisplay = document.getElementById('language-display');
        
        if (nameField) nameField.value = '';
        if (systemPrefixField) systemPrefixField.value = '';
        if (languageField) languageField.value = 'nl';
        if (languageDisplay) languageDisplay.textContent = 'Dutch';
        
        // Scroll to top to show message
        successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else if (errorParam) {
        let errorMessage = 'An error occurred while creating the club.';
        
        switch (errorParam) {
            case 'auth_not_available':
                errorMessage = 'Authentication service is not available.';
                break;
            case 'missing_fields':
                errorMessage = 'All fields are required.';
                break;
            case 'unexpected_error':
                errorMessage = 'An unexpected error occurred. Please try again.';
                break;
            default:
                errorMessage = decodeURIComponent(errorParam.replace(/_/g, ' '));
        }
        
        errorDiv.innerHTML = `<strong>Error:</strong> ${errorMessage}`;
        errorDiv.classList.remove('hidden');
        
        // Scroll to top to show message
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // Form submission handling
    const form = document.querySelector('form[role="form"]');
    const submitBtn = document.getElementById('club-submit-btn');
    
    if (form && submitBtn) {
        form.addEventListener('submit', function() {
            // Hide any existing messages
            if (successDiv) successDiv.classList.add('hidden');
            if (errorDiv) errorDiv.classList.add('hidden');
            
            // Disable submit button and show loading state
            submitBtn.disabled = true;
            submitBtn.textContent = 'Creating Club...';
        });
    }
    
    // Clear URL parameters after processing
    if (successParam || errorParam) {
        const url = new URL(window.location);
        url.searchParams.delete('success');
        url.searchParams.delete('error');
        window.history.replaceState({}, document.title, url.pathname);
    }
}); 