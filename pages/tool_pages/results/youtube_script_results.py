# pages/tool_pages/results/youtube_script_results.py
from fasthtml.common import *
import re
from .base_results import BaseResultsHandler
from .components import create_tab_navigation, create_copy_button, create_tab_switching_script

class YoutubeScriptResultsHandler(BaseResultsHandler):
    """Handler for YouTube script tool results using structured data."""

    def __init__(self, tool_id, tool, results):
        """Initialize using structured results."""
        super().__init__(tool_id, tool, results)
        # Extract structured data provided by the factory
        self.script_content = results.get("script", "Script not generated.")
        self.hooks_list = results.get("hooks", [])
        self.bias_list = results.get("input_bias", [])
        self.questions_list = results.get("open_loop_questions", [])
        # 'titles' is the formatted string list for copy-all
        self.all_content_text = "\n".join(self.titles)
        self.active_tab_id = "script" # Default active tab

    def _create_list_section(self, title, items, item_prefix, section_id_prefix):
        """Helper to create a list section with copy buttons."""
        if not items:
            return P(f"No {title.lower()} generated.", cls="text-gray-500")

        item_elements = []
        for i, item in enumerate(items):
            item_text = re.sub(r'^\d+\.\s*', '', item).strip() # Clean numbering
            item_id_target = f"{section_id_prefix}-content-{i}"
            item_elements.append(
                Div(
                    P(f"{item_prefix}{item_text}", cls="mb-2 whitespace-pre-wrap text-sm"),
                    # Copy button component
                    create_copy_button(text_id=item_id_target),
                    Div(item_text, id=item_id_target, cls="hidden"), # Hidden source
                    cls="p-3 bg-white rounded shadow-sm border border-gray-200"
                )
            )
        return Div(
             H3(title, cls="text-lg font-semibold mb-3 text-center"),
             Div(*item_elements, cls="space-y-3") # Add spacing between items
        )


    def create_script_view(self):
        """Create the main script view."""
        view_id = "script-view"
        classes = "mb-6"
        if self.active_tab_id != "script":
            classes += " hidden"

        return Div(
            H3("Your YouTube Script", cls="text-xl font-bold mb-4 text-center"),
            # Display the script content
            Div(
                P(self.script_content, cls="whitespace-pre-wrap leading-relaxed"),
                cls="p-4 bg-gray-50 rounded border border-gray-200 mb-4",
                id="script-content-display" # ID for the display element
            ),
            # Copy button for the script
            Button(
                "Copy Script", type="button",
                cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2",
                # Target the hidden div containing the raw script text
                **{'data-copy-target': 'script-content-source'}
            ),
            P("", cls="copy-status text-green-600 inline-block"),
            # Hidden div containing the raw script text for copying
            Div(self.script_content, id="script-content-source", cls="hidden"),
            id=view_id,
            cls=classes
        )

    def create_hooks_view(self):
        """Create the hooks view."""
        view_id = "hooks-view"
        classes = "mb-6"
        if self.active_tab_id != "hooks":
             classes += " hidden"

        return Div(
            self._create_list_section("Compelling Hooks", self.hooks_list, "Hook: ", "hook"),
            id=view_id,
            cls=classes
        )

    def create_bias_view(self):
        """Create the input bias view."""
        view_id = "bias-view"
        classes = "mb-6"
        if self.active_tab_id != "bias":
             classes += " hidden"

        return Div(
            self._create_list_section("Input Bias Statements", self.bias_list, "Bias: ", "bias"),
            id=view_id,
            cls=classes
        )

    def create_questions_view(self):
        """Create the open loop questions view."""
        view_id = "questions-view"
        classes = "mb-6"
        if self.active_tab_id != "questions":
             classes += " hidden"

        return Div(
            self._create_list_section("Open Loop Questions", self.questions_list, "Q: ", "question"),
            id=view_id,
            cls=classes
        )

    def create_copy_all_view(self):
        """Create the copy-all view using formatted 'titles'."""
        view_id = "copy-view"
        classes = "mb-6"
        if self.active_tab_id != "copy":
            classes += " hidden"

        return Div(
            H3("Complete Output (Formatted Text)", cls="text-lg font-semibold mb-3"),
            Textarea(
                self.all_content_text,
                id="copy-all-script-textarea", # Unique ID
                rows=20, # Make it taller for scripts
                readonly=True,
                cls="w-full p-3 border rounded font-mono text-sm bg-gray-50"
            ),
            Button(
                "Copy All Formatted Text", type="button",
                cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2 mr-2",
                **{'data-copy-target': 'copy-all-script-textarea', 'data-copy-type': 'textarea'}
            ),
            P("", cls="copy-status text-green-600 inline-block"),
            id=view_id,
            cls=classes
        )

    def create_views(self):
        """Create all views for the YouTube script results."""
        return Div(
            self.create_script_view(),
            self.create_hooks_view(),
            self.create_bias_view(),
            self.create_questions_view(),
            self.create_copy_all_view()
        )

    def create_tabs(self):
        """Create tabs for the YouTube script results."""
        tabs_config = [
            {"id": "script", "label": "Script", "selected": self.active_tab_id == "script"},
            {"id": "hooks", "label": "Hooks", "selected": self.active_tab_id == "hooks"},
            {"id": "bias", "label": "Input Bias", "selected": self.active_tab_id == "bias"},
            {"id": "questions", "label": "Questions", "selected": self.active_tab_id == "questions"},
            {"id": "copy", "label": "Copy Formatted", "selected": self.active_tab_id == "copy"}
        ]
        return create_tab_navigation(tabs_config)

    def render(self):
        """Render the YouTube script results page."""
        return Div(
            H1(f"{self.tool.name} Results", cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
            P("Here is your generated YouTube script content:", cls="text-xl text-gray-600 mb-8 text-center"),
            Div(
                self.create_metadata_section(),
                self.create_tabs(),
                self.create_views(),
                self.create_navigation_buttons(),
                create_tab_switching_script(), # Link the main JS file
                cls="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md border border-gray-200", # Wider
                id="results-container" # Crucial ID for JS targeting
            )
        )