from pymongo import MongoClient
from app.settings import MONGO_URI

mongo = MongoClient(MONGO_URI)
