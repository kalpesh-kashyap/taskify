from flask import Blueprint, request, jsonify
from app.config import Config
from app.auth import token_required
import requests

user_routes = Blueprint('user_routes', __name__)


@user_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        if not data or 'email' not in data or 'password' not in data:
            raise ValueError("email or password required")
        
        user_service_url = f"{Config.USER_SERVICE_URL}/api/user/login"
        response = requests.post(user_service_url, json=data)
        return response.json(), response.status_code
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@user_routes.route("/register",  methods=['POST'])
def register():
    data = request.get_json()

    try:
        if not data or 'email' not in data or 'password' not in data:
            raise ValueError("email or password required")
        
        user_service_url = f"{Config.USER_SERVICE_URL}/api/user/register"     
        response = requests.post(user_service_url, json=data)
        return response.json(), response.status_code
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    

@user_routes.route("/profile", methods=["GET"])
@token_required
def get_user(user_id):
    try:
        print("here at api-gatewaya")
        print(user_id)
        user_service_url = f"{Config.USER_SERVICE_URL}/api/user/profile"
        print(user_service_url)
        response = requests.get(user_service_url, headers={"X-User-ID": user_id})
        return response.json()
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500



