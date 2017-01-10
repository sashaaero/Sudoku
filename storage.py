import sqlite3

db_name = 'db'

def get_fields():
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        print('yeah')

