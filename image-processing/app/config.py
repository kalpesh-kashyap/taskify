from os import getenv, path, getcwd
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = getenv('PORT', '3002')
     # Database configuration
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI", "postgresql://kalpesh:kalpesh@localhost/taskify")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FILE_UPLOAD_PATH = 'uploads'
    PROCESSED_FILE_PATH = path.join(getcwd(), 'processed_files') 
