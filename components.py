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
        ("About", "/about"),
        ("Contact", "/contact")
    ]

    # Create navigation items with appropriate styling
    nav_links = []
    for title, path in nav_items:
        # Apply special styling to the current page link
        is_current = current_page == path
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
            A("bit-tools.com", href="/", cls="text-xl font-bold text-white"),

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
    """
    Creates a consistent footer for all pages.

    Returns:
        A Footer component with copyright and links
    """
    current_year = 2025  # In a real app, use datetime to get current year

    return Footer(
        Div(
            Div(
                P(f"© {current_year} bit-tools.com. All rights reserved.",
                  cls="text-gray-500"),
                cls="mb-4"
            ),
            Div(
                A("Privacy Policy", href="#", cls="text-blue-500 hover:underline mr-4"),
                A("Terms of Service", href="#", cls="text-blue-500 hover:underline"),
                cls="text-sm"
            ),
            cls="container mx-auto px-4 py-6 text-center"
        ),
        cls="bg-gray-100 mt-8"
    )

def page_layout(title, content, current_page="/"):
    """
    Wraps page content with consistent header, footer, and styling.

    Args:
        title: The page title (appears in browser tab)
        content: The main content of the page
        current_page: The current page path for navigation highlighting

    Returns:
        A complete HTML page with header, content, and footer
    """
    return Html(
        Head(
            Title(title),
            # Meta tags for better SEO and mobile display
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Meta(name="description", content=f"{title} - MyWebsite built with FastHTML"),
            # Include Tailwind CSS for styling
            Script(src="https://cdn.tailwindcss.com")
        ),
        Body(
            # Include header with current page highlighted
            header(current_page),

            # Main content area
            Main(
                Div(
                    content,
                    cls="container mx-auto px-4 py-8"
                ),
                cls="min-h-screen"  # Ensures footer stays at bottom
            ),

            # Include footer
            footer()
        )
    )
