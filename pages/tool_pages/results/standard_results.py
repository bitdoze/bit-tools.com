from fasthtml.common import *
import json
from .base_results import BaseResultsHandler
from .components import create_tab_navigation, create_tab_switching_script, create_copy_button, create_copy_script

class StandardResultsHandler(BaseResultsHandler):
    """Handler for standard tool results."""
    
    def create_list_view(self):
        """Create the list view for standard results."""
        list_items = [
            Div(
                P(f"{i+1}. {title}", cls="mb-1 flex-grow", id=f"title-text-{i}"),
                Button(
                    "Copy",
                    type="button",
                    id=f"copy-btn-{i}",
                    cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded ml-2"
                ),
                cls="flex items-center justify-between p-3 bg-white rounded shadow-sm mb-3 hover:shadow-md transition-shadow"
            )
            for i, title in enumerate(self.titles)
        ]
        
        return Div(
            *list_items,
            id="list-view",
            cls="mb-6"
        )
    
    def create_card_view(self):
        """Create the card view for standard results."""
        return Div(
            Div(
                *[
                    Div(
                        P(title, cls="text-center mb-2", id=f"card-text-{i}"),
                        Button(
                            "Copy",
                            type="button",
                            id=f"card-copy-btn-{i}",
                            cls="w-full text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
                        ),
                        cls="p-4 bg-white rounded shadow-sm hover:shadow-md transition-shadow"
                    )
                    for i, title in enumerate(self.titles)
                ],
                cls="grid grid-cols-1 md:grid-cols-2 gap-4"
            ),
            id="card-view",
            cls="mb-6 hidden"
        )
    
    def create_copy_all_view(self):
        """Create the copy-all view for standard results."""
        return Div(
            Textarea(
                "\n".join(self.titles),
                id="copy-all-content",
                rows=10,
                readonly=True,
                cls="w-full p-3 border rounded"
            ),
            create_copy_button("copy-all-content", "copy-all-btn", "copy-all-status"),
            id="copy-view",
            cls="mb-6 hidden"
        )
    
    def create_views(self):
        """Create all views for the standard results."""
        views = {
            "list": self.create_list_view(),
            "card": self.create_card_view(),
            "copy": self.create_copy_all_view()
        }
        
        return Div(*views.values())
    
    def create_tabs(self):
        """Create tabs for the standard results."""
        tabs = [
            {"id": "list", "label": "List View", "selected": True},
            {"id": "card", "label": "Card View", "selected": False},
            {"id": "copy", "label": "Copy All", "selected": False}
        ]
        
        return create_tab_navigation(tabs)
    
    def create_scripts(self):
        """Create scripts for the standard results."""
        return Div(
            # Include the script directly in the page for now
            Script("""
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

                    // Setup copy-all button if it exists
                    const copyAllBtn = document.getElementById('copy-all-btn');
                    const copyAllStatus = document.getElementById('copy-all-status');
                    const copyAllContent = document.getElementById('copy-all-content');
                    
                    if (copyAllBtn && copyAllContent) {
                        copyAllBtn.addEventListener('click', function() {
                            navigator.clipboard.writeText(copyAllContent.value)
                                .then(() => {
                                    copyAllStatus.textContent = 'Copied!';
                                    setTimeout(() => {
                                        copyAllStatus.textContent = '';
                                    }, 2000);
                                })
                                .catch(err => {
                                    copyAllStatus.textContent = 'Failed to copy';
                                    console.error('Failed to copy text: ', err);
                                });
                        });
                    }
                    
                    // Setup individual copy buttons
                    document.querySelectorAll('[id^="copy-btn-"]').forEach(button => {
                        const index = button.id.replace('copy-btn-', '');
                        const textEl = document.getElementById('title-text-' + index);
                        
                        if (textEl) {
                            button.addEventListener('click', function() {
                                const text = textEl.textContent.replace(/^\\d+\\.\\s*/, ''); // Remove numbering
                                
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
            """)
        )
    
    def render(self):
        """Render the standard results page."""
        return Div(
            # Page header
            H1(f"{self.tool.name} Results",
               cls="text-3xl font-bold text-gray-800 mb-2 text-center"),

            P("Here are your generated results:",
              cls="text-xl text-gray-600 mb-8 text-center"),

            # Results section
            Div(
                # Summary of request
                self.create_metadata_section(),

                # Tabs for different views
                self.create_tabs(),

                # Different views
                self.create_views(),

                # Navigation buttons
                self.create_navigation_buttons(),

                # Scripts
                self.create_scripts(),
                
                # Base scripts
                self.get_page_scripts(),

                cls="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md"
            )
        )
