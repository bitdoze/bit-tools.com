from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

def create_openrouter_llm(model_name, api_key, base_url):
    """
    Create a LangChain LLM instance connected to OpenRouter.
    
    Args:
        model_name: The model to use (e.g., "openai/gpt-4o-mini")
        api_key: OpenRouter API key
        base_url: Base URL for OpenRouter API
        
    Returns:
        An initialized LLM instance
    """
    return ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0.7,  # Adjust for more/less creative responses
    )