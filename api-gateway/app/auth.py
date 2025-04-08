import jwt
from functools import wraps
from flask import request, jsonify
from app.config import Config

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id = payload["sub"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"message": "Invalid token!", "error": str(e)}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated_function

