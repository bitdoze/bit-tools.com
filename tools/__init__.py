from .title_generator import title_generator_tool
from .social_post_generator import social_post_generator_tool

_tools = {
    "ai-title-generator": title_generator_tool,  # Updated this line
    "social-media-post-generator": social_post_generator_tool
}

def get_all_tools():
    """Get all available tools."""
    return list(_tools.values())

def get_tool_by_id(tool_id):
    """Get a specific tool by ID."""
    return _tools.get(tool_id)