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
                onclick=f"switchTab('{tab['id']}')",
                cls=f"px-4 py-2 rounded-t {'bg-white text-blue-600 font-bold' if tab['selected'] else 'bg-gray-200 text-gray-700'}"
            )
            for tab in tabs
        ],
        cls="flex mb-4"
    )

def create_copy_button(text_id, button_id, status_id):
    """
    Create a copy button with status indicator.
    
    Args:
        text_id: ID of the element containing the text to copy
        button_id: ID for the copy button
        status_id: ID for the status message element
        
    Returns:
        Component representing the copy button and status
    """
    return Div(
        Button(
            "Copy",
            type="button",
            id=button_id,
            cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
        ),
        P("", id=status_id, cls="text-green-600 inline-block"),
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
    Create the JavaScript for tab switching.
    
    Returns:
        Script component with tab switching functionality
    """
    return Script(src="/static/js/tool-results.js")

def create_copy_script(element_id, button_id, status_id):
    """
    Create the JavaScript for copying text.
    
    Args:
        element_id: ID of the element containing the text to copy
        button_id: ID of the copy button
        status_id: ID of the status message element
        
    Returns:
        Script component with copy functionality
    """
    # This functionality is now included in tool-results.js
    return Div()  # Return an empty div since we're using the external script

def create_markdown_viewer(markdown_text):
    """
    Create a markdown viewer component.
    
    Args:
        markdown_text: The markdown text to display
        
    Returns:
        Component representing the markdown viewer
    """
    return Div(
        # Zero-md script for markdown rendering
        Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register"),
        
        # Markdown content
        NotStr(f"""
        <zero-md>
            <template>
                <style>
                    .markdown-body {{
                        background-color: transparent !important;
                        color: inherit !important;
                        padding: 0 !important;
                        font-family: system-ui, sans-serif !important;
                    }}
                    .markdown-body h2 {{
                        font-size: 1.25rem !important;
                        font-weight: bold !important;
                        margin-top: 1rem !important;
                        margin-bottom: 0.5rem !important;
                        color: #1a202c !important;
                    }}
                    .markdown-body ul {{
                        list-style-type: disc !important;
                        margin-left: 1.5rem !important;
                        margin-bottom: 1rem !important;
                        padding-left: 0 !important;
                    }}
                    .markdown-body li {{
                        margin-bottom: 0.25rem !important;
                        line-height: 1.5 !important;
                    }}
                    .markdown-body p {{
                        margin-bottom: 0.5rem !important;
                        line-height: 1.5 !important;
                    }}
                </style>
            </template>
            <script type="text/markdown">
{markdown_text}
            </script>
        </zero-md>
        """),
        cls="p-4 bg-gray-50 rounded overflow-auto max-h-80"
    )
