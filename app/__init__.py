from flask import  Flask
from flask_cors import CORS
from .views import bp


def create_app(config_object="app.settings"):
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config_object)
    
    
    app.register_blueprint(bp)
    
    return app