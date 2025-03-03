from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

def create_pydantic_agent(model_name, api_key, base_url):
    """
    Create a Pydantic AI Agent connected to OpenRouter.
    
    Args:
        model_name: The model to use (e.g., "openai/gpt-4o-mini")
        api_key: OpenRouter API key
        base_url: Base URL for OpenRouter API
        
    Returns:
        An initialized Pydantic AI Agent
    """
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    
    model = OpenAIModel(model_name, openai_client=client)
    return Agent(model)