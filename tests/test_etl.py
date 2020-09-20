from app import etl
import pandas as pd
from app.extensions import mongo
import pytest


doc_1 = {"_id": 2141219,
         "iswc": "T0420889173",
         "titles": [
             {"title": "MALA YERBA",
              "type": "OriginalTitle"}
         ],
         "right_owners": [
             {"name": "RAFAEL MENDIZABAL ITURAIN",
              "role": "Autor",
              "ipi": "00200703727"},
             {"name": "JOSE CARPENA SORIANO",
                 "role": "Autor",
                 "ipi": "00222061816"},
             {"name": "FRANCISCO MARTINEZ SOCIAS",
                 "role": "Compositor",
                 "ipi": "00222084113"}
         ]
         }

last_doc = {"_id": 611321,
         "iswc": "T0421644792",
         "titles": [
             {"title": "CHA CHA CHA DE BAHIA",
              "type": "OriginalTitle"},
              {"title": "CHACHACHA EN BAHIA",
              "type": "AlternativeType"},
              {"title": "CHA CHACHA EN BAHÍA",
              "type": "AlternativeType"},
              {"title": "CHA CHACHA EN BAHIA",
              "type": "AlternativeType"},
         ],
         "right_owners": [
             {"name": "ENRIQUE JESUS JORRIN Y OLEAGA",
              "role": "Compositor/Autor",
              "ipi": "00015546498"},
             {"name": "EDMOND DAVID BACRI",
                 "role": "Adaptador",
                 "ipi": "00001772516"}
         ]
         }

series_cols ="ISWC,ORIGINAL TITLE,ALTERNATIVE TITLE 1,ALTERNATIVE TITLE 2,ALTERNATIVE TITLE 3,RIGHT OWNER,ROLE,IPI NUMBER,ID SOCIETY".split(",")
serie_1 = pd.Series(
    ["T-042088917-3","MALA YERBA","","","","RAFAEL MENDIZABAL ITURAIN","Autor","200703727",2141219],
    index=series_cols
)
last_serie = pd.Series(
    ["T-042164479-2","CHA CHA CHA DE BAHIA","CHACHACHA EN BAHIA","CHA CHACHA EN BAHÍA","CHA CHACHA EN BAHIA","EDMOND DAVID BACRI","Adaptador","1772516",611321],
    index=series_cols
) 


@pytest.fixture
def df():
    yield etl.read_excel()


def test_read_excel(df):
    print(df)
    assert df.shape == (14, 9)
    assert 'ROLE' in df.columns
    assert any(item.startswith(" ") for item in df.columns) is False, "Some column name starts with ' '"


def test_extract_ipi():
    ipis = ["200703727","222084113", "159586128", "68238360", "00555"]
    for ipi in ipis:
        assert len(etl.extract_ipi(ipi)) ==11
    assert etl.extract_ipi('') ==''


def test_extract_titles():
    assert len(etl.extract_titles(serie_1[1:5].values)) ==1
    assert len(etl.extract_titles(last_serie[1:5].values)) ==4



def test_create_schema(df):
    schema_1 = etl.create_schema(df.iloc[1,:])
    assert isinstance(schema_1, dict) 
    assert schema_1["_id"] == doc_1["_id"] 
    assert schema_1["iswc"] == doc_1["iswc"] 
    assert schema_1["titles"][0]["title"] == doc_1["titles"][0]["title"]
    assert schema_1["right_owners"][0]["name"] in doc_1["right_owners"][1]["name"] 


### Test Load data ###
def test_insert_data(df):
    """Inserts 3 first rows to see if maps the doc_1"""
    for (i,row) in df.iterrows():
        if i > 2:
            break
        obj = etl.create_schema(row)
        etl.insert_data(obj, True)
    query = mongo.test_music_dataset.music_collection.find_one({"_id": obj['_id']})
    assert isinstance(query, dict) 
    assert query["_id"] == doc_1["_id"] 
    assert query["iswc"] == doc_1["iswc"] 
    assert len(query["titles"]) == len(doc_1["titles"])
    assert len(query["right_owners"]) == len(doc_1["right_owners"])
    owners_name_query = [item["name"] for item in query["right_owners"]]
    owners_name_doc_1 = [item["name"] for item in doc_1["right_owners"]]
    assert set(owners_name_query) == set(owners_name_doc_1)
    owners_ipi_query = [item["ipi"] for item in query["right_owners"]]
    owners_ipi_doc_1 = [item["ipi"] for item in doc_1["right_owners"]]
    assert set(owners_ipi_query) == set(owners_ipi_doc_1)

    mongo.test_music_dataset.music_collection.drop()
    assert "music_collection" not in mongo.test_music_dataset.list_collection_names()



def test_load_data(df):
    """Same loop of load_data in etl, testes last document"""
    mongo.test_music_dataset.music_collection.drop()
    for (_,row) in df.iterrows():
        obj = etl.create_schema(row)
        etl.insert_data(obj, True)
    
    all_items = mongo.test_music_dataset.music_collection.find({})
    assert len(list(all_items))==5

    # last item
    query = mongo.test_music_dataset.music_collection.find_one({"_id": last_doc['_id']})
    assert isinstance(query, dict) 
    assert query["_id"] == last_doc["_id"] 
    assert query["iswc"] == last_doc["iswc"] 
    assert len(query["titles"]) == len(last_doc["titles"])
    assert len(query["right_owners"]) == len(last_doc["right_owners"])
    owners_name_query = [item["name"] for item in query["right_owners"]]
    owners_name_last_doc = [item["name"] for item in last_doc["right_owners"]]
    assert set(owners_name_query) == set(owners_name_last_doc)
    owners_ipi_query = [item["ipi"] for item in query["right_owners"]]
    owners_ipi_last_doc = [item["ipi"] for item in last_doc["right_owners"]]
    assert set(owners_ipi_query) == set(owners_ipi_last_doc)
        
    mongo.test_music_dataset.music_collection.drop()
    assert "music_collection" not in mongo.test_music_dataset.list_collection_names()