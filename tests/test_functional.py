import pytest
from app import create_app
from app.extensions import mongo
import json
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


def test_music_data(client):
    res = client.get("/music-data")
    assert res.status_code == 200
    tree = html.fromstring(res.data)
    json_data = tree.xpath("//div[@id = 'music_data']/text()")
    assert len(json.loads(json_data[0])) == 5


def test_retrieve_metadata(client):
    res = client.get("/music-data/T0420889173")
    assert res.status_code == 200
    tree = html.fromstring(res.data)
    json_data = tree.xpath("//div[@id = 'music_data']/text()")
    assert len(json.loads(json_data[0])) == 3


def test_create_delete_db():
    test_db = mongo.test_db
    test_db.test_collection.insert_one({'my_key': 'example'})

    assert 'test_collection' in test_db.list_collection_names()
    assert "my_key" in test_db.test_collection.find_one({})
    test_db.test_collection.drop()
    assert 'test_collection' not in test_db.list_collection_names()


def test_push_another_object_to_list_in_mongo():
    mock_doc1 = {"id":"id1",
                "my_dict_list": [{"name":"BATIRI RCA"}]
                }
    mock_doc2 = {"id":"id1",
                "my_dict_list": [{"name":"BATIRI"}]
                }
    mock_doc3 = {"id":"id1",
                "my_dict_list": [{"name":"BATIRI RI"}]
                }
    test_db = mongo.test_db
    test_db.test_collection2.insert_one(mock_doc1)

    assert 'test_collection2' in test_db.list_collection_names()
    
    query = test_db.test_collection2.find_one({})
    assert "BATIRI RCA" == query['my_dict_list'][0].get('name')

    # update list
    if test_db.test_collection2.find_one({"id":"id1"}):
        test_db.test_collection2.update(
            {"id":"id1"},
            {"$push": {"my_dict_list":mock_doc2["my_dict_list"][0]}}
            )
    
    query = test_db.test_collection2.find_one({})

    assert "BATIRI" == query['my_dict_list'][1].get('name')


    # dont update list if element in array does exist
    query_dict_doc = test_db.test_collection2.find_one( {
                            "my_dict_list": { "$elemMatch": { "name": "BATIRI" } }
                            })
   

    if not query_dict_doc:
         test_db.test_collection2.update(
            {"id":mock_doc2["id"]},
            {"$push": {"my_dict_list":mock_doc2["my_dict_list"][0]}}
            )

    query_total_docs = test_db.test_collection2.find_one({})
    # Not update as dict exist in array
    assert len(query_total_docs['my_dict_list']) ==2

    # # update list if element does not exist
    query_dict_doc = test_db.test_collection2.find_one( {
                            "my_dict_list": { "$elemMatch": { "name": mock_doc3["my_dict_list"][0].get('name') } }
                            })
    print(query_dict_doc)

    if not query_dict_doc:
         test_db.test_collection2.update(
            {"id":mock_doc3["id"]},
            {"$push": {"my_dict_list":mock_doc3["my_dict_list"][0]}}
            )

    query_total_docs = test_db.test_collection2.find_one({})
    # New document addaded
    assert len(query_total_docs['my_dict_list']) ==3

    test_db.test_collection2.drop()
    assert 'test_collection' not in test_db.list_collection_names()


    


