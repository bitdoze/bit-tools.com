# pages/tool_pages/results/components.py
from fasthtml.common import *
from fasthtml.components import NotStr

def create_tab_navigation(tabs):
    """
    Create tab navigation UI.

    Args:
        tabs: List of tab dictionaries with id, label, and selected keys

    Returns:
        Component representing the tab navigation
    """
    return Div(
        *[
            Button(
                tab["label"],
                type="button",
                id=f"tab-{tab['id']}",
                # Using inline onclick which calls the function in tool-results.js
                onclick=f"switchTab('{tab['id']}')",
                # Dynamically set classes based on 'selected' status
                cls=f"px-4 py-2 rounded-t {'bg-white text-blue-600 font-bold' if tab['selected'] else 'bg-gray-200 text-gray-700'}"
            )
            for tab in tabs
        ],
        cls="flex border-b border-gray-300 mb-4" # Added border-b for visual separation
    )

def create_copy_button(text_id, button_id=None, status_id=None):
    """
    Create a copy button with status indicator, relying on external JS.

    Args:
        text_id: ID of the element containing the text to copy (or the text itself if simple)
        button_id: Optional ID for the copy button (usually not needed)
        status_id: Optional ID for the status message element (usually not needed)

    Returns:
        Component representing the copy button and status
    """
    # Button uses data-copy-target to link to the text source
    # JS will find the status element as the next sibling
    return Div(
        Button(
            "Copy",
            type="button",
            # Use class for JS targeting
            cls="copy-button bg-blue-600 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded text-sm mr-2",
            **{'data-copy-target': text_id} # Crucial data attribute for JS
        ),
        # Status element immediately follows the button
        P("", cls="copy-status text-green-600 inline-block text-sm"),
        cls="mt-2 flex items-center"
    )

def create_loading_overlay():
    """
    Create a loading overlay.

    Returns:
        Component representing the loading overlay
    """
    return Div(
        Div(
            Div(cls="w-12 h-12 rounded-full border-4 border-blue-600 border-t-transparent animate-spin"),
            P("Processing your request...", cls="mt-4 text-lg text-blue-600"),
            cls="flex flex-col items-center"
        ),
        id="loading-overlay",
        cls="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    )

def create_tab_switching_script():
    """
    Create the JavaScript link for tab switching and copying.

    Returns:
        Script component linking to the external JS file.
    """
    # Just return the script tag linking to the consolidated JS file
    return Script(src="/static/js/tool-results.js")

def create_copy_script(element_id, button_id, status_id):
    """
    Legacy function - no longer needed as logic is in external JS.

    Returns:
        An empty Div component.
    """
    # Return an empty div since we're using the external script
    return Div()

def create_markdown_viewer(markdown_text):
    """
    Create a markdown viewer component using zero-md.

    Args:
        markdown_text: The markdown text to display

    Returns:
        Component representing the markdown viewer
    """
    # Ensure zero-md script is loaded (might be better in page_layout if used widely)
    # Using NotStr to embed the web component tag and template
    return Div(
        Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register"),
        NotStr(f"""
        <zero-md>
            <template>
                <style>
                    /* Basic styling within the shadow DOM */
                    :host {{ display: block; }} /* Ensure it takes block space */
                    .markdown-body {{
                        background-color: transparent !important; /* Override default bg */
                        color: inherit !important; /* Inherit text color */
                        padding: 0 !important; /* Remove default padding */
                        font-family: inherit !important; /* Use surrounding font */
                        font-size: 0.9rem; /* Slightly smaller font for preview */
                        line-height: 1.6;
                    }}
                    .markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4, .markdown-body h5, .markdown-body h6 {{
                        margin-top: 1em !important;
                        margin-bottom: 0.5em !important;
                        font-weight: 600 !important;
                        line-height: 1.25 !important;
                        color: #1a202c; /* Dark gray for headings */
                        border-bottom: none; /* Remove default borders */
                    }}
                    .markdown-body h2 {{ font-size: 1.25em !important; }}
                    .markdown-body h3 {{ font-size: 1.1em !important; }}
                    .markdown-body ul, .markdown-body ol {{
                        margin-left: 1.5rem !important; /* Indentation */
                        margin-bottom: 1rem !important;
                        padding-left: 0 !important;
                    }}
                    .markdown-body ul {{ list-style-type: disc !important; }}
                    .markdown-body ol {{ list-style-type: decimal !important; }}
                    .markdown-body li {{ margin-bottom: 0.25rem !important; }}
                    .markdown-body p {{ margin-bottom: 0.75rem !important; }}
                    .markdown-body code {{
                        background-color: #edf2f7; /* Light gray background */
                        color: #2d3748; /* Darker gray text */
                        padding: 0.2em 0.4em;
                        border-radius: 3px;
                        font-size: 85%;
                    }}
                    .markdown-body pre > code {{
                        padding: 0;
                        background-color: transparent;
                    }}
                    .markdown-body pre {{
                        background-color: #f7fafc; /* Very light gray */
                        padding: 1em;
                        border-radius: 5px;
                        overflow: auto;
                        margin-bottom: 1rem;
                    }}
                </style>
            </template>
            <script type="text/markdown">
{markdown_text}
            </script>
        </zero-md>
        """),
        cls="p-4 bg-gray-50 rounded border border-gray-200 overflow-auto max-h-96" # Added border, adjusted max-h
    )