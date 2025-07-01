import os
from enum import Enum

from config.user_config import *
from config.secrets import *


class EnumEnvironmentApp(str, Enum):
    production = 'production'
    development = 'development'
    local = 'local'

    @classmethod
    def cur_mode(cls):
        return cls.development if os.getenv('FM_ENV_CONFIG') is None else os.getenv('FM_ENV_CONFIG')

    @classmethod
    def is_prod(cls):
        return cls.cur_mode() == cls.production

    @classmethod
    def is_dev(cls):
        return cls.cur_mode() == cls.development

    @classmethod
    def is_local(cls):
        return cls.cur_mode() == cls.local

    @classmethod
    def get_port(cls):
        if cls.is_prod():
            port = '8000'
        elif cls.is_dev():
            port = '8001'
        elif cls.is_local():
            port = '8002'
        return port

    @classmethod
    def _get_host(cls):
        if cls.is_local():
            host = 'localhost'
        elif cls.is_prod() or cls.is_dev():
            host = '0.0.0.0'
        return host

    @classmethod
    def api_url(cls):
        host = cls._get_host()
        port = cls.get_port()
        return f'http://{host}:{port}'


class ConfigBase(object):
    # Base configuration
    API_TITLE = "PMID PDF API"
    API_VERSION = "1.0.0"
    API_PREFIX = '/api'
    
    # JWT configuration
    SECRET_KEY = SECRET_KEY
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Database connection timeout settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # PDF storage configuration
    PDF_ROOT_PATH = PDF_ROOT_PATH
    
    # Cache settings
    CACHE_TTL = 3600  # 1 hour cache expiration time

    # NCBI API configuration
    NCBI_API_KEY = NCBI_API_KEY
    NCBI_EMAIL = NCBI_EMAIL

    # API authentication
    API_KEYS = API_KEYS.split(',') if API_KEYS else ["test-key"]

class ConfigLocal(ConfigBase):
    # Database configuration
    MYSQL_HOST = MYSQL_DEV_HOST
    MYSQL_PORT = 3306
    MYSQL_USER = MYSQL_DEV_USER
    MYSQL_PASSWORD = MYSQL_DEV_PASSWORD
    MYSQL_DB = MYSQL_DEV_DATABASE
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
    # Local development server settings
    HOST = "localhost"
    PORT = 8002
    DEBUG = True
    
    # Logging settings
    LOG_LEVEL = "DEBUG"


class ConfigDevelopment(ConfigBase):
    # Database configuration
    MYSQL_HOST = MYSQL_DEV_HOST
    MYSQL_PORT = 3306
    MYSQL_USER = MYSQL_DEV_USER
    MYSQL_PASSWORD = MYSQL_DEV_PASSWORD
    MYSQL_DB = MYSQL_DEV_DATABASE
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
    # Development server settings
    HOST = "0.0.0.0"
    PORT = 8001
    DEBUG = True
    
    # Logging settings
    LOG_LEVEL = "INFO"


class ConfigProduction(ConfigBase):
    # Database configuration
    MYSQL_HOST = MYSQL_PROD_HOST
    MYSQL_PORT = 3306
    MYSQL_USER = MYSQL_PROD_USER
    MYSQL_PASSWORD = MYSQL_PROD_PASSWORD
    MYSQL_DB = MYSQL_PROD_DATABASE
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
    # Production server settings
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = False
    
    # Logging settings
    LOG_LEVEL = "WARNING"
    
    # Production environment cache settings
    CACHE_TTL = 86400  # 24 hours cache expiration time


# Environment configuration mapping
MAPPER = {
    EnumEnvironmentApp.production: ConfigProduction,
    EnumEnvironmentApp.development: ConfigDevelopment,
    EnumEnvironmentApp.local: ConfigLocal,
}


# Get current environment configuration
def get_config():
    env = EnumEnvironmentApp.cur_mode()
    return MAPPER.get(env)()  # Instantiate configuration class


# Current configuration instance
config = get_config()