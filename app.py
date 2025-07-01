from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from api.extensions import spec
from utils.api_logger import api_logger

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    spec.register(app)
    
    # Initialize API logger
    api_logger.init_app(app)
    
    # Register blueprints
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix=Config.API_PREFIX)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)