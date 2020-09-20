from flask import  Flask
from flask_cors import CORS
from .views import bp
from .extensions import mongo
from .etl import load_to_mongo



def create_app(config_object="app.settings"):
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config_object)
    
    
    app.register_blueprint(bp)

    insert_op_test_data()

    return app


def insert_op_test_data():
    """Insert data into db"""
    print('HERE')
    mongo.music_dataset.music_collection.drop()
    if not 'music_collection' in mongo.music_dataset.collection_names():
        print('2')
        load_to_mongo()
