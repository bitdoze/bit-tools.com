// static/js/site.js

document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', () => {
            const isExpanded = menuButton.getAttribute('aria-expanded') === 'true';

            // Toggle Tailwind's 'hidden' class on the menu panel
            mobileMenu.classList.toggle('hidden');

            // Update aria-expanded attribute for accessibility
            menuButton.setAttribute('aria-expanded', !isExpanded);

            // Optional: Change button icon (requires two icons in HTML)
            // const openIcon = menuButton.querySelector('.hamburger-icon');
            // const closeIcon = menuButton.querySelector('.close-icon');
            // if (openIcon && closeIcon) {
            //     openIcon.classList.toggle('hidden');
            //     closeIcon.classList.toggle('hidden');
            // }
        });
    } else {
        if (!menuButton) console.warn("Mobile menu button not found.");
        if (!mobileMenu) console.warn("Mobile menu panel not found.");
    }
});

// Optional: Close mobile menu if user clicks outside of it
// document.addEventListener('click', (event) => {
//     const mobileMenu = document.getElementById('mobile-menu');
//     const menuButton = document.getElementById('mobile-menu-button');
//
//     if (mobileMenu && menuButton && !mobileMenu.classList.contains('hidden')) {
//         // Check if the click was outside the menu and the button
//         if (!mobileMenu.contains(event.target) && !menuButton.contains(event.target)) {
//             mobileMenu.classList.add('hidden');
//             menuButton.setAttribute('aria-expanded', 'false');
//             // Optional: Reset button icon here too
//         }
//     }
// });