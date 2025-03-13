from fasthtml.common import *
from tools import get_tool_by_id
from .tool_page import tool_page
from .results import create_results_page

def tool_results_page(tool_id, results):
    """
    Generate a results page for a tool.
    
    Args:
        tool_id: The ID of the tool
        results: The results from the tool processing
        
    Returns:
        Components representing the results page
    """
    tool = get_tool_by_id(tool_id)
    if not tool:
        return error_page("Tool Not Found", "Sorry, the requested tool could not be found.")
        
    # Handle error cases
    if isinstance(results, dict) and "error" in results:
        return error_page("Error", results["error"], f"/tools/{tool_id}")
        
    # Create the results page based on the tool and results
    return create_results_page(tool_id, tool, results)

def error_page(title, message, back_url=None):
    """Generate an error page."""
    if not back_url:
        back_url = "/tools"

    return Div(
        H1(title, cls="text-3xl font-bold text-gray-800 mb-4 text-center"),
        P(message, cls="text-xl text-red-600 mb-6 text-center"),
        A("Back", href=back_url,
          cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
        cls="text-center py-12"
    )
