// Wait for the DOM to load before running the script
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const categorySelect = document.getElementById('category');
    const amountInput = document.getElementById('amount');
    
    const budgetExceededAlert = document.querySelector('.alert-danger');
    const warningRecommendation = document.querySelector('.alert-warning');

    // Add form submission handler
    form.addEventListener('submit', function(event) {
        // Check if category and amount are selected and valid
        if (!categorySelect.value) {
            alert("Please select a category.");
            event.preventDefault();
        }
        
        if (amountInput.value <= 0) {
            alert("Please enter a valid amount.");
            event.preventDefault();
        }
    });

    // Example: Budget check before submission (this can be updated with actual values from your backend)
    const budgetLimit = 1000; // Example budget limit (replace with actual value from the server)
    let totalSpending = 950; // Example current spending (replace with actual value)

    amountInput.addEventListener('input', function() {
        const enteredAmount = parseFloat(amountInput.value);
        
        if (!isNaN(enteredAmount) && (totalSpending + enteredAmount) > budgetLimit) {
            budgetExceededAlert.style.display = 'block';
            warningRecommendation.style.display = 'block';
        } else {
            budgetExceededAlert.style.display = 'none';
            warningRecommendation.style.display = 'none';
        }
    });
});
