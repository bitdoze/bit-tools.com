from fasthtml.common import *

def contact():
    """
    Defines the contact page with a form.

    Returns:
        Components representing the contact page content
    """
    return Div(
        # Page header
        H1("Contact Us",
           cls="text-3xl font-bold text-gray-800 mb-6 text-center"),

        # Contact information and form
        Div(
            # Contact info
            Div(
                H2("Get in Touch", cls="text-2xl font-semibold mb-4"),
                P("We'd love to hear from you! Please use the form or contact "
                  "information below to reach out.",
                  cls="text-gray-600 mb-4"),
                Div(
                    P(Strong("Email: "), "info@mywebsite.com", cls="mb-2"),
                    P(Strong("Phone: "), "+1 (555) 123-4567", cls="mb-2"),
                    P(Strong("Address: "), "123 Web Street, Internet City, 10101", cls="mb-2"),
                    cls="mb-6"
                ),
                cls="mb-8 md:pr-8"
            ),

            # Contact form
            Div(
                H2("Send a Message", cls="text-2xl font-semibold mb-4"),
                Form(
                    # Name field
                    Div(
                        Label("Name", For="name", cls="block text-gray-700 mb-1"),
                        Input(type="text", id="name", name="name",
                              placeholder="Your name",
                              cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"),
                        cls="mb-4"
                    ),
                    # Email field
                    Div(
                        Label("Email", For="email", cls="block text-gray-700 mb-1"),
                        Input(type="email", id="email", name="email",
                              placeholder="Your email",
                              cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"),
                        cls="mb-4"
                    ),
                    # Message field
                    Div(
                        Label("Message", For="message", cls="block text-gray-700 mb-1"),
                        Textarea(id="message", name="message",
                                placeholder="Your message",
                                rows=5,
                                cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"),
                        cls="mb-6"
                    ),
                    # Submit button
                    Button("Send Message",
                           type="submit",
                           cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
                    action="/submit-contact",
                    method="post",
                    cls="bg-white p-6 rounded-lg shadow-md"
                )
            ),
            cls="md:flex"
        )
    )
