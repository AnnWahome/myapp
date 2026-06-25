import os
from datetime import timedelta


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DEFAULT_DB_PATH = os.path.join(INSTANCE_DIR, "culinaryconnect.db")


def _sqlite_uri(path: str) -> str:
    return f"sqlite:///{path.replace('\\', '/')}"


def _resolve_database_uri() -> str:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        if database_url.startswith("sqlite:///") and not database_url.startswith("sqlite:////"):
            database_path = database_url.replace("sqlite:///", "", 1)
            if not os.path.isabs(database_path):
                resolved_path = os.path.abspath(os.path.join(BASE_DIR, database_path))
                os.makedirs(os.path.dirname(resolved_path), exist_ok=True)
                return _sqlite_uri(resolved_path)
        return database_url

    os.makedirs(INSTANCE_DIR, exist_ok=True)
    return _sqlite_uri(DEFAULT_DB_PATH)


class Config:
    """Base configuration class"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri()
    JSON_SORT_KEYS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


# Configuration dictionary for environment selection
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(env: str = None) -> Config:
    """
    Get the appropriate configuration class based on environment.
    
    Args:
        env: Environment name (development, production, testing).
             If None, uses FLASK_ENV environment variable.
             Defaults to 'development' if not set.
    
    Returns:
        Configuration class for the specified environment.
    """
    if env is None:
        env = os.getenv("FLASK_ENV", "development").lower()
    
    return config_by_name.get(env, DevelopmentConfig)
