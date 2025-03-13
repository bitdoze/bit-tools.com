from fasthtml.common import *
import json
from .base_results import BaseResultsHandler
from .components import create_tab_navigation, create_tab_switching_script, create_copy_button, create_copy_script

class StandardResultsHandler(BaseResultsHandler):
    """Handler for standard tool results."""
    
    def create_list_view(self):
        """Create the list view for standard results."""
        list_items = []
        
        for i, content in enumerate(self.titles):
            # Check if the content is short (likely a title) or long (paragraph/post)
            is_long_content = len(content) > 100
            
            if is_long_content:
                # For longer content, use a more spacious layout with preview
                preview = content[:100] + "..." if len(content) > 100 else content
                list_items.append(
                    Div(
                        Div(
                            P(f"{i+1}.", cls="font-bold mr-2 text-gray-500"),
                            P(preview, cls="text-gray-700", id=f"title-preview-{i}"),
                            cls="flex items-start mb-2"
                        ),
                        Div(
                            P(content, cls="whitespace-pre-wrap text-gray-800 mb-3", id=f"title-text-{i}"),
                            cls="hidden" if len(content) > 100 else ""
                        ),
                        Div(
                            Button(
                                "Show More" if len(content) > 100 else "Show Less",
                                type="button",
                                id=f"toggle-btn-{i}",
                                cls="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-2 rounded mr-2"
                            ) if is_long_content else Div(),
                            Button(
                                "Copy",
                                type="button",
                                id=f"copy-btn-{i}",
                                cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
                            ),
                            cls="flex justify-end"
                        ),
                        cls="p-4 bg-white rounded shadow-sm mb-4 hover:shadow-md transition-shadow"
                    )
                )
            else:
                # For shorter content (titles), use the original compact layout
                list_items.append(
                    Div(
                        P(f"{i+1}. {content}", cls="mb-1 flex-grow", id=f"title-text-{i}"),
                        Button(
                            "Copy",
                            type="button",
                            id=f"copy-btn-{i}",
                            cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded ml-2"
                        ),
                        cls="flex items-center justify-between p-3 bg-white rounded shadow-sm mb-3 hover:shadow-md transition-shadow"
                    )
                )
        
        return Div(
            *list_items,
            id="list-view",
            cls="mb-6"
        )
    
    def create_card_view(self):
        """Create the card view for standard results."""
        card_items = []
        
        for i, content in enumerate(self.titles):
            # Check if the content is short (likely a title) or long (paragraph/post)
            is_long_content = len(content) > 100
            
            if is_long_content:
                # For longer content, show a preview with expand/collapse
                preview = content[:80] + "..." if len(content) > 80 else content
                card_items.append(
                    Div(
                        P(preview, cls="text-center mb-2 text-sm", id=f"card-preview-{i}"),
                        P(content, cls="text-center mb-2 text-sm whitespace-pre-wrap hidden", id=f"card-full-{i}"),
                        Div(
                            Button(
                                "Show More",
                                type="button",
                                id=f"card-toggle-btn-{i}",
                                cls="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 py-1 px-2 rounded w-full mb-2"
                            ) if is_long_content else Div(),
                            Button(
                                "Copy",
                                type="button",
                                id=f"card-copy-btn-{i}",
                                cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded w-full"
                            ),
                            cls="flex flex-col"
                        ),
                        cls="p-4 bg-white rounded shadow-sm hover:shadow-md transition-shadow"
                    )
                )
            else:
                # For shorter content, use the original card layout
                card_items.append(
                    Div(
                        P(content, cls="text-center mb-2", id=f"card-text-{i}"),
                        Button(
                            "Copy",
                            type="button",
                            id=f"card-copy-btn-{i}",
                            cls="w-full text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
                        ),
                        cls="p-4 bg-white rounded shadow-sm hover:shadow-md transition-shadow"
                    )
                )
        
        return Div(
            Div(
                *card_items,
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
                    
                    // Setup toggle buttons for list view
                    document.querySelectorAll('[id^="toggle-btn-"]').forEach(button => {
                        const index = button.id.replace('toggle-btn-', '');
                        const previewEl = document.getElementById('title-preview-' + index);
                        const fullTextEl = document.getElementById('title-text-' + index).parentNode;
                        
                        if (previewEl && fullTextEl) {
                            button.addEventListener('click', function() {
                                const isExpanded = !fullTextEl.classList.contains('hidden');
                                
                                if (isExpanded) {
                                    // Collapse
                                    fullTextEl.classList.add('hidden');
                                    previewEl.parentNode.classList.remove('hidden');
                                    button.textContent = 'Show More';
                                } else {
                                    // Expand
                                    fullTextEl.classList.remove('hidden');
                                    button.textContent = 'Show Less';
                                }
                            });
                        }
                    });
                    
                    // Setup toggle buttons for card view
                    document.querySelectorAll('[id^="card-toggle-btn-"]').forEach(button => {
                        const index = button.id.replace('card-toggle-btn-', '');
                        const previewEl = document.getElementById('card-preview-' + index);
                        const fullTextEl = document.getElementById('card-full-' + index);
                        
                        if (previewEl && fullTextEl) {
                            button.addEventListener('click', function() {
                                const isExpanded = !fullTextEl.classList.contains('hidden');
                                
                                if (isExpanded) {
                                    // Collapse
                                    fullTextEl.classList.add('hidden');
                                    previewEl.classList.remove('hidden');
                                    button.textContent = 'Show More';
                                } else {
                                    // Expand
                                    fullTextEl.classList.remove('hidden');
                                    previewEl.classList.add('hidden');
                                    button.textContent = 'Show Less';
                                }
                            });
                        }
                    });
                    
                    // Setup individual copy buttons for list view
                    document.querySelectorAll('[id^="copy-btn-"]').forEach(button => {
                        const index = button.id.replace('copy-btn-', '');
                        const textEl = document.getElementById('title-text-' + index) || 
                                      document.getElementById('title-preview-' + index)?.parentNode.nextElementSibling.firstElementChild;
                        
                        if (textEl) {
                            button.addEventListener('click', function() {
                                // Get text content, removing numbering if present
                                let text = textEl.textContent;
                                text = text.replace(/^\\d+\\.\\s*/, ''); // Remove numbering
                                
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
                    
                    // Setup individual copy buttons for card view
                    document.querySelectorAll('[id^="card-copy-btn-"]').forEach(button => {
                        const index = button.id.replace('card-copy-btn-', '');
                        const textEl = document.getElementById('card-text-' + index) || 
                                      document.getElementById('card-full-' + index);
                        const previewEl = document.getElementById('card-preview-' + index);
                        
                        if (textEl || previewEl) {
                            button.addEventListener('click', function() {
                                // Use full text if available, otherwise use preview
                                const text = textEl ? textEl.textContent : previewEl.textContent;
                                
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
