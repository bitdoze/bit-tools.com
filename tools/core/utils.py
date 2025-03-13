from agno.agent import Agent
from agno.models.openrouter import OpenRouter

def create_agno_agent(model_name, api_key=None, base_url=None):
    """
    Create an Agno Agent connected to OpenRouter.

    Args:
        model_name: The model to use (e.g., "gpt-4o")
        api_key: OpenRouter API key (optional, defaults to env var OPENROUTER_API_KEY)
        base_url: Base URL for OpenRouter API (optional)

    Returns:
        An initialized Agno Agent
    """
    # Set up model parameters
    model_kwargs = {"id": model_name}

    # Add optional parameters if provided
    if api_key:
        model_kwargs["api_key"] = api_key
    if base_url:
        model_kwargs["base_url"] = base_url

    # Create the model instance
    model = OpenRouter(**model_kwargs)

    # Create and return the agent
    return Agent(
        model=model,
        markdown=True
    )
