import sqlite3
from data import sql_queries


class DBWorker:
    def __init__(self, db_path="./data/AQ.db"):
        """
        Initializes a new instance of the DBWorker class.
        :param db_path: The path to the database file.
        """
        self.db_path = db_path

    def get_db_connection(self):
        """
        Function to establish a connection to the database.
        :return: sqlite3 connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn


def create_table(table_name):
    db_obj = DBWorker()
    db_connection = sqlite3.connect(db_obj.db_path)
    db_cursor = db_connection.cursor()
    db_cursor.execute(sql_queries.CREATE_TABLE[table_name])
    db_connection.commit()
    db_connection.close()


def insert_values(table_name, data):
    db_obj = DBWorker()
    db_connection = sqlite3.connect(db_obj.db_path)
    db_cursor = db_connection.cursor()
    db_cursor.execute(sql_queries.INSERT_VALUE[table_name], data)
    db_connection.commit()
    db_connection.close()


def select_values(table_name, columns='*', condition='', data=None):
    if condition == '':
        query_str = f'SELECT "{columns}" FROM {table_name}'
    else:
        query_str = f'SELECT {columns} FROM {table_name}' + condition
    db_obj = DBWorker()
    db_connection = sqlite3.connect(db_obj.db_path)
    db_cursor = db_connection.cursor()
    db_cursor.execute(query_str, (data,))
    results = db_cursor.fetchall()
    print(f'! db.select_values {results=}')
    db_connection.close()
    return results


def update_values(table_name, select_type='all', data=None):
    db_obj = DBWorker()
    db_connection = sqlite3.connect(db_obj.db_path)
    db_cursor = db_connection.cursor()
    db_cursor.execute(sql_queries.UPDATE_VALUE[table_name][select_type], data)
    db_connection.close()
