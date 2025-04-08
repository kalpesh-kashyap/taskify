from flask import Flask
from .config import Config
from .db import db
from flask_migrate import Migrate
from .file_routes import file_routes


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    app.register_blueprint(file_routes)
    db.init_app(app)
    migrate.init_app(app, db)

    return app