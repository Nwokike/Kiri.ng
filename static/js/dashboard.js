// academy/static/academy/js/dashboard.js

// Function to copy the user's referral code to the clipboard
function copyReferralCode() {
    const referralCodeInput = document.getElementById('referralCode');
    referralCodeInput.select();
    document.execCommand('copy');
    alert("Referral code copied to clipboard!"); // Simple alert for user feedback
}

// Initialize Bootstrap tooltips when the page loads
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});