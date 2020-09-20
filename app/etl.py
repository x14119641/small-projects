import pandas as pd
import os


FILE_DIR = os.path.join(
     os.path.split(os.path.dirname(__file__))[0], 
    "op_eng_test", "db_works_test.csv") 



### EXTRACT AND  TRANSFORM ###
def read_excel(file=FILE_DIR):
    """Read csv file and deletes empty spaces on the left in columns"""
    df =  pd.read_csv(file)
    df.columns = df.columns.str.lstrip()
    df.fillna('', inplace=True)
    return df


def create_schema(row):
    """Creates a json object from series

    Args:
        row: pandas series (a row)
    
    Returns:
        json object
    """
    return {
        "_id": row["ID SOCIETY"],
        "iswc": str(row["ISWC"]).replace("-", ""),
        "titles":extract_titles(row[1:5]),
        "right_owners":[{
            "name":row["RIGHT OWNER"],
            "role":row["ROLE"],
            "ipi":extract_ipi(row["IPI NUMBER"])
            }]
    }


def extract_titles(row):
    """Creates a list of dictionaries with the titles data and alternatives if exists

    Args:
        list: row[1:5].values
    
    Return:
        list of dictionaries with title and title type
    """
    data = [
        {"title":row[0], "type": "OriginalTitle"}
        ]
    for item in set(row[1:]):
        if item and item != row[0]:
            data.append(
                {"title":item,"type":"AlternativeType"}
                )
    return data


def extract_ipi(ipi_number):
    """IPI NUMBER must have 11 characters otherwise paddle left 0 till len == 11
    or empty if not ipi number is supplied"""
    return ipi_number if ipi_number == '' else f"{int(ipi_number):011}"


### LOAD TO DATABASE ###
def insert_data(obj, database_test=False):
    from .extensions import mongo
    if database_test:
        collection = mongo.test_music_dataset.music_collection
    else:
        collection = mongo.music_dataset.music_collection

    if collection.find_one({"_id": obj['_id']}):
        collection.update( {"_id": obj['_id']}, {"$push": {"right_owners":{"$each":obj["right_owners"]}}})
        collection.update( {"_id": obj['_id']}, {"$addToSet": {"titles":{"$each":obj["titles"]}}})
    else:
        collection.insert_one(obj)

def load_to_mongo(file=FILE_DIR):
    """Loads data from csv file by row and inserts to mongo"""
    df = read_excel(file)
    for (_,row) in df.iterrows():
        obj = create_schema(row)
        insert_data(obj)
