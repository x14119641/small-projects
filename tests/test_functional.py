import pytest
from app import create_app
from app.extensions import mongo

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
    assert "Navbar" in tree.xpath('//nav/a/text()')
    assert "name" in mongo.db.users.find_one({})


def test_create_delete_db():
    test_db = mongo.test_db
    test_db.test_collection.insert_one({'my_key': 'example'})
    print(test_db.test_collection.find_one({}))

    assert 'test_collection' in test_db.list_collection_names()
    assert "my_key" in test_db.test_collection.find_one({})
    test_db.test_collection.drop()
    assert 'test_collection' not in test_db.list_collection_names()


def test_push_another_object_to_list_in_mongo():
    test_db = mongo.test_db
    test_db.test_collection2.insert_one({
        'id':'id1',
        'my_dict_list': [{"key1":"value1"}]
        })

    assert 'test_collection2' in test_db.list_collection_names()
    query = test_db.test_collection2.find_one({})
    assert "value1" in query['my_dict_list'][0].get('key1')

    # update list
    to_update = {"key2":"value2"}
    if test_db.test_collection2.find_one({"id":"id1"}):
        test_db.test_collection2.update(
            {"id":"id1"},
            {"$push": {"my_dict_list":to_update}}
            )
    
    query = test_db.test_collection2.find_one({})
    assert "value2" in query['my_dict_list'][1].get('key2')

    test_db.test_collection2.drop()
    assert 'test_collection' not in test_db.list_collection_names()


    


