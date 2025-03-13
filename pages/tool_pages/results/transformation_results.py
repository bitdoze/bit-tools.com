from fasthtml.common import *
import json
from .base_results import BaseResultsHandler
from .components import create_copy_button, create_copy_script

class TransformationResultsHandler(BaseResultsHandler):
    """Handler for transformation tool results."""
    
    def __init__(self, tool_id, tool, results):
        """Initialize the transformation results handler."""
        super().__init__(tool_id, tool, results)
        self.original_text = results.get("original_text", "")
        self.transformed_text = results.get("transformed_text", "")
    
    def create_before_after_view(self):
        """Create the before/after view for transformation results."""
        return Div(
            # Original and transformed text
            Div(
                H3("Original Text", cls="text-lg font-bold mb-2"),
                Div(
                    P(self.original_text, cls="whitespace-pre-wrap"),
                    cls="p-4 bg-gray-100 rounded mb-6 overflow-auto max-h-60"
                ),
                H3("Transformed Text", cls="text-lg font-bold mb-2"),
                Div(
                    P(self.transformed_text, cls="whitespace-pre-wrap"),
                    cls="p-4 bg-blue-50 rounded mb-6 overflow-auto max-h-60"
                ),
                Div(
                    Button(
                        "Copy Transformed Text",
                        type="button",
                        id="copy-transformed-btn",
                        cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
                    ),
                    P("", id="copy-status", cls="text-green-600 inline-block"),
                    cls="flex items-center"
                ),
                cls="mb-6"
            ),
            
            # Include the script directly in the page for now
            Script("""
                document.addEventListener('DOMContentLoaded', function() {
                    // Copy functionality for transformed text
                    const copyBtn = document.getElementById('copy-transformed-btn');
                    const statusEl = document.getElementById('copy-status');
                    const transformedTextEl = document.querySelector('.bg-blue-50 p');
                    
                    if (copyBtn && transformedTextEl) {
                        copyBtn.addEventListener('click', function() {
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
                
                // Add event listener for browser navigation events (back/forward buttons)
                window.addEventListener('popstate', function() {
                    // Hide any loading overlays when navigating with browser controls
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
                
                // Force hide loading overlay on page load and back button
                // This ensures the loading overlay is hidden even if the popstate event doesn't fire properly
                document.addEventListener('visibilitychange', function() {
                    if (!document.hidden) {
                        // Page is now visible (e.g., after returning from another tab or using back button)
                        const loadingOverlay = document.getElementById('loading-overlay');
                        if (loadingOverlay) {
                            loadingOverlay.classList.add('hidden');
                        }

                        // Reset any disabled submit buttons
                        const submitButton = document.getElementById('submit-button');
                        if (submitButton) {
                            submitButton.disabled = false;
                        }
                    }
                });
            """)
        )
    
    def render(self):
        """Render the transformation results page."""
        return Div(
            # Page header
            H1(f"{self.tool.name} Results",
               cls="text-3xl font-bold text-gray-800 mb-2 text-center"),

            P("Here is your transformed text:",
              cls="text-xl text-gray-600 mb-8 text-center"),

            # Results section
            Div(
                # Summary of request
                self.create_metadata_section(),

                # Before/after view
                self.create_before_after_view(),

                # Navigation buttons
                self.create_navigation_buttons(),

                # Page scripts
                self.get_page_scripts(),

                cls="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md"
            )
        )
