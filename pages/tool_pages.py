from fasthtml.common import *
from fasthtml.components import NotStr  # Add this import for NotStr component
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
        # Page header with icon
        Div(
            NotStr(tool.icon),  # Changed from Raw to NotStr
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

def error_page(title, message, back_url=None):
    """Generate an error page."""
    if not back_url:
        back_url = "/tools"
        
    return Div(
        H1(title, cls="text-3xl font-bold text-gray-800 mb-4 text-center"),
        P(message, cls="text-xl text-red-600 mb-6 text-center"),
        A("Back", href=back_url,
          cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
        cls="text-center py-12"
    )

def tool_results_page(tool_id, results):
    """Generate an enhanced results page for a tool."""
    tool = get_tool_by_id(tool_id)
    if not tool:
        return error_page("Tool Not Found", "Sorry, the requested tool could not be found.")
    
    # Handle error cases
    if "error" in results:
        return error_page("Error", results["error"], tool.route)

    # Get metadata and titles/content
    metadata = results.get("metadata", {})
    titles = results.get("titles", [])
    
    # Handle text transformation tools
    original_text = results.get("original_text", "")
    transformed_text = results.get("transformed_text", "")
    
    # Determine if this is a transformation tool
    is_transformation = original_text and transformed_text
    
    # Determine if this is an outline tool by checking the tool ID
    is_outline_tool = "outline" in tool_id.lower()
    
    # Create tabs for different ways to view results
    if is_outline_tool:
        tabs = [
            {"id": "list", "label": "List View", "selected": True},
            {"id": "card", "label": "Card View", "selected": False},
            {"id": "markdown", "label": "Markdown", "selected": False},
            {"id": "copy", "label": "Copy All", "selected": False}
        ]
    else:
        tabs = [
            {"id": "list", "label": "List View", "selected": True},
            {"id": "card", "label": "Card View", "selected": False},
            {"id": "copy", "label": "Copy All", "selected": False}
        ]
    
    tab_buttons = Div(
        *[
            Button(
                tab["label"],
                type="button",
                id=f"tab-{tab['id']}",
                onclick=f"switchTab('{tab['id']}')",
                cls=f"px-4 py-2 rounded-t {'bg-white text-blue-600 font-bold' if tab['selected'] else 'bg-gray-200 text-gray-700'}"
            )
            for tab in tabs
        ],
        cls="flex mb-4"
    )
    
    # For transformation tools, show before/after
    if is_transformation:
        return Div(
            # Page header
            H1(f"{tool.name} Results",
               cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
               
            P("Here is your transformed text:",
              cls="text-xl text-gray-600 mb-8 text-center"),
            
            # Results section
            Div(
                # Summary of request
                Div(
                    *[P(f"{key.capitalize()}: {value}", cls="mb-2")
                      for key, value in metadata.items() if key != "count"],
                    cls="mb-6 p-4 bg-gray-50 rounded"
                ),
                
                # Original and transformed text
                Div(
                    H3("Original Text", cls="text-lg font-bold mb-2"),
                    Div(
                        P(original_text, cls="whitespace-pre-wrap"),
                        cls="p-4 bg-gray-100 rounded mb-6 overflow-auto max-h-60"
                    ),
                    H3("Transformed Text", cls="text-lg font-bold mb-2"),
                    Div(
                        P(transformed_text, cls="whitespace-pre-wrap"),
                        cls="p-4 bg-blue-50 rounded mb-6 overflow-auto max-h-60"
                    ),
                    Button(
                        "Copy Transformed Text",
                        type="button",
                        onclick=f"copyText({repr(transformed_text)})",
                        cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    ),
                    cls="mb-6"
                ),
                
                # Navigation buttons
                Div(
                    A(f"Transform More Text",
                      href=tool.route,
                      cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"),
                    A("Back to Tools",
                      href="/tools",
                      cls="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"),
                    cls="flex justify-center mt-6"
                ),
                
                # JavaScript for copy functionality
                Script("""
                    function copyText(text) {
                        navigator.clipboard.writeText(text).then(() => {
                            const button = event.target;
                            const originalText = button.textContent;
                            button.textContent = 'Copied!';
                            button.disabled = true;
                            
                            setTimeout(() => {
                                button.textContent = originalText;
                                button.disabled = false;
                            }, 2000);
                        });
                    }
                    
                    // Hide any loading overlays
                    document.addEventListener('DOMContentLoaded', function() {
                        const loadingOverlay = document.getElementById('loading-overlay');
                        if (loadingOverlay) {
                            loadingOverlay.classList.add('hidden');
                        }
                        
                        // Reset any disabled submit buttons
                        const submitButton = document.getElementById('submit-button');
                        if (submitButton) {
                            submitButton.disabled = false;
                        }
                    });
                """),
                
                cls="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md"
            )
        )
    
    # List view (default)
    if is_outline_tool:
        # For outline tools, preserve the hierarchy and indentation
        list_items = []
        current_section = None
        section_items = []
        
        for i, line in enumerate(titles):
            # Check if this is a main section (no indentation or numbering)
            if line.strip() and (line[0].isalpha() or line[0].isdigit()):
                # If we have a previous section, add it to the list
                if current_section and section_items:
                    list_items.append(
                        Div(
                            P(current_section, cls="font-bold mb-2"),
                            Div(
                                *[P(item, cls="ml-4 mb-1") for item in section_items],
                                cls="mb-3"
                            ),
                            cls="mb-4 p-4 bg-white rounded shadow-md"
                        )
                    )
                    section_items = []
                
                # Start a new section
                current_section = line
            else:
                # This is a subsection or bullet point
                section_items.append(line)
        
        # Add the last section
        if current_section and section_items:
            list_items.append(
                Div(
                    P(current_section, cls="font-bold mb-2"),
                    Div(
                        *[P(item, cls="ml-4 mb-1") for item in section_items],
                        cls="mb-3"
                    ),
                    cls="mb-4 p-4 bg-white rounded shadow-md"
                )
            )
        
        # If we couldn't parse the structure, fall back to treating each line as a separate item
        if not list_items:
            list_items = [
                Div(
                    P(title, cls="mb-1"),
                    cls="p-4 bg-white rounded shadow-md mb-3"
                )
                for title in titles
            ]
        
        # Add a copy button for the entire outline
        list_items.append(
            Div(
                Button(
                    "Copy Entire Outline",
                    type="button",
                    onclick=f"copyText({repr(chr(10).join(titles))})",
                    cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                ),
                cls="text-center mt-4"
            )
        )
        
        list_view = Div(
            *list_items,
            id="list-view",
            cls="mb-6"
        )
        
        # Card view for outlines - show the entire outline in one card
        card_view = Div(
            Div(
                H3("Complete Outline", cls="text-xl font-bold mb-4 text-center"),
                *[P(title, cls="mb-2") for title in titles],
                Button(
                    "Copy Entire Outline",
                    type="button",
                    onclick=f"copyText({repr(chr(10).join(titles))})",
                    cls="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                ),
                cls="p-6 bg-white rounded shadow-lg"
            ),
            id="card-view",
            cls="mb-6 hidden"
        )
    else:
        # Standard list view for non-outline tools
        list_view = Div(
            *[
                Div(
                    P(f"{i+1}. {title}", cls="mb-1 flex-grow"),
                    Button(
                        "Copy",
                        type="button",
                        onclick=f"copyText({repr(title)})",
                        cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded ml-2"
                    ),
                    cls="flex items-center justify-between p-3 bg-white rounded shadow-sm mb-3 hover:shadow-md transition-shadow"
                )
                for i, title in enumerate(titles)
            ],
            id="list-view",
            cls="mb-6"
        )
        
        # Standard card view for non-outline tools
        card_view = Div(
            Div(
                *[
                    Div(
                        P(title, cls="text-center mb-2"),
                        Button(
                            "Copy",
                            type="button",
                            onclick=f"copyText({repr(title)})",
                            cls="w-full text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
                        ),
                        cls="p-4 bg-white rounded shadow-sm hover:shadow-md transition-shadow"
                    )
                    for title in titles
                ],
                cls="grid grid-cols-1 md:grid-cols-2 gap-4"
            ),
            id="card-view",
            cls="mb-6 hidden"
        )
    
    # Markdown view for outline tools
    if is_outline_tool:
        # Convert outline to markdown format
        markdown_lines = []
        current_section = None
        section_items = []
        
        for i, line in enumerate(titles):
            # Check if this is a main section
            if line.strip() and (line[0].isalpha() or line[0].isdigit()):
                # If we have a previous section, add it to the markdown
                if current_section:
                    markdown_lines.append(f"## {current_section}")
                    for item in section_items:
                        markdown_lines.append(f"- {item}")
                    markdown_lines.append("")  # Empty line for spacing
                
                # Start a new section
                current_section = line
                section_items = []
            else:
                # This is a subsection or bullet point
                section_items.append(line)
        
        # Add the last section
        if current_section:
            markdown_lines.append(f"## {current_section}")
            for item in section_items:
                markdown_lines.append(f"- {item}")
        
        # If we couldn't parse the structure, fall back to basic markdown
        if not markdown_lines:
            markdown_lines = [f"- {title}" for title in titles]
        
        # Ensure the markdown text is complete
        markdown_text = "\n".join(markdown_lines)
        
        # Create the markdown view
        markdown_view = Div(
            H3("Markdown Format", cls="text-xl font-bold mb-4 text-center"),
            Div(
                Textarea(
                    markdown_text,
                    rows=15,
                    readonly=True,
                    cls="w-full p-3 border rounded font-mono"
                ),
                Button(
                    "Copy Markdown",
                    type="button",
                    onclick=f"copyText({repr(markdown_text)})",
                    cls="mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                ),
                cls="mb-4"
            ),
            Div(
                H4("Preview:", cls="text-lg font-bold mb-2"),
                Div(
                    # Use zero-md for proper markdown rendering with more specific styling
                    NotStr(f"""
                    <zero-md>
                        <template>
                            <style>
                                .markdown-body {{
                                    background-color: transparent !important;
                                    color: inherit !important;
                                    padding: 0 !important;
                                    font-family: system-ui, sans-serif !important;
                                }}
                                .markdown-body h2 {{
                                    font-size: 1.25rem !important;
                                    font-weight: bold !important;
                                    margin-top: 1rem !important;
                                    margin-bottom: 0.5rem !important;
                                    color: #1a202c !important;
                                }}
                                .markdown-body ul {{
                                    list-style-type: disc !important;
                                    margin-left: 1.5rem !important;
                                    margin-bottom: 1rem !important;
                                    padding-left: 0 !important;
                                }}
                                .markdown-body li {{
                                    margin-bottom: 0.25rem !important;
                                    line-height: 1.5 !important;
                                }}
                                .markdown-body p {{
                                    margin-bottom: 0.5rem !important;
                                    line-height: 1.5 !important;
                                }}
                            </style>
                        </template>
                        <script type="text/markdown">
{markdown_text}
                        </script>
                    </zero-md>
                    """),
                    cls="p-4 bg-gray-50 rounded overflow-auto max-h-80"
                ),
                cls="mt-4"
            ),
            id="markdown-view",
            cls="mb-6 hidden"
        )
    else:
        # No markdown view for non-outline tools
        markdown_view = Div(id="markdown-view", cls="hidden")
    
    # Copy all view
    if is_outline_tool:
        # For outline tools, format the content with proper spacing
        formatted_outline = "\n".join(titles)
        copy_all_view = Div(
            H3("Complete Outline", cls="text-xl font-bold mb-4 text-center"),
            Textarea(
                formatted_outline,
                rows=15,
                readonly=True,
                cls="w-full p-3 border rounded font-mono"
            ),
            Button(
                "Copy All",
                type="button",
                onclick="copyAllText()",
                cls="mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            ),
            id="copy-view",
            cls="mb-6 hidden"
        )
    else:
        # Standard copy all view for non-outline tools
        copy_all_view = Div(
            Textarea(
                "\n".join(titles),
                rows=10,
                readonly=True,
                cls="w-full p-3 border rounded"
            ),
            Button(
                "Copy All",
                type="button",
                onclick="copyAllText()",
                cls="mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            ),
            id="copy-view",
            cls="mb-6 hidden"
        )
    
    # Enhanced JavaScript for tab switching and copy functionality
    enhanced_script = """
        function switchTab(tabId) {
            // Hide all views
            document.getElementById('list-view').classList.add('hidden');
            document.getElementById('card-view').classList.add('hidden');
            document.getElementById('copy-view').classList.add('hidden');
            
            // Hide markdown view if it exists
            const markdownView = document.getElementById('markdown-view');
            if (markdownView) {
                markdownView.classList.add('hidden');
            }
            
            // Show selected view
            document.getElementById(tabId + '-view').classList.remove('hidden');
            
            // Update tab buttons
            document.getElementById('tab-list').classList.remove('bg-white', 'text-blue-600', 'font-bold');
            document.getElementById('tab-list').classList.add('bg-gray-200', 'text-gray-700');
            document.getElementById('tab-card').classList.remove('bg-white', 'text-blue-600', 'font-bold');
            document.getElementById('tab-card').classList.add('bg-gray-200', 'text-gray-700');
            document.getElementById('tab-copy').classList.remove('bg-white', 'text-blue-600', 'font-bold');
            document.getElementById('tab-copy').classList.add('bg-gray-200', 'text-gray-700');
            
            // Update markdown tab if it exists
            const markdownTab = document.getElementById('tab-markdown');
            if (markdownTab) {
                markdownTab.classList.remove('bg-white', 'text-blue-600', 'font-bold');
                markdownTab.classList.add('bg-gray-200', 'text-gray-700');
            }
            
            document.getElementById('tab-' + tabId).classList.remove('bg-gray-200', 'text-gray-700');
            document.getElementById('tab-' + tabId).classList.add('bg-white', 'text-blue-600', 'font-bold');
        }
        
        function copyText(text) {
            navigator.clipboard.writeText(text).then(() => {
                const button = event.target;
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                button.disabled = true;
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.disabled = false;
                }, 2000);
            });
        }
        
        function copyAllText() {
            const textarea = document.querySelector('#copy-view textarea');
            navigator.clipboard.writeText(textarea.value).then(() => {
                const button = document.querySelector('#copy-view button');
                button.textContent = 'Copied!';
                button.disabled = true;
                
                setTimeout(() => {
                    button.textContent = 'Copy All';
                    button.disabled = false;
                }, 2000);
            });
        }
        
        // Hide any loading overlays
        document.addEventListener('DOMContentLoaded', function() {
            const loadingOverlay = document.getElementById('loading-overlay');
            if (loadingOverlay) {
                loadingOverlay.classList.add('hidden');
            }
            
            // Reset any disabled submit buttons
            const submitButton = document.getElementById('submit-button');
            if (submitButton) {
                submitButton.disabled = false;
            }
        });
    """
    
    # Add zero-md script for markdown rendering
    zero_md_script = Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register")
    
    return Div(
        # Page header
        H1(f"{tool.name} Results",
           cls="text-3xl font-bold text-gray-800 mb-2 text-center"),
           
        P("Here are your generated results:",
          cls="text-xl text-gray-600 mb-8 text-center"),
        
        # Zero-md script for markdown rendering
        zero_md_script,
        
        # Results section
        Div(
            # Summary of request
            Div(
                *[P(f"{key.capitalize()}: {value}", cls="mb-2")
                  for key, value in metadata.items() if key != "count"],
                cls="mb-6 p-4 bg-gray-50 rounded"
            ),
            
            # Tabs for different views
            tab_buttons,
            
            # Different views
            list_view,
            card_view,
            markdown_view,
            copy_all_view,
            
            # Navigation buttons
            Div(
                A(f"Generate More",
                  href=tool.route,
                  cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"),
                A("Back to Tools",
                  href="/tools",
                  cls="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"),
                cls="flex justify-center mt-6"
            ),
            
            # Enhanced JavaScript
            Script(enhanced_script),
            
            cls="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md"
        )
    )