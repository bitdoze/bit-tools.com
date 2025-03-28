# tools/core/utils.py
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from typing import Optional, Type
from pydantic import BaseModel
import logging # Add logging

logger = logging.getLogger(__name__)

def create_agno_agent(model_name, api_key=None, base_url=None, response_model: Optional[Type[BaseModel]] = None):
    """
    Create an Agno Agent connected to OpenRouter.

    Args:
        model_name: The model to use (e.g., "gpt-4o")
        api_key: OpenRouter API key (optional, defaults to env var OPENROUTER_API_KEY)
        base_url: Base URL for OpenRouter API (optional)
        response_model: Optional Pydantic model for structured output

    Returns:
        An initialized Agno Agent
    """
    # --- Define the desired max_tokens value ---
    # Using the requested 32000, but be aware of model limits.
    MAX_OUTPUT_TOKENS = 32000
    # A safer default might be 4096 or 8192 if 32k causes issues.

    # Set up model parameters
    model_kwargs = {
        "id": model_name,
        # --- Add max_tokens parameter ---
        "max_tokens": MAX_OUTPUT_TOKENS,
        # --------------------------------
    }
    logger.info(f"Initializing OpenRouter model '{model_name}' with max_tokens={MAX_OUTPUT_TOKENS}")

    # Add optional API key and base URL if provided
    if api_key:
        model_kwargs["api_key"] = api_key
    if base_url:
        model_kwargs["base_url"] = base_url

    # Create the model instance
    try:
        model = OpenRouter(**model_kwargs)
    except Exception as e:
        logger.error(f"Failed to initialize OpenRouter model: {e}", exc_info=True)
        # Handle error appropriately, maybe raise it or return a default/dummy agent
        raise ValueError(f"Failed to create OpenRouter model: {e}") from e


    # --- Agent Configuration ---
    agent_kwargs = {
        "model": model,
        # Keep markdown=True initially, as it can help the LLM structure output
        # even when a response_model is used. Remove if it causes issues.
        "markdown": True
    }

    if response_model:
        agent_kwargs["response_model"] = response_model
        logger.info(f"Agent configured with response_model: {response_model.__name__}")
        # If using response_model causes issues with markdown formatting, uncomment below:
        # agent_kwargs.pop("markdown", None)
        # logger.info("Agent markdown support disabled due to response_model.")


    # Create and return the agent
    try:
        agent = Agent(**agent_kwargs)
        logger.info("Agno Agent created successfully.")
        return agent
    except Exception as e:
        logger.error(f"Failed to initialize Agno Agent: {e}", exc_info=True)
        raise ValueError(f"Failed to create Agno Agent: {e}") from e