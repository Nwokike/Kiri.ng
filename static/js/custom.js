// PWA Install Button Logic
let deferredPrompt;
const installButton = document.getElementById('pwa-install-btn');

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (installButton) {
        installButton.style.display = 'block';
    }
});

if (installButton) {
    installButton.addEventListener('click', async () => {
        if (!deferredPrompt) {
            return;
        }
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        deferredPrompt = null;
        installButton.style.display = 'none';
    });
}

window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    if (installButton) {
        installButton.style.display = 'none';
    }
});

// Dark Mode Logic
const themeToggle = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme');

if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);
    if (currentTheme === 'dark' && themeToggle) {
        themeToggle.checked = true;
    }
}

if (themeToggle) {
    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
}

// Google Translate
function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,ha,ig,yo',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
    }, 'google_translate_element');
}

// Main script to run after the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Smart Navigation Script with Improved Active States
    const path = window.location.pathname;
    const mainHeader = document.getElementById('main-header');
    const subHeaderContainer = document.getElementById('sub-header-container');
    const backButtonContainer = document.getElementById('back-button-container');

    let activeSection = 'services';
    if (path.includes('/academy/')) activeSection = 'academy';
    if (path.includes('/blog/')) activeSection = 'blog';
    if (path.includes('/users/') || path.includes('/profile/')) activeSection = 'profile';
    if (path === '/') activeSection = 'services';

    // Clear all active states and add to current section
    document.querySelectorAll('.bottom-nav-item').forEach(item => {
        item.classList.remove('text-primary', 'active');
    });
    
    const activeNavItem = document.querySelector(`[data-nav="${activeSection}"]`);
    if (activeNavItem) {
        activeNavItem.classList.add('text-primary', 'active');
    }

    // Show appropriate sub-navigation
    const activeSubNavId = `sub-nav-${activeSection}`;
    const activeSubNavHTML = document.getElementById(activeSubNavId)?.innerHTML;
    if (activeSubNavHTML) {
        subHeaderContainer.innerHTML = activeSubNavHTML;
        
        // Mark active sub-navigation link
        subHeaderContainer.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === path) {
                link.classList.add('active');
            }
        });
    }

    // Show back button for detail pages
    const mainTabs = ["/marketplace/", "/academy/dashboard/", "/blog/", "/users/profile/"];
    if (!mainTabs.includes(path) && path !== "/") {
        backButtonContainer.innerHTML = `<a href="javascript:history.back()" class="btn btn-outline-secondary back-btn"><i class="bi bi-arrow-left fs-4"></i></a>`;
    }

    // Adjust padding dynamically
    function adjustPadding() {
        const headerHeight = mainHeader.offsetHeight;
        const subHeaderHeight = subHeaderContainer.offsetHeight;
        document.body.style.paddingTop = `${headerHeight + subHeaderHeight + 20}px`;
        document.body.style.paddingBottom = `80px`;
    }
    
    setTimeout(adjustPadding, 100);
    window.addEventListener('resize', adjustPadding);

    // Loading Spinner for Forms
    const formsToWatch = [
        { formId: 'create-pathway-form', btnId: 'generate-btn', spinnerText: 'Generating your pathway... This may take up to 30 seconds' },
        { formId: 'complete-module-form', btnId: 'complete-module-btn', spinnerText: 'Submitting... This may take up to 20 seconds' },
        { formId: 'ask-ai-form', btnId: 'ask-ai-btn', spinnerText: 'AI is thinking...', loadingId: 'ask-ai-loading' }
    ];

    formsToWatch.forEach(item => {
        const form = document.getElementById(item.formId);
        if (form) {
            form.addEventListener('submit', function() {
                if (form.checkValidity()) {
                    const btn = document.getElementById(item.btnId);
                    const spinner = btn.querySelector('.spinner-border');
                    const btnText = btn.querySelector('.btn-text');
                    
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

    // AI Content Loading Indicator
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        setTimeout(function() { window.location.reload(); }, 7000);
    }

    // Add visual feedback for button clicks
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });
});
