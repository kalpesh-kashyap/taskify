import jwt
from flask import request, jsonify
from functools import wraps
from app.db import db
from datetime import datetime, timedelta
from app.models.user_model import User
from app.config import Config
from werkzeug.security import check_password_hash


def generate_token(user_id):
    """Generate JWT Token"""
    payload = {
        'sub': str(user_id),
        'exp': datetime.utcnow()+timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)
    }
    return jwt.encode(payload,Config.SECRET_KEY,algorithm='HS256')

def verify_password(stored_passowd, provided_password):
    return check_password_hash(stored_passowd, provided_password)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
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

                    
