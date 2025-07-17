// Admin search and pagination functionality for users and clubs tables

class TablePagination {
    constructor(tableType, rowSelector, itemsPerPage = 10) {
        this.tableType = tableType;
        this.rowSelector = rowSelector;
        this.itemsPerPage = itemsPerPage;
        this.currentPage = 1;
        this.allRows = [];
        this.filteredRows = [];
        this.searchTerm = '';
        
        this.init();
    }
    
    init() {
        this.allRows = Array.from(document.querySelectorAll(this.rowSelector));
        this.filteredRows = [...this.allRows];
        this.createPaginationControls();
        this.updateDisplay();
    }
    
    createPaginationControls() {
        const container = document.getElementById(`${this.tableType}-pagination-container`);
        if (!container) return;
        
        container.innerHTML = `
            <div class="flex items-center justify-center px-4 py-3 bg-white border-t border-gray-200 sm:px-6">
                <div class="flex justify-between flex-1 sm:hidden">
                    <button id="${this.tableType}-prev-mobile" class="relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2">
                            <path d="m15 18-6-6 6-6"/>
                        </svg>
                        Previous
                    </button>
                    <button id="${this.tableType}-next-mobile" class="relative ml-3 inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                        Next
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ml-2">
                            <path d="m9 18 6-6-6-6"/>
                        </svg>
                    </button>
                </div>
                <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                    <div>
                        <p class="text-sm text-gray-700">
                            Showing <span id="${this.tableType}-start">0</span>-<span id="${this.tableType}-end">0</span> of <span id="${this.tableType}-total">0</span> results
                        </p>
                    </div>
                    <div>
                        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                            <button id="${this.tableType}-prev" class="relative inline-flex items-center px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-l-md hover:bg-gray-50">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="m15 18-6-6 6-6"/>
                                </svg>
                            </button>
                            <div id="${this.tableType}-page-numbers" class="flex"></div>
                            <button id="${this.tableType}-next" class="relative inline-flex items-center px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-r-md hover:bg-gray-50">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="m9 18 6-6-6-6"/>
                                </svg>
                            </button>
                        </nav>
                    </div>
                </div>
            </div>
        `;
        
        this.bindPaginationEvents();
    }
    
    bindPaginationEvents() {
        // Previous buttons
        document.getElementById(`${this.tableType}-prev`)?.addEventListener('click', () => this.goToPage(this.currentPage - 1));
        document.getElementById(`${this.tableType}-prev-mobile`)?.addEventListener('click', () => this.goToPage(this.currentPage - 1));
        
        // Next buttons  
        document.getElementById(`${this.tableType}-next`)?.addEventListener('click', () => this.goToPage(this.currentPage + 1));
        document.getElementById(`${this.tableType}-next-mobile`)?.addEventListener('click', () => this.goToPage(this.currentPage + 1));
    }
    
    filter(searchTerm) {
        this.searchTerm = searchTerm.toLowerCase().trim();
        
        if (this.searchTerm === '') {
            this.filteredRows = [...this.allRows];
        } else {
            this.filteredRows = this.allRows.filter(row => {
                const searchCell = row.cells[0]; // Email for users, Name for clubs (both now at index 0)
                const text = searchCell.textContent.toLowerCase();
                return text.includes(this.searchTerm);
            });
        }
        
        this.currentPage = 1; // Reset to first page when filtering
        this.updateDisplay();
    }
    
    goToPage(page) {
        const totalPages = Math.ceil(this.filteredRows.length / this.itemsPerPage);
        if (page < 1 || page > totalPages) return;
        
        this.currentPage = page;
        this.updateDisplay();
    }
    
    updateDisplay() {
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const totalPages = Math.ceil(this.filteredRows.length / this.itemsPerPage);
        
        // Hide all rows first
        this.allRows.forEach(row => row.style.display = 'none');
        
        // Show current page rows
        const currentPageRows = this.filteredRows.slice(startIndex, endIndex);
        currentPageRows.forEach(row => row.style.display = '');
        
        // Update pagination info
        const start = this.filteredRows.length > 0 ? startIndex + 1 : 0;
        const end = Math.min(endIndex, this.filteredRows.length);
        
        const startEl = document.getElementById(`${this.tableType}-start`);
        const endEl = document.getElementById(`${this.tableType}-end`);
        const totalEl = document.getElementById(`${this.tableType}-total`);
        
        if (startEl) startEl.textContent = start;
        if (endEl) endEl.textContent = end;
        if (totalEl) totalEl.textContent = this.filteredRows.length;
        
        // Update page numbers
        this.updatePageNumbers(totalPages);
        
        // Update button states
        this.updateButtonStates(totalPages);
        
        // Handle no results
        this.handleNoResults();
    }
    
