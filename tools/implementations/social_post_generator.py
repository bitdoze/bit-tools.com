import re
import logging
from typing import List, Dict, Any
from ..core.factory import create_text_generation_tool
from ..core.registry import registry
from .models import SocialPostList

# Set up logging
logger = logging.getLogger(__name__)

# System prompt for social post generation
social_system_prompt = """
You are a versatile social media content creator specializing in platform-specific posts. Follow these key principles and guidelines:

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

Platform-Specific Guidelines:

For Twitter:
- Keep it under 280 characters
- Use hashtags strategically
- Create engagement hooks
- Include calls to action
- Use emojis appropriately

For Bluesky:
- Similar to Twitter but more tech-focused
- Engage with the tech community
- Use relevant hashtags
- Create discussion points
- Keep it professional yet engaging

For Facebook:
- Longer format allowed
- Include visual descriptions
- Create shareable content
- Encourage discussion
- Use formatting for readability

For Reddit:
- Platform-specific formatting
- Focus on community value
- Include TL;DR when needed
- Be authentic and direct
- Follow subreddit conventions

Return your results as a structured list of 10 posts with each post as a separate element.
"""

# User prompt template for social post generation
social_user_prompt_template = """
Create 10 engaging {platform} posts for content about: {topic}. Tone: {tone}. Make them platform-appropriate.

Please return a list of 10 unique posts following the guidelines in the system prompt. Each post should be complete and ready to publish.
"""

# Define custom tips and benefits for the social post generator
social_post_tips = [
    "Keep Twitter posts under 280 characters for optimal engagement",
    "Use relevant hashtags to increase discoverability",
    "Include a call-to-action in your posts to boost engagement",
    "Use emojis strategically to add personality to your posts",
    "Tailor your content to each platform's unique audience",
    "Post at optimal times for your target audience"
]

social_post_benefits = [
    "Save time creating platform-specific social media content",
    "Maintain a consistent posting schedule with ready-to-use content",
    "Increase engagement with professionally crafted posts",
    "Experiment with different tones and styles to find what works best",
    "Build a stronger social media presence across multiple platforms"
]

# Create the social post generator tool
SocialPostGeneratorClass = create_text_generation_tool(
    name="Social Media Post Generator",
    description="Create engaging social media posts for Twitter, Bluesky, Facebook, or Reddit in various tones.",
    icon="""<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z" />
    </svg>""",
    system_prompt=social_system_prompt,
    user_prompt_template=social_user_prompt_template,
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
                {"value": "Twitter", "label": "Twitter", "selected": True},
                {"value": "Bluesky", "label": "Bluesky"},
                {"value": "Facebook", "label": "Facebook"},
                {"value": "Reddit", "label": "Reddit"}
            ]
        },
        "tone": {
            "type": "select",
            "label": "Tone",
            "options": [
                {"value": "No specific tone", "label": "No specific tone", "selected": True},
                {"value": "Funny", "label": "Funny"},
                {"value": "Serious", "label": "Serious"},
                {"value": "Controversial", "label": "Controversial"},
                {"value": "Inspirational", "label": "Inspirational"},
                {"value": "Educational", "label": "Educational"},
                {"value": "Professional", "label": "Professional"}
            ]
        }
    },
    response_model=SocialPostList
)

# Add custom tips and benefits
SocialPostGeneratorClass.tips = social_post_tips
SocialPostGeneratorClass.benefits = social_post_benefits

# Instantiate the tool
social_post_generator_tool = SocialPostGeneratorClass()

# Register the tool with the registry
registry.register(social_post_generator_tool, categories=["Content Creation"])
