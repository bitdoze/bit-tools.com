# Bit Tools Implementation Plan

## Phase 1: Core Architecture Improvements

### 1. Enhanced Tool Registry System (`tools/registry.py`)

Create a new `ToolRegistry` class that will manage tool registration and retrieval:

```python
from typing import Dict, List, Type, Optional
from .base import BaseTool

class ToolRegistry:
    """Registry for managing AI tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._categories: Dict[str, List[str]] = {}
    
    def register(self, tool: BaseTool, categories: List[str] = None):
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
```

### 2. Specialized Tool Base Classes (`tools/base_types.py`)

Create specialized base classes for different types of text tools:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from .base import BaseTool

class TextGenerationTool(BaseTool, ABC):
    """Base class for text generation tools."""
    
    @property
    def tool_type(self) -> str:
        return "text_generation"
    
    @property
    def default_system_prompt(self) -> str:
        """Default system prompt for this tool type."""
        return """
        You are a versatile text generation assistant. Create high-quality, 
        engaging content based on the user's requirements.
        """
    
    def get_system_prompt(self) -> str:
        """Get the system prompt, allowing for customization."""
        return self.default_system_prompt
    
    @abstractmethod
    async def generate_text(self, inputs: Dict[str, Any]) -> List[str]:
        """Generate text based on inputs."""
        pass
    
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and generate text."""
        try:
            # Validate inputs
            validation_errors = self.validate_inputs(inputs)
            if validation_errors:
                return {"error": "Validation failed", "validation_errors": validation_errors}
            
            # Generate text
            generated_texts = await self.generate_text(inputs)
            
            # Return results
            return {
                "metadata": {
                    **{k: v for k, v in inputs.items() if k in self.input_form_fields},
                    "count": len(generated_texts)
                },
                "titles": generated_texts  # Using 'titles' for backward compatibility
            }
        except Exception as e:
            return {"error": f"Failed to generate text: {str(e)}"}

class TextTransformationTool(BaseTool, ABC):
    """Base class for text transformation tools."""
    
    @property
    def tool_type(self) -> str:
        return "text_transformation"
    
    @abstractmethod
    async def transform_text(self, text: str, options: Dict[str, Any]) -> str:
        """Transform the input text based on options."""
        pass
    
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and transform text."""
        try:
            # Validate inputs
            validation_errors = self.validate_inputs(inputs)
            if validation_errors:
                return {"error": "Validation failed", "validation_errors": validation_errors}
            
            # Get input text
            text = inputs.get("text", "").strip()
            if not text:
                return {"error": "Please provide text to transform."}
            
            # Transform text
            transformed_text = await self.transform_text(
                text, 
                {k: v for k, v in inputs.items() if k != "text"}
            )
            
            # Return results
            return {
                "metadata": {
                    **{k: v for k, v in inputs.items() if k in self.input_form_fields},
                },
                "original_text": text,
                "transformed_text": transformed_text
            }
        except Exception as e:
            return {"error": f"Failed to transform text: {str(e)}"}
```

### 3. Tool Factory (`tools/factory.py`)

Create a factory to simplify creating new tools:

```python
from typing import Dict, Any, List, Type, Callable, Awaitable
from .base import BaseTool
from .base_types import TextGenerationTool, TextTransformationTool

