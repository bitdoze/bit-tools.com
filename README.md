# Bit Tools

Bit Tools is a web application built with FastHTML that provides various AI-powered content generation tools. The application allows users to generate blog outlines, social media posts, titles, YouTube thumbnail ideas, and more.

## Project Structure

The project is organized into the following directories:

- `components/`: UI components for the website (header, footer, page layout)
- `pages/`: Page content and routes
  - `pages/tool_pages/`: Tool page and results page components
    - `pages/tool_pages/results/`: Modular components for different result types
- `static/`: Static assets (images, JavaScript)
- `tools/`: AI tool implementations
  - `tools/core/`: Core functionality (base classes, registry, factory)
  - `tools/implementations/`: Specific tool implementations

## How to Run

1. Make sure you have Python installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
4. Open your browser and navigate to `http://localhost:8000`

## How to Add a New Tool

Adding a new tool to the application is straightforward:

1. **Create a new tool implementation file** in the `tools/implementations/` directory
2. **Use the factory functions** to create your tool:
   - For text generation tools: `create_text_generation_tool`
   - For text transformation tools: `create_text_transformation_tool`
3. **Register your tool** with the registry

### Example: Creating a Text Generation Tool

```python
# tools/implementations/my_new_tool.py
import re
from typing import List, Dict, Any
from ..core.factory import create_text_generation_tool
from ..core.registry import registry

# Define your system prompt
system_prompt = """
Your system prompt here...
"""

# Define your user prompt template
user_prompt_template = """
Your user prompt template here with {placeholders}...
"""

# Define a post-processing function
def process_results(text: str) -> List[str]:
    # Process the text and return a list of results
    results = []
    # Your processing logic here...
    return results

# Create the tool
MyNewToolClass = create_text_generation_tool(
    name="My New Tool",
    description="Description of what your tool does.",
    icon="""<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <!-- Your SVG path here -->
    </svg>""",
    system_prompt=system_prompt,
    user_prompt_template=user_prompt_template,
    input_form_fields={
        "field1": {
            "type": "textarea",
            "label": "Field Label",
            "placeholder": "Placeholder text...",
            "required": True,
            "rows": 3
        },
        "field2": {
            "type": "select",
            "label": "Select Option",
            "options": [
                {"value": "option1", "label": "Option 1", "selected": True},
                {"value": "option2", "label": "Option 2"}
            ]
        }
    },
    post_process_func=process_results
)

# Instantiate the tool
my_new_tool = MyNewToolClass()

# Register the tool with the registry
registry.register(my_new_tool, categories=["Your Category"])
```

### Import Your Tool

After creating your tool, import it in the `tools/__init__.py` file:

```python
# Import your new tool
from .implementations.my_new_tool import my_new_tool
```

## Resources

This website is built with FastHTML. Check out these articles for more information:

1. [FastHTML For Beginners: Build An UI to Python App in 5 Minutes](https://www.bitdoze.com/fasthtml-start/)
2. [Create a Multi-Page Website with FastHTML: Complete Structure Tutorial](https://www.bitdoze.com/fasthtml-multiple-pages/)
