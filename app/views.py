from flask import Blueprint, render_template
from .extensions import mongo

bp = Blueprint('index', __name__,
               template_folder='templates')


@bp.route('/')
def index():
    user_collection = mongo.db.users
    user_collection.insert_one({'name': 'Example'})
    return render_template('public/index.html')
