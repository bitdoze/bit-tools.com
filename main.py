# main.py
from fasthtml.common import *
# Import Starlette's Response types if needed for redirects etc.
# from starlette.responses import RedirectResponse (example)

# Import page content from the pages directory
from pages.home import home as home_page
from pages.about import about as about_page
from pages.contact import contact as contact_page
from pages.tools import tools as tools_page
from pages.tool_pages import tool_page, tool_results_page

# Import the tools registry
from tools import get_all_tools, get_tool_by_id

# Import the page layout component
from components.page_layout import page_layout

# --- CHANGE HERE: Use fast_app() ---
# It sets up defaults including static file serving from a 'static' directory
# It also provides 'rt' for routing.
# Enable debug mode for better error messages during development
app, rt = fast_app(debug=True)
# --- END CHANGE ---

# --- CHANGE HERE: Use @rt decorator ---
@rt("/")
def get_home(): # Changed function name slightly to avoid potential conflicts if reusing 'home'
    """Handler for the home page route."""
    return page_layout(
        title="Home - Bit Tools",
        content=home_page(),
        current_page="/"
    )

@rt("/about")
def get_about(): # Changed function name
    return page_layout(
        title="About Us - Bit Tools",
        content=about_page(),
        current_page="/about"
    )

@rt("/contact")
def get_contact(): # Changed function name
    return page_layout(
        title="Contact Us - Bit Tools",
        content=contact_page(),
        current_page="/contact"
    )

@rt("/submit-contact")
def post_submit_contact(name: str, email: str, message: str): # Changed function name and decorator
    """Handler for contact form submission."""
    # Note: 'subject' field from form isn't used here, add if needed
    acknowledgment = Div(
        Div(
            H1("Thank You!", cls="text-2xl font-bold mb-4"),
            P(f"Hello {name}, we've received your message and will respond to {email} soon.", cls="mb-4"),
            A("Return Home", href="/", cls="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600")
        , cls="bg-white p-6 rounded-lg shadow-md")
    , cls="max-w-md mx-auto")

    return page_layout(
        title="Thank You - Bit Tools",
        content=acknowledgment,
        current_page="/contact"
    )

@rt("/tools")
def get_tools(): # Changed function name
    return page_layout(
        title="AI Tools - Bit Tools",
        content=tools_page(),
        current_page="/tools"
    )

# --- CHANGE HERE: Routing with path parameters ---
@rt("/tools/{tool_id}")
def get_tool_page_handler(tool_id: str): # Changed function name
    tool = get_tool_by_id(tool_id)
    if not tool:
        error_content = Div(
            Div(
                H1("Tool Not Found", cls="text-2xl font-bold mb-4"),
                P("Sorry, the requested tool could not be found.", cls="mb-4"),
                A("Back to Tools", href="/tools", cls="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600")
            , cls="bg-white p-6 rounded-lg shadow-md")
        , cls="max-w-md mx-auto")

        # Consider returning a proper 404 status code
        # from starlette.responses import HTMLResponse
        # return HTMLResponse(page_layout(...), status_code=404)
        return page_layout(
            title="Tool Not Found - Bit Tools",
            content=error_content,
            current_page="/tools"
        )

    return page_layout(
        title=f"{tool.name} - Bit Tools",
        content=tool_page(tool_id),
        current_page=f"/tools/{tool_id}"
    )

# --- CHANGE HERE: Catch-all route ---
# Note: FastHTML with fast_app might handle 404s automatically if debug=False.
# You might need a custom exception handler as shown in docs if you want a specific page.
# Let's keep it simple for now. If you get FastAPI's default 404, customize later.
# @rt("/{path:path}")
# def get_not_found(path: str): ... (Removed for now, rely on default or add exception handler)


# --- CHANGE HERE: POST route for tool processing ---
@rt("/tools/{tool_id}/process")
async def post_process_tool(tool_id: str, request): # Changed function name
    """Handler for tool form submission."""
    tool = get_tool_by_id(tool_id)
    if not tool:
        error_content = Div(
            H1("Tool Not Found", cls="text-2xl font-bold mb-4"),
            P("Sorry, the requested tool could not be found.", cls="mb-4"),
            A("Back to Tools", href="/tools", cls="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"),
            cls="container mx-auto max-w-md bg-white p-6 rounded-lg shadow-md text-center"
        )
        # Consider returning a proper 404 status code
        return page_layout(
            title="Tool Not Found - Bit Tools",
            content=error_content,
            current_page="/tools"
        )

    try:
        form_data = await request.form()
        # Convert form_data (which is MultiDict-like) to a plain dict
        inputs = {key: form_data.get(key) for key in form_data.keys()}
        results = await tool.process(inputs)

        # --- Check for errors returned by the tool's process method ---
        if isinstance(results, dict) and "error" in results:
             error_message = results.get("error", "An unknown processing error occurred.")
             # Log the detailed error if available
             if "validation_errors" in results:
                 print(f"Validation Errors: {results['validation_errors']}") # Log to console
             elif "details" in results:
                 print(f"Error Details: {results['details']}") # Log to console

             error_content = Div(
                 H1("Processing Error", cls="text-2xl font-bold mb-4"),
                 P(f"An error occurred: {error_message}", cls="mb-4"),
                 A("Try Again", href=f"/tools/{tool_id}", cls="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"),
                 cls="container mx-auto max-w-md bg-white p-6 rounded-lg shadow-md text-center"
             )
             # Consider returning a 400 or 500 status code depending on error type
             return page_layout(
                 title="Error - Bit Tools",
                 content=error_content,
                 current_page=f"/tools/{tool_id}"
             )
        # --- End Error Check ---


        # Proceed to results page if no error dictionary from process()
        return page_layout(
            title=f"{tool.name} Results - Bit Tools",
            content=tool_results_page(tool_id, results), # Pass results dict
            current_page=f"/tools/{tool_id}"
        )
    except Exception as e:
        # Catch unexpected errors during processing or rendering results
        import traceback
        print("------ UNEXPECTED ERROR ------")
        traceback.print_exc() # Print full traceback to console
        print("-----------------------------")

        error_content = Div(
            H1("Unexpected Error", cls="text-2xl font-bold mb-4"),
            P(f"An unexpected error occurred: {str(e)}", cls="mb-4"),
            P("Please check the console logs for more details.", cls="text-sm text-gray-500 mb-4"),
            A("Try Again", href=f"/tools/{tool_id}", cls="inline-block px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"),
            cls="container mx-auto max-w-md bg-white p-6 rounded-lg shadow-md text-center"
        )

        # Return 500 Internal Server Error
        # from starlette.responses import HTMLResponse
        # return HTMLResponse(page_layout(...), status_code=500)
        return page_layout(
            title="Error - Bit Tools",
            content=error_content,
            current_page=f"/tools/{tool_id}"
        )

# --- Run the application ---
if __name__ == "__main__":
    # Use the serve() function which works with the app created by fast_app()
    serve()