    updatePageNumbers(totalPages) {
        const pageNumbersContainer = document.getElementById(`${this.tableType}-page-numbers`);
        if (!pageNumbersContainer) return;
        
        pageNumbersContainer.innerHTML = '';
        
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            button.className = i === this.currentPage 
                ? 'relative inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#3D2E7C] border border-[#3D2E7C]'
                : 'relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50';
            
            button.addEventListener('click', () => this.goToPage(i));
            pageNumbersContainer.appendChild(button);
        }
    }
    
    updateButtonStates(totalPages) {
        const prevButtons = [
            document.getElementById(`${this.tableType}-prev`),
            document.getElementById(`${this.tableType}-prev-mobile`)
        ];
        const nextButtons = [
            document.getElementById(`${this.tableType}-next`),
            document.getElementById(`${this.tableType}-next-mobile`)
        ];
        
        prevButtons.forEach(btn => {
            if (btn) {
                btn.disabled = this.currentPage === 1;
                btn.className = btn.className.replace(/opacity-50|cursor-not-allowed/g, '');
                if (btn.disabled) {
                    btn.className += ' opacity-50 cursor-not-allowed';
                }
            }
        });
        
        nextButtons.forEach(btn => {
            if (btn) {
                btn.disabled = this.currentPage === totalPages || totalPages === 0;
                btn.className = btn.className.replace(/opacity-50|cursor-not-allowed/g, '');
                if (btn.disabled) {
                    btn.className += ' opacity-50 cursor-not-allowed';
                }
            }
        });
    }
    
    handleNoResults() {
        const noResultsDiv = document.getElementById(`no-${this.tableType}-found`);
        const tbody = document.getElementById(`${this.tableType}-tbody`);
        
        if (this.filteredRows.length === 0 && this.searchTerm !== '') {
            if (noResultsDiv) noResultsDiv.classList.remove('hidden');
            if (tbody) tbody.style.display = 'none';
        } else {
            if (noResultsDiv) noResultsDiv.classList.add('hidden');
            if (tbody) tbody.style.display = '';
        }
    }
}

// Global pagination instances
let usersPagination;
let clubsPagination;

// Admin invite popup functionality
function openAdminInvitePopup(button) {
    const clubId = button.getAttribute('data-club-id');
    const clubName = button.getAttribute('data-club-name');
    
    const popup = document.getElementById('admin-invite-popup');
    const clubIdInput = document.getElementById('admin_invite_club_id');
    const emailInput = document.getElementById('admin_invite_email');
    const title = document.getElementById('admin-invite-form-title');
    const subtitle = document.getElementById('admin-invite-form-subtitle');
    
    if (!popup || !clubIdInput || !emailInput) return;
    
    // Set club ID
    clubIdInput.value = clubId;
    
    // Update title and subtitle with club name
    if (title) title.textContent = `Send Registration Link for ${clubName}`;
    if (subtitle) subtitle.textContent = `Enter the email address where the registration link for ${clubName} should be sent.`;
    
    // Clear previous values and messages
    emailInput.value = '';
    const errorDiv = document.getElementById('admin-invite-error');
    const successDiv = document.getElementById('admin-invite-success');
    if (errorDiv) errorDiv.classList.add('hidden');
    if (successDiv) successDiv.classList.add('hidden');
    
    // Show popup
    TeambeeUtils.disableScroll();
    popup.classList.remove('hidden');
    
    setTimeout(() => {
        const modalContent = popup.querySelector('.bg-white');
        if (modalContent) {
            modalContent.style.transform = 'scale(1)';
            modalContent.style.opacity = '1';
        }
    }, 10);
    
    // Focus email input and setup validation
    setTimeout(() => {
        emailInput.focus();
        validateAdminInviteForm();
    }, 100);
}

function closeAdminInvitePopup() {
    const popup = document.getElementById('admin-invite-popup');
    if (!popup) return;
    
    const modalContent = popup.querySelector('.bg-white');
    if (modalContent) {
        modalContent.style.transform = 'scale(0.95)';
        modalContent.style.opacity = '0';
    }
    
    setTimeout(() => {
        popup.classList.add('hidden');
        TeambeeUtils.enableScroll();
        
        // Reset form
        const form = document.getElementById('admin-invite-form');
        if (form) {
            form.reset();
            const errorDiv = document.getElementById('admin-invite-error');
            const successDiv = document.getElementById('admin-invite-success');
            if (errorDiv) errorDiv.classList.add('hidden');
            if (successDiv) successDiv.classList.add('hidden');
            setTimeout(validateAdminInviteForm, 10);
        }
    }, 200);
}

