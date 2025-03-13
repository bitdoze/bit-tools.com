from fasthtml.common import *
from fasthtml.components import NotStr
from tools import get_tool_by_id

def create_form_field(field_id, field_config):
    """Create a form field based on configuration."""
    field_type = field_config.get("type", "text")
    label_text = field_config.get("label", field_id.capitalize())

    # Create the label
    label = Label(label_text, For=field_id, cls="block text-gray-700 font-semibold mb-2")

    # Create the input field based on type
    if field_type == "textarea":
        input_field = Textarea(
            id=field_id,
            name=field_id,
            placeholder=field_config.get("placeholder", ""),
            rows=field_config.get("rows", 3),
            required=field_config.get("required", False),
            cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"
        )
    elif field_type == "select":
        options = []
        for option in field_config.get("options", []):
            options.append(
                Option(
                    option.get("label", option.get("value", "")),
                    value=option.get("value", ""),
                    selected=option.get("selected", False)
                )
            )
        input_field = Select(
            *options,
            id=field_id,
            name=field_id,
            cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"
        )
    else:  # Default to text input
        input_field = Input(
            type=field_type,
            id=field_id,
            name=field_id,
            placeholder=field_config.get("placeholder", ""),
            required=field_config.get("required", False),
            cls="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-500"
        )

    return Div(
        label,
        input_field,
        cls="mb-6"
    )

def get_tool_tips_section(tool):
    """Get tool-specific tips section."""
    # Check if the tool has custom tips
    if hasattr(tool, 'tips') and tool.tips:
        # Tool has custom tips
        tips_items = [Li(tip, cls="mb-2") for tip in tool.tips]
        return Div(
            H2(f"Tips for {tool.name}", cls="text-2xl font-semibold mb-4 text-blue-700"),
            Ul(
                *tips_items,
                cls="list-disc pl-5 space-y-2 text-blue-800"
            ),
            cls="mt-12 max-w-2xl mx-auto bg-blue-50 p-6 rounded-lg"
        )
    else:
        # Generic tips for tools without custom tips
        return Div(
            H3("Tips for Better Results", cls="text-xl font-semibold mb-4"),
            Ul(
                Li("Be specific about your topic - include key points you want to highlight", cls="mb-2"),
                Li("Consider your target audience and what would appeal to them", cls="mb-2"),
                Li("The more context you provide, the better the results will be", cls="mb-2"),
                Li("Try different options to see what works best for your needs", cls="mb-2"),
                cls="list-disc list-inside text-gray-700"
            ),
            cls="mt-12 max-w-2xl mx-auto bg-blue-50 p-6 rounded-lg"
        )

def get_tool_benefits_section(tool):
    """Get tool-specific benefits section."""
    # Check if the tool has custom benefits
    if hasattr(tool, 'benefits') and tool.benefits:
        # Tool has custom benefits
        benefit_items = [Li(benefit, cls="mb-2") for benefit in tool.benefits]
        return Div(
            H2(f"Elevate Your Content with {tool.name}", cls="text-3xl font-bold text-blue-800 mb-6"),
            Div(
                P(f"Our {tool.name} helps you create high-quality content efficiently. By using this AI-powered tool, you can:", cls="text-gray-700"),
                Ul(
                    *benefit_items,
                    cls="list-disc pl-8 space-y-2 text-gray-700 mt-4"
                ),
                P(f"Use these AI-generated {tool.name.lower()} as a starting point to create content that captures attention and drives engagement.", cls="text-gray-700 mt-4"),
                cls="space-y-6"
            ),
            cls="mt-16 bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-xl shadow-lg max-w-2xl mx-auto"
        )
    else:
        # No benefits section for tools without custom benefits
        return Div()

def tool_page(tool_id):
    """
    Generate a tool page based on the tool ID.

    Args:
        tool_id: The ID of the tool to display

    Returns:
        Components representing the tool page content
    """
    # Get the tool
    tool = get_tool_by_id(tool_id)
    if not tool:
        return Div(
            H1("Tool Not Found", cls="text-3xl font-bold text-gray-800 mb-4 text-center"),
            P("Sorry, the requested tool could not be found.",
              cls="text-xl text-gray-600 mb-6 text-center"),
            A("Back to Tools", href="/tools",
              cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
            cls="text-center py-12"
        )

    # Create form fields
    form_fields = []
    for field_id, field_config in tool.input_form_fields.items():
        form_fields.append(create_form_field(field_id, field_config))

    # Add submit button with loading state
    form_fields.append(
        Div(
            Button("Generate",
                   type="submit",
                   id="submit-button",
                   cls="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded"),
            cls="mt-2"
        )
    )

    return Div(
        # Page header with icon
        Div(
            NotStr(tool.icon),
            cls="text-blue-600 w-16 h-16 mx-auto mb-4"
        ),
        H1(tool.name,
           cls="text-3xl font-bold text-gray-800 mb-2 text-center"),

        P(f"Generate {tool.name.lower()} with the help of AI.",
          cls="text-xl text-gray-600 mb-8 text-center"),

        # Tool interface
        Div(
            Form(
                *form_fields,
                action=f"/tools/{tool_id}/process",
                method="post",
                id="tool-form",
                onsubmit="return showLoading();",
                cls="bg-white p-6 rounded-lg shadow-md"
            ),
            # Loading overlay
            Div(
                Div(
                    Div(cls="w-12 h-12 rounded-full border-4 border-blue-600 border-t-transparent animate-spin"),
                    P("Processing your request...", cls="mt-4 text-lg text-blue-600"),
                    cls="flex flex-col items-center"
                ),
                id="loading-overlay",
                cls="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
            ),
            cls="max-w-2xl mx-auto relative"
        ),

        # Tool-specific tips section
        get_tool_tips_section(tool),
        
        # Tool benefits section
        get_tool_benefits_section(tool),

        # JavaScript for loading state
        Script("""
            function showLoading() {
                document.getElementById('loading-overlay').classList.remove('hidden');
                document.getElementById('submit-button').disabled = true;
                // Return true to allow the form to submit
                return true;
            }

            // Make sure loading overlay is hidden when page loads
            document.addEventListener('DOMContentLoaded', function() {
                // Reset any previous state
                const loadingOverlay = document.getElementById('loading-overlay');
                if (loadingOverlay) {
                    loadingOverlay.classList.add('hidden');
                }

                const submitButton = document.getElementById('submit-button');
                if (submitButton) {
                    submitButton.disabled = false;
                }
            });
            
            // Handle browser back/forward navigation
            window.addEventListener('popstate', function() {
                // Reset loading state when using browser navigation controls
                const loadingOverlay = document.getElementById('loading-overlay');
                if (loadingOverlay) {
                    loadingOverlay.classList.add('hidden');
                }

                const submitButton = document.getElementById('submit-button');
                if (submitButton) {
                    submitButton.disabled = false;
                }
            });
            
            // Force hide loading overlay on page load and back button
            // This ensures the loading overlay is hidden even if the popstate event doesn't fire properly
            document.addEventListener('visibilitychange', function() {
                if (!document.hidden) {
                    // Page is now visible (e.g., after returning from another tab or using back button)
                    const loadingOverlay = document.getElementById('loading-overlay');
                    if (loadingOverlay) {
                        loadingOverlay.classList.add('hidden');
                    }

                    const submitButton = document.getElementById('submit-button');
                    if (submitButton) {
                        submitButton.disabled = false;
                    }
                }
            });
        """)
    )
