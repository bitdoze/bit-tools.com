# components/header.py

from fasthtml.common import *
# --- Import NotStr ---
from fasthtml.components import NotStr
# ---------------------

def header(current_page="/"):
    """
    Creates a consistent header with navigation menu on the right (desktop)
    and a working mobile menu toggle using NotStr for the SVG icon.
    """
    # --- Define Navigation Items (remains the same) ---
    nav_items = [
        ("Home", "/"),
        ("Tools", "/tools"),
        ("About", "/about"),
        ("Contact", "/contact")
    ]

    # --- Create Desktop Navigation Links (remains the same) ---
    desktop_nav_links = []
    for title, path in nav_items:
        is_current = current_page == path or (
            path == "/tools" and current_page.startswith("/tools/")
        )
        link_class = "text-white hover:text-gray-200 px-3 py-2 rounded-md text-sm font-medium transition-colors"
        if is_current:
            link_class += " bg-blue-700"
        desktop_nav_links.append(A(title, href=path, cls=link_class))

    # --- Create Mobile Navigation Links (remains the same) ---
    mobile_nav_links = []
    for title, path in nav_items:
        is_current = current_page == path or (
             path == "/tools" and current_page.startswith("/tools/")
        )
        link_class = "block rounded-md px-3 py-2 text-base font-medium"
        if is_current:
            link_class += " bg-blue-700 text-white"
        else:
            link_class += " text-gray-300 hover:bg-blue-700 hover:text-white"
        mobile_nav_links.append(A(title, href=path, cls=link_class))

    # --- Define the SVG string for the hamburger icon ---
    hamburger_svg_string = '''
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="block h-6 w-6">
      <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
    </svg>
    '''
    # Note: We use stroke="currentColor" here, which should inherit the button's text color.
    # If it still fails, change it directly in the string to stroke="white" or stroke="#E5E7EB"

    # --- Return the Header Component Structure ---
    return Header(
        Nav(
            Div( # Main container for header content (inside Nav)
                # Logo on the left (remains the same)
                A(
                    Img(src="/static/images/logo.svg",
                        alt="Bit Tools Logo",
                        cls="block h-10 w-auto"),
                    href="/",
                    cls="flex-shrink-0 flex items-center"
                ),

                # Desktop Navigation Links Container (remains the same)
                Div(
                    Div(
                        *desktop_nav_links,
                        cls="flex space-x-4"
                    ),
                    cls="hidden sm:ml-auto sm:flex sm:items-center"
                ),

                # --- Mobile Menu Button Container ---
                Div( # Container for the button
                    Button(
                        Span("Open main menu", cls="sr-only"),
                        # --- Use NotStr to inject the SVG string ---
                        NotStr(hamburger_svg_string),
                        # -------------------------------------------
                        type="button",
                        id="mobile-menu-button",
                        # Apply text color to the button for currentColor to work in SVG
                        cls="inline-flex items-center justify-center rounded-md p-2 text-gray-200 hover:text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white",
                        aria_controls="mobile-menu",
                        aria_expanded="false"
                    ),
                    # Container positioning
                    cls="ml-auto flex items-center sm:hidden z-10"
                ),
                cls="relative flex h-16 items-center justify-between"
            ),
            cls="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8"
        ),

        # Mobile Menu Panel (Dropdown - unchanged)
        Div(
            Div(
                *mobile_nav_links,
                cls="space-y-1 px-2 pb-3 pt-2"
            ),
            id="mobile-menu",
            cls="sm:hidden hidden"
        ),
        cls="bg-blue-600 shadow-md"
    )