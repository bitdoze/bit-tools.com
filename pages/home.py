from fasthtml.common import *
from fasthtml.components import NotStr
from tools import get_all_tools
from component.social_icons import social_icons

def home():
    """
    Defines the home page content.

    Returns:
        Components representing the home page content
    """
    # Get tools for display
    tools_list = get_all_tools()
    
    return Div(
        # Hero section with social icons
        Div(
            Div(
                Div(
                    H1(
                        "Welcome to ",
                        Span("Bit Tools", 
                             cls="bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-indigo-500 sm:whitespace-nowrap"),
                        cls="text-5xl md:text-[3.50rem] font-bold leading-tighter tracking-tighter mb-4 font-heading"
                    ),
                    Div(
                        P("Create engaging content with our AI-powered tools.",
                          cls="text-xl text-gray-600 mb-8"),
                        cls="max-w-3xl mx-auto"
                    ),
                    # Use the social icons component
                    social_icons(),
                    cls="text-center pb-10 md:pb-16"
                ),
                cls="py-12 md:py-20"
            ),
            cls="max-w-6xl mx-auto px-4 sm:px-6"
        ),

        # Tools section (replacing Key Features)
        Div(
            H2("Our Tools", cls="text-3xl font-bold text-center mb-8"),
            Div(
                *[
                    Div(
                        Div(
                            Div(
                                NotStr(tool.icon),
                                cls="text-blue-600 w-12 h-12 mr-4"
                            ),
                            Div(
                                H3(tool.name, cls="text-xl font-semibold mb-2"),
                                P(tool.description, cls="text-gray-600"),
                                cls="flex-1"
                            ),
                            cls="flex items-start"
                        ),
                        A("Try it now →", 
                          href=tool.route,
                          cls="mt-4 inline-block text-blue-600 hover:text-blue-800 font-medium"),
                        cls="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
                    )
                    for tool in tools_list
                ],
                cls="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12"
            ),
            cls="py-8 max-w-6xl mx-auto px-4 sm:px-6"
        ),
        cls="relative overflow-hidden"  # Moved this to be the last argument of the outer Div
    )
