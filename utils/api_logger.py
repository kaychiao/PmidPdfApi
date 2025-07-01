import os
import json
import logging
import datetime
from logging.handlers import RotatingFileHandler
from flask import request, g, current_app
import time

class ApiLogger:
    """
    API Logger for tracking API requests and responses
    
    Logs are stored in a hierarchical structure:
    logs/YYYY-MM/DD/api_calls.log
    
    Log format follows the standard:
    [TIMESTAMP] [LOG_LEVEL] [APP_NAME] REQUEST_URL=... REQUEST_METHOD=... REQUEST_DATA={...} MESSAGE=...
    [TIMESTAMP] [LOG_LEVEL] [APP_NAME] MESSAGE=响应 Info: Path:..., Query:..., Json:... Runtime:...
    """
    
    def __init__(self, app=None, log_dir='logs', app_name='pmid-pdf-api'):
        self.log_dir = log_dir
        self.logger = None
        self.app_name = app_name
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        # Create logs directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Set up logger
        self.logger = logging.getLogger('api_logger')
        self.logger.setLevel(logging.INFO)
        
        # Configure log format - we'll handle formatting in our methods
        formatter = logging.Formatter('%(message)s')
        
        # Add handlers
        self._setup_handlers(formatter)
        
        # Register middleware
        app.before_request(self._before_request)
        app.after_request(self._after_request)
    
    def _setup_handlers(self, formatter):
        """Set up log handlers with the current date structure"""
        # Get current date
        now = datetime.datetime.now()
        year_month = now.strftime('%Y-%m')
        day = now.strftime('%d')
        
        # Create directory structure
        log_path = os.path.join(self.log_dir, year_month, day)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        
        # Create log file path
        log_file = os.path.join(log_path, 'api_calls.log')
        
        # Create rotating file handler (10MB per file, max 10 files)
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10
        )
        handler.setFormatter(formatter)
        
        # Remove old handlers if they exist
        for hdlr in self.logger.handlers[:]:
            self.logger.removeHandler(hdlr)
        
        # Add new handler
        self.logger.addHandler(handler)
    
    def _before_request(self):
        """Log request information before processing"""
        # Skip logging for static files
        if request.path.startswith('/static'):
            return
        
        # Store start time for duration calculation
        g.start_time = time.time()
        
        # Capture request data
        try:
            # Format request body
            request_data = {}
            
            # Add query parameters
            if request.args:
                request_data['parameters'] = json.dumps(dict(request.args))
            else:
                request_data['parameters'] = '{}'
                
            # Add request body for POST/PUT/PATCH requests
            if request.method in ['POST', 'PUT', 'PATCH'] and request.is_json:
                request_data['body'] = json.dumps(request.get_json())
            else:
                request_data['body'] = '{}'
            
            # Get client IP address
            client_ip = request.remote_addr
            
            # Format log entry according to the specified format
            timestamp = datetime.datetime.now().isoformat()
            log_message = f"[{timestamp}] [INFO] [{self.app_name}] REQUEST_URL={request.path} REQUEST_METHOD={request.method} REQUEST_DATA={request_data} IP={client_ip} MESSAGE=PMID PDF API"
            
            # Log the formatted message
            self.logger.info(log_message)
        except Exception as e:
            self.logger.error(f"[{datetime.datetime.now().isoformat()}] [ERROR] [{self.app_name}] Error logging request: {str(e)}")
    
    def _after_request(self, response):
        """Log response information after processing"""
        # Skip logging for static files
        if request.path.startswith('/static'):
            return response
        
        # Ensure handlers are up to date with current date
        self._setup_handlers(self.logger.handlers[0].formatter if self.logger.handlers else logging.Formatter('%(message)s'))
        
        # Calculate request duration
        duration = time.time() - getattr(g, 'start_time', time.time())
        
        # Capture response data
        try:
            # Get query parameters
            query_params = dict(request.args)
            
            # Get response body for JSON responses
            response_body = '{}'
            if response.content_type and 'application/json' in response.content_type:
                try:
                    # Get response data without consuming the response
                    response_data = response.get_data().decode('utf-8')
                    response_body = response_data
                except (ValueError, UnicodeDecodeError):
                    response_body = '<non-JSON or binary data>'
            
            # Get client IP address
            client_ip = request.remote_addr
            
            # Format log entry according to the specified format
            timestamp = datetime.datetime.now().isoformat()
            log_message = f"[{timestamp}] [INFO] [{self.app_name}] MESSAGE=Response Info: IP: {client_ip}, Path: {request.path}, Query: {json.dumps(query_params)}, Json: {response_body} Runtime: {duration:.3f}"
            
            # Log the formatted message
            self.logger.info(log_message)
        except Exception as e:
            self.logger.error(f"[{datetime.datetime.now().isoformat()}] [ERROR] [{self.app_name}] Error logging response: {str(e)}")
        
        return response
    
    def log_error(self, error, path=None):
        """Log an error that occurred during request processing"""
        timestamp = datetime.datetime.now().isoformat()
        path = path or getattr(request, 'path', 'unknown')
        
        log_message = f"[{timestamp}] [ERROR] [{self.app_name}] MESSAGE=Error occurred on path: {path}, Error: {str(error)}"
        self.logger.error(log_message)

# Create singleton instance
api_logger = ApiLogger()
