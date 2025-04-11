document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('language-dropdown-button');
    const menu = document.getElementById('language-dropdown-menu');
    
    if (button && menu) {
        // Toggle dropdown when button is clicked
        button.addEventListener('click', function(event) {
            event.stopPropagation(); // Stop event from bubbling up
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
}); 