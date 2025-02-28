from fasthtml.common import *


def header(current_page="/"):
    """
    Creates a consistent header with navigation.

    Args:
        current_page: The current page path, used to highlight the active link

    Returns:
        A Header component with navigation
    """
    # Define the SVG logo as a string
    logo_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="300" height="60">
  <!-- AI Logo Element on Left -->
  <g fill="white">
    <!-- Brain/Circuit Node Design -->
    <circle cx="60" cy="50" r="25" fill="none" stroke="white" stroke-width="2"/>
    <circle cx="60" cy="50" r="4"/>
    
    <!-- Connection Lines -->
    <line x1="60" y1="25" x2="60" y2="15" stroke="white" stroke-width="2"/>
    <line x1="60" y1="75" x2="60" y2="85" stroke="white" stroke-width="2"/>
    <line x1="35" y1="50" x2="25" y2="50" stroke="white" stroke-width="2"/>
    <line x1="85" y1="50" x2="95" y2="50" stroke="white" stroke-width="2"/>
    
    <!-- Neural Network Nodes -->
    <circle cx="60" cy="15" r="4"/>
    <circle cx="60" cy="85" r="4"/>
    <circle cx="25" cy="50" r="4"/>
    <circle cx="95" cy="50" r="4"/>
    
    <!-- Additional Connection Lines -->
    <line x1="43" y1="33" x2="35" y2="25" stroke="white" stroke-width="2"/>
    <line x1="77" y1="33" x2="85" y2="25" stroke="white" stroke-width="2"/>
    <line x1="43" y1="67" x2="35" y2="75" stroke="white" stroke-width="2"/>
    <line x1="77" y1="67" x2="85" y2="75" stroke="white" stroke-width="2"/>
    
    <!-- Additional Nodes -->
    <circle cx="35" cy="25" r="4"/>
    <circle cx="85" cy="25" r="4"/>
    <circle cx="35" cy="75" r="4"/>
    <circle cx="85" cy="75" r="4"/>
  </g>
  
  <!-- Text "Bit Tools" on Right -->
  <text x="120" y="60" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="white">Bit Tools</text>
</svg>'''

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
            A(
                NotStr(logo_svg),  # Use NotStr to prevent HTML escaping
                href="/",
                cls="flex items-center"
            ),
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