from enum import Enum, auto
from typing import Dict, Any, Optional, Tuple

class ErrorCodes(Enum):
    """
    Error codes for the API
    
    Error code ranges:
    - 1000-1099: Authentication errors
    - 1100-1199: Database errors
    - 1200-1299: PDF-related errors
    - 1300-1399: External service errors
    - 1400-1499: Request errors
    - 9000-9999: Internal server errors
    
    Each error code has a numeric value and a string identifier.
    The string identifier is used in API responses for better readability.
    """
    # Authentication errors (1000-1099)
    INVALID_API_KEY = (1000, "INVALID_API_KEY")
    INVALID_CREDENTIALS = (1001, "INVALID_CREDENTIALS")
    TOKEN_EXPIRED = (1002, "TOKEN_EXPIRED")
    AUTH_ERROR = (1003, "AUTH_ERROR")
    INSUFFICIENT_PERMISSIONS = (1004, "INSUFFICIENT_PERMISSIONS")
    
    # Database errors (1100-1199)
    DATABASE_ERROR = (1100, "DATABASE_ERROR")
    RECORD_NOT_FOUND = (1101, "RECORD_NOT_FOUND")
    
    # PDF-related errors (1200-1299)
    ARTICLE_NOT_FOUND = (1200, "ARTICLE_NOT_FOUND")
    PDF_NOT_AVAILABLE = (1201, "PDF_NOT_AVAILABLE")
    PDF_DOWNLOAD_FAILED = (1202, "PDF_DOWNLOAD_FAILED")
    
    # Request errors (1400-1499)
    INVALID_REQUEST = (1400, "INVALID_REQUEST")
    MISSING_PARAMETER = (1401, "MISSING_PARAMETER")
    INVALID_PARAMETER = (1402, "INVALID_PARAMETER")
    
    # External service errors (1300-1399)
    PUBMED_SERVICE_ERROR = (1300, "PUBMED_SERVICE_ERROR")
    EXTERNAL_SERVICE_ERROR = (1301, "EXTERNAL_SERVICE_ERROR")
    
    # Internal server errors (9000-9999)
    INTERNAL_SERVER_ERROR = (9000, "INTERNAL_SERVER_ERROR")
    
    def __init__(self, code: int, identifier: str):
        self.code = code
        self.identifier = identifier
    
    @property
    def value(self) -> int:
        """Return the numeric error code"""
        return self.code
    
    @property
    def string_code(self) -> str:
        """Return the string identifier for the error code"""
        return self.identifier
    
    @classmethod
    def get_message(cls, error_code) -> str:
        """
        Get the default message for an error code
        
        Args:
            error_code (ErrorCodes): Error code enum
            
        Returns:
            str: Default error message
        """
        messages = {
            cls.INVALID_API_KEY: "Invalid or missing API key",
            cls.INVALID_CREDENTIALS: "Invalid username or password",
            cls.TOKEN_EXPIRED: "Authentication token has expired",
            cls.AUTH_ERROR: "Authentication error",
            cls.INSUFFICIENT_PERMISSIONS: "Insufficient permissions to access this resource",
            cls.DATABASE_ERROR: "Database error occurred",
            cls.RECORD_NOT_FOUND: "Record not found",
            cls.ARTICLE_NOT_FOUND: "Article not found",
            cls.PDF_NOT_AVAILABLE: "PDF not available for this article",
            cls.PDF_DOWNLOAD_FAILED: "Failed to download PDF",
            cls.INVALID_REQUEST: "Invalid request",
            cls.MISSING_PARAMETER: "Required parameter is missing",
            cls.INVALID_PARAMETER: "Parameter has invalid value",
            cls.PUBMED_SERVICE_ERROR: "Error communicating with PubMed service",
            cls.EXTERNAL_SERVICE_ERROR: "Error communicating with external service",
            cls.INTERNAL_SERVER_ERROR: "Internal server error"
        }
        
        return messages.get(error_code, "Unknown error")