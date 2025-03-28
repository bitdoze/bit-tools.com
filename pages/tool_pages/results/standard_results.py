# pages/tool_pages/results/standard_results.py
from fasthtml.common import *
import json
import re # Import re for cleaning text in copy
from .base_results import BaseResultsHandler
from .components import create_tab_navigation, create_copy_button, create_tab_switching_script

class StandardResultsHandler(BaseResultsHandler):
    """Handler for standard tool results (titles, social posts, etc.)."""

    def __init__(self, tool_id, tool, results):
        """Initialize the standard results handler."""
        super().__init__(tool_id, tool, results)
        # Determine default active tab (e.g., 'list')
        self.active_tab_id = "list"
        # Prepare text for "Copy All" - join the list of titles/content
        self.all_content_text = "\n".join(self.titles) # Use self.titles processed by base class

    def create_list_view(self):
        """Create the list view."""
        view_id = "list-view"
        # Set visibility based on the active tab
        classes = "mb-6 space-y-3" # Add space between items
        if self.active_tab_id != "list":
            classes += " hidden"

        list_items = []
        if not self.titles:
             return Div(P("No results generated.", cls="text-gray-500"), id=view_id, cls=classes)

        for i, content in enumerate(self.titles):
            content_id_target = f"list-content-{i}"
            # Clean potential numbering like "1. " from the start for display
            display_content = re.sub(r'^\d+\.\s*', '', content).strip()
            # The actual content to copy (might be the original 'content' if cleaning is display-only)
            copy_content = content # Copy the original content line

            list_items.append(
                Div(
                    # Displayable content
                    P(display_content, cls="flex-grow mr-4 whitespace-pre-wrap"), # Allow wrapping
                    # Copy button and status (using component)
                    # The component now creates the button and the status P element
                    create_copy_button(text_id=content_id_target),
                    # Hidden div holding the exact text to copy
                    Div(copy_content, id=content_id_target, cls="hidden"),
                    cls="flex items-center justify-between p-3 bg-white rounded shadow-sm border border-gray-200" # Added border
                 )
            )

        return Div(*list_items, id=view_id, cls=classes)

    def create_card_view(self):
        """Create the card view."""
        view_id = "card-view"
        # Set visibility based on the active tab
        classes = "mb-6"
        if self.active_tab_id != "card":
            classes += " hidden"

        card_items = []
        if not self.titles:
            return Div(P("No results generated.", cls="text-gray-500"), id=view_id, cls=classes)

        for i, content in enumerate(self.titles):
            content_id_target = f"card-content-{i}"
            display_content = re.sub(r'^\d+\.\s*', '', content).strip()
            copy_content = content

            card_items.append(
                Div(
                    # Display content (truncated potentially)
                    P(display_content[:120] + ('...' if len(display_content) > 120 else ''),
                      cls="text-sm mb-3 h-16 overflow-hidden"), # Fixed height, overflow hidden
                    # Copy button and status (using component)
                    create_copy_button(text_id=content_id_target),
                    # Hidden div holding the exact text to copy
                    Div(copy_content, id=content_id_target, cls="hidden"),
                    cls="p-4 bg-white rounded shadow border border-gray-200 flex flex-col justify-between" # Added border
                )
            )

        return Div(
            Div(*card_items, cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"),
            id=view_id,
            cls=classes
        )

    def create_copy_all_view(self):
        """Create the copy-all view."""
        view_id = "copy-view"
        # Set visibility based on the active tab
        classes = "mb-6"
        if self.active_tab_id != "copy":
            classes += " hidden"

        return Div(
            H3("All Generated Content", cls="text-lg font-semibold mb-3"),
            Textarea(
                self.all_content_text,
                id="copy-all-content", # ID for the textarea
                rows=12,
                readonly=True,
                cls="w-full p-3 border rounded bg-gray-50 font-mono text-sm" # Added font styling
            ),
            # Button needs data-copy-target and data-copy-type for JS
            Button(
                "Copy All Text", type="button",
                cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2 mr-2",
                **{'data-copy-target': 'copy-all-content', 'data-copy-type': 'textarea'} # Specify target and type
            ),
            P("", cls="copy-status text-green-600 inline-block"), # Status element
            id=view_id,
            cls=classes
        )

    def create_views(self):
        """Create all views for the standard results."""
        # The individual view methods now handle their own visibility based on self.active_tab_id
        return Div(
            self.create_list_view(),
            self.create_card_view(),
            self.create_copy_all_view()
        )

    def create_tabs(self):
        """Create tabs for the standard results."""
        tabs_config = [
            {"id": "list", "label": "List View", "selected": self.active_tab_id == "list"},
            {"id": "card", "label": "Card View", "selected": self.active_tab_id == "card"},
            {"id": "copy", "label": "Copy All", "selected": self.active_tab_id == "copy"}
        ]
        # Use the component to generate tab navigation
        return create_tab_navigation(tabs_config)


    def render(self):
        """Render the standard results page."""
        return Div(
            H1(f"{self.tool.name} Results", cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
            P("Here are your generated results:", cls="text-xl text-gray-600 mb-8 text-center"),
            Div(
                self.create_metadata_section(),
                self.create_tabs(), # Generate tabs
                self.create_views(), # Generate views (list, card, copy)
                self.create_navigation_buttons(),
                create_tab_switching_script(), # Link the main JS file
                cls="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-md border border-gray-200", # Increased max-width slightly
                id="results-container" # Crucial ID for JS targeting
            )
        )