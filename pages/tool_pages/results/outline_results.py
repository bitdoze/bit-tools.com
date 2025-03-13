from fasthtml.common import *
from fasthtml.components import NotStr
import json
from .base_results import BaseResultsHandler
from .components import create_tab_navigation, create_tab_switching_script, create_copy_button, create_copy_script, create_markdown_viewer

class OutlineResultsHandler(BaseResultsHandler):
    """Handler for outline tool results."""
    
    def __init__(self, tool_id, tool, results):
        """Initialize the outline results handler."""
        super().__init__(tool_id, tool, results)
        self.generate_markdown()
    
    def generate_markdown(self):
        """Generate markdown from the outline."""
        markdown_lines = []
        try:
            current_section = None
            section_items = []

            for line in self.titles:
                line = line.strip()
                if not line:
                    continue

                # Check if this is a main section (heading-like)
                if (line.startswith('#') or
                    line[0].isupper() or
                    any(line.startswith(prefix) for prefix in ["Introduction", "Conclusion", "I.", "II.", "III."])):

                    # Add previous section to markdown
                    if current_section:
                        markdown_lines.append(f"## {current_section}")
                        for item in section_items:
                            markdown_lines.append(f"- {item}")
                        markdown_lines.append("")  # Empty line for spacing

                    # Start new section
                    current_section = line
                    section_items = []
                else:
                    # This is a subsection or bullet point
                    section_items.append(line)

            # Add the last section
            if current_section:
                markdown_lines.append(f"## {current_section}")
                for item in section_items:
                    markdown_lines.append(f"- {item}")
        except Exception as e:
            # If parsing failed, fall back to basic markdown list
            markdown_lines = [f"- {title}" for title in self.titles]

        self.markdown_text = "\n".join(markdown_lines)
    
    def create_list_view(self):
        """Create the list view for outline results."""
        list_items = []

        # Try to parse the outline structure
        try:
            current_section = None
            section_items = []

            for line in self.titles:
                line = line.strip()
                if not line:
                    continue

                # Check if this is a main section (heading-like)
                if (line.startswith('#') or
                    line[0].isupper() or
                    any(line.startswith(prefix) for prefix in ["Introduction", "Conclusion", "I.", "II.", "III."])):

                    # If we have a previous section, add it to the list
                    if current_section and section_items:
                        list_items.append(
                            Div(
                                P(current_section, cls="font-bold mb-2"),
                                Div(
                                    *[P(item, cls="ml-4 mb-1") for item in section_items],
                                    cls="mb-3"
                                ),
                                cls="mb-4 p-4 bg-white rounded shadow-md"
                            )
                        )
                        section_items = []

                    # Start a new section
                    current_section = line
                else:
                    # This is a subsection or bullet point
                    section_items.append(line)

            # Add the last section
            if current_section and section_items:
                list_items.append(
                    Div(
                        P(current_section, cls="font-bold mb-2"),
                        Div(
                            *[P(item, cls="ml-4 mb-1") for item in section_items],
                            cls="mb-3"
                        ),
                        cls="mb-4 p-4 bg-white rounded shadow-md"
                    )
                )
        except Exception as e:
            list_items = []

        # If parsing failed or produced no results, fall back to treating each line as separate
        if not list_items:
            list_items = [
                Div(
                    P(title, cls="mb-1"),
                    cls="p-4 bg-white rounded shadow-md mb-3"
                )
                for title in self.titles
            ]

        return Div(
            *list_items,
            id="list-view",
            cls="mb-6"
        )
    
    def create_card_view(self):
        """Create the card view for outline results."""
        return Div(
            Div(
                H3("Complete Outline", cls="text-xl font-bold mb-4 text-center"),
                *[P(title, cls="mb-2") for title in self.titles],
                cls="p-6 bg-white rounded shadow-lg"
            ),
            id="card-view",
            cls="mb-6 hidden"
        )
    
    def create_markdown_view(self):
        """Create the markdown view for outline results."""
        return Div(
            H3("Markdown Format", cls="text-xl font-bold mb-4 text-center"),
            Div(
                Textarea(
                    self.markdown_text,
                    id="markdown-content",
                    rows=15,
                    readonly=True,
                    cls="w-full p-3 border rounded font-mono"
                ),
                create_copy_button("markdown-content", "copy-markdown-btn", "markdown-copy-status"),
                cls="mb-4"
            ),
            Div(
                H4("Preview:", cls="text-lg font-bold mb-2"),
                create_markdown_viewer(self.markdown_text),
                cls="mt-4"
            ),
            id="markdown-view",
            cls="mb-6 hidden"
        )
    
    def create_copy_all_view(self):
        """Create the copy-all view for outline results."""
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
        """Create all views for the outline results."""
        views = {
            "list": self.create_list_view(),
            "card": self.create_card_view(),
            "markdown": self.create_markdown_view(),
            "copy": self.create_copy_all_view()
        }
        
        return Div(*views.values())
    
    def create_tabs(self):
        """Create tabs for the outline results."""
        tabs = [
            {"id": "list", "label": "List View", "selected": True},
            {"id": "card", "label": "Card View", "selected": False},
            {"id": "markdown", "label": "Markdown", "selected": False},
            {"id": "copy", "label": "Copy All", "selected": False}
        ]
        
        return create_tab_navigation(tabs)
    
    def create_scripts(self):
        """Create scripts for the outline results."""
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
                    
                    // Setup markdown copy button if it exists
                    const copyMarkdownBtn = document.getElementById('copy-markdown-btn');
                    const markdownStatus = document.getElementById('markdown-copy-status');
                    const markdownContent = document.getElementById('markdown-content');
                    
                    if (copyMarkdownBtn && markdownContent) {
                        copyMarkdownBtn.addEventListener('click', function() {
                            navigator.clipboard.writeText(markdownContent.value)
                                .then(() => {
                                    markdownStatus.textContent = 'Copied!';
                                    setTimeout(() => {
                                        markdownStatus.textContent = '';
                                    }, 2000);
                                })
                                .catch(err => {
                                    markdownStatus.textContent = 'Failed to copy';
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
            """),
            
            # Zero-md script for markdown rendering
            Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register")
        )
    
    def render(self):
        """Render the outline results page."""
        return Div(
            # Page header
            H1(f"{self.tool.name} Results",
               cls="text-3xl font-bold text-gray-800 mb-2 text-center"),

            P("Here is your generated outline:",
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
