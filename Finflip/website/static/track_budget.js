document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling
    const budgetForm = document.querySelector('form');
    
    if (budgetForm) {
        budgetForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent the form from submitting
            
            // Get form inputs
            const monthlyBudget = document.querySelector('#monthly_budget').value;
            
            // Basic form validation
            if (monthlyBudget.trim() === '') {
                alert('Please enter your monthly budget');
                return;
            }

            // Log the form data for debugging
            console.log('Form submitted:', { monthlyBudget });

            // Allow form submission after validation
            budgetForm.submit();
        });
    }
});
