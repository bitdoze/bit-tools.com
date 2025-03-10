import re
from typing import List, Dict, Any
from .factory import create_text_generation_tool
from .registry import registry

# System prompt for title generation
title_system_prompt = """
You are a versatile content title generator specializing in catchy, platform-specific titles. Follow these key principles and guidelines:

Key Principles:
1. High energy and motivation
2. Direct and no-nonsense approach
3. Practical advice and actionable insights
4. Empowerment and positivity
5. Repetition for emphasis

Detailed Guidelines:
1. Use Powerful, Motivational Language
   - Start sentences with strong verbs
   - Employ imperative statements
   - Use intensifiers like "absolutely," "definitely," "100%"
2. Keep It Real and Direct
   - Cut through the fluff - get straight to the point
   - Use colloquial language and slang
   - Don't shy away from occasional profanity (if appropriate for the platform)
3. Focus on Practicality
   - Provide specific, actionable steps
   - Use real-world examples and case studies
   - Break down complex ideas into simple, doable tasks
4. Create a Sense of Urgency
   - Use phrases like "right now," "immediately," "don't wait"
   - Emphasize the cost of inaction
   - Highlight time-sensitive opportunities
5. Incorporate Personal Anecdotes (when relevant)
   - Share stories from entrepreneurial journeys
   - Use failures as teaching moments
   - Connect personal experiences to broader principles
6. Embrace Repetition
   - Repeat key phrases for emphasis
   - Use variations of the same idea to drive the point home
   - Create memorable catchphrases
7. Engage Directly with the Audience
   - Use "you" and "your" frequently
   - Ask rhetorical questions
   - Challenge the reader to take action
8. Use Contrast for Impact
   - Juxtapose old thinking with new perspectives
   - Highlight the difference between action and inaction
   - Compare short-term discomfort with long-term gains
9. Leverage Visual Structure (when applicable)
   - Use ALL CAPS for emphasis
   - Break long ideas into short, punchy phrases

Apply these principles and guidelines to create engaging, platform-appropriate titles.
"""

# User prompt template for title generation
title_user_prompt_template = """
Create 10 engaging {platform} titles for content about: {topic}. Tone: {style}. Make them catchy and platform-appropriate. Don't include 'sure' or numbering. Apply the principles and guidelines provided in the system prompt. Please only include the titles and nothing else
"""

# Post-processing function for titles
def process_titles(text: str) -> List[str]:
    # Remove common introductory phrases
    text = re.sub(r'^.*?(?:here are|here\'s)\s+\d+.*?:\s*\n*', '', text, flags=re.IGNORECASE | re.MULTILINE)

    # Split and clean titles
    titles = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    for line in lines:
        # Remove any numbering (1., 2., etc) or bullet points
        cleaned_line = re.sub(r'^\d+\.\s*|\*\s*|\-\s*', '', line)
        if cleaned_line:
            titles.append(cleaned_line)

    # Remove duplicates while preserving order
    seen = set()
    unique_titles = [t for t in titles if not (t in seen or seen.add(t))]

    # Return at most 10 titles
    return unique_titles[:10]

# Create the title generator tool
TitleGeneratorClass = create_text_generation_tool(
    name="AI Title Generator",
    description="Create engaging titles for YouTube videos, articles, or TikTok posts in various styles.",
    icon="""<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
    </svg>""",
    system_prompt=title_system_prompt,
    user_prompt_template=title_user_prompt_template,
    input_form_fields={
        "topic": {
            "type": "textarea",
            "label": "What's your content about?",
            "placeholder": "Describe your content topic in detail for better results...",
            "required": True,
            "rows": 3
        },
        "platform": {
            "type": "select",
            "label": "Platform",
            "options": [
                {"value": "YouTube", "label": "YouTube", "selected": True},
                {"value": "Article", "label": "Article"},
                {"value": "TikTok", "label": "TikTok"}
            ]
        },
        "style": {
            "type": "select",
            "label": "Style",
            "options": [
                {"value": "Professional", "label": "Professional", "selected": True},
                {"value": "Funny", "label": "Funny"}
            ]
        }
    },
    post_process_func=process_titles
)

# Instantiate the tool
title_generator_tool = TitleGeneratorClass()

# Register the tool with the registry
registry.register(title_generator_tool, categories=["Content Creation"])
