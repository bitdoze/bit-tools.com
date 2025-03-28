# tools/core/factory.py
from typing import Dict, Any, List, Type, Callable, Optional
from .base import BaseTool
from .base_types import TextGenerationTool, TextTransformationTool
from pydantic import BaseModel, ValidationError
import json
import logging
import re # Import re for cleaning

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- create_text_transformation_tool remains the same ---
# (Keep the existing function as it was)
def create_text_transformation_tool(
    name: str,
    description: str,
    icon: Optional[str] = None,
    system_prompt: Optional[str] = None,
    user_prompt_template: Optional[str] = None,
    input_form_fields: Optional[Dict[str, Dict[str, Any]]] = None
) -> Type[TextTransformationTool]:
    """
    Factory function to create a text transformation tool class.
    (Implementation remains the same as in fasthtml-agno2.txt)
    """
    class CustomTextTransformationTool(TextTransformationTool):
        @property
        def name(self) -> str: return name
        @property
        def description(self) -> str: return description
        @property
        def icon(self) -> str: return icon if icon else super().icon
        @property
        def input_form_fields(self) -> Dict[str, Dict[str, Any]]:
            if input_form_fields: return input_form_fields
            return { "text": { "type": "textarea", "label": "Text to transform", "placeholder": "Enter the text...", "required": True, "rows": 5 } }

        async def transform_text(self, text: str, options: Dict[str, Any]) -> str:
            from ..utils import create_agno_agent
            from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL
            agent = create_agno_agent(DEFAULT_MODEL, OPENROUTER_API_KEY, OPENROUTER_BASE_URL)
            prompt_vars = {"text": text, **options}
            formatted_user_prompt = user_prompt_template.format(**prompt_vars) if user_prompt_template else f"Transform: {text}"
            agent.system_message = system_prompt if system_prompt else "You are a text transformation assistant."
            try:
                logger.info(f"Sending transformation prompt: {formatted_user_prompt[:100]}...")
                response = agent.run(formatted_user_prompt)
                if hasattr(response, 'content'): result_text = response.content
                elif hasattr(response, 'message'): result_text = response.message
                elif hasattr(response, 'text'): result_text = response.text
                elif hasattr(response, 'answer'): result_text = response.answer
                else: result_text = str(response)
                return result_text
            except Exception as e:
                logger.error(f"Error transforming text: {str(e)}", exc_info=True)
                raise
    return CustomTextTransformationTool


