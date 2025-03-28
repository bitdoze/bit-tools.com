import re
from typing import List, Dict, Any
from ..core.factory import create_text_generation_tool
from ..core.registry import registry
from .models import ThumbnailIdeas

# System prompt for thumbnail idea generation
thumbnail_system_prompt = """
You are a versatile YouTube Thumbnails generator specializing in catchy, YouTube Thumbnails. Follow these key principles and guidelines:

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

Return your results in a structured format with 5 unique thumbnail ideas, each with background, main image, text, and additional elements.
"""

# User prompt template for thumbnail idea generation
thumbnail_user_prompt_template = """
Generate 5 unique thumbnail ideas for a YouTube video about: {topic}.

For each idea, provide:
- Background: Describe the background style and colors
- Main Image: Describe the central image or graphic
- Text: Provide the main text or headline (short and engaging, use CAPS for emphasis)
- Additional Elements: Describe any icons, graphics, or additional visual elements

Make the ideas diverse, engaging, and tailored to attract clicks on YouTube. Ensure each idea is distinct and creative.
"""

# Define custom tips and benefits for the thumbnail generator
thumbnail_tips = [
    "Use bold, contrasting colors to stand out",
    "Include close-up faces or emotions when relevant",
    "Keep text large and limited to 3-4 words",
    "Ensure your thumbnail is clear at small sizes",
    "Use high-quality, relevant images",
    "Create a consistent style for your channel"
]

thumbnail_benefits = [
    "Save time brainstorming thumbnail concepts",
    "Increase your video's visibility on YouTube",
    "Attract more viewers with eye-catching designs",
    "Experiment with different styles and approaches",
    "Maintain consistency while keeping your content fresh"
]

# Create the thumbnail idea generator tool
ThumbnailGeneratorClass = create_text_generation_tool(
    name="YouTube Thumbnail Ideas Generator",
    description="Create eye-catching thumbnail concepts for your YouTube videos.",
    icon="""<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
    </svg>""",
    system_prompt=thumbnail_system_prompt,
    user_prompt_template=thumbnail_user_prompt_template,
    input_form_fields={
        "topic": {
            "type": "textarea",
            "label": "What's your YouTube video about?",
            "placeholder": "Describe your video topic in detail for better results...",
            "required": True,
            "rows": 3
        }
    },
    response_model=ThumbnailIdeas
)

# Add custom tips and benefits
ThumbnailGeneratorClass.tips = thumbnail_tips
ThumbnailGeneratorClass.benefits = thumbnail_benefits

# Instantiate the tool
thumbnail_generator_tool = ThumbnailGeneratorClass()

# Register the tool with the registry
registry.register(thumbnail_generator_tool, categories=["Content Creation"])
