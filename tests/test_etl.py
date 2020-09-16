from app import etl
import pytest


@pytest.fixture
def df():
    yield etl.read_excel()


def test_read_excel(df):
    print(df)
    assert df.shape == (14,9)
    assert 'ROLE' in df.columns

'''
def test_create_schema(df):
    ROW_1 = df.iloc[1,:]
    print(ROW_1)
    schema_1 = etl.create_schema(ROW_1)
    print(schema_1)
    '''