from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from api.response_handler import ApiResponse, ErrorCode
from config import Config

# Get API keys from configuration
API_KEYS = Config.API_KEYS

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key in API_KEYS:
            return f(*args, **kwargs)
        return ApiResponse.error(
            message="Invalid or missing API key",
            code=ErrorCode.INVALID_API_KEY,
            status_code=401
        )
    return decorated_function

def authenticate_user(username, password):
    # This is a placeholder for actual user authentication
    # In a real application, you would check the credentials against a database
    if username == "admin" and password == "password":
        return {"id": 1, "username": username}
    return None

def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = authenticate_user(username, password)
    if not user:
        return ApiResponse.error(
            message="Invalid username or password",
            code=ErrorCode.INVALID_CREDENTIALS,
            status_code=401
        )
    
    access_token = create_access_token(identity=user["id"])
    return ApiResponse.success(
        data={"access_token": access_token},
        message="Login successful"
    )

def get_current_user():
    return get_jwt_identity()