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

    // Form submission handling
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the form from submitting

            // Get form inputs
            const email = document.querySelector('#email').value;
            const password = document.querySelector('#password').value;

            // Basic form validation
            if (email.trim() === '' || password.trim() === '') {
                alert('Please fill in all fields');
                return;
            }

            // Here you would typically send the form data to your server
            // For this example, we'll just log it to the console
            console.log('Form submitted:', { email, password });

            // Clear the form
            loginForm.reset();
        });
    }

    // Password visibility toggle
    const passwordInput = document.querySelector('#password');
    const togglePassword = document.querySelector('#togglePassword');
    
    if (passwordInput && togglePassword) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.classList.toggle('show-password');
        });
    }
});