def create_text_generation_tool(
    name: str,
    description: str,
    icon: str = None,
    system_prompt: str = None,
    user_prompt_template: str = None,
    input_form_fields: Dict[str, Dict[str, Any]] = None,
    post_process_func: Callable[[str], List[str]] = None
) -> Type[TextGenerationTool]:
    """
    Factory function to create a text generation tool class.
    
    Args:
        name: The name of the tool
        description: The description of the tool
        icon: SVG icon for the tool (optional)
        system_prompt: System prompt for the LLM (optional)
        user_prompt_template: Template for the user prompt (optional)
        input_form_fields: Configuration for input form fields (optional)
        post_process_func: Function to post-process the LLM output (optional)
        
    Returns:
        A new TextGenerationTool subclass
    """
    class CustomTextGenerationTool(TextGenerationTool):
        @property
        def name(self) -> str:
            return name
        
        @property
        def description(self) -> str:
            return description
        
        @property
        def icon(self) -> str:
            if icon:
                return icon
            return super().icon
        
        @property
        def default_system_prompt(self) -> str:
            if system_prompt:
                return system_prompt
            return super().default_system_prompt
        
        @property
        def input_form_fields(self) -> Dict[str, Dict[str, Any]]:
            if input_form_fields:
                return input_form_fields
            return {
                "topic": {
                    "type": "textarea",
                    "label": "What's your content about?",
                    "placeholder": "Describe your content in detail for better results...",
                    "required": True,
                    "rows": 3
                }
            }
        
        async def generate_text(self, inputs: Dict[str, Any]) -> List[str]:
            from .utils import create_pydantic_agent
            from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL
            
            # Set up the Pydantic AI Agent
            agent = create_pydantic_agent(
                DEFAULT_MODEL,
                OPENROUTER_API_KEY,
                OPENROUTER_BASE_URL
            )
            
            # Format the user prompt with the input variables
            formatted_user_prompt = user_prompt_template.format(**inputs) if user_prompt_template else f"Generate content about: {inputs.get('topic', '')}"
            
            # Combine system and user prompts
            combined_prompt = f"{self.get_system_prompt()}\n\n{formatted_user_prompt}"
            
            # Run the agent with the combined prompt
            result = await agent.run(combined_prompt)
            
            # Process the result
            result_text = result.data.strip()
            
            # Apply post-processing if provided
            if post_process_func:
                return post_process_func(result_text)
            
            # Default processing: split by lines
            return [line.strip() for line in result_text.split('\n') if line.strip()]
    
    return CustomTextGenerationTool
```

### 4. Update `tools/__init__.py`

Update the tools initialization to use the new registry system:

```python
from .title_generator import title_generator_tool
from .social_post_generator import social_post_generator_tool
from .registry import registry

# Register existing tools
registry.register(title_generator_tool, categories=["Content Creation"])
registry.register(social_post_generator_tool, categories=["Content Creation", "Social Media"])

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
```

### 5. Enhanced Error Handling (`tools/errors.py`)

Create a standardized error system:

```python
from enum import Enum
from typing import Dict, Any, List, Optional

class ErrorCode(Enum):
    INVALID_INPUT = "invalid_input"
    API_ERROR = "api_error"
    RATE_LIMIT = "rate_limit"
    INTERNAL_ERROR = "internal_error"

class ToolError(Exception):
    """Base exception for tool-related errors."""
    
    def __init__(
        self, 
        code: ErrorCode, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)
```

### 6. Update `BaseTool.validate_inputs` in `tools/base.py`

Enhance the validation method in the base tool class:

```python
def validate_inputs(self, inputs: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Validate the inputs and return detailed error information.
    
    Args:
        inputs: Dictionary of input parameters from the form
        
    Returns:
        List of error dictionaries with field, code, and message
    """
    errors = []
    
    for field_id, field_config in self.input_form_fields.items():
        # Check required fields
        if field_config.get("required", False) and not inputs.get(field_id):
            errors.append({
                "field": field_id,
                "code": "required",
                "message": f"{field_config.get('label', field_id)} is required"
            })
        
        # Check field-specific validation
        if field_id in inputs and inputs[field_id]:
            # Example: max length validation
            max_length = field_config.get("maxLength")
            if max_length and len(inputs[field_id]) > max_length:
                errors.append({
                    "field": field_id,
                    "code": "max_length",
                    "message": f"{field_config.get('label', field_id)} exceeds maximum length of {max_length}"
                })
    
    return errors
```

## Phase 2: Frontend Enhancements

### 1. Enhanced Tool Results UI (`pages/tool_pages.py`)

Update the tool results page to include multiple view options:

```python
# This will be implemented after the core architecture improvements
```

### 2. Accessibility Improvements

Add ARIA attributes and ensure keyboard navigation:

```python
# This will be implemented after the core architecture improvements
```

### 3. Responsive Design Improvements

Ensure the website works well on all device sizes:

```python
# This will be implemented after the core architecture improvements
```

## Phase 3: Example New Tool Implementation

### 1. Blog Post Outline Generator

Create a new tool using the factory:

```python
# This will be implemented after the core architecture improvements
```

## Implementation Order

1. Create `tools/registry.py`
2. Create `tools/base_types.py`
3. Create `tools/factory.py`
4. Create `tools/errors.py`
5. Update `tools/base.py`
6. Update `tools/__init__.py`
7. Implement frontend enhancements
8. Create example new tool