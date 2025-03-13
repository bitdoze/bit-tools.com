from fasthtml.common import *
from .base_results import BaseResultsHandler
from .components import create_tab_navigation, create_tab_switching_script, create_copy_button

class YoutubeScriptResultsHandler(BaseResultsHandler):
    """Handler for YouTube script tool results."""
    
    def create_script_view(self):
        """Create the script view."""
        # Extract the script from the titles
        script_text = ""
        script_started = False
        
        for line in self.titles:
            if line.strip() == "SCRIPT:":
                script_started = True
                continue
            elif line.strip() in ["HOOKS:", "INPUT BIAS:", "OPEN LOOP QUESTIONS:"]:
                script_started = False
            
            if script_started and line.strip():
                script_text += line + "\n"
        
        return Div(
            H3("Your YouTube Script", cls="text-xl font-bold mb-4 text-center"),
            Div(
                P(script_text, cls="whitespace-pre-wrap"),
                cls="p-4 bg-white rounded shadow-md mb-6 overflow-auto max-h-80"
            ),
            create_copy_button("script-content", "copy-script-btn", "script-copy-status"),
            Textarea(
                script_text,
                id="script-content",
                cls="hidden"
            ),
            id="script-view",
            cls="mb-6"
        )
    
    def create_hooks_view(self):
        """Create the hooks view."""
        # Extract hooks from the titles
        hooks = []
        hooks_started = False
        
        for line in self.titles:
            if line.strip() == "HOOKS:":
                hooks_started = True
                continue
            elif line.strip() in ["SCRIPT:", "INPUT BIAS:", "OPEN LOOP QUESTIONS:"]:
                hooks_started = False
            
            if hooks_started and line.strip():
                hooks.append(line)
        
        hook_items = []
        for i, hook in enumerate(hooks):
            # Remove numbering if present
            hook_text = re.sub(r'^\d+\.\s*', '', hook)
            
            hook_items.append(
                Div(
                    P(hook_text, cls="mb-2"),
                    Button(
                        "Copy",
                        type="button",
                        id=f"hook-copy-btn-{i}",
                        cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
                    ),
                    cls="p-4 bg-white rounded shadow-sm mb-3 hover:shadow-md transition-shadow"
                )
            )
        
        return Div(
            H3("Hooks for Your Video", cls="text-xl font-bold mb-4 text-center"),
            P("Use these hooks to grab your viewers' attention:", cls="mb-4 text-center text-gray-600"),
            *hook_items,
            id="hooks-view",
            cls="mb-6 hidden"
        )
    
    def create_bias_view(self):
        """Create the input bias view."""
        # Extract input bias from the titles
        bias_statements = []
        bias_started = False
        
        for line in self.titles:
            if line.strip() == "INPUT BIAS:":
                bias_started = True
                continue
            elif line.strip() in ["SCRIPT:", "HOOKS:", "OPEN LOOP QUESTIONS:"]:
                bias_started = False
            
            if bias_started and line.strip():
                bias_statements.append(line)
        
        bias_items = []
        for i, bias in enumerate(bias_statements):
            # Remove numbering if present
            bias_text = re.sub(r'^\d+\.\s*', '', bias)
            
            bias_items.append(
                Div(
                    P(bias_text, cls="mb-2"),
                    Button(
                        "Copy",
                        type="button",
                        id=f"bias-copy-btn-{i}",
                        cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
                    ),
                    cls="p-4 bg-white rounded shadow-sm mb-3 hover:shadow-md transition-shadow"
                )
            )
        
        return Div(
            H3("Input Bias Statements", cls="text-xl font-bold mb-4 text-center"),
            P("Use these statements to establish credibility:", cls="mb-4 text-center text-gray-600"),
            *bias_items,
            id="bias-view",
            cls="mb-6 hidden"
        )
    
    def create_questions_view(self):
        """Create the open loop questions view."""
        # Extract questions from the titles
        questions = []
        questions_started = False
        
        for line in self.titles:
            if line.strip() == "OPEN LOOP QUESTIONS:":
                questions_started = True
                continue
            elif line.strip() in ["SCRIPT:", "HOOKS:", "INPUT BIAS:"]:
                questions_started = False
            
            if questions_started and line.strip():
                questions.append(line)
        
        question_items = []
        for i, question in enumerate(questions):
            # Remove numbering if present
            question_text = re.sub(r'^\d+\.\s*', '', question)
            
            question_items.append(
                Div(
                    P(question_text, cls="mb-2"),
                    Button(
                        "Copy",
                        type="button",
                        id=f"question-copy-btn-{i}",
                        cls="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 py-1 px-2 rounded"
                    ),
                    cls="p-4 bg-white rounded shadow-sm mb-3 hover:shadow-md transition-shadow"
                )
            )
        
        return Div(
            H3("Open Loop Questions", cls="text-xl font-bold mb-4 text-center"),
            P("Use these questions to create curiosity:", cls="mb-4 text-center text-gray-600"),
            *question_items,
            id="questions-view",
            cls="mb-6 hidden"
        )
    
    def create_copy_all_view(self):
        """Create the copy-all view."""
        return Div(
            H3("Complete Output", cls="text-xl font-bold mb-4 text-center"),
            Textarea(
                "\n".join(self.titles),
                id="copy-all-content",
                rows=15,
                readonly=True,
                cls="w-full p-3 border rounded font-mono"
            ),
            create_copy_button("copy-all-content", "copy-all-btn", "copy-all-status"),
            id="copy-view",
            cls="mb-6 hidden"
        )
    
    def create_views(self):
        """Create all views for the YouTube script results."""
        views = {
            "script": self.create_script_view(),
            "hooks": self.create_hooks_view(),
            "bias": self.create_bias_view(),
            "questions": self.create_questions_view(),
            "copy": self.create_copy_all_view()
        }
        
        return Div(*views.values())
    
    def create_tabs(self):
        """Create tabs for the YouTube script results."""
        tabs = [
            {"id": "script", "label": "Script", "selected": True},
            {"id": "hooks", "label": "Hooks", "selected": False},
            {"id": "bias", "label": "Input Bias", "selected": False},
            {"id": "questions", "label": "Questions", "selected": False},
            {"id": "copy", "label": "Copy All", "selected": False}
        ]
        
        return create_tab_navigation(tabs)
    
    def create_scripts(self):
        """Create scripts for the YouTube script results."""
        return Script("""
            document.addEventListener('DOMContentLoaded', function() {
                // Tab switching functionality
                window.switchTab = function(tabId) {
                    // Hide all views
                    const views = document.querySelectorAll('[id$="-view"]');
                    views.forEach(view => {
                        view.classList.add('hidden');
                    });
                    
                    // Show selected view
                    const selectedView = document.getElementById(tabId + '-view');
                    if (selectedView) {
                        selectedView.classList.remove('hidden');
                    }
                    
                    // Update tab buttons
                    const tabs = document.querySelectorAll('[id^="tab-"]');
                    tabs.forEach(tab => {
                        tab.classList.remove('bg-white', 'text-blue-600', 'font-bold');
                        tab.classList.add('bg-gray-200', 'text-gray-700');
                    });
                    
                    const selectedTab = document.getElementById('tab-' + tabId);
                    if (selectedTab) {
                        selectedTab.classList.remove('bg-gray-200', 'text-gray-700');
                        selectedTab.classList.add('bg-white', 'text-blue-600', 'font-bold');
                    }
                };

                // Setup copy buttons for script
                const copyScriptBtn = document.getElementById('copy-script-btn');
                const scriptCopyStatus = document.getElementById('script-copy-status');
                const scriptContent = document.getElementById('script-content');
                
                if (copyScriptBtn && scriptContent) {
                    copyScriptBtn.addEventListener('click', function() {
                        navigator.clipboard.writeText(scriptContent.value)
                            .then(() => {
                                scriptCopyStatus.textContent = 'Copied!';
                                setTimeout(() => {
                                    scriptCopyStatus.textContent = '';
                                }, 2000);
                            })
                            .catch(err => {
                                scriptCopyStatus.textContent = 'Failed to copy';
                                console.error('Failed to copy text: ', err);
                            });
                    });
                }
                
                // Setup copy buttons for hooks
                document.querySelectorAll('[id^="hook-copy-btn-"]').forEach(button => {
                    button.addEventListener('click', function() {
                        const text = button.previousElementSibling.textContent;
                        
                        navigator.clipboard.writeText(text)
                            .then(() => {
                                button.textContent = 'Copied!';
                                setTimeout(() => {
                                    button.textContent = 'Copy';
                                }, 2000);
                            })
                            .catch(err => {
                                console.error('Failed to copy text: ', err);
                            });
                    });
                });
                
                // Setup copy buttons for bias statements
                document.querySelectorAll('[id^="bias-copy-btn-"]').forEach(button => {
                    button.addEventListener('click', function() {
                        const text = button.previousElementSibling.textContent;
                        
                        navigator.clipboard.writeText(text)
                            .then(() => {
                                button.textContent = 'Copied!';
                                setTimeout(() => {
                                    button.textContent = 'Copy';
                                }, 2000);
                            })
                            .catch(err => {
                                console.error('Failed to copy text: ', err);
                            });
                    });
                });
                
                // Setup copy buttons for questions
                document.querySelectorAll('[id^="question-copy-btn-"]').forEach(button => {
                    button.addEventListener('click', function() {
                        const text = button.previousElementSibling.textContent;
                        
                        navigator.clipboard.writeText(text)
                            .then(() => {
                                button.textContent = 'Copied!';
                                setTimeout(() => {
                                    button.textContent = 'Copy';
                                }, 2000);
                            })
                            .catch(err => {
                                console.error('Failed to copy text: ', err);
                            });
                    });
                });
                
                // Setup copy-all button
                const copyAllBtn = document.getElementById('copy-all-btn');
                const copyAllStatus = document.getElementById('copy-all-status');
                const copyAllContent = document.getElementById('copy-all-content');
                
                if (copyAllBtn && copyAllContent) {
                    copyAllBtn.addEventListener('click', function() {
                        navigator.clipboard.writeText(copyAllContent.value)
                            .then(() => {
                                copyAllStatus.textContent = 'Copied!';
                                setTimeout(() => {
                                    copyAllStatus.textContent = '';
                                }, 2000);
                            })
                            .catch(err => {
                                copyAllStatus.textContent = 'Failed to copy';
                                console.error('Failed to copy text: ', err);
                            });
                    });
                }
            });
        """)
    
    def render(self):
        """Render the YouTube script results page."""
        return Div(
            # Page header
            H1(f"{self.tool.name} Results",
               cls="text-3xl font-bold text-gray-800 mb-2 text-center"),

            P("Here is your generated YouTube script content:",
              cls="text-xl text-gray-600 mb-8 text-center"),

            # Results section
            Div(
                # Summary of request
                self.create_metadata_section(),

                # Tabs for different views
                self.create_tabs(),

                # Different views
                self.create_views(),

                # Navigation buttons
                self.create_navigation_buttons(),

                # Scripts
                self.create_scripts(),
                
                # Base scripts
                self.get_page_scripts(),

                cls="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md"
            )
        )
