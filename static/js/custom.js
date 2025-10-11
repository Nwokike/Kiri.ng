// =============================
// PWA Install Button Logic
// =============================
let deferredPrompt;
const installButton = document.getElementById('pwa-install-btn');

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (installButton) installButton.style.display = 'block';
});

if (installButton) {
    installButton.addEventListener('click', async () => {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        deferredPrompt = null;
        installButton.style.display = 'none';
    });
}

window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    if (installButton) installButton.style.display = 'none';
});


// =============================
// Push Notifications
// =============================
function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

function requestNotificationPermission() {
    if (!('Notification' in window)) {
        console.log('This browser does not support notifications');
        return;
    }
    
    if (Notification.permission === 'granted') {
        subscribeToPushNotifications();
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                subscribeToPushNotifications();
            }
        });
    }
}

function subscribeToPushNotifications() {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
        navigator.serviceWorker.ready.then(registration => {
            const vapidPublicKey = 'BEl62iUYgUivxIkv69yViEuiBIa-Ib9-SkvMeAtA3LFgDhVxRr6-sWBkGGk0kqMG8dUG0gk5cGfE1RmJqzqBQqg';
            
            registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
            }).then(subscription => {
                sendSubscriptionToServer(subscription);
            }).catch(err => {
                console.log('Failed to subscribe:', err);
            });
        });
    }
}

function sendSubscriptionToServer(subscription) {
    fetch('/api/push-subscribe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(subscription)
    }).then(response => {
        if (response.ok) {
            console.log('Push subscription sent to server');
        }
    }).catch(err => {
        console.error('Error sending subscription:', err);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Auto-request notification permission for logged-in users
if (document.querySelector('[data-user-authenticated="true"]')) {
    setTimeout(requestNotificationPermission, 3000);
}


// =============================
// Dark Mode Logic
// =============================
const themeToggle = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme');

if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);
    if (currentTheme === 'dark' && themeToggle) themeToggle.checked = true;
}

if (themeToggle) {
    themeToggle.addEventListener('change', function () {
        const newTheme = this.checked ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}


// =============================
// Google Translate Integration
// =============================
function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,ha,ig,yo',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
    }, 'google_translate_element');
}

// 🚀 ADDED THIS NEW SECTION 🚀
// =============================
// Reusable Referral Code Logic
// =============================
function copyReferralCode() {
    const referralCodeInput = document.getElementById('referralCode');
    
    if (referralCodeInput) {
        const referralCode = referralCodeInput.value;
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(referralCode)
                .then(() => {
                    alert("Referral link copied to clipboard!");
                })
                .catch(() => {
                    fallbackCopy(referralCodeInput);
                });
        } else {
            fallbackCopy(referralCodeInput);
        }
    } else {
        console.error("Could not find element with ID 'referralCode'");
    }
}

function fallbackCopy(inputElement) {
    inputElement.select();
    inputElement.setSelectionRange(0, 99999);
    try {
        document.execCommand('copy');
        alert("Referral link copied to clipboard!");
    } catch (err) {
        alert("Failed to copy. Please select and copy manually.");
    }
}


// =============================
// Main App Logic (after DOM load)
// =============================
document.addEventListener('DOMContentLoaded', function () {

    // ----- Smart Navigation -----
    const path = window.location.pathname;
    const mainHeader = document.getElementById('main-header');
    const subHeaderContainer = document.getElementById('sub-header-container');
    const backButtonContainer = document.getElementById('back-button-container');

    let activeSection = 'services';
    if (path.includes('/academy/')) activeSection = 'academy';
    if (path.includes('/blog/')) activeSection = 'blog';
    if (path.includes('/users/') || path.includes('/profile/')) activeSection = 'profile';
    if (path === '/') activeSection = 'services';

    // Clear existing active states
    document.querySelectorAll('.bottom-nav-item').forEach(item =>
        item.classList.remove('text-primary', 'active')
    );

    // Set current active section
    const activeNavItem = document.querySelector(`[data-nav="${activeSection}"]`);
    if (activeNavItem) activeNavItem.classList.add('text-primary', 'active');

    // ----- Sub-Navigation Rendering -----
    const activeSubNavId = `sub-nav-${activeSection}`;
    const activeSubNavHTML = document.getElementById(activeSubNavId)?.innerHTML;
    if (activeSubNavHTML) {
        subHeaderContainer.innerHTML = activeSubNavHTML;

        // Highlight current sub-nav item
        subHeaderContainer.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === path) link.classList.add('active');
        });
    }

    // ----- Back Button -----
    const mainTabs = ["/marketplace/", "/academy/dashboard/", "/blog/", "/users/profile/"];
    if (!mainTabs.includes(path) && path !== "/") {
        backButtonContainer.innerHTML = `
            <a href="javascript:history.back()" 
               class="btn btn-outline-secondary back-btn">
                <i class="bi bi-arrow-left fs-4"></i>
            </a>`;
    }

    // ----- Dynamic Padding -----
    function adjustPadding() {
        const headerHeight = mainHeader?.offsetHeight || 0;
        const subHeaderHeight = subHeaderContainer?.offsetHeight || 0;
        document.body.style.paddingTop = `${headerHeight + subHeaderHeight + 20}px`;
        document.body.style.paddingBottom = `80px`;
    }

    setTimeout(adjustPadding, 100);
    window.addEventListener('resize', adjustPadding);


    // =============================
    // Form Submission Loading States
    // =============================
    const formsToWatch = [
        {
            formId: 'create-pathway-form',
            btnId: 'generate-btn',
            spinnerText: 'Generating your pathway... This may take up to 30 seconds'
        },
        {
            formId: 'complete-module-form',
            btnId: 'complete-module-btn',
            spinnerText: 'Submitting... This may take up to 20 seconds'
        },
        {
            formId: 'ask-ai-form',
            btnId: 'ask-ai-btn',
            spinnerText: 'AI is thinking...',
            loadingId: 'ask-ai-loading'
        }
    ];

    formsToWatch.forEach(item => {
        const form = document.getElementById(item.formId);
        if (form) {
            form.addEventListener('submit', function () {
                if (form.checkValidity()) {
                    const btn = document.getElementById(item.btnId);
                    const spinner = btn?.querySelector('.spinner-border');
                    const btnText = btn?.querySelector('.btn-text');

                    if (spinner) spinner.classList.remove('d-none');
                    if (btnText) btnText.innerText = item.spinnerText;
                    if (btn) btn.disabled = true;

                    if (item.loadingId) {
                        const loadingMsg = document.getElementById(item.loadingId);
                        if (loadingMsg) loadingMsg.classList.remove('d-none');
                    }
                }
            });
        }
    });


    // =============================
    // AI Content Auto-Reload Indicator
    // =============================
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) setTimeout(() => window.location.reload(), 7000);


    // =============================
    // Button Click Visual Feedback
    // =============================
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function () {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => { this.style.transform = ''; }, 100);
        });
    });
});
