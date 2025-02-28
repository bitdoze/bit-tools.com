from fasthtml.common import *

def header(current_page="/"):
    """
    Creates a consistent header with navigation.

    Args:
        current_page: The current page path, used to highlight the active link

    Returns:
        A Header component with navigation
    """
    nav_items = [
        ("Home", "/"),
        ("Tools", "/tools"),
        ("About", "/about"),
        ("Contact", "/contact")
    ]

    nav_links = []
    for title, path in nav_items:
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
            A("Bit Tools", href="/", cls="text-xl font-bold text-white"),
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