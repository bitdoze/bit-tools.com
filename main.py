from fasthtml.common import *

# Import page content from the pages directory
from pages.home import home as home_page
from pages.about import about as about_page
from pages.contact import contact as contact_page

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

# Run the application
if __name__ == "__main__":
    # Using FastHTML's built-in serve() function
    serve()
