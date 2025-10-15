"""
Application factory module for Flask backend.
Implements the application factory pattern for better modularity and testability.
"""

from flask import Flask, jsonify
from datetime import datetime, timezone
import os


def create_app(config_name=None):
    """
    Application factory function.

    Args:
        config_name (str): Configuration name ('development', 'production', 'testing').
                           If None, uses the FLASK_ENV environment variable or defaults to 'development'.

    Returns:
        Flask: Configured Flask application instance.
    """
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    # Import configuration
    from config import config
    config_obj = config.get(config_name, config['default'])

    # Ensure instance folder exists
    os.makedirs(config_obj.INSTANCE_PATH, exist_ok=True)

    # Create Flask app instance
    app = Flask(__name__, instance_path=config_obj.INSTANCE_PATH)
    app.config.from_object(config_obj)

    # Initialize extensions
    initialize_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Create database tables
    with app.app_context():
        from extensions import db
        db.create_all()

    # Register root route
    @app.route('/')
    def index():
        """Root endpoint to verify API is running."""
        return jsonify({
            'message': 'Gamify API is running',
            'version': '1.0.0',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'docs': '/api/docs'
        })

    return app


def initialize_extensions(app):
    """
    Initialize Flask extensions with the app instance.

    Args:
        app (Flask): Flask application instance.
    """
    from extensions import db, cors
    from flasgger import Swagger

    # Initialize database
    db.init_app(app)

    # Initialize CORS
    cors.init_app(app, resources={
        r"/api/*": {"origins": app.config['CORS_ORIGINS']}
    })

    # Initialize Swagger with proper parameters
    Swagger(
        app,
        config=app.config['SWAGGER_CONFIG'],
        template=app.config['SWAGGER_TEMPLATE']
    )


def register_blueprints(app):
    """
    Register Flask blueprints with the app instance.

    Args:
        app (Flask): Flask application instance.
    """
    from routes import api_bp

    app.register_blueprint(api_bp, url_prefix='/api')


def register_error_handlers(app):
    """
    Register custom error handlers for the application.

    Args:
        app (Flask): Flask application instance.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Resource not found',
            'message': str(error)
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        from extensions import db
        db.session.rollback()
        return jsonify({
            'error': 'Internal server error',
            'message': str(error)
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad request',
            'message': str(error)
        }), 400


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)