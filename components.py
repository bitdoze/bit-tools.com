from fasthtml.common import *

def header(current_page="/"):
    """
    Creates a consistent header with navigation.

    Args:
        current_page: The current page path, used to highlight the active link

    Returns:
        A Header component with navigation
    """
    # Define the navigation links
    nav_items = [
        ("Home", "/"),
        ("Tools", "/tools"),  # Added Tools link
        ("About", "/about"),
        ("Contact", "/contact")
    ]

    # Create navigation items with appropriate styling
    nav_links = []
    for title, path in nav_items:
        # Apply special styling to the current page link
        is_current = current_page == path or (
            current_page.startswith("/tools/") and path == "/tools"
        )
        link_class = "text-white hover:text-gray-300 px-3 py-2"
        if is_current:
            link_class += " font-bold underline"

        nav_links.append(
            Li(
                A(title, href=path, cls=link_class)
            )
        )

    return Header(
        Div(
            # Website logo/name
            A("Bit Tools", href="/", cls="text-xl font-bold text-white"),

            # Navigation menu
            Nav(
                Ul(
                    *nav_links,
                    cls="flex space-x-2"
                ),
                cls="ml-auto"
            ),
            cls="container mx-auto flex items-center justify-between px-4 py-3"
        ),
        cls="bg-blue-600 shadow-md"
    )

def footer():
    """Creates a consistent footer."""
    return Footer(
        Div(
            P("© 2023 Bit Tools. All rights reserved.", cls="text-center text-gray-500"),
            cls="container mx-auto px-4 py-6"
        ),
        cls="bg-gray-100 mt-auto"
    )

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
            Script(src="https://cdn.tailwindcss.com"),
            # Added analytics script
            Script(defer=True, **{"data-domain": "bit-tools.com", "src": "https://an.bitdoze.com/js/script.js"}),
        ),
        Body(
            Div(
                header(current_page),
                Main(
                    Div(
                        content,
                        cls="container mx-auto px-4 py-8"
                    ),
                    cls="flex-grow"
                ),
                footer(),
                cls="flex flex-col min-h-screen"
            )
        )
    )
