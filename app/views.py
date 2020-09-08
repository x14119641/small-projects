from flask import Blueprint
from .extensions import mongo

bp = Blueprint('views', __name__)

@bp.route('/')
def index():
    user_collection = mongo.db.users
    user_collection.insert_one({'name': 'Example'})
    return "<h1>Index</h1>"