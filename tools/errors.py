from enum import Enum
from typing import Dict, Any, Optional

class ErrorCode(Enum):
    """Error codes for tool-related errors."""
    INVALID_INPUT = "invalid_input"
    API_ERROR = "api_error"
    RATE_LIMIT = "rate_limit"
    INTERNAL_ERROR = "internal_error"

class ToolError(Exception):
    """Base exception for tool-related errors."""
    
    def __init__(
        self, 
        code: ErrorCode, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a dictionary for API responses."""
        return {
            "error": {
                "code": self.code.value,
                "message": self.message,
                "details": self.details
            }
        }