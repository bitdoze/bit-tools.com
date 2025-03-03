# Import the registry
from .registry import registry

# Import tool modules to ensure they're registered
# Note: We don't need to register them here as they're already registered in their respective files
from . import title_generator
from . import social_post_generator
from . import blog_outline_generator

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