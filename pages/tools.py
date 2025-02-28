from fasthtml.common import *
from tools import get_all_tools

def tools():
    """
    Defines the tools overview page.
    
    Returns:
        Components representing the tools page content
    """
    # Get all registered tools
    all_tools = get_all_tools()
    
    # Create tool cards
    tool_cards = []
    for tool in all_tools:
        tool_cards.append(
            Div(
                Div(
                    H2(tool.name, cls="text-2xl font-semibold mb-2"),
                    P(tool.description, cls="text-gray-600 mb-4"),
                    A("Use Tool",
                      href=tool.route,
                      cls="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
                    cls="p-6"
                ),
                cls="bg-white rounded-lg shadow-md transition-transform hover:scale-105"
            )
        )
    
    return Div(
        # Page header
        H1("AI Tools",
           cls="text-3xl font-bold text-gray-800 mb-6 text-center"),
           
        P("Explore our collection of AI-powered tools to help with your creative and productivity needs.",
          cls="text-xl text-gray-600 mb-8 text-center"),
        
        # Tools grid
        Div(
            *tool_cards,
            cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        )
    )