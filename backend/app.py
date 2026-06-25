from flask import Flask, jsonify
from config import get_config
from extensions import db, bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
import os


def create_app(config_name: str = None):
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment name (development, production, testing).
                    If None, uses FLASK_ENV environment variable (defaults to development).
    
    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Get configuration based on environment
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development").lower()
    
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Log the environment for debugging
    app.logger.info(f"Starting Flask app in {config_name} mode")

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    CORS(app)

    from auth.routes import auth_bp
    from recipes import recipes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "environment": config_name})

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
