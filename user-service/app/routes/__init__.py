from flask import Blueprint

from .user_routes import user_routes


api_routes = Blueprint('api_routes', __name__, url_prefix="/api")

api_routes.register_blueprint(user_routes, url_prefix='/user')