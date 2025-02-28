from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .utils import create_openrouter_llm
from .base import BaseTool
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL
import re

social_prompt_template = """
You are a versatile social media content creator specializing in platform-specific posts. Follow these key principles:

Key Principles:
1. High energy and motivation
2. Direct and no-nonsense approach
3. Practical advice and actionable insights
4. Empowerment and positivity
5. Repetition for emphasis

Platform-Specific Guidelines for {platform}:

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

Topic: {topic}
Tone: {tone}

Create 10 engaging, platform-optimized posts that:
- Use powerful, motivational language
- Get straight to the point
- Create urgency when appropriate
- Engage directly with the audience
- Are optimized for {platform}

Format each post on a new line. Make them platform-appropriate.
"""

class SocialPostGenerator(BaseTool):
    """Social Post Generator tool implementation."""
    
    @property
    def name(self) -> str:
        return "Social Media Post Generator"
    
    @property
    def description(self) -> str:
        return "Create engaging social media posts for Twitter, Bluesky, Facebook, or Reddit in various tones."
    
    @property
    def icon(self) -> str:
        return """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z" />
        </svg>"""
    
    @property
    def input_form_fields(self) -> dict:
        return {
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
        }
    
    def process(self, inputs):
        """Process the inputs and generate posts."""
        try:
            topic = inputs.get("topic", "").strip()
            platform = inputs.get("platform", "Twitter")
            tone = inputs.get("tone", "No specific tone")
            
            if not topic:
                return {
                    "error": "Please provide a topic for your posts."
                }
            
            posts = self._generate_posts(topic, platform, tone)
            
            return {
                "metadata": {
                    "topic": topic,
                    "platform": platform,
                    "tone": tone,
                    "count": len(posts)
                },
                "titles": posts  # Using 'titles' to maintain compatibility with existing UI
            }
            
        except Exception as e:
            return {
                "error": f"Failed to generate posts: {str(e)}"
            }

    def _generate_posts(self, topic, platform, tone):
        """Generate social media posts using the LLM."""
        llm = create_openrouter_llm(
            DEFAULT_MODEL,
            OPENROUTER_API_KEY,
            OPENROUTER_BASE_URL
        )
        
        prompt = PromptTemplate(
            input_variables=["topic", "platform", "tone"],
            template=social_prompt_template
        )
        
        chain = prompt | llm
        result = chain.invoke({"topic": topic, "platform": platform, "tone": tone})
        
        # Process the result to get a list of posts
        posts_text = result.content.strip()
        
        # Remove common introductory phrases
        posts_text = re.sub(r'^.*?(?:here are|here\'s)\s+\d+.*?:\s*\n*', '', posts_text, flags=re.IGNORECASE | re.MULTILINE)
        posts_text = re.sub(r'Okay,?\s*', '', posts_text, flags=re.IGNORECASE)
        
        # Split and clean posts
        posts = []
        lines = [line.strip() for line in posts_text.split('\n') if line.strip()]
        
        for line in lines:
            cleaned_line = re.sub(r'^\d+\.\s*|\*\s*|\-\s*', '', line)
            if cleaned_line:
                posts.append(cleaned_line)
        
        return posts[:10]  # Ensure we return at most 10 posts

# Create an instance of the tool
social_post_generator_tool = SocialPostGenerator()