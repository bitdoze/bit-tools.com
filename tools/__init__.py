from .title_generator import TitleGenerator

# Create an instance of the tool
title_generator = TitleGenerator()

# Registry of all available tools
TOOLS = {
    title_generator.id: title_generator,  # Use the tool's ID property
}

def get_all_tools():
    """Return all registered tools."""
    return list(TOOLS.values())

def get_tool_by_id(tool_id):
    """Get a tool by its ID."""
    return TOOLS.get(tool_id)