from flask import Blueprint, render_template
from bson.json_util import dumps
import json
from .extensions import mongo

bp = Blueprint('index', __name__,
               template_folder='templates')


@bp.route('/')
def index():
    user_collection = mongo.db.users
    user_collection.insert_one({'name': 'Example'})
    return render_template('public/index.html')


@bp.route('/music-data')
def music_data():
    data = mongo.music_dataset.music_collection.find({})
    data = dumps(data)
    return render_template('public/music_data.html', data = data)

