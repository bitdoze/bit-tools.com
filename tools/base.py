from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseTool(ABC):
    """
    Abstract base class for all AI tools.
    
    This provides a standard interface for tool implementation,
    making it easier to add new tools to the system.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the tool."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the tool does."""
        pass
    
    @property
    def id(self) -> str:
        """Return the tool ID used in URLs and for lookup."""
        return self.name.lower().replace(' ', '-')
    
    @property
    def route(self) -> str:
        """Return the URL route for the tool."""
        return f"/tools/{self.id}"
    
    @abstractmethod
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the inputs and return the results.
        
        Args:
            inputs: Dictionary of input parameters from the form
            
        Returns:
            Dictionary of results to be passed to the results page
        """
        pass
    
    @property
    @abstractmethod
    def input_form_fields(self) -> Dict[str, Dict[str, Any]]:
        """
        Return the configuration for the input form fields.
        
        Returns:
            Dictionary containing form field definitions
        """
        pass
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> List[str]:
        """
        Validate the inputs and return error messages.
        
        Args:
            inputs: Dictionary of input parameters from the form
            
        Returns:
            List of error messages, empty if validation passed
        """
        return []