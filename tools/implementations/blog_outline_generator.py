import re
from typing import List, Dict, Any
from ..core.factory import create_text_generation_tool
from ..core.registry import registry
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

Target audience: {target_audience}
Purpose: {tone}

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
    post_process_func=process_blog_outline
)

# Add custom tips and benefits
BlogOutlineGeneratorClass.tips = blog_outline_tips
BlogOutlineGeneratorClass.benefits = blog_outline_benefits

# Instantiate the tool
blog_outline_generator_tool = BlogOutlineGeneratorClass()

# Register the tool with the registry
registry.register(blog_outline_generator_tool, categories=["Content Creation"])
