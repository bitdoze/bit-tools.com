from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional, Dict, Any, Union


class GeneratedTitles(BaseModel):
    titles: List[str] = Field(default_factory=list, description="A list of 10 engaging titles based on the user's topic, platform, and style.")

    @model_validator(mode='after')
    def ensure_titles(self) -> 'GeneratedTitles':
        """Ensure titles is a valid list"""
        if not isinstance(self.titles, list):
            if isinstance(self.titles, str):
                # Split the string into lines if it's a single string
                self.titles = [line.strip() for line in self.titles.split('\n') if line.strip()]
            else:
                # Default to empty list if not valid
                self.titles = []
        return self


class SocialPost(BaseModel):
    platform: Optional[str] = Field(None, description="The social media platform the post is for.")
    content: str = Field("", description="The content of the social media post.")


class SocialPostList(BaseModel):
    posts: List[SocialPost] = Field(default_factory=list, description="A list of generated social media posts.")

    @model_validator(mode='after')
    def ensure_posts(self) -> 'SocialPostList':
        """Ensure posts is a valid list"""
        if not isinstance(self.posts, list) or not self.posts:
            # Create a default post with empty content if no posts are found
            self.posts = [SocialPost(content="No content generated")]
        return self


class ThumbnailIdea(BaseModel):
    background: str = Field("", description="The background style and colors of the thumbnail.")
    main_image: str = Field("", description="The central image or graphic of the thumbnail.")
    text: str = Field("", description="The main text or headline for the thumbnail (short and engaging).")
    additional_elements: Optional[str] = Field(None, description="Any icons, graphics, or additional visual elements.")


class ThumbnailIdeas(BaseModel):
    ideas: List[ThumbnailIdea] = Field(default_factory=list, description="A list of unique thumbnail ideas for a YouTube video.")
    thumbnail_ideas: Optional[List[ThumbnailIdea]] = Field(default_factory=list, description="Alternative field name for ideas.")

    @model_validator(mode='after')
    def consolidate_ideas(self) -> 'ThumbnailIdeas':
        """Consolidate ideas from both fields and ensure there's at least one idea"""
        # Combine both fields if they exist
        all_ideas = []
        if self.ideas:
            all_ideas.extend(self.ideas)
        if self.thumbnail_ideas:
            all_ideas.extend(self.thumbnail_ideas)
        
        # Use the combined list for both fields
        self.ideas = all_ideas
        self.thumbnail_ideas = all_ideas
        
        # If still empty, create a default idea
        if not all_ideas:
            default_idea = ThumbnailIdea(
                background="Default blue gradient background",
                main_image="Central image related to the topic",
                text="YOUR TOPIC HERE",
                additional_elements="Optional decorative elements"
            )
            self.ideas = [default_idea]
            self.thumbnail_ideas = [default_idea]
            
        return self


class OutlineSection(BaseModel):
    title: str = Field("", description="The title of this section or subsection.")
    heading: Optional[str] = Field(None, description="Alternative field for title.")
    points: List[str] = Field(default_factory=list, description="Brief bullet points or notes on what to cover in this section.")
    subsections: List['OutlineSection'] = Field(default_factory=list, description="Nested subsections, if any.")
    subpoints: List[Union[str, Dict[str, Any]]] = Field(default_factory=list, description="Alternative field for subsections.")

    @model_validator(mode='after')
    def process_fields(self) -> 'OutlineSection':
        # Use heading as title if title is empty
        if not self.title and self.heading:
            self.title = self.heading
            
        # If no title is provided, use a default
        if not self.title:
            self.title = "Untitled Section"
            
        # Process subpoints as either strings or subsections
        processed_subsections = []
        for item in self.subpoints:
            if isinstance(item, str):
                # If it's a string, add it to points
                self.points.append(item)
            elif isinstance(item, dict):
                # If it's a dictionary, try to convert to OutlineSection
                try:
                    if 'title' in item or 'heading' in item:
                        processed_subsections.append(OutlineSection(**item))
                except Exception:
                    # If conversion fails, add as a point
                    self.points.append(str(item))
                    
        # Add any processed subsections from subpoints
        if processed_subsections:
            self.subsections.extend(processed_subsections)
            
        return self


class BlogOutline(BaseModel):
    introduction: Optional[OutlineSection] = Field(default=None)
    main_sections: List[OutlineSection] = Field(default_factory=list)
    conclusion: Optional[OutlineSection] = Field(default=None)
    sections: List[OutlineSection] = Field(default_factory=list, description="Alternative field for main_sections.")
    outline_sections: List[OutlineSection] = Field(default_factory=list, description="Alternative field for sections.")

    @model_validator(mode='after')
    def process_outline(self) -> 'BlogOutline':
        # Consolidate sections from all fields
        all_sections = []
        if self.main_sections:
            all_sections.extend(self.main_sections)
        if self.sections:
            all_sections.extend(self.sections)
        if self.outline_sections:
            all_sections.extend(self.outline_sections)
            
        # Set all section fields to the consolidated list
        self.main_sections = all_sections
        self.sections = all_sections
        self.outline_sections = all_sections
        
        # Create a default introduction if none exists
        if not self.introduction:
            self.introduction = OutlineSection(
                title="Introduction",
                points=["Introduction to the topic", "Why it matters", "What will be covered"]
            )
            
        # Create a default conclusion if none exists
        if not self.conclusion:
            self.conclusion = OutlineSection(
                title="Conclusion",
                points=["Summary of key points", "Final thoughts", "Call to action"]
            )
            
        # If no sections were found, create at least one default section
        if not all_sections:
            default_section = OutlineSection(
                title="Main Content",
                points=["First important point", "Second important point", "Third important point"]
            )
            self.main_sections = [default_section]
            self.sections = [default_section]
            self.outline_sections = [default_section]
            
        return self


# Required for self-referencing models
OutlineSection.model_rebuild()


class YoutubeScriptOutput(BaseModel):
    script: str = Field("", description="The main YouTube video script, including mystery, knowledge gap, preview hook, and call to action.")
    hooks: List[str] = Field(default_factory=list, description="A list of 12 compelling hooks (questions, statements, stories, stats).")
    input_bias: List[str] = Field(default_factory=list, description="A list of 5 input bias variations highlighting research/effort.")
    open_loop_questions: List[str] = Field(default_factory=list, description="A list of 10 open loop questions a viewer might have.")
    sections: List[Dict[str, str]] = Field(default_factory=list, description="Optional script broken into sections.")

    @model_validator(mode='after')
    def ensure_content(self) -> 'YoutubeScriptOutput':
        # If script is empty but sections exist, compile them into a script
        if not self.script and self.sections:
            compiled_script = ""
            for section in self.sections:
                if isinstance(section, dict):
                    title = section.get('title', '')
                    content = section.get('content', '')
                    if title:
                        compiled_script += f"## {title}\n\n"
                    if content:
                        compiled_script += f"{content}\n\n"
            
            self.script = compiled_script.strip()
            
        # Ensure we have at least one hook
        if not self.hooks:
            self.hooks = ["How to master this topic quickly", "The one thing most people miss about this subject"]
            
        # Ensure we have at least one input bias
        if not self.input_bias:
            self.input_bias = ["After researching this topic extensively", "Based on my analysis"]
            
        # Ensure we have at least one open loop question
        if not self.open_loop_questions:
            self.open_loop_questions = ["What's the most important thing to remember?", "How can I apply this information?"]
            
        return self
