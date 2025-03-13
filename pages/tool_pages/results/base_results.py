from fasthtml.common import *
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

class BaseResultsHandler:
    """Base class for handling tool results."""
    
    def __init__(self, tool_id, tool, results):
        """
        Initialize the results handler.
        
        Args:
            tool_id: The ID of the tool
            tool: The tool instance
            results: The results from the tool processing
        """
        self.tool_id = tool_id
        self.tool = tool
        self.results = results
        self.metadata = results.get("metadata", {})
        
        # Process titles if present
        self.titles = results.get("titles", [])
        if isinstance(self.titles, str):
            self.titles = self.titles.split('\n')
        
        # Filter out empty titles
        self.titles = [title for title in self.titles if title.strip()]
    
    def create_metadata_section(self):
        """Create the metadata section of the results page."""
        if not self.metadata:
            return Div(cls="mb-4")
            
        return Div(
            *[P(f"{key.capitalize()}: {value}", cls="mb-2")
              for key, value in self.metadata.items() if key != "count"],
            cls="mb-6 p-4 bg-gray-50 rounded"
        )
    
    def create_navigation_buttons(self):
        """Create navigation buttons for the results page."""
        return Div(
            A(f"Generate More",
              href=f"/tools/{self.tool_id}",
              cls="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"),
            A("Back to Tools",
              href="/tools",
              cls="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded"),
            cls="flex justify-center mt-6"
        )
    
    def get_page_scripts(self):
        """Get the JavaScript for the results page."""
        return Script("""
            document.addEventListener('DOMContentLoaded', function() {
                // Hide any loading overlays
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
            
            // Add event listener for browser navigation events (back/forward buttons)
            window.addEventListener('popstate', function() {
                // Hide any loading overlays when navigating with browser controls
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
            
            // Force hide loading overlay on page load and back button
            // This ensures the loading overlay is hidden even if the popstate event doesn't fire properly
            document.addEventListener('visibilitychange', function() {
                if (!document.hidden) {
                    // Page is now visible (e.g., after returning from another tab or using back button)
                    const loadingOverlay = document.getElementById('loading-overlay');
                    if (loadingOverlay) {
                        loadingOverlay.classList.add('hidden');
                    }

                    // Reset any disabled submit buttons
                    const submitButton = document.getElementById('submit-button');
                    if (submitButton) {
                        submitButton.disabled = false;
                    }
                }
            });
        """)
    
    def render(self):
        """
        Render the results page.
        
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement render()")
