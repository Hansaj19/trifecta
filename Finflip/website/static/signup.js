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
    const signupForm = document.querySelector('form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the form from submitting

            // Get form inputs
            const email = document.querySelector('#email').value;
            const firstName = document.querySelector('#firstName').value;
            const password1 = document.querySelector('#password1').value;
            const password2 = document.querySelector('#password2').value;

            // Basic form validation
            if (email.trim() === '' || firstName.trim() === '' || password1.trim() === '' || password2.trim() === '') {
                alert('Please fill in all fields');
                return;
            }

            if (password1 !== password2) {
                alert('Passwords do not match');
                return;
            }

            // Here you would typically send the form data to your server
            // For this example, we'll just log it to the console
            console.log('Form submitted:', { email, firstName, password: password1 });

            // Clear the form
            signupForm.reset();
        });
    }

    // Password visibility toggle for password inputs
    const passwordInputs = [document.querySelector('#password1'), document.querySelector('#password2')];
    const toggleButtons = [document.querySelector('#togglePassword1'), document.querySelector('#togglePassword2')];

    toggleButtons.forEach((toggle, index) => {
        if (passwordInputs[index] && toggle) {
            toggle.addEventListener('click', function() {
                const type = passwordInputs[index].getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInputs[index].setAttribute('type', type);
                this.classList.toggle('show-password');
            });
        }
    });
});
