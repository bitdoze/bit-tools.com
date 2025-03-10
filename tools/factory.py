from typing import Dict, Any, List, Type, Callable, Optional
from .base import BaseTool
from .base_types import TextGenerationTool, TextTransformationTool
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_text_generation_tool(
    name: str,
    description: str,
    icon: Optional[str] = None,
    system_prompt: Optional[str] = None,
    user_prompt_template: Optional[str] = None,
    input_form_fields: Optional[Dict[str, Dict[str, Any]]] = None,
    post_process_func: Optional[Callable[[str], List[str]]] = None
) -> Type[TextGenerationTool]:
    """
    Factory function to create a text generation tool class.

    Args:
        name: The name of the tool
        description: The description of the tool
        icon: SVG icon for the tool (optional)
        system_prompt: System prompt for the LLM (optional)
        user_prompt_template: Template for the user prompt (optional)
        input_form_fields: Configuration for input form fields (optional)
        post_process_func: Function to post-process the LLM output (optional)

    Returns:
        A new TextGenerationTool subclass
    """
    class CustomTextGenerationTool(TextGenerationTool):
        @property
        def name(self) -> str:
            return name

        @property
        def description(self) -> str:
            return description

        @property
        def icon(self) -> str:
            if icon:
                return icon
            return super().icon

        @property
        def default_system_prompt(self) -> str:
            if system_prompt:
                return system_prompt
            return super().default_system_prompt

        @property
        def input_form_fields(self) -> Dict[str, Dict[str, Any]]:
            if input_form_fields:
                return input_form_fields
            return {
                "topic": {
                    "type": "textarea",
                    "label": "What's your content about?",
                    "placeholder": "Describe your content in detail for better results...",
                    "required": True,
                    "rows": 3
                }
            }

        async def generate_text(self, inputs: Dict[str, Any]) -> List[str]:
            from .utils import create_agno_agent
            from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL

            # Set up the Agno Agent
            agent = create_agno_agent(
                DEFAULT_MODEL,
                OPENROUTER_API_KEY,
                OPENROUTER_BASE_URL
            )

            # Format the user prompt with the input variables
            formatted_user_prompt = user_prompt_template.format(**inputs) if user_prompt_template else f"Generate content about: {inputs.get('topic', '')}"

            # Set the system prompt (Agno handles this differently)
            if system_prompt:
                agent.system_message = system_prompt

            try:
                # Run the agent with the user prompt
                logger.info(f"Sending prompt to Agno: {formatted_user_prompt[:100]}...")
                response = agent.run(formatted_user_prompt)

                # Log the response type and structure for debugging
                logger.info(f"Response type: {type(response)}")
                logger.info(f"Response attributes: {dir(response)}")

                # Extract the result text based on RunResponse structure
                if hasattr(response, 'content'):
                    result_text = response.content
                elif hasattr(response, 'message'):
                    result_text = response.message
                elif hasattr(response, 'text'):
                    result_text = response.text
                elif hasattr(response, 'answer'):
                    result_text = response.answer
                else:
                    # Try direct string representation as fallback
                    result_text = str(response)
                    # If the response has a complex structure, try to inspect it
                    try:
                        if hasattr(response, '__dict__'):
                            logger.info(f"Response dict: {vars(response)}")
                    except:
                        pass

                logger.info(f"Extracted text (first 100 chars): {result_text[:100]}...")

                # Apply post-processing if provided
                if post_process_func:
                    processed_result = post_process_func(result_text)
                    logger.info(f"Post-processed into {len(processed_result)} items")
                    return processed_result

                # Default processing: split by lines
                return [line.strip() for line in result_text.split('\n') if line.strip()]

            except Exception as e:
                logger.error(f"Error generating text: {str(e)}", exc_info=True)
                raise

    return CustomTextGenerationTool

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

    Args:
        name: The name of the tool
        description: The description of the tool
        icon: SVG icon for the tool (optional)
        system_prompt: System prompt for the LLM (optional)
        user_prompt_template: Template for the user prompt (optional)
        input_form_fields: Configuration for input form fields (optional)

    Returns:
        A new TextTransformationTool subclass
    """
    class CustomTextTransformationTool(TextTransformationTool):
        @property
        def name(self) -> str:
            return name

        @property
        def description(self) -> str:
            return description

        @property
        def icon(self) -> str:
            if icon:
                return icon
            return super().icon

        @property
        def input_form_fields(self) -> Dict[str, Dict[str, Any]]:
            if input_form_fields:
                return input_form_fields
            return {
                "text": {
                    "type": "textarea",
                    "label": "Text to transform",
                    "placeholder": "Enter the text you want to transform...",
                    "required": True,
                    "rows": 5
                }
            }

        async def transform_text(self, text: str, options: Dict[str, Any]) -> str:
            from .utils import create_agno_agent
            from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL

            # Set up the Agno Agent
            agent = create_agno_agent(
                DEFAULT_MODEL,
                OPENROUTER_API_KEY,
                OPENROUTER_BASE_URL
            )

            # Format the user prompt with the input variables
            prompt_vars = {"text": text, **options}
            formatted_user_prompt = user_prompt_template.format(**prompt_vars) if user_prompt_template else f"Transform the following text: {text}"

            # Set the system prompt
            if system_prompt:
                agent.system_message = system_prompt
            else:
                agent.system_message = """
                You are a text transformation assistant. Transform the provided text according to the user's requirements.
                """

            try:
                # Run the agent with the formatted prompt
                logger.info(f"Sending prompt to Agno: {formatted_user_prompt[:100]}...")
                response = agent.run(formatted_user_prompt)

                # Extract the result text based on RunResponse structure
                if hasattr(response, 'content'):
                    result_text = response.content
                elif hasattr(response, 'message'):
                    result_text = response.message
                elif hasattr(response, 'text'):
                    result_text = response.text
                elif hasattr(response, 'answer'):
                    result_text = response.answer
                else:
                    # Try direct string representation as fallback
                    result_text = str(response)
                    # Log the response structure for debugging
                    logger.info(f"Response type: {type(response)}")
                    logger.info(f"Response attributes: {dir(response)}")
                    try:
                        if hasattr(response, '__dict__'):
                            logger.info(f"Response dict: {vars(response)}")
                    except:
                        pass

                return result_text

            except Exception as e:
                logger.error(f"Error transforming text: {str(e)}", exc_info=True)
                raise

    return CustomTextTransformationTool
