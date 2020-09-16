import pandas as pd
import os


FILE_DIR = os.path.join(
     os.path.split(os.path.dirname(__file__))[0], 
    "op_eng_test", "db_works_test.csv") 

def read_excel(file=FILE_DIR):
    return pd.read_csv(file)



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
        "titles":"extract titles",
        "right_owners":[{
            "name":row["RIGHT OWNER"],
            "role":row["ROLE"],
            "ipi":"ipi_extract"}]
    }