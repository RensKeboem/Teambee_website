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
            <div class="flex items-center justify-between px-4 py-3 bg-white border-t border-gray-200 sm:px-6">
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
                const searchCell = this.tableType === 'users' ? row.cells[1] : row.cells[1]; // Email for users, Name for clubs
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
}); 