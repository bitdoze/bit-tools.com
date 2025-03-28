# pages/tool_pages/results/transformation_results.py
from fasthtml.common import *
import json
from .base_results import BaseResultsHandler
from .components import create_copy_button, create_tab_switching_script # Import script link

class TransformationResultsHandler(BaseResultsHandler):
    """Handler for transformation tool results (e.g., rephrasing)."""

    def __init__(self, tool_id, tool, results):
        """Initialize the transformation results handler."""
        super().__init__(tool_id, tool, results)
        self.original_text = results.get("original_text", "Original text not provided.")
        self.transformed_text = results.get("transformed_text", "Transformation failed or no text generated.")

    def create_before_after_view(self):
        """Create the before/after view for transformation results."""
        # No tabs needed, so this is the main content view
        return Div(
            # Original Text Section
            Div(
                H3("Original Text", cls="text-lg font-bold mb-2 text-gray-700"),
                Div(
                    P(self.original_text, cls="whitespace-pre-wrap text-sm leading-relaxed"),
                    cls="p-4 bg-gray-100 rounded border border-gray-200 mb-6 max-h-72 overflow-y-auto" # Scrollable
                ),
                cls="mb-6"
            ),
            # Transformed Text Section
            Div(
                H3("Transformed Text", cls="text-lg font-bold mb-2 text-blue-700"),
                Div(
                    P(self.transformed_text, cls="whitespace-pre-wrap text-sm leading-relaxed"),
                    # Add an ID to the container div for easier targeting if needed
                    id="transformed-text-content-display",
                    cls="p-4 bg-blue-50 rounded border border-blue-200 mb-4 max-h-72 overflow-y-auto" # Scrollable
                ),
                # Copy button targeting the hidden source div
                Button(
                    "Copy Transformed Text", type="button",
                    cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2",
                    **{'data-copy-target': 'transformed-text-content-source'}
                ),
                P("", cls="copy-status text-green-600 inline-block"),
                # Hidden div containing the raw transformed text for copying
                Div(self.transformed_text, id="transformed-text-content-source", cls="hidden"),
                cls="mb-6"
            ),
        )

    def render(self):
        """Render the transformation results page."""
        # Transformation results don't typically have tabs
        return Div(
            H1(f"{self.tool.name} Results", cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
            P("Here is your transformed text:", cls="text-xl text-gray-600 mb-8 text-center"),
            Div(
                self.create_metadata_section(),
                # No Tabs needed for simple before/after
                self.create_before_after_view(),
                self.create_navigation_buttons(),
                create_tab_switching_script(), # Link the main JS file for copy button
                cls="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-md border border-gray-200", # Increased width slightly
                id="results-container" # Crucial ID for JS targeting
            )
        )