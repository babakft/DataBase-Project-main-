

document.addEventListener('DOMContentLoaded', function() {
    initDashboard();
    initCounterAnimations();
    initTableInteractions();
    initRealTimeUpdates();
});

function initDashboard() {

    const statsCards = document.querySelectorAll('.stats-card');
    statsCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';

        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });

    // Animate requests table
    const requestsCard = document.querySelector('.requests-card');
    if (requestsCard) {
        requestsCard.style.opacity = '0';
        requestsCard.style.transform = 'translateY(30px)';

        setTimeout(() => {
            requestsCard.style.transition = 'all 0.6s ease';
            requestsCard.style.opacity = '1';
            requestsCard.style.transform = 'translateY(0)';
        }, 600);
    }
}

function initCounterAnimations() {
    const counters = document.querySelectorAll('.stats-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });

    counters.forEach(counter => {
        observer.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.textContent);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

function initTableInteractions() {
    // Add click handlers for table rows
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('click', function(e) {
            // Don't trigger if clicking on buttons
            if (e.target.closest('.btn')) {
                return;
            }

            // Add selection effect
            tableRows.forEach(r => r.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Add sorting functionality to table headers
    const tableHeaders = document.querySelectorAll('.table thead th');
    tableHeaders.forEach((header, index) => {
        if (index < tableHeaders.length - 1) { // Exclude actions column
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => sortTable(index));
        }
    });
}

function sortTable(columnIndex) {
    const table = document.querySelector('.table tbody');
    const rows = Array.from(table.querySelectorAll('tr'));

    // Toggle sort direction
    const header = document.querySelectorAll('.table thead th')[columnIndex];
    const isAscending = !header.classList.contains('sort-desc');

    // Remove sort classes from all headers
    document.querySelectorAll('.table thead th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Add sort class to current header
    header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    // Sort rows
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();

        // Try to compare as numbers first
        const aNum = parseFloat(aText);
        const bNum = parseFloat(bText);

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        }

        // Compare as strings
        return isAscending ?
            aText.localeCompare(bText, 'fa') :
            bText.localeCompare(aText, 'fa');
    });

    // Re-append sorted rows
    rows.forEach(row => table.appendChild(row));
}

function initRealTimeUpdates() {
    // Check for updates every 30 seconds
    setInterval(checkForUpdates, 30000);
}

function checkForUpdates() {
    // This would typically make an AJAX request to check for new data
    // For now, we'll just show a subtle indicator that we're checking
    const indicator = document.createElement('div');
    indicator.className = 'update-indicator';
    indicator.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i>';
    indicator.style.cssText = `
        position: fixed;
        top: 20px;
        left: 20px;
        background: rgba(99, 102, 241, 0.9);
        color: white;
        padding: 0.5rem;
        border-radius: 50%;
        z-index: 9999;
        font-size: 0.8rem;
    `;

    document.body.appendChild(indicator);

    setTimeout(() => {
        indicator.remove();
    }, 2000);
}

// Utility functions for dashboard
const Dashboard = {
    // Show notification
    showNotification: function(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} position-fixed`;
        notification.style.cssText = `
            top: 100px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            animation: slideInRight 0.3s ease;
        `;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close float-end" onclick="this.parentElement.remove()"></button>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
    },

    // Refresh stats
    refreshStats: function() {
        // This would make an AJAX request to get updated statistics
        this.showNotification('آمار به‌روزرسانی شد', 'success');
    },

    // Filter requests by status
    filterRequests: function(status) {
        const rows = document.querySelectorAll('.table tbody tr');
        rows.forEach(row => {
            const statusCell = row.cells[3]; // Status column
            if (status === 'all' || statusCell.textContent.includes(status)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
};

// Add CSS for sorting indicators
const sortingStyles = document.createElement('style');
sortingStyles.textContent = `
    .table thead th.sort-asc::after {
        content: ' ↑';
        color: #6366f1;
    }

    .table thead th.sort-desc::after {
        content: ' ↓';
        color: #6366f1;
    }

    .table tbody tr.selected {
        background: rgba(99, 102, 241, 0.2) !important;
    }

    .table tbody tr {
        transition: all 0.3s ease;
    }

    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .update-indicator {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
`;
document.head.appendChild(sortingStyles);

// Add filter buttons to the dashboard
function addFilterButtons() {
    const cardHeader = document.querySelector('.requests-card .card-header');
    if (cardHeader) {
        const filterContainer = document.createElement('div');
        filterContainer.className = 'filter-buttons';
        filterContainer.innerHTML = `
            <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-outline-light active" onclick="Dashboard.filterRequests('all')">همه</button>
                <button type="button" class="btn btn-outline-warning" onclick="Dashboard.filterRequests('در انتظار')">در انتظار</button>
                <button type="button" class="btn btn-outline-primary" onclick="Dashboard.filterRequests('در حال انجام')">در حال انجام</button>
                <button type="button" class="btn btn-outline-success" onclick="Dashboard.filterRequests('تکمیل شده')">تکمیل شده</button>
            </div>
        `;

        // Insert filter buttons before the "new request" button
        const newRequestBtn = cardHeader.querySelector('.btn-success');
        if (newRequestBtn) {
            cardHeader.insertBefore(filterContainer, newRequestBtn);
        } else {
            cardHeader.appendChild(filterContainer);
        }

        // Add click handlers for filter buttons
        const filterButtons = filterContainer.querySelectorAll('.btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                filterButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
}

// Add search functionality
function addSearchBox() {
    const cardHeader = document.querySelector('.requests-card .card-header');
    if (cardHeader) {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        searchContainer.innerHTML = `
            <div class="input-group input-group-sm" style="width: 250px;">
                <input type="text" class="form-control" placeholder="جستجو در درخواست‌ها..." id="requestSearch">
                <button class="btn btn-outline-secondary" type="button" onclick="clearSearch()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        cardHeader.appendChild(searchContainer);

        // Add search functionality
        const searchInput = searchContainer.querySelector('#requestSearch');
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.table tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
}

function clearSearch() {
    const searchInput = document.getElementById('requestSearch');
    if (searchInput) {
        searchInput.value = '';
        const event = new Event('input');
        searchInput.dispatchEvent(event);
    }
}

// Initialize additional features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add filter and search after a short delay to ensure DOM is fully loaded
    setTimeout(() => {
        addFilterButtons();
        addSearchBox();
    }, 500);
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R to refresh stats
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        Dashboard.refreshStats();
    }

    // Ctrl/Cmd + F to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const searchInput = document.getElementById('requestSearch');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// Add tooltip functionality
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Export dashboard utilities for global use
window.Dashboard = Dashboard;