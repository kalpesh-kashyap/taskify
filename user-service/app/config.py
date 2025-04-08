from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # secret key for sesson and JWt encryption
    SECRET_KEY = os.getenv("SECRET_KEY", "4IwPSHRx/8mSux1lJTggBDlVdFOOCR55TVq08FxhR4A=")

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://kalpesh:kalpesh@localhost/taskify")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = 3600

    # Environment Configuration for Debugging
    DEBUG=os.getenv('DEBUG', True)