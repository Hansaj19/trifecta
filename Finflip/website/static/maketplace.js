// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuToggle = document.querySelector('.toggle-btn');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
        });
    }

    // Confirm deletion of products
    const deleteForms = document.querySelectorAll('form[action*="delete_product"]');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const confirmed = confirm('Are you sure you want to remove this product?');
            if (!confirmed) {
                e.preventDefault(); // Prevent form submission if not confirmed
            }
        });
    });

    // Optional: Log action or perform additional tasks
    // For example, you could log product actions
    const productCards = document.querySelectorAll('.card');

    productCards.forEach(card => {
        card.addEventListener('click', function() {
            const productTitle = card.querySelector('.card-title').innerText;
            console.log(`Product clicked: ${productTitle}`);
            // You can add more actions here, like redirecting to a product detail page
        });
    });
});
