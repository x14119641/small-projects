import pytest
from app import create_app
from app.extensions import mongo

from pymongo import MongoClient
from lxml import html


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    with app.app_context():          
        pass
             
        yield client
    


def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    tree = html.fromstring(res.data)
    
    assert "Home" in tree.xpath('//title/text()')
    #print(res.data)
    assert "Navbar" in tree.xpath('//nav/a/text()')
    assert "name" in mongo.db.users.find_one({})
