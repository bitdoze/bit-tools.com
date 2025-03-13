from fasthtml.common import *
from .base_results import BaseResultsHandler
from .transformation_results import TransformationResultsHandler
from .outline_results import OutlineResultsHandler
from .standard_results import StandardResultsHandler
from .youtube_script_results import YoutubeScriptResultsHandler

def create_results_page(tool_id, tool, results):
    """
    Create a results page based on the tool type and results.
    
    Args:
        tool_id: The ID of the tool
        tool: The tool instance
        results: The results from the tool processing
        
    Returns:
        Components representing the results page
    """
    # Determine the type of results and use the appropriate handler
    if "transformed_text" in results:
        handler = TransformationResultsHandler(tool_id, tool, results)
    elif "outline" in tool_id.lower():
        handler = OutlineResultsHandler(tool_id, tool, results)
    elif "youtube-script" in tool_id.lower():
        handler = YoutubeScriptResultsHandler(tool_id, tool, results)
    else:
        handler = StandardResultsHandler(tool_id, tool, results)
        
    return handler.render()
