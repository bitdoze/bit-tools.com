from fasthtml.common import *
from fasthtml.components import NotStr
from tools import get_tool_by_id
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

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
    logger.info(f"Rendering results page for tool: {tool_id}")
    logger.info(f"Results type: {type(results)}")

    # Try to log the results for debugging
    try:
        logger.info(f"Results sample: {str(results)[:200]}...")
    except:
        logger.info("Could not log results sample")

    # Get the tool
    tool = get_tool_by_id(tool_id)
    if not tool:
        return error_page("Tool Not Found", "Sorry, the requested tool could not be found.")

    # Handle error cases
    if isinstance(results, dict) and "error" in results:
        return error_page("Error", results["error"], f"/tools/{tool_id}")

    # Try to convert string results to dict if needed
    if isinstance(results, str):
        try:
            results = json.loads(results)
        except:
            # If conversion fails, wrap the string in a dict with titles key
            results = {"titles": [results]}

    # Ensure results is a dictionary
    if not isinstance(results, dict):
        results = {"titles": [str(results)]}

    # Get metadata and titles/content
    metadata = results.get("metadata", {})

    # Get titles - handle both list and string formats
    titles = results.get("titles", [])
    if isinstance(titles, str):
        titles = titles.split('\n')

    # Filter out empty titles
    titles = [title for title in titles if title.strip()]

    # Handle text transformation tools
    original_text = results.get("original_text", "")
    transformed_text = results.get("transformed_text", "")

    # Determine if this is a transformation tool
    is_transformation = original_text and transformed_text

    # Determine if this is an outline tool by checking the tool ID
    is_outline_tool = "outline" in tool_id.lower()

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
                    Div(
                        Button(
                            "Copy Transformed Text",
                            type="button",
                            id="copy-transformed-btn",
                            cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
                        ),
                        P("", id="copy-status", cls="text-green-600 inline-block"),
                        cls="flex items-center"
                    ),
                    cls="mb-6"
                ),

                # Navigation buttons
                Div(
                    A(f"Transform More Text",
                      href=f"/tools/{tool_id}",
                      cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"),
                    A("Back to Tools",
                      href="/tools",
                      cls="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"),
                    cls="flex justify-center mt-6"
                ),

                # JavaScript for copy functionality
                Script(f"""
                    document.addEventListener('DOMContentLoaded', function() {{
                        const copyBtn = document.getElementById('copy-transformed-btn');
                        const statusEl = document.getElementById('copy-status');

                        copyBtn.addEventListener('click', function() {{
                            const text = {json.dumps(transformed_text)};

                            navigator.clipboard.writeText(text)
                                .then(() => {{
                                    statusEl.textContent = 'Copied!';
                                    setTimeout(() => {{
                                        statusEl.textContent = '';
                                    }}, 2000);
                                }})
                                .catch(err => {{
                                    statusEl.textContent = 'Failed to copy';
                                    console.error('Failed to copy text: ', err);
                                }});
                        }});

                        // Hide any loading overlays
                        const loadingOverlay = document.getElementById('loading-overlay');
                        if (loadingOverlay) {{
                            loadingOverlay.classList.add('hidden');
                        }}
                    }});
                """),

                cls="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md"
            )
        )

    # Create views based on tool type and content
    views = {}

    # List view (default)
    if is_outline_tool:
        # For outline tools, preserve the hierarchy and indentation
        list_items = []

        # Try to parse the outline structure
        try:
            current_section = None
            section_items = []

            for line in titles:
                line = line.strip()
                if not line:
                    continue

                # Check if this is a main section (heading-like)
                if (line.startswith('#') or
                    line[0].isupper() or
                    any(line.startswith(prefix) for prefix in ["Introduction", "Conclusion", "I.", "II.", "III."])):

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
        except Exception as e:
            logger.error(f"Error parsing outline structure: {str(e)}")
            list_items = []

        # If parsing failed or produced no results, fall back to treating each line as separate
        if not list_items:
            list_items = [
                Div(
                    P(title, cls="mb-1"),
                    cls="p-4 bg-white rounded shadow-md mb-3"
                )
                for title in titles
            ]

        views["list"] = Div(
            *list_items,
            id="list-view",
            cls="mb-6"
        )

        # Card view - show the entire outline in one card
        views["card"] = Div(
            Div(
                H3("Complete Outline", cls="text-xl font-bold mb-4 text-center"),
                *[P(title, cls="mb-2") for title in titles],
                cls="p-6 bg-white rounded shadow-lg"
            ),
            id="card-view",
            cls="mb-6 hidden"
        )

        # Markdown view for outline tools
        markdown_lines = []
        try:
            current_section = None
            section_items = []

            for line in titles:
                line = line.strip()
                if not line:
                    continue

                # Similar logic to list view parsing
                if (line.startswith('#') or
                    line[0].isupper() or
                    any(line.startswith(prefix) for prefix in ["Introduction", "Conclusion", "I.", "II.", "III."])):

                    # Add previous section to markdown
                    if current_section:
                        markdown_lines.append(f"## {current_section}")
                        for item in section_items:
                            markdown_lines.append(f"- {item}")
                        markdown_lines.append("")  # Empty line for spacing

                    # Start new section
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
        except Exception as e:
            logger.error(f"Error generating markdown: {str(e)}")
            markdown_lines = []

        # If parsing failed, fall back to basic markdown list
        if not markdown_lines:
            markdown_lines = [f"- {title}" for title in titles]

        markdown_text = "\n".join(markdown_lines)

        views["markdown"] = Div(
            H3("Markdown Format", cls="text-xl font-bold mb-4 text-center"),
            Div(
                Textarea(
                    markdown_text,
                    id="markdown-content",
                    rows=15,
                    readonly=True,
                    cls="w-full p-3 border rounded font-mono"
                ),
                Div(
                    Button(
                        "Copy Markdown",
                        type="button",
                        id="copy-markdown-btn",
                        cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
                    ),
                    P("", id="markdown-copy-status", cls="text-green-600 inline-block"),
                    cls="mt-2 flex items-center"
                ),
                cls="mb-4"
            ),
            Div(
                H4("Preview:", cls="text-lg font-bold mb-2"),
                Div(
                    # Use zero-md for proper markdown rendering
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
        # Standard list view for non-outline tools
        views["list"] = Div(
            *[
                Div(
                    P(f"{i+1}. {title}", cls="mb-1 flex-grow", id=f"title-text-{i}"),
                    Button(
                        "Copy",
                        type="button",
                        id=f"copy-btn-{i}",
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
        views["card"] = Div(
            Div(
                *[
                    Div(
                        P(title, cls="text-center mb-2", id=f"card-text-{i}"),
                        Button(
                            "Copy",
                            type="button",
                            id=f"card-copy-btn-{i}",
                            cls="w-full text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
                        ),
                        cls="p-4 bg-white rounded shadow-sm hover:shadow-md transition-shadow"
                    )
                    for i, title in enumerate(titles)
                ],
                cls="grid grid-cols-1 md:grid-cols-2 gap-4"
            ),
            id="card-view",
            cls="mb-6 hidden"
        )

    # All tools have a copy-all view
    views["copy"] = Div(
        Textarea(
            "\n".join(titles),
            id="copy-all-content",
            rows=10,
            readonly=True,
            cls="w-full p-3 border rounded"
        ),
        Div(
            Button(
                "Copy All",
                type="button",
                id="copy-all-btn",
                cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
            ),
            P("", id="copy-all-status", cls="text-green-600 inline-block"),
            cls="mt-2 flex items-center"
        ),
        id="copy-view",
        cls="mb-6 hidden"
    )

    # Define available tabs based on views
    tabs = [
        {"id": "list", "label": "List View", "selected": True},
        {"id": "card", "label": "Card View", "selected": False},
    ]

    # Add markdown tab only for outline tools
    if is_outline_tool:
        tabs.append({"id": "markdown", "label": "Markdown", "selected": False})

    # All tools have copy-all tab
    tabs.append({"id": "copy", "label": "Copy All", "selected": False})

    # Create tab buttons
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

    # Prepare individual title copying JavaScript
    copy_title_js = ""
    for i, title in enumerate(titles):
        # Escape any quotes in the title
        safe_title = title.replace("'", "\\'").replace('"', '\\"')
        copy_title_js += f"""
        document.getElementById('copy-btn-{i}')?.addEventListener('click', function() {{
            navigator.clipboard.writeText("{safe_title}");
            this.textContent = 'Copied!';
            setTimeout(() => {{
                this.textContent = 'Copy';
            }}, 2000);
        }});

        document.getElementById('card-copy-btn-{i}')?.addEventListener('click', function() {{
            navigator.clipboard.writeText("{safe_title}");
            this.textContent = 'Copied!';
            setTimeout(() => {{
                this.textContent = 'Copy';
            }}, 2000);
        }});
        """

    # Enhanced JavaScript for tab switching and copy functionality
    enhanced_script = f"""
        document.addEventListener('DOMContentLoaded', function() {{
            // Tab switching function
            window.switchTab = function(tabId) {{
                // Hide all views
                document.getElementById('list-view').classList.add('hidden');
                document.getElementById('card-view').classList.add('hidden');
                document.getElementById('copy-view').classList.add('hidden');

                // Hide markdown view if it exists
                const markdownView = document.getElementById('markdown-view');
                if (markdownView) {{
                    markdownView.classList.add('hidden');
                }}

                // Show selected view
                document.getElementById(tabId + '-view').classList.remove('hidden');

                // Update tab buttons
                const tabs = document.querySelectorAll('[id^="tab-"]');
                tabs.forEach(tab => {{
                    tab.classList.remove('bg-white', 'text-blue-600', 'font-bold');
                    tab.classList.add('bg-gray-200', 'text-gray-700');
                }});

                document.getElementById('tab-' + tabId).classList.remove('bg-gray-200', 'text-gray-700');
                document.getElementById('tab-' + tabId).classList.add('bg-white', 'text-blue-600', 'font-bold');
            }};

            // Copy-all button
            const copyAllBtn = document.getElementById('copy-all-btn');
            const copyAllStatus = document.getElementById('copy-all-status');
            const copyAllContent = document.getElementById('copy-all-content');

            if (copyAllBtn && copyAllContent) {{
                copyAllBtn.addEventListener('click', function() {{
                    navigator.clipboard.writeText(copyAllContent.value)
                        .then(() => {{
                            copyAllStatus.textContent = 'Copied!';
                            setTimeout(() => {{
                                copyAllStatus.textContent = '';
                            }}, 2000);
                        }})
                        .catch(err => {{
                            copyAllStatus.textContent = 'Failed to copy';
                            console.error('Failed to copy text: ', err);
                        }});
                }});
            }}

            // Markdown copy button
            const copyMarkdownBtn = document.getElementById('copy-markdown-btn');
            const markdownStatus = document.getElementById('markdown-copy-status');
            const markdownContent = document.getElementById('markdown-content');

            if (copyMarkdownBtn && markdownContent) {{
                copyMarkdownBtn.addEventListener('click', function() {{
                    navigator.clipboard.writeText(markdownContent.value)
                        .then(() => {{
                            markdownStatus.textContent = 'Copied!';
                            setTimeout(() => {{
                                markdownStatus.textContent = '';
                            }}, 2000);
                        }})
                        .catch(err => {{
                            markdownStatus.textContent = 'Failed to copy';
                            console.error('Failed to copy text: ', err);
                        }});
                }});
            }}

            // Individual title copy buttons
            {copy_title_js}

            // Hide any loading overlays
            const loadingOverlay = document.getElementById('loading-overlay');
            if (loadingOverlay) {{
                loadingOverlay.classList.add('hidden');
            }}

            // Reset any disabled submit buttons
            const submitButton = document.getElementById('submit-button');
            if (submitButton) {{
                submitButton.disabled = false;
            }}
        }});
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
            ) if metadata else Div(cls="mb-4"),

            # Tabs for different views
            tab_buttons,

            # Different views
            *[view for view in views.values()],

            # Navigation buttons
            Div(
                A(f"Generate More",
                  href=f"/tools/{tool_id}",
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
