# pages/tool_pages/results/thumbnail_results.py
from fasthtml.common import *
from .base_results import BaseResultsHandler
from .components import create_tab_navigation, create_copy_button, create_tab_switching_script

class ThumbnailResultsHandler(BaseResultsHandler):
    """Handler for YouTube Thumbnail Ideas results using structured data."""

    def __init__(self, tool_id, tool, results):
        """Initialize using structured results."""
        super().__init__(tool_id, tool, results)
        # The factory should place the list of idea dicts into 'ideas'
        self.ideas_list = results.get("ideas", [])
        # 'titles' created by factory is a formatted string list for display/copy-all
        self.all_content_text = "\n".join(self.titles)
        self.active_tab_id = "list" # Default active tab

    def create_list_view(self):
        """Create the list view for thumbnail ideas."""
        view_id = "list-view"
        classes = "mb-6 space-y-4" # Add space between items
        if self.active_tab_id != "list":
            classes += " hidden"

        if not self.ideas_list:
             return Div(P("No thumbnail ideas generated.", cls="text-gray-500"), id=view_id, cls=classes)

        list_items = []
        for i, idea in enumerate(self.ideas_list):
            idea_id_target = f"list-idea-content-{i}"
            # Ensure idea is a dict, fallback if it's somehow a string
            if not isinstance(idea, dict): idea = {"text": str(idea)}

            # Prepare content lines for display
            content_lines = [
                P(Span("Background: ", cls="font-semibold"), f"{idea.get('background', 'N/A')}", cls="mb-1 text-sm"),
                P(Span("Main Image: ", cls="font-semibold"), f"{idea.get('main_image', 'N/A')}", cls="mb-1 text-sm"),
                P(Span("Text: ", cls="font-semibold"), f"{idea.get('text', 'N/A')}", cls="mb-1 text-sm"),
                P(Span("Elements: ", cls="font-semibold"), f"{idea.get('additional_elements', 'N/A')}", cls="mb-1 text-sm"),
            ]
            # Prepare text for the copy button
            copy_text = "\n".join([
                f"Background: {idea.get('background', 'N/A')}",
                f"Main Image: {idea.get('main_image', 'N/A')}",
                f"Text: {idea.get('text', 'N/A')}",
                f"Elements: {idea.get('additional_elements', 'N/A')}"
            ])

            list_items.append(
                Div(
                    H4(f"Thumbnail Idea {i+1}", cls="text-lg font-bold mb-2 text-blue-700"),
                    *content_lines,
                    # Copy button and status (using component)
                    create_copy_button(text_id=idea_id_target),
                    Div(copy_text, id=idea_id_target, cls="hidden"), # Hidden content for copy
                    cls="p-4 bg-white rounded shadow border border-gray-200"
                )
            )

        return Div(*list_items, id=view_id, cls=classes)

    def create_card_view(self):
        """Create the card view for thumbnail ideas."""
        view_id = "card-view"
        classes = "mb-6"
        if self.active_tab_id != "card":
             classes += " hidden"

        if not self.ideas_list:
            return Div(P("No thumbnail ideas generated.", cls="text-gray-500"), id=view_id, cls=classes)

        card_items = []
        for i, idea in enumerate(self.ideas_list):
             idea_id_target = f"card-idea-content-{i}"
             if not isinstance(idea, dict): idea = {"text": str(idea)}

             copy_text = "\n".join([
                f"Background: {idea.get('background', 'N/A')}",
                f"Main Image: {idea.get('main_image', 'N/A')}",
                f"Text: {idea.get('text', 'N/A')}",
                f"Elements: {idea.get('additional_elements', 'N/A')}"
             ])

             card_items.append(
                Div(
                    H4(f"Idea {i+1}", cls="text-md font-bold mb-2 text-center text-blue-700"),
                    P(f"{idea.get('text', 'N/A')}", cls="text-center text-sm mb-1 font-semibold max-h-24 overflow-auto whitespace-pre-wrap"), # Scrollable with max height
                    P(f"Image: {idea.get('main_image', 'N/A')}", cls="text-center text-xs text-gray-600 mb-3 max-h-24 overflow-auto whitespace-pre-wrap"), # Scrollable with max height
                    # Copy button and status (using component)
                    create_copy_button(text_id=idea_id_target),
                    Div(copy_text, id=idea_id_target, cls="hidden"), # Hidden content for copy
                    cls="p-4 bg-white rounded shadow border border-gray-200 flex flex-col justify-between"
                )
             )

        return Div(
            Div(*card_items, cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"),
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
            H3("All Ideas (Formatted Text)", cls="text-lg font-semibold mb-3"),
            Textarea(
                self.all_content_text, # Use pre-formatted text from 'titles'
                id="copy-all-ideas-textarea", # Unique ID
                rows=15,
                readonly=True,
                cls="w-full p-3 border rounded font-mono text-sm bg-gray-50"
            ),
             Button(
                "Copy All Formatted Text", type="button",
                cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2 mr-2",
                **{'data-copy-target': 'copy-all-ideas-textarea', 'data-copy-type': 'textarea'}
            ),
            P("", cls="copy-status text-green-600 inline-block"),
            id=view_id,
            cls=classes
        )

    def create_views(self):
        """Create all views for the thumbnail results."""
        return Div(
            self.create_list_view(),
            self.create_card_view(),
            self.create_copy_all_view()
        )

    def create_tabs(self):
        """Create tabs for the thumbnail results."""
        tabs_config = [
            {"id": "list", "label": "List View", "selected": self.active_tab_id == "list"},
            {"id": "card", "label": "Card View", "selected": self.active_tab_id == "card"},
            {"id": "copy", "label": "Copy Formatted", "selected": self.active_tab_id == "copy"}
        ]
        return create_tab_navigation(tabs_config)


    def render(self):
        """Render the thumbnail results page."""
        return Div(
            H1(f"{self.tool.name} Results", cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
            P("Here are your generated thumbnail ideas:", cls="text-xl text-gray-600 mb-8 text-center"),
            Div(
                self.create_metadata_section(),
                self.create_tabs(),
                self.create_views(),
                self.create_navigation_buttons(),
                create_tab_switching_script(), # Link the main JS file
                cls="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md border border-gray-200", # Increased width
                id="results-container" # Crucial ID for JS targeting
            )
        )