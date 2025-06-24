// Admin search functionality for users and clubs tables

// Search function for users
function filterUsers(searchTerm) {
    const rows = document.querySelectorAll('.user-row');
    const noResultsDiv = document.getElementById('no-users-found');
    const tbody = document.getElementById('users-tbody');
    let visibleCount = 0;
    
    searchTerm = searchTerm.toLowerCase().trim();
    
    rows.forEach(row => {
        const emailCell = row.cells[1]; // Email is in the second column (index 1)
        const email = emailCell.textContent.toLowerCase();
        
        if (searchTerm === '' || email.includes(searchTerm)) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    // Show/hide no results message
    if (visibleCount === 0 && searchTerm !== '') {
        if (noResultsDiv) noResultsDiv.classList.remove('hidden');
        if (tbody) tbody.style.display = 'none';
    } else {
        if (noResultsDiv) noResultsDiv.classList.add('hidden');
        if (tbody) tbody.style.display = '';
    }
}

// Search function for clubs
function filterClubs(searchTerm) {
    const rows = document.querySelectorAll('.club-row');
    const noResultsDiv = document.getElementById('no-clubs-found');
    const tbody = document.getElementById('clubs-tbody');
    let visibleCount = 0;
    
    searchTerm = searchTerm.toLowerCase().trim();
    
    rows.forEach(row => {
        const nameCell = row.cells[1]; // Club name is in the second column (index 1)
        const clubName = nameCell.textContent.toLowerCase();
        
        if (searchTerm === '' || clubName.includes(searchTerm)) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    // Show/hide no results message
    if (visibleCount === 0 && searchTerm !== '') {
        if (noResultsDiv) noResultsDiv.classList.remove('hidden');
        if (tbody) tbody.style.display = 'none';
    } else {
        if (noResultsDiv) noResultsDiv.classList.add('hidden');
        if (tbody) tbody.style.display = '';
    }
}

// Initialize search functionality when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Set up user search
    const userSearch = document.getElementById('user-search');
    if (userSearch) {
        userSearch.addEventListener('input', function(event) {
            filterUsers(event.target.value);
        });
    }
    
    // Set up club search
    const clubSearch = document.getElementById('club-search');
    if (clubSearch) {
        clubSearch.addEventListener('input', function(event) {
            filterClubs(event.target.value);
        });
    }
}); 