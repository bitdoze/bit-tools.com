# components/page_layout.py

from fasthtml.common import *
from .header import header
from .footer import footer

def page_layout(title, content, current_page="/"):
    """
    Creates a consistent page layout with header and footer.

    Args:
        title: The page title
        content: The main content components
        current_page: The current page path

    Returns:
        A complete HTML page
    """
    return Html(
        Head(
            Title(title),
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Link(rel="icon", href="/static/images/favicon.svg", type="image/svg+xml"),
            Script(src="https://cdn.tailwindcss.com"),
            Script(defer=True, **{"data-domain": "bit-tools.com", "src": "https://an.bitdoze.com/js/script.js"}),
            # --- INCLUDE SITE-WIDE JS ---
            Script(src="/static/js/site.js", defer=True), # Use defer to load after HTML parsing
            # --- INCLUDE TOOL-SPECIFIC JS (if needed on results pages) ---
            # This should be added by the result page components/handlers now
            # Script(src="/static/js/tool-results.js", defer=True), # Removed from here
            # --- Optional: Zero-MD for markdown ---
            # Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register"),
        ),
        Body(
            Div(
                header(current_page), # Pass current_page to header
                Main(
                    Div(
                        content,
                        cls="container mx-auto px-4 py-8"
                    ),
                    cls="flex-grow"
                ),
                footer(),
                cls="flex flex-col min-h-screen bg-gray-50"
            )
        )
    )