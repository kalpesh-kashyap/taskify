import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "4IwPSHRx/8mSux1lJTggBDlVdFOOCR55TVq08FxhR4A=")
    APP_PORT = os.getenv("PORT", "3000")

    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:3001')
    IMAGE_PROCESS_SERVICE = os.getenv('IMAGE_PROCESS_SERVICE', 'http://localhost:3002')

    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = 3600