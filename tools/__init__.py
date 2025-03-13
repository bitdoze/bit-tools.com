# Import the registry
from .core.registry import registry

# Import tool implementations to ensure they're registered
from .implementations import blog_outline_generator
from .implementations import social_post_generator
# Import title and thumbnail generators directly
from .implementations.title_generator import title_generator_tool
from .implementations.thumbnail_generator import thumbnail_generator_tool
from .implementations.youtube_script_generator import youtube_script_generator_tool

def get_all_tools():
    """Get all available tools."""
    return registry.get_all_tools()

def get_tool_by_id(tool_id):
    """Get a specific tool by ID."""
    return registry.get_tool(tool_id)

def get_tools_by_category(category):
    """Get all tools in a specific category."""
    return registry.get_tools_by_category(category)

def get_categories():
    """Get all tool categories."""
    return registry.get_categories()
