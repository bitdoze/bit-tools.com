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

# Initialize the FastHTML application with Pico CSS enabled
app, rt = fast_app(
    pico=True,  # Enable Pico CSS
    hdrs=(
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css"),
        Style("""
            :root {
                --primary: #1095c1;
                --primary-hover: #0a6d8e;
            }
            .container {
                margin: 0 auto;
                padding: 0 20px;
                max-width: 1200px;
            }
            .text-center {
                text-align: center;
            }
        """)
    )
)

@app.get("/")
def home():
    """Handler for the home page route."""
    return page_layout(
        title="Home - Bit Tools",
        content=home_page(),
        current_page="/"
    )

@app.get("/about")
def about():
    return page_layout(
        title="About Us - Bit Tools",
        content=about_page(),
        current_page="/about"
    )

@app.get("/contact")
def contact():
    return page_layout(
        title="Contact Us - Bit Tools",
        content=contact_page(),
        current_page="/contact"
    )

@app.post("/submit-contact")
def submit_contact(name: str, email: str, message: str):
    """Handler for contact form submission."""
    acknowledgment = Container(
        Card(
            H1("Thank You!"),
            P(f"Hello {name}, we've received your message and will respond to {email} soon."),
            A("Return Home", href="/", role="button")
        )
    )
    return page_layout(
        title="Thank You - Bit Tools",
        content=acknowledgment,
        current_page="/contact"
    )

@app.get("/tools")
def tools():
    return page_layout(
        title="AI Tools - Bit Tools",
        content=tools_page(),
        current_page="/tools"
    )

@app.get("/tools/{tool_id}")
def tool_page_handler(tool_id: str):
    tool = get_tool_by_id(tool_id)
    if not tool:
        error_content = Container(
            Card(
                H1("Tool Not Found"),
                P("Sorry, the requested tool could not be found."),
                A("Back to Tools", href="/tools", role="button")
            )
        )
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

@app.get("/{path:path}")
def not_found(path: str):
    error_content = Container(
        Card(
            H1("404 - Page Not Found"),
            P(f"Sorry, the page '/{path}' does not exist."),
            A("Return Home", href="/", role="button")
        )
    )
    return page_layout(
        title="404 Not Found - Bit Tools",
        content=error_content,
        current_page="/"
    )

@app.post("/tools/{tool_id}/process")
async def process_tool(tool_id: str, request):
    """Handler for tool form submission."""
    tool = get_tool_by_id(tool_id)
    if not tool:
        error_content = Article(
            H1("Tool Not Found"),
            P("Sorry, the requested tool could not be found."),
            A("Back to Tools", href="/tools", role="button"),
            cls="container text-center"
        )
        return page_layout(
            title="Tool Not Found - Bit Tools",
            content=error_content,
            current_page="/tools"
        )
    
    try:
        form_data = await request.form()
        inputs = {key: value for key, value in form_data.items()}
        results = tool.process(inputs)
        
        return page_layout(
            title=f"{tool.name} Results - Bit Tools",
            content=tool_results_page(tool_id, results),
            current_page=f"/tools/{tool_id}"
        )
    except Exception as e:
        error_content = Article(
            H1("Processing Error"),
            P(f"An error occurred while processing your request: {str(e)}"),
            A("Try Again", href=f"/tools/{tool_id}", role="button"),
            cls="container text-center"
        )
        return page_layout(
            title="Error - Bit Tools",
            content=error_content,
            current_page=f"/tools/{tool_id}"
        )

# Run the application
if __name__ == "__main__":
    serve()