function validateAdminInviteForm() {
    const emailInput = document.getElementById('admin_invite_email');
    const submitBtn = document.getElementById('admin-invite-submit-btn');
    
    if (!emailInput || !submitBtn) return;
    
    const email = emailInput.value.trim();
    const isEmailValid = TeambeeUtils.validateEmail(email);
    
    // Update submit button state
    submitBtn.disabled = !isEmailValid;
    if (isEmailValid) {
        submitBtn.classList.remove('bg-gray-400', 'cursor-not-allowed');
        submitBtn.classList.add('bg-[#3D2E7C]', 'hover:bg-[#3D2E7C]/90');
    } else {
        submitBtn.classList.add('bg-gray-400', 'cursor-not-allowed');
        submitBtn.classList.remove('bg-[#3D2E7C]', 'hover:bg-[#3D2E7C]/90');
    }
    
    // Email field visual feedback
    if (email && !isEmailValid) {
        emailInput.classList.add('border-red-500');
        emailInput.classList.remove('border-gray-300');
    } else {
        emailInput.classList.remove('border-red-500');
        emailInput.classList.add('border-gray-300');
    }
}

// Initialize search and pagination functionality when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize users pagination if users table exists
    if (document.getElementById('users-tbody')) {
        usersPagination = new TablePagination('users', '.user-row', 10);
        
        // Set up user search
        const userSearch = document.getElementById('user-search');
        if (userSearch) {
            userSearch.addEventListener('input', function(event) {
                usersPagination.filter(event.target.value);
            });
        }
    }
    
    // Initialize clubs pagination if clubs table exists
    if (document.getElementById('clubs-tbody')) {
        clubsPagination = new TablePagination('clubs', '.club-row', 10);
        
        // Set up club search
        const clubSearch = document.getElementById('club-search');
        if (clubSearch) {
            clubSearch.addEventListener('input', function(event) {
                clubsPagination.filter(event.target.value);
            });
        }
    }
    
    // Setup admin invite popup functionality
    const adminInvitePopup = document.getElementById('admin-invite-popup');
    const adminInviteForm = document.getElementById('admin-invite-form');
    const closeAdminInviteBtn = document.getElementById('close-admin-invite-popup');
    
    // Setup click handlers for invite trigger buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('admin-invite-trigger')) {
            e.preventDefault();
            openAdminInvitePopup(e.target);
        }
    });
    
    if (adminInvitePopup && adminInviteForm) {
        // Setup close button
        if (closeAdminInviteBtn) {
            closeAdminInviteBtn.addEventListener('click', function(e) {
                e.preventDefault();
                closeAdminInvitePopup();
            });
        }
        
        // Close popup when clicking outside
        adminInvitePopup.addEventListener('click', function(e) {
            if (e.target === adminInvitePopup || e.target.classList.contains('backdrop-blur-sm')) {
                closeAdminInvitePopup();
            }
        });
        
        // Close popup when pressing Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && adminInvitePopup && !adminInvitePopup.classList.contains('hidden')) {
                closeAdminInvitePopup();
            }
        });
        
        // Setup form validation
        const emailInput = document.getElementById('admin_invite_email');
        if (emailInput) {
            emailInput.addEventListener('input', validateAdminInviteForm);
            emailInput.addEventListener('blur', validateAdminInviteForm);
        }
        
        // Setup form submission
        adminInviteForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('admin-invite-submit-btn');
            const buttonText = document.getElementById('admin-invite-button-text');
            const buttonLoading = document.getElementById('admin-invite-button-loading');
            const errorDiv = document.getElementById('admin-invite-error');
            const successDiv = document.getElementById('admin-invite-success');
            
            if (!submitBtn || !buttonText || !buttonLoading) return;
            
            // Hide previous messages
            if (errorDiv) errorDiv.classList.add('hidden');
            if (successDiv) successDiv.classList.add('hidden');
            
            // Show loading state
            submitBtn.disabled = true;
            buttonText.classList.add('hidden');
            buttonLoading.classList.remove('hidden');
            
            try {
                const formData = new FormData(adminInviteForm);
                
                const response = await fetch('/admin/send-registration-link', {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    if (successDiv) {
                        successDiv.textContent = result.message;
                        successDiv.classList.remove('hidden');
                    }
                    // Auto-close popup after 3 seconds
                    setTimeout(closeAdminInvitePopup, 3000);
                } else {
                    if (errorDiv) {
                        errorDiv.textContent = result.message;
                        errorDiv.classList.remove('hidden');
                    }
                }
            } catch (error) {
                console.error('Admin invite form error:', error);
                if (errorDiv) {
                    errorDiv.textContent = 'Network error. Please check your connection and try again.';
                    errorDiv.classList.remove('hidden');
                }
            } finally {
                buttonText.classList.remove('hidden');
                buttonLoading.classList.add('hidden');
                validateAdminInviteForm();
            }
        });
        
        // Initial validation
        validateAdminInviteForm();
    }
    
    // Delete confirmation popup functionality
    setupDeleteConfirmation();
});

