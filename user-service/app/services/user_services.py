# app/services/user_service.py

from app.db import db  # Import db from app/db.py
from app.models.user_model import User
from sqlalchemy.exc import SQLAlchemyError
from app.auth import generate_token, verify_password

def register_user(email, password):
    try:
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already in use")

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        return user

    except ValueError as ve:
        raise ve

    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception("Database error occurred: " + str(e))
    except Exception as e:
        raise Exception("An unexpected error occurred: " + str(e))
    

def login_user(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("Invalid email/password")

        if verify_password(user.password, password):
            raise ValueError("Invalid email/password")
        return generate_token(user_id=user.id)
    except ValueError as ve:
        raise ve
    except SQLAlchemyError as e:
        raise Exception("Database error occurred: " + str(e))
    except Exception as e:
        raise Exception("An unexpected error occurred: " + str(e))
    
def getUserProfile(user_id):
    try :
        user = User.query.get(user_id)
        if not user:
            raise Exception("User not found")
        return {"email": user.email}
    except SQLAlchemyError as e:
        raise Exception("Database error occurred: " + str(e))
    except Exception as e:
        raise Exception("An unexpected error occurred: " + str(e))
        


