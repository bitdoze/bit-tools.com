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
    async def generate_text(self, inputs: Dict[str, Any]) -> List[str]:
        """Generate text based on inputs."""
        pass
    
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and generate text."""
        try:
            # Validate inputs
            validation_errors = self.validate_inputs(inputs)
            if validation_errors:
                return {"error": "Validation failed", "validation_errors": validation_errors}
            
            # Generate text
            generated_texts = await self.generate_text(inputs)
            
            # Return results
            return {
                "metadata": {
                    **{k: v for k, v in inputs.items() if k in self.input_form_fields},
                    "count": len(generated_texts)
                },
                "titles": generated_texts  # Using 'titles' for backward compatibility
            }
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