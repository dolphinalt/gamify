import os


class Config:
    """Base configuration class with default settings."""

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(INSTANCE_PATH, "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Swagger configuration
    SWAGGER_CONFIG = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }

    SWAGGER_TEMPLATE = {
        "swagger": "2.0",
        "info": {
            "title": "Gamify API",
            "description": "API for managing events and tasks in a gamified calendar application",
            "version": "1.0.0"
        },
        "basePath": "/api",
        "schemes": ["http"],
    }


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False

    # Override with more secure settings for production
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        Config.SQLALCHEMY_DATABASE_URI
    )


class TestingConfig(Config):
    """Testing environment configuration."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}