import pandas as pd
import os


FILE_DIR = os.path.join(
     os.path.split(os.path.dirname(__file__))[0], 
    "op_eng_test", "db_works_test.csv") 

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
            "ipi":row["IPI NUMBER"]
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
    """IPI NUMBER must have 11 characters otherwise paddle left 0 till len == 11"""
    return ipi_number if ipi_number == '' else f"{int(ipi_number):011}"