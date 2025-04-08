from flask import Blueprint, request, jsonify
from app.services.user_services import register_user, login_user, getUserProfile
from app.auth import token_required

user_routes = Blueprint('user_routes', __name__)


@user_routes.route("/register", methods=["POST"])
def regiter_user():
    try:
        data = request.get_json()

        print(data, "from the user-service")

        if not data or 'email' not in data or 'password' not in data:
            raise ValueError("email or password missing") 

        email = data["email"]
        password = data["password"]

        user = register_user(email=email, password=password)

        return jsonify({"message": f"User {user.email} created successfully"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500  
    

@user_routes.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        print(data)

        if not data or 'email' not in data or 'password' not in data:
            raise ValueError("email or password missing") 
        
        email = data["email"]
        password = data["password"]

        user = login_user(email=email, password=password)
        return jsonify({"token": user})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500  
    

@user_routes.route("/profile", methods=["GET"])    
# @token_required
def get_profile():
    try:
        print("reach here")
        user_id = request.headers.get("X-User-ID")
        print(user_id)
        user = getUserProfile(user_id=user_id)
        return jsonify({"data": user})
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500  