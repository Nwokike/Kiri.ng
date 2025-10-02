// --- THIS IS THE NEW DARK MODE LOGIC (at the top of the file) ---
const themeToggle = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme');

// Set the initial theme on page load
if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);
    if (currentTheme === 'dark' && themeToggle) {
        themeToggle.checked = true;
    }
}

// Listener for the toggle switch
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
// --- END NEW LOGIC ---

// Function for Google Translate
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
    // --- Smart Navigation Script ---
    const path = window.location.pathname;
    const mainHeader = document.getElementById('main-header');
    const subHeaderContainer = document.getElementById('sub-header-container');
    const backButtonContainer = document.getElementById('back-button-container');

    let activeSection = 'services';
    if (path.includes('/academy/')) activeSection = 'academy';
    if (path.includes('/blog/')) activeSection = 'blog';
    if (path.includes('/users/') || path.includes('/profile/')) activeSection = 'profile';
    if (path === '/') activeSection = 'services';

    document.querySelectorAll('.bottom-nav-item').forEach(item => item.classList.remove('text-primary'));
    const activeNavItem = document.querySelector(`[data-nav="${activeSection}"]`);
    if (activeNavItem) activeNavItem.classList.add('text-primary');

    const activeSubNavId = `sub-nav-${activeSection}`;
    const activeSubNavHTML = document.getElementById(activeSubNavId)?.innerHTML;
    if (activeSubNavHTML) {
        subHeaderContainer.innerHTML = activeSubNavHTML;
        subHeaderContainer.querySelectorAll('.nav-link').forEach(link => {
            if (link.getAttribute('href') === path) {
                link.classList.add('active');
            }
        });
    }

    const mainTabs = ["/marketplace/", "/academy/dashboard/", "/blog/", "/users/profile/"];
    if (!mainTabs.includes(path) && path !== "/") {
        backButtonContainer.innerHTML = `<a href="javascript:history.back()" class="btn btn-light"><i class="bi bi-arrow-left fs-4"></i></a>`;
    }

    function adjustPadding() {
        const headerHeight = mainHeader.offsetHeight;
        const subHeaderHeight = subHeaderContainer.offsetHeight;
        document.body.style.paddingTop = `${headerHeight + subHeaderHeight}px`;
        document.body.style.paddingBottom = `80px`;
    }
    setTimeout(adjustPadding, 100);
    window.addEventListener('resize', adjustPadding);

    // --- Loading Spinner Simulations ---
    const formsToWatch = [
        { formId: 'create-pathway-form', btnId: 'generate-btn', spinnerText: 'Generating...' },
        { formId: 'complete-module-form', btnId: 'complete-module-btn', spinnerText: 'Submitting...' }
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
                }
            });
        }
    });

    // --- AI Content Loading Indicator ---
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        setTimeout(function() { window.location.reload(); }, 7000);
    }
});
