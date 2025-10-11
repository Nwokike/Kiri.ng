// academy/static/academy/js/dashboard.js

// Function to copy the user's referral code to the clipboard using modern Clipboard API
function copyReferralCode() {
    const referralCodeInput = document.getElementById('referralCode');
    const referralCode = referralCodeInput.value;
    
    // Check if modern Clipboard API is available (HTTPS required)
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(referralCode)
            .then(() => {
                alert("Referral code copied to clipboard!");
            })
            .catch(() => {
                // Fallback if clipboard API fails
                fallbackCopy(referralCodeInput);
            });
    } else {
        // Fallback for older browsers or non-HTTPS contexts
        fallbackCopy(referralCodeInput);
    }
}

// Fallback copy function
function fallbackCopy(inputElement) {
    inputElement.select();
    inputElement.setSelectionRange(0, 99999); // For mobile devices
    try {
        document.execCommand('copy');
        alert("Referral code copied to clipboard!");
    } catch (err) {
        alert("Failed to copy. Please select and copy manually.");
    }
}

// Function to show the referral code
function showReferralCode() {
    const section = document.getElementById('referralCodeSection');
    const btn = document.getElementById('generateReferralBtn');
    section.style.display = 'block';
    btn.style.display = 'none';
}

// Initialize Bootstrap tooltips when the page loads
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});