from typing import Dict, List, Optional
from .base import BaseTool

class ToolRegistry:
    """Registry for managing AI tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._categories: Dict[str, List[str]] = {}
    
    def register(self, tool: BaseTool, categories: Optional[List[str]] = None):
        """Register a tool with optional categories."""
        tool_id = tool.id
        self._tools[tool_id] = tool
        
        # Register categories
        if categories:
            for category in categories:
                if category not in self._categories:
                    self._categories[category] = []
                self._categories[category].append(tool_id)
    
    def get_tool(self, tool_id: str) -> Optional[BaseTool]:
        """Get a tool by ID."""
        return self._tools.get(tool_id)
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def get_tools_by_category(self, category: str) -> List[BaseTool]:
        """Get all tools in a specific category."""
        tool_ids = self._categories.get(category, [])
        return [self._tools[tool_id] for tool_id in tool_ids if tool_id in self._tools]
    
    def get_categories(self) -> List[str]:
        """Get all categories."""
        return list(self._categories.keys())

# Create a singleton instance
registry = ToolRegistry()
