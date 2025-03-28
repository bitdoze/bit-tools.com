// static/js/tool-results.js

/**
 * Switches the active tab and content pane.
 * @param {string} targetTabId - The ID of the tab content pane to show.
 */
function switchTab(targetTabId) {
    const resultsContainer = document.getElementById('results-container');
    if (!resultsContainer) {
        console.error("Results container not found.");
        return;
    }

    // Get all tab buttons and content panes within the container
    const tabButtons = resultsContainer.querySelectorAll('button[id^="tab-"]');
    const contentPanes = resultsContainer.querySelectorAll('div[id$="-view"]'); // Assumes content divs end with '-view'

    // Hide all content panes
    contentPanes.forEach(pane => {
        pane.classList.add('hidden');
    });

    // Deactivate all tab buttons
    tabButtons.forEach(button => {
        button.classList.remove('bg-white', 'text-blue-600', 'font-bold');
        button.classList.add('bg-gray-200', 'text-gray-700');
    });

    // Show the target content pane
    const targetPane = document.getElementById(`${targetTabId}-view`);
    if (targetPane) {
        targetPane.classList.remove('hidden');
    } else {
        console.warn(`Content pane with ID '${targetTabId}-view' not found.`);
    }

    // Activate the target tab button
    const targetButton = document.getElementById(`tab-${targetTabId}`);
    if (targetButton) {
        targetButton.classList.remove('bg-gray-200', 'text-gray-700');
        targetButton.classList.add('bg-white', 'text-blue-600', 'font-bold');
    } else {
        console.warn(`Tab button with ID 'tab-${targetTabId}' not found.`);
    }
}

/**
 * Copies text to the clipboard and provides feedback.
 * @param {HTMLElement} copyButton - The button element that was clicked.
 */
async function copyToClipboard(copyButton) {
    const targetId = copyButton.dataset.copyTarget;
    const copyType = copyButton.dataset.copyType || 'element'; // Default to 'element' if type not specified
    const statusElement = copyButton.nextElementSibling; // Assumes status <p> is the immediate next sibling

    if (!targetId) {
        console.error("Copy target ID not found in button's data-copy-target attribute.");
        if (statusElement) statusElement.textContent = "Error: No target!";
        return;
    }

    const targetElement = document.getElementById(targetId);

    if (!targetElement) {
        console.error(`Target element with ID '${targetId}' not found.`);
        if (statusElement) statusElement.textContent = "Error: Target missing!";
        return;
    }

    let textToCopy = '';
    if (copyType === 'textarea' || targetElement.tagName === 'TEXTAREA' || targetElement.tagName === 'INPUT') {
        textToCopy = targetElement.value;
    } else {
        // Use textContent for divs/paragraphs to get raw text without HTML
        textToCopy = targetElement.textContent;
    }

    if (!textToCopy) {
        console.warn(`No text found to copy from target '${targetId}'.`);
        if (statusElement) statusElement.textContent = "Nothing to copy!";
        setTimeout(() => {
            if (statusElement) statusElement.textContent = "";
        }, 2000);
        return;
    }

    try {
        await navigator.clipboard.writeText(textToCopy);
        console.log(`Copied: ${textToCopy.substring(0, 50)}...`);
        if (statusElement) statusElement.textContent = "Copied!";
    } catch (err) {
        console.error('Failed to copy text: ', err);
        if (statusElement) statusElement.textContent = "Copy failed!";
    } finally {
        // Clear the status message after a delay
        setTimeout(() => {
            if (statusElement) statusElement.textContent = "";
        }, 2000);
    }
}

// --- Event Listener Setup ---
document.addEventListener('DOMContentLoaded', () => {
    const resultsContainer = document.getElementById('results-container');

    if (resultsContainer) {
        // Add delegated event listener for copy buttons
        resultsContainer.addEventListener('click', (event) => {
            // Check if the clicked element is a copy button or inside one
            const copyButton = event.target.closest('.copy-button');
            if (copyButton) {
                event.preventDefault(); // Prevent potential form submission if button is in a form
                copyToClipboard(copyButton);
            }
        });

        // Add delegated event listener for tab buttons (alternative to inline onclick)
        // Note: This assumes your tab buttons have a common class like 'tab-button'
        // If using inline onclick="switchTab(...)", this part is not strictly necessary
        // but can be cleaner. Let's assume inline onclick for now based on components.py.
        // If you remove onclick from components.py, uncomment and adapt this:
        /*
        resultsContainer.addEventListener('click', (event) => {
            const tabButton = event.target.closest('button[id^="tab-"]'); // More specific selector
            if (tabButton && tabButton.id.startsWith('tab-')) {
                const tabId = tabButton.id.substring(4); // Extract 'list' from 'tab-list'
                switchTab(tabId);
            }
        });
        */

        // Ensure the default active tab's content is visible on load
        const initialActiveButton = resultsContainer.querySelector('button[id^="tab-"].bg-white');
        if (initialActiveButton) {
            const initialTabId = initialActiveButton.id.substring(4);
            const initialPane = document.getElementById(`${initialTabId}-view`);
            if (initialPane) {
                // Ensure only the active one is visible
                 const contentPanes = resultsContainer.querySelectorAll('div[id$="-view"]');
                 contentPanes.forEach(pane => {
                    if (pane.id !== initialPane.id) {
                         pane.classList.add('hidden');
                    } else {
                         pane.classList.remove('hidden');
                    }
                 });
            }
        } else {
            // Fallback: If no active tab marked, show the first tab's content
            const firstTabButton = resultsContainer.querySelector('button[id^="tab-"]');
            if (firstTabButton) {
                const firstTabId = firstTabButton.id.substring(4);
                switchTab(firstTabId); // Initialize the first tab
            }
        }

    } else {
        console.warn("Results container with ID 'results-container' not found. Tab and copy functionality might not work.");
    }

    // Hide loading overlay if it exists from the previous page
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
    }
     // Ensure submit button on the *previous* page (if navigated back) is re-enabled
     // This might not reliably find the button if it's not cached, but worth trying.
    const submitButton = document.getElementById('submit-button');
    if (submitButton) {
        submitButton.disabled = false;
    }
});

// Additional handling for browser back/forward navigation
window.addEventListener('popstate', function() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
    }
    const submitButton = document.getElementById('submit-button');
    if (submitButton) {
        submitButton.disabled = false;
    }
    // Re-evaluate active tab based on potential state changes (if implemented)
    // For now, just ensure loading is hidden. A more complex SPA might need state restoration here.
});

// Handle page visibility changes (e.g., switching tabs)
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // Page is visible again
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.classList.add('hidden');
        }
        const submitButton = document.getElementById('submit-button');
        if (submitButton) {
            submitButton.disabled = false;
        }
    }
});