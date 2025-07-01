from config.app_config import config as app_config

# Export configuration
Config = app_config

# For backward compatibility, keep the following attributes
if __name__ == "__main__":
    print(f"Current environment: {Config.__class__.__name__}")
    print(f"Database URI: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"API Title: {Config.API_TITLE}")
    print(f"Debug mode: {Config.DEBUG}")