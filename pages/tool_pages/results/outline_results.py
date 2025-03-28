# pages/tool_pages/results/outline_results.py
from fasthtml.common import *
from fasthtml.components import NotStr
import json
import re # Import re
from .base_results import BaseResultsHandler
from .components import create_tab_navigation, create_copy_button, create_markdown_viewer, create_tab_switching_script

class OutlineResultsHandler(BaseResultsHandler):
    """Handler for structured or unstructured blog outline tool results."""

    def __init__(self, tool_id, tool, results):
        """Initialize the outline results handler."""
        super().__init__(tool_id, tool, results)
        self.active_tab_id = "list" # Default active tab

        # Use 'titles' from base class (which is prepared by the factory)
        self.outline_lines = self.titles

        # Generate markdown from the potentially structured lines
        self.markdown_text = self._generate_markdown_from_lines(self.outline_lines)
        # Text for copy-all is just the raw lines joined
        self.all_content_text = "\n".join(self.outline_lines)

    def _generate_markdown_from_lines(self, lines):
        """Generate markdown from a list of outline strings, trying to infer structure."""
        markdown_lines = []
        current_indent = 0
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:
                continue # Skip empty lines

            # Check for existing markdown headers
            if stripped_line.startswith('#'):
                markdown_lines.append(stripped_line)
                current_indent = stripped_line.count('#') # Track heading level
            # Check for existing markdown list items
            elif stripped_line.startswith(('-', '*', '+')):
                 # Calculate indent based on leading spaces before the marker
                 indent_level = (len(line) - len(line.lstrip(' '))) // 2 # Simple 2-space indent assumption
                 markdown_lines.append("  " * indent_level + stripped_line)
            # Check for common outline structures (Roman numerals, Letters, Numbers)
            elif re.match(r'^[IVXLCDM]+\.\s+', stripped_line):
                 markdown_lines.append(f"## {stripped_line}") # Assume H2
                 current_indent = 2
            elif re.match(r'^[A-Z]\.\s+', stripped_line):
                 markdown_lines.append(f"### {stripped_line}") # Assume H3
                 current_indent = 3
            elif re.match(r'^\d+\.\s+', stripped_line):
                 markdown_lines.append(f"#### {stripped_line}") # Assume H4
                 current_indent = 4
            # Default: Treat as a bullet point under the current indent level
            else:
                 # Indent based on the last heading or list item level seen
                 indent_prefix = "  " * max(0, current_indent -1) # Indent under the last heading/item
                 markdown_lines.append(f"{indent_prefix}- {stripped_line}")

        return "\n".join(markdown_lines)


    def create_list_view(self):
        """Create the list view for outline results."""
        view_id = "list-view"
        classes = "mb-6 p-4 bg-gray-50 rounded border border-gray-200"
        if self.active_tab_id != "list":
            classes += " hidden"

        if not self.outline_lines:
            return Div(P("No outline content generated.", cls="text-gray-500"), id=view_id, cls=classes)

        # Display lines using pre-wrap to respect original formatting/indentation
        list_items = [P(line or "\u00A0", # Use non-breaking space for empty lines to maintain structure
                        cls="whitespace-pre-wrap mb-1 font-mono text-sm leading-relaxed")
                      for line in self.outline_lines]

        return Div(*list_items, id=view_id, cls=classes)

    def create_card_view(self):
        """Create the card view (shows full outline in one scrollable card)."""
        view_id = "card-view"
        classes = "mb-6"
        if self.active_tab_id != "card":
             classes += " hidden"

        if not self.outline_lines:
            return Div(P("No outline content generated.", cls="text-gray-500"), id=view_id, cls=classes)

        card_content = [P(line or "\u00A0",
                          cls="whitespace-pre-wrap mb-1 font-mono text-sm leading-relaxed")
                        for line in self.outline_lines]

        return Div(
            Div(
                H3("Complete Outline", cls="text-lg font-semibold mb-3"),
                Div(*card_content, cls="max-h-[60vh] overflow-y-auto p-4 bg-gray-50 rounded border border-gray-200"),
                # Add a copy button for the card view content
                Button(
                    "Copy Outline", type="button",
                    cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-3 mr-2",
                    **{'data-copy-target': 'card-copy-source', 'data-copy-type': 'element'}
                ),
                P("", cls="copy-status text-green-600 inline-block"),
                # Hidden source for the card copy button
                Div("\n".join(self.outline_lines), id='card-copy-source', cls='hidden')
            ),
            id=view_id,
            cls=classes
        )

    def create_markdown_view(self):
        """Create the markdown view for outline results."""
        view_id = "markdown-view"
        classes = "mb-6"
        if self.active_tab_id != "markdown":
            classes += " hidden"

        return Div(
            H3("Markdown Format", cls="text-lg font-semibold mb-3"),
            Div(
                Textarea(
                    self.markdown_text,
                    id="markdown-content-textarea", # Unique ID for textarea
                    rows=15,
                    readonly=True,
                    cls="w-full p-3 border rounded font-mono text-sm bg-gray-50"
                ),
                 Button(
                    "Copy Markdown", type="button",
                    cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2 mr-2",
                    **{'data-copy-target': 'markdown-content-textarea', 'data-copy-type': 'textarea'} # Target the textarea
                ),
                P("", cls="copy-status text-green-600 inline-block"),
                cls="mb-4"
            ),
            Div(
                H4("Markdown Preview:", cls="text-md font-semibold mb-2"),
                create_markdown_viewer(self.markdown_text), # Use component for preview
                cls="mt-4"
            ),
            id=view_id,
            cls=classes
        )

    def create_copy_all_view(self):
        """Create the copy-all view for raw outline results."""
        view_id = "copy-view"
        classes = "mb-6"
        if self.active_tab_id != "copy":
            classes += " hidden"

        return Div(
            H3("Raw Outline Text", cls="text-lg font-semibold mb-3"),
            Textarea(
                self.all_content_text, # Use raw lines joined
                id="copy-all-content-textarea", # Unique ID
                rows=15,
                readonly=True,
                cls="w-full p-3 border rounded font-mono text-sm bg-gray-50"
            ),
             Button(
                "Copy Raw Text", type="button",
                cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2 mr-2",
                **{'data-copy-target': 'copy-all-content-textarea', 'data-copy-type': 'textarea'} # Target the textarea
            ),
            P("", cls="copy-status text-green-600 inline-block"),
            id=view_id,
            cls=classes
        )

    def create_views(self):
        """Create all views for the outline results."""
        return Div(
            self.create_list_view(),
            self.create_card_view(),
            self.create_markdown_view(),
            self.create_copy_all_view()
        )

    def create_tabs(self):
        """Create tabs for the outline results."""
        tabs_config = [
            {"id": "list", "label": "Outline View", "selected": self.active_tab_id == "list"},
            {"id": "card", "label": "Scrollable Card", "selected": self.active_tab_id == "card"},
            {"id": "markdown", "label": "Markdown", "selected": self.active_tab_id == "markdown"},
            {"id": "copy", "label": "Copy Raw", "selected": self.active_tab_id == "copy"}
        ]
        return create_tab_navigation(tabs_config)

    def render(self):
        """Render the outline results page."""
        return Div(
            H1(f"{self.tool.name} Results", cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
            P("Here is your generated outline:", cls="text-xl text-gray-600 mb-8 text-center"),
            Div(
                self.create_metadata_section(),
                self.create_tabs(),
                self.create_views(),
                self.create_navigation_buttons(),
                create_tab_switching_script(), # Link the main JS file
                # Script for zero-md needs to be loaded for the preview
                Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register"),
                cls="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md border border-gray-200", # Wider for outlines
                id="results-container" # Crucial ID for JS targeting
            )
        )