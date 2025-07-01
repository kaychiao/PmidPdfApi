from flask import jsonify
from typing import Dict, Any, Optional, Union, List, Type
from pydantic import BaseModel
from http import HTTPStatus
from enum import Enum, auto

class ErrorCode(Enum):
    """
    Standardized error codes for API responses
    
    This enum centralizes all error codes used in the application,
    making them easier to manage and maintain.
    """
    # Authentication errors
    AUTH_ERROR = "AUTH_ERROR"
    INVALID_API_KEY = "INVALID_API_KEY"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    
    # Request errors
    INVALID_REQUEST = "INVALID_REQUEST"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    
    # Resource errors
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    
    # Server errors
    SERVER_ERROR = "SERVER_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    
    # PDF specific errors
    PDF_NOT_FOUND = "PDF_NOT_FOUND"
    DOWNLOAD_FAILED = "DOWNLOAD_FAILED"
    
    # Generic error
    GENERIC_ERROR = "ERROR"

class ApiResponse:
    """
    Unified API response handler
    
    This class provides a standardized way to create API responses
    with consistent structure and format.
    """
    
    @staticmethod
    def success(data: Union[Dict[str, Any], BaseModel, List, None] = None, 
                message: str = "Success", 
                status_code: int = HTTPStatus.OK) -> tuple:
        """
        Create a success response
        
        Args:
            data: Response data, can be a dict, Pydantic model, list or None
            message: Success message
            status_code: HTTP status code
            
        Returns:
            tuple: (jsonified response, status code)
        """
        if isinstance(data, BaseModel):
            data = data.dict()
        
        response = {
            "status": "success",
            "message": message,
            "data": data
        }
        
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str, 
              code: Union[str, ErrorCode] = ErrorCode.GENERIC_ERROR, 
              details: Optional[Dict[str, Any]] = None,
              status_code: int = HTTPStatus.BAD_REQUEST) -> tuple:
        """
        Create an error response
        
        Args:
            message: Error message
            code: Error code (string or ErrorCode enum)
            details: Additional error details
            status_code: HTTP status code
            
        Returns:
            tuple: (jsonified response, status code)
        """
        # Convert ErrorCode enum to string if needed
        if isinstance(code, ErrorCode):
            code = code.value
            
        response = {
            "status": "error",
            "code": code,
            "message": message,
            "details": details
        }
        
        return jsonify(response), status_code
    
    @staticmethod
    def warning(message: str,
                code: str = "WARNING",
                details: Optional[Dict[str, Any]] = None,
                status_code: int = HTTPStatus.OK) -> tuple:
        """
        Create a warning response
        
        Args:
            message: Warning message
            code: Warning code
            details: Additional warning details
            status_code: HTTP status code (usually 200 for warnings)
            
        Returns:
            tuple: (jsonified response, status code)
        """
        response = {
            "status": "warning",
            "code": code,
            "message": message,
            "details": details
        }
        
        return jsonify(response), status_code
    
    @classmethod
    def from_model(cls, 
                  model_instance: BaseModel, 
                  status_code: int = HTTPStatus.OK) -> tuple:
        """
        Create a response from a Pydantic model instance
        
        Args:
            model_instance: Pydantic model instance
            status_code: HTTP status code
            
        Returns:
            tuple: (jsonified response, status code)
        """
        return jsonify(model_instance.dict()), status_code
        
    @staticmethod
    def from_pydantic(model_class: Type[BaseModel], 
                     data: Dict[str, Any], 
                     status_code: int = HTTPStatus.OK) -> tuple:
        """
        Create a response using a Pydantic model class
        
        Args:
            model_class: Pydantic model class
            data: Data to be validated by the model
            status_code: HTTP status code
            
        Returns:
            tuple: (jsonified response, status code)
        """
        model_instance = model_class(**data)
        return jsonify(model_instance.dict()), status_code