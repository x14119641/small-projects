from app import etl
import pandas as pd
import pytest


row_1 = {"_id": 2141219,
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

series_cols ="ISWC,ORIGINAL TITLE,ALTERNATIVE TITLE 1,ALTERNATIVE TITLE 2,ALTERNATIVE TITLE 3,RIGHT OWNER,ROLE,IPI NUMBER,ID SOCIETY".split(",")
serie_1 = pd.Series(
    ["T-042088917-3","MALA YERBA","","","","RAFAEL MENDIZABAL ITURAIN","Autor","200703727",2141219],
    index=series_cols
)
last_serie = pd.Series(
    ["T-042164479-2","CHA CHA CHA DE BAHIA","CHACHACHA EN BAHIA","CHA CHACHA EN BAHÍA","CHA CHACHA EN BAHIA","EDMOND DAVID BACRI","Adaptador","1772516",611321],
    index=series_cols
) 


print(serie_1)
print(serie_1[1:5].values)
print(etl.extract_titles(serie_1[1:5].values))
print(last_serie[1:5].values)
print(etl.extract_titles(last_serie[1:5].values))


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


'''
def test_create_schema(df):
    ROW_1 = df.iloc[1,:]
    print(ROW_1)
    schema_1 = etl.create_schema(ROW_1)
    print(schema_1)
    '''
