from fasthtml.common import *
from fasthtml.components import NotStr  # Changed from Raw to NotStr
from tools import get_all_tools, get_categories, get_tools_by_category

def create_tool_card(tool):
    """Create a card for a tool."""
    return A(
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
            cls="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow h-full"
        ),
        href=tool.route,
        cls="block h-full"
    )

def tools():
    """Generate the tools listing page with categories."""
    categories = get_categories()
    
    # If no categories, fall back to showing all tools without categories
    if not categories:
        tools_list = get_all_tools()
        tool_cards = [create_tool_card(tool) for tool in tools_list]
        
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
    
    # Create sections for each category
    category_sections = []
    
    for category in categories:
        tools_in_category = get_tools_by_category(category)
        
        if not tools_in_category:
            continue
        
        tool_cards = [create_tool_card(tool) for tool in tools_in_category]
        
        category_section = Div(
            H2(category,
               cls="text-2xl font-bold text-gray-800 mb-6 mt-12"),
            Div(
                *tool_cards,
                cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            ),
            cls="mb-8"
        )
        
        category_sections.append(category_section)
    
    return Div(
        H1("AI Tools",
           cls="text-3xl font-bold text-gray-800 mb-8 text-center"),
        P("Enhance your content creation with our AI-powered tools.",
          cls="text-xl text-gray-600 mb-8 text-center"),
        *category_sections,
        cls="container mx-auto px-4 py-8"
    )