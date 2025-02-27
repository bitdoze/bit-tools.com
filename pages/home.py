from fasthtml.common import *

def home():
    """
    Defines the home page content.

    Returns:
        Components representing the home page content
    """
    return Div(
        # Hero section
        Div(
            H1("Welcome to bit-tools.com",
               cls="text-4xl font-bold text-gray-800 mb-4"),
            P("Build beautiful web applications with FastHTML and Python.",
              cls="text-xl text-gray-600 mb-6"),
            Div(
                A("Get Started",
                  href="/about",
                  cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"),
                A("Learn More",
                  href="/contact",
                  cls="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"),
                cls="flex"
            ),
            cls="py-12 text-center"
        ),

        # Features section
        Div(
            H2("Key Features", cls="text-3xl font-bold text-center mb-8"),
            Div(
                # Feature 1
                Div(
                    H3("Easy to Learn", cls="text-xl font-semibold mb-2"),
                    P("Built on Python, making web development accessible to everyone.",
                      cls="text-gray-600"),
                    cls="bg-white p-6 rounded-lg shadow-md"
                ),
                # Feature 2
                Div(
                    H3("Highly Productive", cls="text-xl font-semibold mb-2"),
                    P("Create web applications faster with fewer lines of code.",
                      cls="text-gray-600"),
                    cls="bg-white p-6 rounded-lg shadow-md"
                ),
                # Feature 3
                Div(
                    H3("Scalable", cls="text-xl font-semibold mb-2"),
                    P("Easily expand your application as your needs grow.",
                      cls="text-gray-600"),
                    cls="bg-white p-6 rounded-lg shadow-md"
                ),
                cls="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
            ),
            cls="py-8"
        )
    )
