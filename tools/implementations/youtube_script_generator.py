import re
from typing import List, Dict, Any
from ..core.factory import create_text_generation_tool
from ..core.registry import registry
from .models import YoutubeScriptOutput

# System prompt for YouTube script generation
youtube_script_system_prompt = """
You are a YouTube creator who is creating video scripts that follows:
- informative tone
- Knowledge Gap add in first 30 seconds
- Mystery
- Preview Hook
- call to action
You are creating the video scripts on the keyword asked by the user.

Your response should be structured with:
1. A complete script that starts with a mystery, adds a knowledge gap, includes a preview hook, and ends with a call to action
2. 12 compelling hooks (questions, statements, stories, statistics)
3. 5 input bias variations highlighting research/effort
4. 10 open loop questions a viewer might have

Return your response in a structured format as specified.
"""

# User prompt template for YouTube script generation
youtube_script_user_prompt_template = """
Generate a YouTube script for a video about: {topic}.

Return your response in a structured format with:
1. A script section with your complete YouTube script
2. 12 hooks (mix of questions, statements, stories, and statistics)
3. 5 input bias statements (highlighting research/effort)
4. 10 open loop questions (what viewers might wonder)
"""

# Define custom tips and benefits for the YouTube script generator
youtube_script_tips = [
    "Start with a strong hook to grab attention",
    "Include a knowledge gap in the first 30 seconds",
    "Use a preview hook to keep viewers watching",
    "Maintain an informative tone throughout",
    "End with a clear call to action",
    "Use open loop questions to create curiosity"
]

youtube_script_benefits = [
    "Save time on script writing and content planning",
    "Create more engaging and viewer-retaining content",
    "Develop multiple hooks to test and optimize",
    "Establish credibility with input bias statements",
    "Generate curiosity with open loop questions"
]

# Create the YouTube script generator tool
YoutubeScriptGeneratorClass = create_text_generation_tool(
    name="YouTube Script Generator",
    description="Create engaging YouTube video scripts with hooks, input bias, and open loop questions.",
    icon="""<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
    </svg>""",
    system_prompt=youtube_script_system_prompt,
    user_prompt_template=youtube_script_user_prompt_template,
    input_form_fields={
        "topic": {
            "type": "textarea",
            "label": "What's your YouTube video about?",
            "placeholder": "Describe your video topic in detail for better results...",
            "required": True,
            "rows": 3
        }
    },
    response_model=YoutubeScriptOutput
)

# Add custom tips and benefits
YoutubeScriptGeneratorClass.tips = youtube_script_tips
YoutubeScriptGeneratorClass.benefits = youtube_script_benefits

# Instantiate the tool
youtube_script_generator_tool = YoutubeScriptGeneratorClass()

# Register the tool with the registry
registry.register(youtube_script_generator_tool, categories=["Content Creation"])
