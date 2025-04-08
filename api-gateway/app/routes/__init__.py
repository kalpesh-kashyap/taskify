from flask import Blueprint
from .users_routes import user_routes
from .image_processing import file_upload

api_routes = Blueprint('api_routes', __name__, url_prefix="/api")

api_routes.register_blueprint(user_routes, url_prefix="/user")
api_routes.register_blueprint(file_upload, url_prefix="/file")