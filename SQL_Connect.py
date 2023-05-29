import sqlite3
from sqlite3 import Error

def connection_sql(path):
    connection = None
    try:
        connection = sqlite3.connect(r"c:\Users\rsahu\Documents\git_files\Repo1\data.db")
        print('Connection established')
        data_entry = 'CREATE TABLE IF NOT EXISTS Stud_Data (Name TEXT, Age INT, Class INT)'
        connection.execute(data_entry)

        connection.close()
        
    except Error:
        print('Error!')

    return connection