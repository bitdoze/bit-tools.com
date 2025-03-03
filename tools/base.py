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
    def icon(self) -> str:
        # Default icon if not overridden
        return """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 9.563C9 9.252 9.252 9 9.563 9h4.874c.311 0 .563.252.563.563v4.874c0 .311-.252.563-.563.563H9.564A.562.562 0 0 1 9 14.437V9.564Z" />
        </svg>"""
    
    @property
    def id(self) -> str:
        """Return the tool ID used in URLs and for lookup."""
        return self.name.lower().replace(' ', '-')
    
    @property
    def route(self) -> str:
        """Return the URL route for the tool."""
        return f"/tools/{self.id}"
    
    @abstractmethod
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
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
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate the inputs and return detailed error information.
        
        Args:
            inputs: Dictionary of input parameters from the form
            
        Returns:
            List of error dictionaries with field, code, and message
        """
        errors = []
        
        for field_id, field_config in self.input_form_fields.items():
            # Check required fields
            if field_config.get("required", False) and not inputs.get(field_id):
                errors.append({
                    "field": field_id,
                    "code": "required",
                    "message": f"{field_config.get('label', field_id)} is required"
                })
            
            # Check field-specific validation
            if field_id in inputs and inputs[field_id]:
                # Example: max length validation
                max_length = field_config.get("maxLength")
                if max_length and len(str(inputs[field_id])) > max_length:
                    errors.append({
                        "field": field_id,
                        "code": "max_length",
                        "message": f"{field_config.get('label', field_id)} exceeds maximum length of {max_length}"
                    })
                
                # Example: min length validation
                min_length = field_config.get("minLength")
                if min_length and len(str(inputs[field_id])) < min_length:
                    errors.append({
                        "field": field_id,
                        "code": "min_length",
                        "message": f"{field_config.get('label', field_id)} must be at least {min_length} characters"
                    })
        
        return errors