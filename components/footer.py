from fasthtml.common import *

def footer():
    """Creates a consistent footer."""
    return Footer(
        Div(
            P("© 2025 Bit Tools. All rights reserved.", cls="text-center text-gray-500"),
            cls="container mx-auto px-4 py-6"
        ),
        cls="bg-gray-100 mt-auto"
    )