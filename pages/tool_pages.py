from fasthtml.common import *
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
        # Page header
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
                    P("Generating titles...", cls="mt-4 text-lg text-blue-600"),
                    cls="flex flex-col items-center"
                ),
                id="loading-overlay",
                cls="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
            ),
            cls="max-w-2xl mx-auto relative"
        ),
        
        # Tips section
        Div(
            H3("Tips for Better Results", cls="text-xl font-semibold mb-4"),
            Ul(
                Li("Be specific about your topic - include key points you want to highlight", cls="mb-2"),
                Li("Consider your target audience and what would appeal to them", cls="mb-2"),
                Li("The more context you provide, the better the results will be", cls="mb-2"),
                Li("Try different options to see what works best for your needs", cls="mb-2"),
                cls="list-disc list-inside text-gray-700"
            ),
            cls="mt-12 max-w-2xl mx-auto bg-blue-50 p-6 rounded-lg"
        ),
        
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
        """)
    )

def tool_results_page(tool_id, results):
    """Generate a results page for a tool."""
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
    
    # Handle error cases
    if "error" in results:
        return Div(
            H1("Error", cls="text-3xl font-bold text-gray-800 mb-4 text-center"),
            P(results["error"], cls="text-xl text-red-600 mb-6 text-center"),
            A("Try Again", href=tool.route, 
              cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
            cls="text-center py-12"
        )

    # Get metadata and titles
    metadata = results.get("metadata", {})
    titles = results.get("titles", [])
    
    # Ensure we have titles to display
    if not titles and "topic" in results:
        topic = results.get("topic", "")
        platform = results.get("platform", "")
        style = results.get("style", "")
        titles = results.get("titles", [])
        metadata = {"topic": topic, "platform": platform, "style": style}
    
    return Div(
        # Page header
        H1(f"{tool.name} Results",
           cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
           
        P("Here are your generated titles:",
          cls="text-xl text-gray-600 mb-8 text-center"),
        
        # Results section
        Div(
            # Summary of request
            Div(
                P(f"Topic: {metadata.get('topic', '')}", cls="mb-2"),
                P(f"Platform: {metadata.get('platform', '')}", cls="mb-2"),
                P(f"Style: {metadata.get('style', '')}", cls="mb-2"),
                cls="mb-6 p-4 bg-gray-50 rounded"
            ),
            
            # Individual title cards with fixed copy functionality
            Div(
                *[
                    Div(
                        P(f"{i+1}. {title}", cls="mb-1 flex-grow"),
                        Button(
                            "Copy",
                            type="button",
                            onclick=f"copyText('{title.replace('\'', '\\\'').replace('\"', '\\\"').replace('\n', ' ')}')",
                            cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded ml-2"
                        ),
                        cls="flex items-center justify-between p-3 bg-white rounded shadow-sm mb-3 hover:shadow-md transition-shadow"
                    )
                    for i, title in enumerate(titles)
                ],
                cls="mb-6"
            ),
            
            # Navigation buttons
            Div(
                A(f"Generate More Titles",
                  href=tool.route,
                  cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"),
                A("Back to Tools",
                  href="/tools",
                  cls="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"),
                cls="flex justify-center mt-6"
            ),
            
            # Updated JavaScript for copy functionality and hide loading overlay
            Script("""
                function copyText(text) {
                    const tempInput = document.createElement('textarea');
                    tempInput.value = text;
                    document.body.appendChild(tempInput);
                    tempInput.select();
                    document.execCommand('copy');
                    document.body.removeChild(tempInput);
                    
                    const button = event.target;
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    button.disabled = true;
                    
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 2000);
                }
                
                // Hide any loading overlays that might still be visible from the previous page
                document.addEventListener('DOMContentLoaded', function() {
                    const loadingOverlay = document.getElementById('loading-overlay');
                    if (loadingOverlay) {
                        loadingOverlay.classList.add('hidden');
                    }
                    
                    // Also reset any disabled submit buttons
                    const submitButton = document.getElementById('submit-button');
                    if (submitButton) {
                        submitButton.disabled = false;
                    }
                });
            """),
            
            cls="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md"
        )
    )