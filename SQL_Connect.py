import sqlite3
from sqlite3 import Error

def connection_sql(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print('Connection established')
    except Error:
        print('Error!')

    return connection