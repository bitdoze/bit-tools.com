import re
from typing import List, Dict, Any
from ..core.factory import create_text_generation_tool
from ..core.registry import registry
from .models import BlogOutline
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

Return your outline in a structured format with:
- An introduction section with title and bullet points
- Main sections, each with title, bullet points, and potential subsections
- A conclusion section with title and bullet points

Every section should have a descriptive title and a list of key points to cover.
"""

# User prompt template for blog outline generation
blog_outline_user_prompt_template = """
Create a detailed blog post outline for a {word_count}-word article about: {topic}

Target audience: {target_audience}
Purpose: {tone}

Return a structured outline with:
1. Introduction section
2. Main content sections (with any subsections)
3. Conclusion section

For each section and subsection, include:
- A descriptive title
- 3-5 bullet points on what to cover
"""

# Define custom tips and benefits for the blog outline generator
blog_outline_tips = [
    "Include a compelling introduction and conclusion in your outline",
    "Break down complex topics into digestible sections",
    "Consider adding FAQs to address common reader questions",
    "Plan for visual elements like images, charts, or infographics",
    "Include a call-to-action at the end of your blog post",
    "Research keywords to include in your headings for better SEO"
]

blog_outline_benefits = [
    "Save time planning your blog content structure",
    "Create more organized and coherent blog posts",
    "Ensure comprehensive coverage of your topic",
    "Improve reader engagement with a logical flow",
    "Make the writing process faster and more efficient"
]

# Create the blog outline generator tool
BlogOutlineGeneratorClass = create_text_generation_tool(
    name="Blog Outline Generator",
    description="Create a structured outline for your blog post.",
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
        "word_count": {
            "type": "select",
            "label": "Word Count",
            "options": [
                {"value": "500", "label": "Short (500 words)", "selected": False},
                {"value": "1000", "label": "Medium (1000 words)", "selected": True},
                {"value": "1500", "label": "Long (1500 words)", "selected": False},
                {"value": "2000", "label": "Comprehensive (2000+ words)", "selected": False}
            ]
        },
        "target_audience": {
            "type": "textarea",
            "label": "Target Audience",
            "placeholder": "Who is your target audience?",
            "required": False,
            "rows": 2
        },
        "tone": {
            "type": "select",
            "label": "Tone",
            "options": [
                {"value": "professional", "label": "Professional", "selected": True},
                {"value": "casual", "label": "Casual"},
                {"value": "educational", "label": "Educational"},
                {"value": "humorous", "label": "Humorous"}
            ]
        },
        "sections": {
            "type": "select",
            "label": "Number of Sections",
            "options": [
                {"value": "3-5", "label": "3-5 Sections", "selected": True},
                {"value": "5-7", "label": "5-7 Sections"},
                {"value": "7-10", "label": "7-10 Sections"}
            ]
        }
    },
    response_model=BlogOutline
)

# Add custom tips and benefits
BlogOutlineGeneratorClass.tips = blog_outline_tips
BlogOutlineGeneratorClass.benefits = blog_outline_benefits

# Instantiate the tool
blog_outline_generator_tool = BlogOutlineGeneratorClass()

# Register the tool with the registry
registry.register(blog_outline_generator_tool, categories=["Content Creation"])
