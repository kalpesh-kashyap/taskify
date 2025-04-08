from flask import Flask, jsonify
from .config import Config
from .routes import api_routes

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(api_routes)

    # Error handlers
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    return app