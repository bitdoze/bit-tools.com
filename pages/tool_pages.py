# pages/tool_pages.py
from fasthtml.common import *
from fasthtml.components import NotStr
from tools import get_tool_by_id
import json
import logging
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Set up logging
logger = logging.getLogger(__name__)

# --- create_form_field, tool_page, error_page remain the same ---
# (Keep existing functions as they were)
def create_form_field(field_id, field_config):
    """Create a form field based on configuration."""
    # (Implementation remains the same as in fasthtml-agno2.txt)
    field_type = field_config.get("type", "text")
    label_text = field_config.get("label", field_id.capitalize())
    label = Label(label_text, For=field_id, cls="block text-gray-700 font-semibold mb-2")
    if field_type == "textarea":
        input_field = Textarea(id=field_id, name=field_id, placeholder=field_config.get("placeholder", ""), rows=field_config.get("rows", 3), required=field_config.get("required", False), cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500")
    elif field_type == "select":
        options = [Option(opt.get("label", opt.get("value", "")), value=opt.get("value", ""), selected=opt.get("selected", False)) for opt in field_config.get("options", [])]
        input_field = Select(*options, id=field_id, name=field_id, cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500")
    else:
        input_field = Input(type=field_type, id=field_id, name=field_id, placeholder=field_config.get("placeholder", ""), required=field_config.get("required", False), cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500")
    return Div(label, input_field, cls="mb-6")

def tool_page(tool_id):
    """Generate a tool page based on the tool ID."""
    # (Implementation remains the same as in fasthtml-agno2.txt)
    tool = get_tool_by_id(tool_id)
    if not tool:
        return Div(H1("Tool Not Found", cls="text-3xl font-bold text-gray-800 mb-4 text-center"), P("Sorry...", cls="text-xl text-gray-600 mb-6 text-center"), A("Back to Tools", href="/tools", cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"), cls="text-center py-12")
    form_fields = [create_form_field(fid, fconfig) for fid, fconfig in tool.input_form_fields.items()]
    form_fields.append(Div(Button("Generate", type="submit", id="submit-button", cls="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded"), cls="mt-2"))
    return Div( Div(NotStr(tool.icon), cls="text-blue-600 w-16 h-16 mx-auto mb-4"), H1(tool.name, cls="text-3xl font-bold text-gray-800 mb-2 text-center"), P(f"Generate {tool.name.lower()} with AI.", cls="text-xl text-gray-600 mb-8 text-center"), Div(Form(*form_fields, action=f"/tools/{tool_id}/process", method="post", id="tool-form", onsubmit="return showLoading();", cls="bg-white p-6 rounded-lg shadow-md"), Div(Div(Div(cls="w-12 h-12 rounded-full border-4 border-blue-600 border-t-transparent animate-spin"), P("Processing...", cls="mt-4 text-lg text-blue-600"), cls="flex flex-col items-center"), id="loading-overlay", cls="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"), cls="max-w-2xl mx-auto relative"), Div(H3("Tips", cls="text-xl font-semibold mb-4"), Ul(*[Li(tip, cls="mb-2") for tip in tool.tips] if hasattr(tool, 'tips') and tool.tips else [Li("Be specific.", cls="mb-2"), Li("Consider your audience.", cls="mb-2"), Li("Provide context.", cls="mb-2")], cls="list-disc list-inside text-gray-700"), cls="mt-12 max-w-2xl mx-auto bg-blue-50 p-6 rounded-lg"), Script(""" function showLoading() { document.getElementById('loading-overlay').classList.remove('hidden'); document.getElementById('submit-button').disabled = true; return true; } document.addEventListener('DOMContentLoaded', function() { const loadingOverlay = document.getElementById('loading-overlay'); if (loadingOverlay) { loadingOverlay.classList.add('hidden'); } const submitButton = document.getElementById('submit-button'); if (submitButton) { submitButton.disabled = false; } }); window.addEventListener('popstate', function() { const loadingOverlay = document.getElementById('loading-overlay'); if (loadingOverlay) { loadingOverlay.classList.add('hidden'); } const submitButton = document.getElementById('submit-button'); if (submitButton) { submitButton.disabled = false; } }); document.addEventListener('visibilitychange', function() { if (!document.hidden) { const loadingOverlay = document.getElementById('loading-overlay'); if (loadingOverlay) { loadingOverlay.classList.add('hidden'); } const submitButton = document.getElementById('submit-button'); if (submitButton) { submitButton.disabled = false; } } }); """))

def error_page(title, message, back_url=None):
    """Generate an error page."""
    # (Implementation remains the same as in fasthtml-agno2.txt)
    if not back_url: back_url = "/tools"
    return Div(H1(title, cls="text-3xl font-bold text-gray-800 mb-4 text-center"), P(message, cls="text-xl text-red-600 mb-6 text-center"), A("Back", href=back_url, cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"), cls="text-center py-12")

# Updated tool_results_page function
def tool_results_page(tool_id, results: Dict[str, Any]):
    """
    Generate an enhanced results page for a tool.
    Assumes `results` is a dictionary, potentially containing structured data.
    """
    logger.info(f"Rendering results page for tool: {tool_id}")
    logger.info(f"Results keys: {results.keys() if isinstance(results, dict) else 'Not a dict'}")

    # Get the tool
    tool = get_tool_by_id(tool_id)
    if not tool:
        return error_page("Tool Not Found", "Sorry, the requested tool could not be found.")

    # Handle error directly from results dictionary
    if isinstance(results, dict) and "error" in results:
        error_message = results.get("error", "An unknown error occurred.")
        logger.error(f"Tool processing error for {tool_id}: {error_message}")
        # Optionally include raw_text if available for debugging
        if "raw_text" in results:
             logger.error(f"Raw text at time of error: {results['raw_text'][:500]}...")
        return error_page("Processing Error", error_message, f"/tools/{tool_id}")

    # Ensure results is a dictionary (should be by now from the factory)
    if not isinstance(results, dict):
        logger.error(f"Results are not a dictionary for {tool_id}. Type: {type(results)}")
        return error_page("Internal Error", "Failed to process tool results correctly.", f"/tools/{tool_id}")

    # --- Simplified Logic: Route directly to the appropriate handler ---
    # The factory now prepares the `results` dictionary consistently.
    # The results/__init__.py will choose the correct handler based on tool_id/results keys.

    from .tool_pages.results import create_results_page # Import locally to avoid circularity if needed

    try:
        return create_results_page(tool_id, tool, results)
    except Exception as e:
        logger.error(f"Error creating results page for {tool_id}: {str(e)}", exc_info=True)
        return error_page("Display Error", f"Could not display results: {str(e)}", f"/tools/{tool_id}")