from fasthtml.common import *

# Import page content from the pages directory
from pages.home import home as home_page
from pages.about import about as about_page
from pages.contact import contact as contact_page
from pages.tools import tools as tools_page
from pages.tool_pages import tool_page, tool_results_page

# Import the tools registry
from tools import get_all_tools, get_tool_by_id

# Import the page layout component
from components import page_layout

# Initialize the FastHTML application
app = FastHTML()

# Define route for the home page
@app.get("/")
def home():
    """Handler for the home page route."""
    return page_layout(
        title="Home - MyWebsite",
        content=home_page(),
        current_page="/"
    )

# Define route for the about page
@app.get("/about")
def about():
    """Handler for the about page route."""
    return page_layout(
        title="About Us - MyWebsite",
        content=about_page(),
        current_page="/about"
    )

# Define route for the contact page
@app.get("/contact")
def contact():
    """Handler for the contact page route."""
    return page_layout(
        title="Contact Us - MyWebsite",
        content=contact_page(),
        current_page="/contact"
    )

# Handle form submission (for the contact form)
@app.post("/submit-contact")
def submit_contact(name: str, email: str, message: str):
    """
    Handler for contact form submission.

    In a real application, you might store this data or send an email.
    """
    # Simple acknowledgment page
    acknowledgment = Div(
        H1("Thank You!", cls="text-3xl font-bold text-gray-800 mb-4"),
        P(f"Hello {name}, we've received your message and will respond to {email} soon.",
          cls="text-xl text-gray-600 mb-6"),
        A("Return Home", href="/", cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
        cls="text-center py-12"
    )

    return page_layout(
        title="Thank You - MyWebsite",
        content=acknowledgment,
        current_page="/contact"
    )

# Handle 404 Not Found errors
@app.get("/{path:path}")
def not_found(path: str):
    """Handler for any routes that don't match the defined routes."""
    error_content = Div(
        H1("404 - Page Not Found", cls="text-3xl font-bold text-gray-800 mb-4"),
        P(f"Sorry, the page '/{path}' does not exist.",
          cls="text-xl text-gray-600 mb-6"),
        A("Return Home", href="/", cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
        cls="text-center py-12"
    )

    return page_layout(
        title="404 Not Found - MyWebsite",
        content=error_content,
        current_page="/"
    )

# Define route for the tools overview page
# Move the tools route before the catch-all 404 route
@app.get("/tools")
def tools():
    """Handler for the tools overview page route."""
    return page_layout(
        title="AI Tools - Bit Tools",
        content=tools_page(),
        current_page="/tools"
    )

@app.get("/tools/{tool_id}")
def tool_page_handler(tool_id: str):
    """Handler for individual tool pages."""
    tool = get_tool_by_id(tool_id)
    if not tool:
        return page_layout(
            title="Tool Not Found - Bit Tools",
            content=Div(
                H1("Tool Not Found", cls="text-3xl font-bold text-gray-800 mb-4 text-center"),
                P("Sorry, the requested tool could not be found.",
                  cls="text-xl text-gray-600 mb-6 text-center"),
                A("Back to Tools", href="/tools", 
                  cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
                cls="text-center py-12"
            ),
            current_page="/tools"
        )
    
    return page_layout(
        title=f"{tool.name} - Bit Tools",
        content=tool_page(tool_id),
        current_page=f"/tools/{tool_id}"
    )

# Move the 404 route to the end
@app.get("/{path:path}")
def not_found(path: str):
    """Handler for any routes that don't match the defined routes."""
    error_content = Div(
        H1("404 - Page Not Found", cls="text-3xl font-bold text-gray-800 mb-4"),
        P(f"Sorry, the page '/{path}' does not exist.",
          cls="text-xl text-gray-600 mb-6"),
        A("Return Home", href="/", cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
        cls="text-center py-12"
    )

    return page_layout(
        title="404 Not Found - Bit Tools",
        content=error_content,
        current_page="/"
    )

# Handle tool processing
@app.post("/tools/{tool_id}/process")
async def process_tool(tool_id: str, request):
    """
    Handler for tool form submission.
    
    Args:
        tool_id: The ID of the tool to process
        request: The request object containing form data
    """
    tool = get_tool_by_id(tool_id)
    if not tool:
        return page_layout(
            title="Tool Not Found - Bit Tools",
            content=Div(
                H1("Tool Not Found", cls="text-3xl font-bold text-gray-800 mb-4 text-center"),
                P("Sorry, the requested tool could not be found.",
                  cls="text-xl text-gray-600 mb-6 text-center"),
                A("Back to Tools", href="/tools", 
                  cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
                cls="text-center py-12"
            ),
            current_page="/tools"
        )
    
    try:
        # Get form data
        form_data = await request.form()
        inputs = {key: value for key, value in form_data.items()}
        
        # Process the inputs
        results = tool.process(inputs)
        
        # Return the results page
        return page_layout(
            title=f"{tool.name} Results - Bit Tools",
            content=tool_results_page(tool_id, results),
            current_page=f"/tools/{tool_id}"
        )
    except Exception as e:
        # Handle errors gracefully
        error_content = Div(
            H1("Processing Error", cls="text-3xl font-bold text-gray-800 mb-4 text-center"),
            P(f"Sorry, there was an error processing your request: {str(e)}",
              cls="text-xl text-gray-600 mb-6 text-center"),
            A("Try Again", href=f"/tools/{tool_id}", 
              cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
            cls="text-center py-12"
        )

        return page_layout(
            title="Error - Bit Tools",
            content=error_content,
            current_page=f"/tools/{tool_id}"
        )

# Run the application
if __name__ == "__main__":
    # Using FastHTML's built-in serve() function
    serve()
