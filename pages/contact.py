from fasthtml.common import *
from components.social_icons import social_icons


def contact():
    """
    Defines the contact page with a form.

    Returns:
        Components representing the contact page content
    """
    return Div(
        # Page header
        Div(
            H1("Contact Us",
               cls="text-4xl font-bold text-gray-800 mb-2 text-center"),
            P("Get in touch with us for any questions or feedback",
              cls="text-xl text-gray-600 mb-8 text-center"),
            cls="py-8"
        ),

        # Contact information and form
        Div(
            # Contact info
            Div(
                Div(
                    H2("Contact Information", cls="text-2xl font-semibold mb-6"),
                    
                    # Email with icon
                    Div(
                        NotStr('''<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>'''),
                        Div(
                            P("Email", cls="text-sm text-gray-500"),
                            P("dragos@bit-tools.com", cls="font-medium"),
                            cls="ml-4"
                        ),
                        cls="flex items-center mb-6"
                    ),
                    
                    # Connect with us section
                    Div(
                        H3("Connect With Us", cls="text-xl font-semibold mb-4"),
                        social_icons(),
                           
                    
                        cls="mt-8"
                    ),
                    
                    # FAQ or additional info
                    Div(
                        H3("Quick Response", cls="text-xl font-semibold mb-3"),
                        P("We typically respond to all inquiries within 24-48 hours during business days.",
                          cls="text-gray-600 mb-4"),
                        cls="mt-8 bg-blue-50 p-6 rounded-lg"
                    ),
                    
                    cls="bg-white p-8 rounded-lg shadow-md h-full"
                ),
                cls="w-full md:w-2/5 mb-8 md:mb-0 md:pr-6"
            ),

            # Contact form
            Div(
                Div(
                    H2("Send a Message", cls="text-2xl font-semibold mb-6"),
                    Form(
                        # Name field
                        Div(
                            Label("Name", For="name", cls="block text-gray-700 font-medium mb-2"),
                            Input(type="text", id="name", name="name",
                                placeholder="Your name",
                                cls="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"),
                            cls="mb-6"
                        ),
                        # Email field
                        Div(
                            Label("Email", For="email", cls="block text-gray-700 font-medium mb-2"),
                            Input(type="email", id="email", name="email",
                                placeholder="Your email address",
                                cls="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"),
                            cls="mb-6"
                        ),
                        # Subject field
                        Div(
                            Label("Subject", For="subject", cls="block text-gray-700 font-medium mb-2"),
                            Input(type="text", id="subject", name="subject",
                                placeholder="What is this regarding?",
                                cls="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"),
                            cls="mb-6"
                        ),
                        # Message field
                        Div(
                            Label("Message", For="message", cls="block text-gray-700 font-medium mb-2"),
                            Textarea(id="message", name="message",
                                    placeholder="Your message here...",
                                    rows=6,
                                    cls="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"),
                            cls="mb-6"
                        ),
                        # Submit button
                        Button("Send Message",
                            type="submit",
                            cls="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300"),
                        action="/submit-contact",
                        method="post",
                        cls="w-full"
                    ),
                    cls="bg-white p-8 rounded-lg shadow-md"
                ),
                cls="w-full md:w-3/5"
            ),
            cls="md:flex gap-6 max-w-6xl mx-auto"
        ),
        cls="container mx-auto px-4 py-12"
    )
