Welcome to the next installment of our FastHTML series! In our previous article, we explored how to create a multi-page website with a consistent header and footer. Now, we're going to take it up a notch by adding an interactive AI-powered tool that generates creative titles based on user input.

In this tutorial, we'll build an AI Title Generator that leverages the power of LangChain and OpenRouter to connect with advanced language models like GPT-4o-mini. This will demonstrate how to integrate AI capabilities into your FastHTML website and provide a foundation for adding more tools in the future.

## Why Add Interactive AI Tools to Your Website?

AI-powered tools can significantly enhance your website's functionality and value to users:

- **Engagement**: Interactive tools keep visitors on your site longer
- **Value**: Provide useful services that solve real problems for your audience
- **Differentiation**: Stand out from competitors with unique AI capabilities
- **Scalability**: Create a platform for multiple tools without starting from scratch each time
- **Learning**: Gain experience with AI integration that you can apply to future projects

Let's get started by building an AI Title Generator that creates engaging titles for YouTube videos, articles, and TikTok posts in different styles like "Funny" or "Professional."

## FastHTML AI Tools Series

This article is part of our FastHTML series:

- [FastHTML Get Started](https://www.bitdoze.com/fasthtml-start/)
- [FastHTML Multiple Pages](https://www.bitdoze.com/fasthtml-multiple-pages/)
- FastHTML AI Tools Integration (this article)

## Setting Up for AI Integration

### Step 1: Expand Your Project Structure

Building on our previous multi-page website structure, we'll add new files and directories to support AI tools:

```
mywebsite/
├── main.py              # Main application entry point
├── components.py        # Reusable UI components
├── config.py            # Configuration settings (API keys, etc.)
├── pages/               # Individual page content
│   ├── __init__.py      # Makes pages a proper Python package
│   ├── home.py          # Home page content
│   ├── about.py         # About page content
│   ├── contact.py       # Contact page content
│   └── tools.py         # New page listing all available tools
└── tools/               # Individual tool implementations
    ├── __init__.py      # Makes tools a proper Python package
    ├── title_generator.py   # AI Title Generator tool
    └── utils.py         # Shared utility functions for tools
```

This structure allows us to:
1. Keep our code organized as we add more tools
2. Share common functionality between tools
3. Centralize configuration for API keys and settings
4. Create a dedicated page that showcases all available tools

### Step 2: Install Required Dependencies

First, make sure you have the necessary packages installed:

```bash
pip install fasthtml langchain langchain-openai python-dotenv
```

### Step 3: Set Up Configuration

Create a `config.py` file to store your API keys and settings:

**File: `mywebsite/config.py`**

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Default model to use
DEFAULT_MODEL = "openai/gpt-4o-mini"

# Application settings
DEBUG = True
```

For security, create a `.env` file in your project root to store your actual API key:

**File: `mywebsite/.env`**

```
OPENROUTER_API_KEY=your_api_key_here
```

Make sure to add `.env` to your `.gitignore` file to prevent accidentally exposing your API key.

### Step 4: Create the AI Title Generator Tool

Now, let's implement the AI Title Generator tool:

**File: `mywebsite/tools/utils.py`**

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

def create_openrouter_llm(model_name, api_key, base_url):
    """
    Create a LangChain LLM instance connected to OpenRouter.
    
    Args:
        model_name: The model to use (e.g., "openai/gpt-4o-mini")
        api_key: OpenRouter API key
        base_url: Base URL for OpenRouter API
        
    Returns:
        An initialized LLM instance
    """
    return ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0.7,  # Adjust for more/less creative responses
    )
```

**File: `mywebsite/tools/title_generator.py`**

```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .utils import create_openrouter_llm
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL

# Create a prompt template for generating titles
title_prompt_template = """
You are a creative title generator specialized in creating engaging titles for different platforms.

PLATFORM: {platform}
STYLE: {style}
TOPIC: {topic}

Your task is to generate 5 attention-grabbing titles for the specified platform that match the requested style and are relevant to the topic.

For YouTube titles:
- Include numbers or curiosity gaps when appropriate
- Consider SEO and searchability
- Keep length between 40-60 characters
- Make them clickable but not clickbait

For Article titles:
- Be clear and informative
- Include keywords for SEO
- Consider using subtitles or colons for structure
- Keep length between 50-70 characters

For TikTok titles:
- Be short, catchy, and trendy
- Include relevant hashtags when appropriate
- Use emojis sparingly if it fits the style
- Keep length under 40 characters

The titles should match the {style} style. If "Funny", use humor and playfulness. If "Professional", be authoritative and informative.

Generate 5 unique titles that would perform well on {platform}:
"""

def generate_titles(topic, platform, style):
    """
    Generate creative titles using the LLM.
    
    Args:
        topic: The topic for the titles
        platform: The platform (YouTube, Article, TikTok)
        style: The style (Funny, Professional)
        
    Returns:
        A list of generated titles
    """
    # Set up the LLM
    llm = create_openrouter_llm(
        DEFAULT_MODEL,
        OPENROUTER_API_KEY,
        OPENROUTER_BASE_URL
    )
    
    # Create the prompt
    prompt = PromptTemplate(
        input_variables=["topic", "platform", "style"],
        template=title_prompt_template
    )
    
    # Create and run the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"topic": topic, "platform": platform, "style": style})
    
    # Process the result to get a list of titles
    titles_text = result["text"].strip()
    titles = [line.strip() for line in titles_text.split("\n") if line.strip()]
    
    # Extract just the titles, removing any numbering or prefix
    clean_titles = []
    for title in titles:
        # Remove numbering like "1.", "2.", "-", "*", etc.
        if any(title.startswith(prefix) for prefix in ["1.", "2.", "3.", "4.", "5.", "-", "*"]):
            # Find the position after the prefix and any whitespace
            pos = 0
            while pos < len(title) and (title[pos].isdigit() or title[pos] in ".-*: "):
                pos += 1
            title = title[pos:].strip()
        clean_titles.append(title)
    
    return clean_titles[:5]  # Ensure we return at most 5 titles
```

### Step 5: Create a Tools Overview Page

Next, let's create a page that lists all the available tools:

**File: `mywebsite/pages/tools.py`**

```python
from fasthtml.common import *

def tools():
    """
    Defines the tools overview page.
    
    Returns:
        Components representing the tools page content
    """
    return Div(
        # Page header
        H1("AI Tools",
           cls="text-3xl font-bold text-gray-800 mb-6 text-center"),
           
        P("Explore our collection of AI-powered tools to help with your creative and productivity needs.",
          cls="text-xl text-gray-600 mb-8 text-center"),
        
        # Tools grid
        Div(
            # Title Generator Tool
            Div(
                Div(
                    H2("AI Title Generator", cls="text-2xl font-semibold mb-2"),
                    P("Create engaging titles for YouTube videos, articles, or TikTok posts in various styles.",
                      cls="text-gray-600 mb-4"),
                    A("Use Tool",
                      href="/tools/title-generator",
                      cls="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
                    cls="p-6"
                ),
                cls="bg-white rounded-lg shadow-md transition-transform hover:scale-105"
            ),
            
            # Placeholder for future tools (commented out for now)
            # Div(
            #     Div(
            #         H2("Coming Soon: Text Summarizer", cls="text-2xl font-semibold mb-2"),
            #         P("Automatically summarize long articles and documents into concise bullet points.",
            #           cls="text-gray-600 mb-4"),
            #         Div("Coming Soon",
            #           cls="inline-block bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded cursor-not-allowed"),
            #         cls="p-6"
            #     ),
            #     cls="bg-white rounded-lg shadow-md opacity-75"
            # ),
            
            cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        )
    )
```

### Step 6: Create the Title Generator Page

Now, let's create the page for our AI Title Generator tool:

**File: `mywebsite/pages/title_generator.py`**

```python
from fasthtml.common import *

def title_generator():
    """
    Defines the AI Title Generator tool page.
    
    Returns:
        Components representing the title generator page content
    """
    return Div(
        # Page header
        H1("AI Title Generator",
           cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
           
        P("Generate engaging titles for your content with the help of AI.",
          cls="text-xl text-gray-600 mb-8 text-center"),
        
        # Tool interface
        Div(
            Form(
                # Topic input
                Div(
                    Label("What's your content about?", For="topic", cls="block text-gray-700 font-semibold mb-2"),
                    Textarea(id="topic", name="topic",
                            placeholder="Describe your content topic in detail for better results...",
                            rows=3,
                            required=True,
                            cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"),
                    cls="mb-6"
                ),
                
                # Platform selection
                Div(
                    Label("Platform", For="platform", cls="block text-gray-700 font-semibold mb-2"),
                    Select(
                        Option("YouTube", value="YouTube", selected=True),
                        Option("Article", value="Article"),
                        Option("TikTok", value="TikTok"),
                        id="platform",
                        name="platform",
                        cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"
                    ),
                    cls="mb-6"
                ),
                
                # Style selection
                Div(
                    Label("Style", For="style", cls="block text-gray-700 font-semibold mb-2"),
                    Select(
                        Option("Professional", value="Professional", selected=True),
                        Option("Funny", value="Funny"),
                        id="style",
                        name="style",
                        cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"
                    ),
                    cls="mb-6"
                ),
                
                # Submit button
                Div(
                    Button("Generate Titles",
                           type="submit",
                           cls="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded"),
                    cls="mt-2"
                ),
                
                action="/tools/generate-titles",
                method="post",
                cls="bg-white p-6 rounded-lg shadow-md"
            ),
            cls="max-w-2xl mx-auto"
        ),
        
        # Tips section
        Div(
            H3("Tips for Better Results", cls="text-xl font-semibold mb-4"),
            Ul(
                Li("Be specific about your topic - include key points you want to highlight", cls="mb-2"),
                Li("Consider your target audience and what would appeal to them", cls="mb-2"),
                Li("The more context you provide, the better the titles will be", cls="mb-2"),
                Li("Try different platforms and styles to see what works best", cls="mb-2"),
                cls="list-disc list-inside text-gray-700"
            ),
            cls="mt-12 max-w-2xl mx-auto bg-blue-50 p-6 rounded-lg"
        )
    )

def title_results(topic, platform, style, titles):
    """
    Displays the generated titles.
    
    Args:
        topic: The topic that was entered
        platform: The selected platform
        style: The selected style
        titles: List of generated titles
        
    Returns:
        Components displaying the results
    """
    return Div(
        # Page header
        H1("Generated Titles",
           cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
           
        P(f"Here are your {style} titles for {platform}:",
          cls="text-xl text-gray-600 mb-8 text-center"),
        
        # Results section
        Div(
            # Summary of request
            Div(
                P(Strong("Topic: "), topic, cls="mb-2"),
                P(Strong("Platform: "), platform, cls="mb-2"),
                P(Strong("Style: "), style, cls="mb-2"),
                cls="mb-6 p-4 bg-gray-50 rounded"
            ),
            
            # Generated titles
            Div(
                H3("Generated Titles", cls="text-xl font-semibold mb-4"),
                *(Div(
                    P(title, cls="mb-1"),
                    Button("Copy",
                         type="button",
                         onclick=f"navigator.clipboard.writeText('{title.replace("'", "\\'")}'); this.textContent = 'Copied!'; setTimeout(() => this.textContent = 'Copy', 2000);",
                         cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded ml-2"),
                    cls="flex items-center justify-between p-3 bg-white rounded shadow-sm mb-3"
                ) for title in titles),
                cls="mb-6"
            ),
            
            # Back button
            Div(
                A("Generate More Titles",
                  href="/tools/title-generator",
                  cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"),
                A("Back to Tools",
                  href="/tools",
                  cls="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"),
                cls="flex justify-center mt-6"
            ),
            
            cls="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md"
        )
    )
```

### Step 7: Update the Components with a New Nav Link

Now, let's update the header component to include a link to our tools page:

**File: `mywebsite/components.py` (updated)**

```python
from fasthtml.common import *

def header(current_page="/"):
    """
    Creates a consistent header with navigation.

    Args:
        current_page: The current page path, used to highlight the active link

    Returns:
        A Header component with navigation
    """
    # Define the navigation links
    nav_items = [
        ("Home", "/"),
        ("Tools", "/tools"),  # Added Tools link
        ("About", "/about"),
        ("Contact", "/contact")
    ]

    # Create navigation items with appropriate styling
    nav_links = []
    for title, path in nav_items:
        # Apply special styling to the current page link
        is_current = current_page == path or (
            current_page.startswith("/tools/") and path == "/tools"
        )
        link_class = "text-white hover:text-gray-300 px-3 py-2"
        if is_current:
            link_class += " font-bold underline"

        nav_links.append(
            Li(
                A(title, href=path, cls=link_class)
            )
        )

    return Header(
        Div(
            # Website logo/name
            A("MyWebsite", href="/", cls="text-xl font-bold text-white"),

            # Navigation menu
            Nav(
                Ul(
                    *nav_links,
                    cls="flex space-x-2"
                ),
                cls="ml-auto"
            ),
            cls="container mx-auto flex items-center justify-between px-4 py-3"
        ),
        cls="bg-blue-600 shadow-md"
    )

# Rest of the components.py file remains the same
```

I've updated the `header` function to include a link to the Tools page and added logic to highlight the Tools link for any page under the `/tools/` path.

### Step 8: Update the Main Application with New Routes

Finally, let's update the main application to include routes for our new pages:

**File: `mywebsite/main.py` (updated)**

```python
from fasthtml.common import *

# Import page content from the pages directory
from pages.home import home as home_page
from pages.about import about as about_page
from pages.contact import contact as contact_page
from pages.tools import tools as tools_page
from pages.title_generator import title_generator as title_generator_page
from pages.title_generator import title_results as title_results_page

# Import the title generator tool
from tools.title_generator import generate_titles

# Import the page layout component
from components import page_layout

# Initialize the FastHTML application
app = FastHTML()

# Original routes from previous example...

# Define route for the tools overview page
@app.get("/tools")
def tools():
    """Handler for the tools overview page route."""
    return page_layout(
        title="AI Tools - MyWebsite",
        content=tools_page(),
        current_page="/tools"
    )

# Define route for the title generator tool
@app.get("/tools/title-generator")
def title_generator():
    """Handler for the title generator tool page."""
    return page_layout(
        title="AI Title Generator - MyWebsite",
        content=title_generator_page(),
        current_page="/tools/title-generator"
    )

# Handle title generation form submission
@app.post("/tools/generate-titles")
async def generate_titles_handler(topic: str, platform: str, style: str):
    """
    Handler for title generation form submission.
    
    Calls the LangChain-powered title generator and displays results.
    """
    try:
        # Call the title generator function
        titles = generate_titles(topic, platform, style)
        
        # Return the results page
        return page_layout(
            title="Generated Titles - MyWebsite",
            content=title_results_page(
                topic=topic,
                platform=platform,
                style=style,
                titles=titles
            ),
            current_page="/tools/title-generator"
        )
    except Exception as e:
        # Handle errors gracefully
        error_content = Div(
            H1("Generation Error", cls="text-3xl font-bold text-gray-800 mb-4"),
            P(f"Sorry, there was an error generating titles: {str(e)}",
              cls="text-xl text-gray-600 mb-6"),
            A("Try Again", href="/tools/title-generator", 
              cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
            cls="text-center py-12"
        )

        return page_layout(
            title="Error - MyWebsite",
            content=error_content,
            current_page="/tools/title-generator"
        )

# Rest of the existing routes...

# Run the application
if __name__ == "__main__":
    # Using FastHTML's built-in serve() function
    serve()
```

## Running Your AI-Powered Website

With all the files in place, you can now run your application:

```bash
python main.py
```

Visit `http://localhost:5001/tools` to see the tools overview page, and click on the AI Title Generator to start using your new AI-powered tool!

## Making Your Tool Architecture Extensible

The structure we've created makes it easy to add more tools in the future. Here's how you can expand on this foundation:

### Adding a New Tool

To add another AI tool (for example, a text summarizer):

1. Create a new file in the `tools/` directory (e.g., `tools/summarizer.py`)
2. Implement the tool's functionality using LangChain
3. Create a new page file in the `pages/` directory (e.g., `pages/summarizer.py`)
4. Add the tool to the tools overview page in `pages/tools.py`
5. Add routes for the new tool in `main.py`

### Improving the Tools Infrastructure

As you add more tools, you might want to enhance your infrastructure:

1. **Create a base Tool class**: Standardize how tools are implemented and loaded
2. **Implement caching**: Store results to reduce API costs and improve performance
3. **Add user accounts**: Allow users to save their favorite generated content
4. **Implement rate limiting**: Manage API usage and prevent abuse
5. **Add analytics**: Track which tools are most popular
6. **Create an admin dashboard**: Monitor tool usage and performance

Here's an example of how you might structure a base Tool class:

```python
# mywebsite/tools/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseTool(ABC):
    """
    Abstract base class for all AI tools.
    
    This provides a standard interface for tool implementation,
    making it easier to add new tools to the system.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the tool."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the tool does."""
        pass
    
    @property
    def route(self) -> str:
        """Return the URL route for the tool."""
        return f"/tools/{self.name.lower().replace(' ', '-')}"
    
    @abstractmethod
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the inputs and return the results.
        
        Args:
            inputs: Dictionary of input parameters from the form
            
        Returns:
            Dictionary of results to be passed to the results page
        """
        pass
    
    @abstractmethod
    def get_input_form(self) -> Dict[str, Any]:
        """
        Return the configuration for the input form.
        
        Returns:
            Dictionary containing form field definitions
        """
        pass
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> List[str]:
        """
        Validate the inputs and return error messages.
        
        Args:
            inputs: Dictionary of input parameters from the form
            
        Returns:
            List of error messages, empty if validation passed
        """
        return []

```

## Conclusion

Congratulations! You've successfully added an AI-powered Title Generator to your FastHTML website. This demonstrates how you can integrate powerful AI capabilities using LangChain and external APIs.

The modular structure we've created allows you to:

1. Add more AI tools easily by following the same pattern
2. Keep your code organized and maintainable
3. Share common functionality between different tools
4. Create a cohesive user experience

In the future, you can expand this foundation to create a comprehensive suite of AI tools, making your website even more valuable to users. Some ideas for additional tools include:

- Text summarization
- Keyword extraction
- Grammar and style checking
- Content paraphrasing
- SEO optimization suggestions
- Image description generation

By leveraging the power of modern language models through LangChain and OpenRouter, you can create sophisticated AI tools without having to build everything from scratch. This approach lets you focus on creating a great user experience while the underlying AI technology handles the complex processing.

Happy coding, and enjoy building your AI-powered web applications with FastHTML!