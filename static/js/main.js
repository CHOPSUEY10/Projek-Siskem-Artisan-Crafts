// Main JavaScript for Artisan Crafts

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap tooltip is available
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (window.bootstrap && window.bootstrap.Tooltip) {
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Initialize popovers if Bootstrap popover is available
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    if (window.bootstrap && window.bootstrap.Popover) {
        var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert && alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('a[href*="add-to-cart"]');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add visual feedback
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Adding...';
            this.classList.add('disabled');
            
            // Reset after a short delay (the page will redirect anyway)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.classList.remove('disabled');
            }, 1000);
        });
    });

    // Quantity controls enhancement
    const quantityControls = document.querySelectorAll('.quantity-controls');
    quantityControls.forEach(control => {
        const minusBtn = control.querySelector('a[href*="remove-single-item"]');
        const plusBtn = control.querySelector('a[href*="add-to-cart"]');
        
        if (minusBtn) {
            minusBtn.addEventListener('click', function(e) {
                this.classList.add('btn-outline-danger');
                setTimeout(() => {
                    this.classList.remove('btn-outline-danger');
                }, 200);
            });
        }
        
        if (plusBtn) {
            plusBtn.addEventListener('click', function(e) {
                this.classList.add('btn-outline-success');
                setTimeout(() => {
                    this.classList.remove('btn-outline-success');
                }, 200);
            });
        }
    });

    // Price filter form enhancement
    const priceFilterForm = document.querySelector('.price-filter-form');
    if (priceFilterForm) {
        const minPriceInput = priceFilterForm.querySelector('#min_price');
        const maxPriceInput = priceFilterForm.querySelector('#max_price');
        
        function validatePriceRange() {
            const minPrice = parseFloat(minPriceInput.value) || 0;
            const maxPrice = parseFloat(maxPriceInput.value) || Infinity;
            
            if (minPrice > maxPrice && maxPrice !== Infinity) {
                maxPriceInput.setCustomValidity('Maximum price must be greater than minimum price');
            } else {
                maxPriceInput.setCustomValidity('');
            }
        }
        
        if (minPriceInput && maxPriceInput) {
            minPriceInput.addEventListener('input', validatePriceRange);
            maxPriceInput.addEventListener('input', validatePriceRange);
        }
    }

    // Search functionality (if search input exists)
    const searchInput = document.querySelector('#searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Implement search functionality here
                console.log('Searching for:', this.value);
            }, 300);
        });
    }

    // Image lazy loading fallback
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }

    // Newsletter subscription
    const newsletterForm = document.querySelector('form[action*="newsletter"]');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            // Simulate subscription
            const button = this.querySelector('button');
            const originalText = button.textContent;
            button.textContent = 'Subscribing...';
            button.disabled = true;
            
            setTimeout(() => {
                button.textContent = 'Subscribed!';
                button.classList.remove('btn-primary');
                button.classList.add('btn-success');
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('btn-success');
                    button.classList.add('btn-primary');
                    button.disabled = false;
                    this.reset();
                }, 2000);
            }, 1000);
        });
    }

    // Cart count animation
    function animateCartCount() {
        const cartBadge = document.querySelector('.navbar .badge');
        if (cartBadge) {
            cartBadge.style.transform = 'scale(1.2)';
            setTimeout(() => {
                cartBadge.style.transform = 'scale(1)';
            }, 200);
        }
    }

    // Product card hover effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Category card hover effects
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1.1)';
                icon.style.transition = 'transform 0.3s ease';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1)';
            }
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton && this.checkValidity()) {
                const originalText = submitButton.textContent;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitButton.disabled = true;
                
                // Re-enable button after form submission (in case of validation errors)
                setTimeout(() => {
                    if (submitButton.disabled) {
                        submitButton.textContent = originalText;
                        submitButton.disabled = false;
                    }
                }, 5000);
            }
        });
    });
});

// Utility functions
function showToast(message, type = 'info') {
    // Create a simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.style.minWidth = '300px';
    
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

// Export for use in other scripts
window.ArtisanCrafts = {
    showToast,
    formatPrice
};
