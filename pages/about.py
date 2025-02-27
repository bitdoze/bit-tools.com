from fasthtml.common import *

def about():
    """
    Defines the about page content.

    Returns:
        Components representing the about page content
    """
    return Div(
        # Page header
        H1("About Us",
           cls="text-3xl font-bold text-gray-800 mb-6 text-center"),

        # Main content
        Div(
            # Company description
            Div(
                H2("Our Story", cls="text-2xl font-semibold mb-4"),
                P("Founded in 2025, MyWebsite was created to help developers build "
                  "beautiful web applications using Python. Our mission is to make "
                  "web development accessible, enjoyable, and productive.",
                  cls="text-gray-600 mb-4"),
                P("We believe that Python developers should be able to create "
                  "stunning web applications without having to learn multiple "
                  "languages and frameworks.",
                  cls="text-gray-600 mb-4"),
                cls="mb-8"
            ),

            # Team section
            Div(
                H2("Our Team", cls="text-2xl font-semibold mb-4"),
                Div(
                    # Team member 1
                    Div(
                        H3("Jane Doe", cls="text-xl font-semibold"),
                        P("Founder & CEO", cls="text-gray-500 italic mb-2"),
                        P("Python enthusiast with 15 years of experience in web development.",
                          cls="text-gray-600"),
                        cls="bg-white p-4 rounded shadow-md"
                    ),
                    # Team member 2
                    Div(
                        H3("John Smith", cls="text-xl font-semibold"),
                        P("CTO", cls="text-gray-500 italic mb-2"),
                        P("Full-stack developer with a passion for clean, maintainable code.",
                          cls="text-gray-600"),
                        cls="bg-white p-4 rounded shadow-md"
                    ),
                    cls="grid grid-cols-1 md:grid-cols-2 gap-6"
                )
            )
        )
    )
