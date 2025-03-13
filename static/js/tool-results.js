/**
 * Tool Results JavaScript
 * 
 * This file contains the JavaScript functionality for the tool results pages.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    window.switchTab = function(tabId) {
        // Hide all views
        const views = document.querySelectorAll('[id$="-view"]');
        views.forEach(view => {
            view.classList.add('hidden');
        });
        
        // Show selected view
        const selectedView = document.getElementById(tabId + '-view');
        if (selectedView) {
            selectedView.classList.remove('hidden');
        }
        
        // Update tab buttons
        const tabs = document.querySelectorAll('[id^="tab-"]');
        tabs.forEach(tab => {
            tab.classList.remove('bg-white', 'text-blue-600', 'font-bold');
            tab.classList.add('bg-gray-200', 'text-gray-700');
        });
        
        const selectedTab = document.getElementById('tab-' + tabId);
        if (selectedTab) {
            selectedTab.classList.remove('bg-gray-200', 'text-gray-700');
            selectedTab.classList.add('bg-white', 'text-blue-600', 'font-bold');
        }
    };

    // Copy functionality
    function setupCopyButton(buttonId, textId, statusId) {
        const copyBtn = document.getElementById(buttonId);
        const statusEl = document.getElementById(statusId);
        const contentEl = document.getElementById(textId);
        
        if (copyBtn && contentEl) {
            copyBtn.addEventListener('click', function() {
                const text = contentEl.value || contentEl.textContent;
                
                navigator.clipboard.writeText(text)
                    .then(() => {
                        statusEl.textContent = 'Copied!';
                        setTimeout(() => {
                            statusEl.textContent = '';
                        }, 2000);
                    })
                    .catch(err => {
                        statusEl.textContent = 'Failed to copy';
                        console.error('Failed to copy text: ', err);
                    });
            });
        }
    }

    // Setup copy-all button if it exists
    setupCopyButton('copy-all-btn', 'copy-all-content', 'copy-all-status');
    
    // Setup markdown copy button if it exists
    setupCopyButton('copy-markdown-btn', 'markdown-content', 'markdown-copy-status');
    
    // Setup transformed text copy button if it exists
    const copyTransformedBtn = document.getElementById('copy-transformed-btn');
    if (copyTransformedBtn) {
        const statusEl = document.getElementById('copy-status');
        const transformedTextEl = document.querySelector('.bg-blue-50 p');
        
        if (transformedTextEl) {
            copyTransformedBtn.addEventListener('click', function() {
                const text = transformedTextEl.textContent;
                
                navigator.clipboard.writeText(text)
                    .then(() => {
                        statusEl.textContent = 'Copied!';
                        setTimeout(() => {
                            statusEl.textContent = '';
                        }, 2000);
                    })
                    .catch(err => {
                        statusEl.textContent = 'Failed to copy';
                        console.error('Failed to copy text: ', err);
                    });
            });
        }
    }
    
    // Setup individual copy buttons
    document.querySelectorAll('[id^="copy-btn-"]').forEach(button => {
        const index = button.id.replace('copy-btn-', '');
        const textEl = document.getElementById('title-text-' + index);
        
        if (textEl) {
            button.addEventListener('click', function() {
                const text = textEl.textContent.replace(/^\d+\.\s*/, ''); // Remove numbering
                
                navigator.clipboard.writeText(text)
                    .then(() => {
                        button.textContent = 'Copied!';
                        setTimeout(() => {
                            button.textContent = 'Copy';
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Failed to copy text: ', err);
                    });
            });
        }
    });
    
    document.querySelectorAll('[id^="card-copy-btn-"]').forEach(button => {
        const index = button.id.replace('card-copy-btn-', '');
        const textEl = document.getElementById('card-text-' + index);
        
        if (textEl) {
            button.addEventListener('click', function() {
                const text = textEl.textContent;
                
                navigator.clipboard.writeText(text)
                    .then(() => {
                        button.textContent = 'Copied!';
                        setTimeout(() => {
                            button.textContent = 'Copy';
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Failed to copy text: ', err);
                    });
            });
        }
    });

    // Hide any loading overlays
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
    }

    // Reset any disabled submit buttons
    const submitButton = document.getElementById('submit-button');
    if (submitButton) {
        submitButton.disabled = false;
    }
});
