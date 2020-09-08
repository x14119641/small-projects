import pytest
from app import create_app
from app.extensions import mongo
import logging
import os
from pymongo import MongoClient



@pytest.fixture
def client():
    settings_path = os.path.join(
        os.path.abspath(__name__), "settings.csg"
    )
    print(os.path.abspath(__file__))
    print('#####',settings_path)
    app = create_app()
    app.config["TESTING"] = True
    #mongo = MongoClient()
    #mongo.init_app(app)
    client = app.test_client()
    #with app.test_client() as client:
    with app.app_context():          
        pass
             
        yield client
    


def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Index" in res.data
    assert "name" in mongo.db.users.find_one({})