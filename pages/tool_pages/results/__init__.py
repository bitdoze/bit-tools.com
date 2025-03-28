# pages/tool_pages/results/__init__.py
from fasthtml.common import *
from .base_results import BaseResultsHandler
from .transformation_results import TransformationResultsHandler
from .outline_results import OutlineResultsHandler
from .standard_results import StandardResultsHandler
from .youtube_script_results import YoutubeScriptResultsHandler
from .thumbnail_results import ThumbnailResultsHandler # Import the new handler

def create_results_page(tool_id, tool, results):
    """
    Create a results page based on the tool type and results.
    Routes to the appropriate handler.
    """
    # Determine the type of results and use the appropriate handler
    if "transformed_text" in results:
        handler_class = TransformationResultsHandler
    elif "thumbnail" in tool_id.lower() and ("thumbnail_ideas" in results or "ideas" in results):
         handler_class = ThumbnailResultsHandler # Route to new handler
    elif "outline" in tool_id.lower(): # Check for outline structure if needed
        # Check if results contain keys specific to the BlogOutline model
        if "introduction" in results and "main_sections" in results and "conclusion" in results:
             handler_class = OutlineResultsHandler
        else: # Fallback for potentially unstructured outlines
             handler_class = StandardResultsHandler
    elif "youtube-script" in tool_id.lower():
        # Check if results contain keys specific to YoutubeScriptOutput
        if "script" in results and "hooks" in results:
             handler_class = YoutubeScriptResultsHandler
        else: # Fallback for potentially unstructured scripts
             handler_class = StandardResultsHandler
    else:
        # Default handler for titles, social posts, etc.
        handler_class = StandardResultsHandler

    # Instantiate and render
    handler = handler_class(tool_id, tool, results)
    return handler.render()