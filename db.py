import os

import psycopg2
from psycopg2.extras import DictCursor

DB_NAME = os.getenv('DB_NAME', 'rpas')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PWD = os.getenv('DB_PWD', '1234')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', 5432)


def get_db_handles():
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PWD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor(cursor_factory=DictCursor)

    return connection, cursor


def get_data(data_type):
    conn, cursor = get_db_handles()

    query = ''
    if data_type == 'raw':
        query = get_raw_query()
    elif data_type == 'prediction':
        query = get_prediction_query()
    elif data_type in ('train', 'test'):
        query = get_train_test_query(data_type)

    cursor.execute(query)

    data = cursor.fetchall()

    return data


def get_data_values(data_type, data_id):
    conn, cursor = get_db_handles()

    query = f"""
        SELECT 
            D.DATA_VALUE
        FROM {data_type}_DATA_VALUES AS D
        WHERE    
            D.{data_type}_DATA_ID = {data_id}      
        """
    cursor.execute(query)

    data = cursor.fetchall()
    flatten_data = sum(data, [])

    return flatten_data


def get_raw_query():
    return f"""
        SELECT 
            RD.WELL_ID,
            RD.PARAMETER,
            RD.ID
        FROM RAW_DATA AS RD
        ORDER BY
            RD.ID DESC         
        """


def get_prediction_query():
    return f"""
        SELECT 
            RD.WELL_ID,
            RD.PARAMETER,
            PD.TEST_DATA_ID,
            TD.CORRECTIONS AS TEST_DATA_CORRECTIONS,
            TD.NORMALIZATION_VALUE,
            M.NETWORK,
            PD.MODEL_ID,
            PD.ID
        FROM PREDICTION_DATA AS PD
            INNER JOIN TEST_DATA AS TD
                ON PD.TEST_DATA_ID = TD.ID
            INNER JOIN RAW_DATA AS RD 
                ON TD.RAW_DATA_ID = RD.ID
            INNER JOIN MODELS AS M
                ON PD.MODEL_ID = M.ID
        ORDER BY
            PD.ID DESC     
    """


def get_train_test_query(data_type):
    return f"""
        SELECT 
            RD.WELL_ID,
            RD.PARAMETER,
            D.RAW_DATA_ID,
            D.CORRECTIONS,
            D.NORMALIZATION_VALUE,
            D.ID
        FROM {data_type}_DATA AS D
            INNER JOIN RAW_DATA AS RD 
                ON D.RAW_DATA_ID = RD.ID
        ORDER BY
            D.ID DESC         
        """
