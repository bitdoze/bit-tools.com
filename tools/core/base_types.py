from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from .base import BaseTool

class TextGenerationTool(BaseTool, ABC):
    """Base class for text generation tools."""
    
    @property
    def tool_type(self) -> str:
        return "text_generation"
    
    @property
    def default_system_prompt(self) -> str:
        """Default system prompt for this tool type."""
        return """
        You are a versatile text generation assistant. Create high-quality, 
        engaging content based on the user's requirements.
        """
    
    def get_system_prompt(self) -> str:
        """Get the system prompt, allowing for customization."""
        return self.default_system_prompt
    
    @abstractmethod
    async def generate_text(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate text based on inputs and return a dictionary with results."""
        pass
    
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and generate text."""
        try:
            # Validate inputs
            validation_errors = self.validate_inputs(inputs)
            if validation_errors:
                return {"error": "Validation failed", "validation_errors": validation_errors}
            
            # Generate text and get results
            results = await self.generate_text(inputs)
            
            # If there's an error in the results, return it directly
            if "error" in results:
                return results
            
            # Make sure metadata is included
            if "metadata" not in results:
                results["metadata"] = {
                    **{k: v for k, v in inputs.items() if k in self.input_form_fields}
                }
                
            # Make sure titles is included for backward compatibility
            if "titles" not in results and "error" not in results:
                # Try to find some content to use as titles
                if "content" in results:
                    results["titles"] = [results["content"]]
                else:
                    # Look for any list in the results to use
                    for key, value in results.items():
                        if isinstance(value, list) and value and key != "metadata":
                            results["titles"] = value
                            break
                    
                    # If still no titles, use a default
                    if "titles" not in results:
                        results["titles"] = ["Content generated successfully"]
            
            # Add count to metadata if not present
            if "metadata" in results and "count" not in results["metadata"]:
                if "titles" in results and isinstance(results["titles"], list):
                    results["metadata"]["count"] = len(results["titles"])
            
            return results
            
        except Exception as e:
            return {"error": f"Failed to generate text: {str(e)}"}

class TextTransformationTool(BaseTool, ABC):
    """Base class for text transformation tools."""
    
    @property
    def tool_type(self) -> str:
        return "text_transformation"
    
    @abstractmethod
    async def transform_text(self, text: str, options: Dict[str, Any]) -> str:
        """Transform the input text based on options."""
        pass
    
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and transform text."""
        try:
            # Validate inputs
            validation_errors = self.validate_inputs(inputs)
            if validation_errors:
                return {"error": "Validation failed", "validation_errors": validation_errors}
            
            # Get input text
            text = inputs.get("text", "").strip()
            if not text:
                return {"error": "Please provide text to transform."}
            
            # Transform text
            transformed_text = await self.transform_text(
                text, 
                {k: v for k, v in inputs.items() if k != "text"}
            )
            
            # Return results
            return {
                "metadata": {
                    **{k: v for k, v in inputs.items() if k in self.input_form_fields},
                },
                "original_text": text,
                "transformed_text": transformed_text
            }
        except Exception as e:
            return {"error": f"Failed to transform text: {str(e)}"}
