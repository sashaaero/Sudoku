import sqlite3 as sql

db_name = 'db'

# this check for table runs when 'storage' was imported
with sql.connect(db_name) as connection:
    cursor = connection.cursor()
    # check if table exists
    result = cursor.execute('select name from sqlite_master where type="table" and name="fields"')
    if len(result.fetchall()) == 0:
        cursor.execute('create table fields(data, was_solved)')

def save_field(field, was_solved=False):
    with sql.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('insert into fields values("%s", %r)' % (field, was_solved))

def set_solved(field):
    with sql.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute() # Надо поле поменять


def get_fields():
    with sql.connect(db_name) as connection:
        cursor = connection.cursor()
        # check if table exists
        result = cursor.execute('select * from fields')



get_fields()