def create_text_generation_tool(
    name: str,
    description: str,
    icon: Optional[str] = None,
    system_prompt: Optional[str] = None,
    user_prompt_template: Optional[str] = None,
    input_form_fields: Optional[Dict[str, Dict[str, Any]]] = None,
    response_model: Optional[Type[BaseModel]] = None
) -> Type[TextGenerationTool]:
    """
    Factory function to create a text generation tool class.
    (Refined version)
    """
    class CustomTextGenerationTool(TextGenerationTool):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Store the response model for structured output
            self._response_model = response_model # Use internal var to avoid pydantic conflict

        @property
        def name(self) -> str: return name
        @property
        def description(self) -> str: return description
        @property
        def icon(self) -> str: return icon if icon else super().icon
        @property
        def default_system_prompt(self) -> str: return system_prompt if system_prompt else super().default_system_prompt
        @property
        def input_form_fields(self) -> Dict[str, Dict[str, Any]]:
            if input_form_fields: return input_form_fields
            return { "topic": { "type": "textarea", "label": "Topic", "placeholder": "Describe...", "required": True, "rows": 3 } }

        async def generate_text(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            from ..utils import create_agno_agent
            from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL

            agent = create_agno_agent(
                DEFAULT_MODEL,
                OPENROUTER_API_KEY,
                OPENROUTER_BASE_URL,
                response_model=self._response_model
            )

            formatted_user_prompt = user_prompt_template.format(**inputs) if user_prompt_template else f"Generate content about: {inputs.get('topic', '')}"

            if system_prompt:
                agent.system_message = system_prompt

            try:
                logger.info(f"Sending generation prompt: {formatted_user_prompt[:100]}...")
                response = agent.run(formatted_user_prompt)

                # --- Process the response ---
                return self._process_response(response, inputs)

            except Exception as e:
                logger.error(f"Error generating text: {str(e)}", exc_info=True)
                return {"error": f"Error generating content: {str(e)}", "metadata": inputs}

        def _process_response(self, response, inputs: Dict[str, Any]) -> Dict[str, Any]:
            """Process the model response, handling structured or unstructured output."""
            base_result = {"metadata": inputs} # Start with metadata

            raw_content_str = self._extract_raw_content(response)

            if not raw_content_str:
                 logger.warning("Received empty content from LLM.")
                 base_result["error"] = "Received empty response from AI."
                 base_result["titles"] = ["AI failed to generate content."]
                 return base_result

            # If a response model is expected, try to parse structured output
            if self._response_model:
                try:
                    # Attempt validation directly using Pydantic
                    # Agno should ideally return the validated object in response.content
                    if hasattr(response, 'content') and isinstance(response.content, self._response_model):
                         structured_content = response.content
                         logger.info(f"Received validated Pydantic object: {type(structured_content).__name__}")
                    else:
                        # Fallback: Try parsing the raw string
                        logger.info(f"Attempting to parse raw content into {self._response_model.__name__}")
                        cleaned_content = self._clean_llm_output(raw_content_str)
                        # Use model_validate_json for robustness
                        structured_content = self._response_model.model_validate_json(cleaned_content)
                        logger.info(f"Successfully parsed raw content into Pydantic object: {type(structured_content).__name__}")

                    # Convert Pydantic model to dict and merge with base_result
                    content_dict = structured_content.model_dump(mode='json') # Use mode='json' for better serialization
                    base_result.update(content_dict)
                    # Create a formatted 'titles' list for display compatibility
                    base_result['titles'] = self._format_structured_titles(structured_content)
                    base_result['is_structured'] = True # Flag for results handlers
                    logger.info("Successfully processed structured output.")
                    return base_result

                except (ValidationError, json.JSONDecodeError, Exception) as e:
                    logger.warning(f"Failed to parse/validate structured output ({type(e).__name__}): {str(e)}. Falling back to unstructured.", exc_info=False) # Log less verbosely on fallback
                    # Fallback to processing the raw string if structured parsing fails
                    base_result['titles'] = self._process_unstructured_text(raw_content_str)
                    base_result['raw_text'] = raw_content_str # Include raw text for debugging
                    base_result['is_structured'] = False
                    return base_result
            else:
                # No response model expected, process as unstructured text
                base_result['titles'] = self._process_unstructured_text(raw_content_str)
                base_result['raw_text'] = raw_content_str
                base_result['is_structured'] = False
                return base_result

        def _extract_raw_content(self, response) -> str:
            """Extracts the primary text content from various Agno response formats."""
            if hasattr(response, 'content'):
                content = response.content
                # If content is a Pydantic model, serialize it; otherwise, convert to string
                return content.model_dump_json() if isinstance(content, BaseModel) else str(content or "")
            elif hasattr(response, 'message'): return str(response.message or "")
            elif hasattr(response, 'text'): return str(response.text or "")
            elif hasattr(response, 'answer'): return str(response.answer or "")
            else: return str(response or "")

        def _clean_llm_output(self, text: str) -> str:
            """Basic cleaning of LLM output, removing markdown fences."""
            # Remove markdown code block fences (json, etc.)
            cleaned = re.sub(r'^```[a-zA-Z]*\s*', '', text.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r'\s*```$', '', cleaned.strip(), flags=re.MULTILINE)
            return cleaned.strip()

        def _process_unstructured_text(self, text: str) -> List[str]:
            """Processes unstructured text into a list of lines."""
            return [line.strip() for line in text.split('\n') if line.strip()]

        def _format_structured_titles(self, structured_content: BaseModel) -> List[str]:
            """Creates a list of strings for display from various Pydantic models."""
            # Import models locally to avoid circular dependency issues if needed
            from ..implementations.models import (
                GeneratedTitles, SocialPostList, ThumbnailIdeas, BlogOutline, YoutubeScriptOutput
            )

            if isinstance(structured_content, GeneratedTitles):
                return structured_content.titles[:10] # Limit to 10

            elif isinstance(structured_content, SocialPostList):
                # Format: "Platform: Content" or just Content if platform unknown
                return [
                    f"{post.platform}: {post.content}" if post.platform else post.content
                    for post in structured_content.posts[:10] # Limit to 10
                ]

            elif isinstance(structured_content, ThumbnailIdeas):
                formatted_ideas = []
                ideas_to_format = structured_content.ideas or structured_content.thumbnail_ideas or []
                for i, idea in enumerate(ideas_to_format[:5]): # Limit to 5
                    formatted_ideas.append(f"**Thumbnail Idea {i+1}:**")
                    formatted_ideas.append(f"- **Background:** {idea.background or 'N/A'}")
                    formatted_ideas.append(f"- **Main Image:** {idea.main_image or 'N/A'}")
                    formatted_ideas.append(f"- **Text:** {idea.text or 'N/A'}")
                    formatted_ideas.append(f"- **Elements:** {idea.additional_elements or 'N/A'}")
                    formatted_ideas.append("---") # Separator
                return formatted_ideas

            elif isinstance(structured_content, BlogOutline):
                lines = []
                def _add_section_md(section: Optional[OutlineSection], level=0):
                    if not section or not section.title: return
                    prefix = "#" * (level + 2) # Start with H2 for Introduction/Conclusion
                    lines.append(f"{prefix} {section.title}")
                    if section.points:
                        for point in section.points:
                            lines.append(f"- {point}")
                    lines.append("") # Add space after points
                    if section.subsections:
                        for sub in section.subsections:
                            _add_section_md(sub, level + 1)

                _add_section_md(structured_content.introduction, 0)
                if structured_content.main_sections:
                     lines.append("## Main Sections") # Add a header for main sections
                     lines.append("")
                for section in structured_content.main_sections:
                    _add_section_md(section, 1) # Main sections start at H3
                _add_section_md(structured_content.conclusion, 0)
                return lines

            elif isinstance(structured_content, YoutubeScriptOutput):
                lines = ["### SCRIPT:", structured_content.script, "---", "### HOOKS:"]
                lines.extend([f"- {h}" for h in structured_content.hooks])
                lines.extend(["---", "### INPUT BIAS:"])
                lines.extend([f"- {b}" for b in structured_content.input_bias])
                lines.extend(["---", "### OPEN LOOP QUESTIONS:"])
                lines.extend([f"- {q}" for q in structured_content.open_loop_questions])
                return lines

            else:
                # Default fallback: represent the model as a string list
                try:
                    # Try dumping to dict and formatting key-value pairs
                    data = structured_content.model_dump(mode='json')
                    return [f"{k}: {v}" for k, v in data.items()]
                except:
                    return [str(structured_content)]

    return CustomTextGenerationTool