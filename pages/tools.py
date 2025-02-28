from fasthtml.common import *
from fasthtml.components import NotStr  # Changed from Raw to NotStr
from tools import get_all_tools

def tools():
    """Generate the tools listing page."""
    tools_list = get_all_tools()
    
    tool_cards = []
    for tool in tools_list:
        tool_cards.append(
            A(
                Div(
                    # Tool icon - using NotStr for SVG rendering
                    Div(
                        NotStr(tool.icon),  # Changed from Raw to NotStr
                        cls="text-blue-600 mb-4"
                    ),
                    H2(tool.name, 
                       cls="text-xl font-bold text-gray-800 mb-2"),
                    P(tool.description,
                      cls="text-gray-600"),
                    cls="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
                ),
                href=tool.route,
                cls="block"
            )
        )
    
    return Div(
        H1("AI Tools",
           cls="text-3xl font-bold text-gray-800 mb-8 text-center"),
        P("Enhance your content creation with our AI-powered tools.",
          cls="text-xl text-gray-600 mb-12 text-center"),
        Div(
            *tool_cards,
            cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        ),
        cls="container mx-auto px-4 py-8"
    )