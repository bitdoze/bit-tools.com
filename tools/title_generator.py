from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .utils import create_openrouter_llm
from .base import BaseTool
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL
import re

# Create a prompt template for generating titles
# Updated prompt template with better guidelines
title_prompt_template = """
You are a versatile content title generator specializing in catchy, platform-specific titles. Follow these key principles:

Key Principles:
1. High energy and motivation
2. Direct and no-nonsense approach
3. Practical advice and actionable insights
4. Empowerment and positivity
5. Repetition for emphasis

Platform-Specific Guidelines for {platform}:

For YouTube:
- Use powerful, motivational language
- Create urgency ("Must Watch", "Do This Now")
- Include numbers and specific outcomes
- Use emotional triggers and curiosity gaps
- Focus on searchability and click-through

For Article:
- Start with strong verbs
- Use "How to" and "Why" formats
- Include specific benefits
- Focus on SEO-friendly keywords
- Consider using subtitles or colons

For TikTok:
- Keep it short and punchy
- Use trending phrases
- Include relevant emojis
- Add popular hashtags
- Make it memorable and shareable

Topic: {topic}
Style: {style}

Create 10 engaging, high-impact titles that:
- Use powerful, motivational language
- Get straight to the point
- Create urgency when appropriate
- Engage directly with the audience
- Are optimized for {platform}

Format each title on a new line. Make them catchy and platform-appropriate.
"""

class TitleGenerator(BaseTool):
    """Title Generator tool implementation."""
    
    @property
    def name(self) -> str:
        return "AI Title Generator"
    
    @property
    def description(self) -> str:
        return "Create engaging titles for YouTube videos, articles, or TikTok posts in various styles."
    
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
        }
    
    def process(self, inputs):
        """Process the inputs and generate titles."""
        try:
            topic = inputs.get("topic", "").strip()
            platform = inputs.get("platform", "YouTube")
            style = inputs.get("style", "Professional")
            
            if not topic:
                return {
                    "error": "Please provide a topic for your titles."
                }
            
            titles = self._generate_titles(topic, platform, style)
            
            # Group titles by category for better presentation
            return {
                "metadata": {
                    "topic": topic,
                    "platform": platform,
                    "style": style,
                    "count": len(titles)
                },
                "titles": titles
            }
            
        except Exception as e:
            return {
                "error": f"Failed to generate titles: {str(e)}"
            }

    def _generate_titles(self, topic, platform, style):
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
        
        # Use the newer RunnableSequence approach instead of LLMChain
        chain = prompt | llm
        
        # Run the chain
        result = chain.invoke({"topic": topic, "platform": platform, "style": style})
        
        # Process the result to get a list of titles
        titles_text = result.content.strip()
        
        # Improved title extraction
        # First try to split by numbered lines
        titles = []
        lines = [line.strip() for line in titles_text.split('\n') if line.strip()]
        
        for line in lines:
            # Remove any numbering (1., 2., etc) or bullet points
            cleaned_line = re.sub(r'^\d+\.\s*|\*\s*|\-\s*', '', line)
            if cleaned_line:
                titles.append(cleaned_line)
        
        # If we don't have enough titles, try alternative parsing
        if len(titles) < 10:
            # Try to extract titles with more flexible pattern
            all_possible_titles = re.findall(r'(?:^|\n)(?:\d+\.|\*|\-|\–)?\s*([^\n]+)', titles_text)
            titles.extend([t.strip() for t in all_possible_titles if t.strip()])
            
            # Remove duplicates while preserving order
            seen = set()
            titles = [t for t in titles if not (t in seen or seen.add(t))]
        
        # Ensure exactly 10 titles
        if len(titles) < 10:
            # Request more titles if we don't have enough
            additional_result = chain.invoke({
                "topic": topic,
                "platform": platform,
                "style": style
            })
            additional_titles = [
                re.sub(r'^\d+\.\s*|\*\s*|\-\s*', '', line.strip())
                for line in additional_result.content.strip().split('\n')
                if line.strip()
            ]
            titles.extend(additional_titles)
        
        # Return exactly 10 unique titles
        return list(dict.fromkeys(titles))[:10]

# Create an instance of the tool for easy importing
title_generator_tool = TitleGenerator()