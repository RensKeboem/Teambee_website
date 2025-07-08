// Auto-open success stories panel for direct links
document.addEventListener('DOMContentLoaded', function() {
    // Check if we should auto-open success stories based on a data attribute
    const autoOpenElement = document.querySelector('[data-auto-open-success-stories]');
    
    if (autoOpenElement) {
        const targetUrl = autoOpenElement.getAttribute('data-target-url');
        
        // Wait a bit for all other scripts to load
        setTimeout(function() {
            const showStoriesBtn = document.getElementById('show-success-stories');
            if (showStoriesBtn) {
                showStoriesBtn.click();
            }
            
            // Update the URL to show the target path without triggering a navigation
            if (window.history && window.history.replaceState && targetUrl) {
                window.history.replaceState(null, '', targetUrl);
            }
        }, 100);
    }
}); 