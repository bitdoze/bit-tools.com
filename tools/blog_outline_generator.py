import re
from typing import List, Dict, Any
from .factory import create_text_generation_tool
from .registry import registry
import logging

# Set up logging
logger = logging.getLogger(__name__)

# System prompt for blog outline generation
blog_outline_system_prompt = """
You are a professional blog outline generator. Create well-structured, comprehensive outlines for blog posts that will help writers create engaging, informative content. Follow these guidelines:

1. Create a logical flow from introduction to conclusion
2. Include main sections and subsections with clear hierarchy
3. Be specific and actionable in section titles
4. Consider SEO best practices
5. Adapt the outline to the target audience and purpose
6. Include suggestions for key points to cover in each section
7. Provide a mix of informational and engaging sections

Your outlines should be comprehensive enough to guide the writing process while allowing for creativity and expansion.
"""

# User prompt template for blog outline generation
blog_outline_user_prompt_template = """
Create a detailed blog post outline for a {word_count}-word article about: {topic}

Target audience: {audience}
Purpose: {purpose}

Include an introduction, main sections with subsections, and a conclusion. For each section, provide brief notes on what to cover.
"""

# Post-processing function for blog outlines
def process_blog_outline(text: str) -> List[str]:
    # Log the received text for debugging
    logger.info(f"Processing blog outline text (length: {len(text)})")
    logger.info(f"Text sample: {text[:200]}...")

    # Remove common introductory phrases
    text = re.sub(r'^.*?(?:here\'s|here is).*?outline.*?:\s*\n*', '', text, flags=re.IGNORECASE | re.MULTILINE)

    # Split by lines and clean
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    logger.info(f"Processed into {len(lines)} lines")

    # Process the outline
    return lines

# Create the blog outline generator tool
BlogOutlineGeneratorClass = create_text_generation_tool(
    name="Blog Post Outline Generator",
    description="Create detailed, structured outlines for blog posts on any topic.",
    icon="""<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
    </svg>""",
    system_prompt=blog_outline_system_prompt,
    user_prompt_template=blog_outline_user_prompt_template,
    input_form_fields={
        "topic": {
            "type": "textarea",
            "label": "Blog Topic",
            "placeholder": "Describe your blog topic in detail...",
            "required": True,
            "rows": 3
        },
        "audience": {
            "type": "text",
            "label": "Target Audience",
            "placeholder": "e.g., Beginners, Marketing Professionals, Parents",
            "required": True
        },
        "purpose": {
            "type": "select",
            "label": "Content Purpose",
            "options": [
                {"value": "Educate", "label": "Educate", "selected": True},
                {"value": "Entertain", "label": "Entertain"},
                {"value": "Inspire", "label": "Inspire"},
                {"value": "Persuade", "label": "Persuade"},
                {"value": "Sell", "label": "Sell"}
            ]
        },
        "word_count": {
            "type": "select",
            "label": "Approximate Word Count",
            "options": [
                {"value": "500-800", "label": "Short (500-800 words)"},
                {"value": "1000-1500", "label": "Medium (1000-1500 words)", "selected": True},
                {"value": "2000-3000", "label": "Long (2000-3000 words)"}
            ]
        }
    },
    post_process_func=process_blog_outline
)

# Instantiate the tool
blog_outline_generator_tool = BlogOutlineGeneratorClass()

# Register the tool with the registry
registry.register(blog_outline_generator_tool, categories=["Content Creation"])
