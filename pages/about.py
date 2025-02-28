from fasthtml.common import *
from components.social_icons import social_icons
def about():
    """
    Defines the about page content.

    Returns:
        Components representing the about page content
    """
    return Div(
        # Page header
        H1("About Bit Tools",
           cls="text-3xl font-bold text-gray-800 mb-6 text-center"),

        # Main content
        Div(
            # Platform description
            Div(
                H2("Our Mission", cls="text-2xl font-semibold mb-4"),
                P("Welcome to Bit Tools, your go-to platform for AI-powered content creation tools. "
                  "We're dedicated to helping you create engaging content with minimal effort using "
                  "the power of artificial intelligence.",
                  cls="text-gray-600 mb-4"),
                P("Our tools are designed to be simple, effective, and accessible to everyone, "
                  "whether you're a content creator, marketer, or social media manager.",
                  cls="text-gray-600 mb-4"),
                
                # Features list
                H3("What We Offer", cls="text-xl font-semibold mt-6 mb-3"),
                Ul(
                    Li("🚀 AI-powered content generation", cls="mb-2"),
                    Li("🔧 Platform-specific optimizations", cls="mb-2"),
                    Li("🎯 Customizable tone and style options", cls="mb-2"),
                    Li("⚡ Fast and efficient results", cls="mb-2"),
                    cls="list-disc pl-6 text-gray-600 mb-6"
                ),
                cls="mb-8"
            ),

            # About the creator
            Div(
                H2("About the Creator", cls="text-2xl font-semibold mb-4"),
                P("Hey there! I'm Dragos, an IT professional with over a decade of experience "
                  "and a DevOps specialist for the past four years. I'm passionate about sharing "
                  "knowledge and helping others find the right tools for their needs.",
                  cls="text-gray-600 mb-4"),
                
                P("Beyond Bit Tools, I run several other technical platforms:",
                  cls="text-gray-600 mb-4"),
                
                Ul(
                    Li(
                        A("ToolHunt", href="https://toolhunt.net", cls="text-blue-600 hover:text-blue-800"),
                        " - A collection of self-hosted tools and Mac apps, built with Astro and AI",
                        cls="mb-2"
                    ),
                    Li(
                        A("WPDoze", href="https://wpdoze.com", cls="text-blue-600 hover:text-blue-800"),
                        " - WordPress tutorials and insights",
                        cls="mb-2"
                    ),
                    Li(
                        A("BitDoze", href="https://bitdoze.com", cls="text-blue-600 hover:text-blue-800"),
                        " - Linux, static sites, CMS, VPS, and DevOps resources",
                        cls="mb-2"
                    ),
                    cls="list-disc pl-6 text-gray-600 mb-6"
                ),
                cls="mb-8 bg-white p-6 rounded-lg shadow-md"
            ),

            # Connect section
            Div(
                H2("Connect With Me", cls="text-2xl font-semibold mb-4"),
                social_icons(),
                cls="mb-8"
            ),

            # Beyond Tech section
            Div(
                H2("Beyond Tech", cls="text-2xl font-semibold mb-4"),
                P("When I'm not working on technical projects, you can find me:",
                  cls="text-gray-600 mb-4"),
                Ul(
                    Li("✈️ Exploring new destinations", cls="mb-2"),
                    Li("🎬 Enjoying movies", cls="mb-2"),
                    Li("🌐 Managing multiple affiliate sites", cls="mb-2"),
                    Li("📚 Sharing knowledge with the community", cls="mb-2"),
                    cls="list-disc pl-6 text-gray-600"
                ),
                cls="bg-gray-50 p-6 rounded-lg"
            ),
            cls="max-w-4xl mx-auto"
        ),
        cls="container mx-auto px-4 py-12"
    )
