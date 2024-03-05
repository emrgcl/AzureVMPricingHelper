from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from .routes.routes import api as offers_api
from .database import db

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    db.init_app(app)

    api = Api(app, title='Offers API', version='1.0', description='An API for fetching offers')
    api.add_namespace(offers_api)

    return app