// Delete confirmation popup functionality
function setupDeleteConfirmation() {
    const deletePopup = document.getElementById('delete-confirmation-popup');
    const closeDeleteBtn = document.getElementById('close-delete-popup');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const deleteUserEmail = document.getElementById('delete-user-email');
    
    if (!deletePopup) return;
    
    let currentDeleteData = null;
    
    // Show delete confirmation popup
    function showDeletePopup(userData) {
        currentDeleteData = userData;
        
        // Update popup content
        if (deleteUserEmail) {
            deleteUserEmail.textContent = userData.email;
        }
        
        // Show popup
        TeambeeUtils.disableScroll();
        deletePopup.classList.remove('hidden');
        
        setTimeout(() => {
            const modalContent = deletePopup.querySelector('.bg-white');
            if (modalContent) {
                modalContent.style.transform = 'scale(1)';
                modalContent.style.opacity = '1';
            }
        }, 10);
        
        // Focus the cancel button for accessibility
        setTimeout(() => {
            if (cancelDeleteBtn) cancelDeleteBtn.focus();
        }, 100);
    }
    
    // Hide delete confirmation popup
    function hideDeletePopup() {
        const modalContent = deletePopup.querySelector('.bg-white');
        if (modalContent) {
            modalContent.style.transform = 'scale(0.95)';
            modalContent.style.opacity = '0';
        }
        
        setTimeout(() => {
            deletePopup.classList.add('hidden');
            TeambeeUtils.enableScroll();
            currentDeleteData = null;
        }, 200);
    }
    
    // Handle delete button clicks
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-user-btn')) {
            e.preventDefault();
            
            const userId = e.target.getAttribute('data-user-id');
            const userEmail = e.target.getAttribute('data-user-email');
            
            if (userId && userEmail) {
                showDeletePopup({
                    id: userId,
                    email: userEmail,
                    button: e.target
                });
            }
        }
    });
    
    // Handle confirm delete
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', async function() {
            if (!currentDeleteData) return;
            
            // Disable button and show loading state
            confirmDeleteBtn.disabled = true;
            confirmDeleteBtn.textContent = 'Deleting...';
            
            try {
                const response = await fetch(`/admin/delete-user/${currentDeleteData.id}`, {
                    method: 'POST',
                    headers: {
                        'HX-Request': 'true'
                    }
                });
                
                if (response.ok) {
                    const result = await response.text();
                    
                    if (result.trim() === '') {
                        // Success - remove the table row
                        const tableRow = currentDeleteData.button.closest('tr');
                        if (tableRow) {
                            tableRow.remove();
                        }
                        hideDeletePopup();
                    } else {
                        // Error - show error message
                        console.error('Delete failed:', result);
                        alert('Failed to delete user. Please try again.');
                    }
                } else {
                    console.error('Delete request failed:', response.statusText);
                    alert('Failed to delete user. Please try again.');
                }
            } catch (error) {
                console.error('Delete error:', error);
                alert('Network error. Please try again.');
            } finally {
                // Reset button state
                confirmDeleteBtn.disabled = false;
                confirmDeleteBtn.textContent = 'Delete User';
            }
        });
    }
    
    // Handle close/cancel buttons
    [closeDeleteBtn, cancelDeleteBtn].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                hideDeletePopup();
            });
        }
    });
    
    // Close popup when clicking outside
    deletePopup.addEventListener('click', function(e) {
        if (e.target === deletePopup || e.target.classList.contains('backdrop-blur-sm')) {
            hideDeletePopup();
        }
    });
    
    // Close popup when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && deletePopup && !deletePopup.classList.contains('hidden')) {
            hideDeletePopup();
        }
    });
} 