import mysql.connector
import traceback
import json


# Create Databse and Table if it does not exist
def create_db():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='$ecurity0ff!cer',
    )
    cursor = db.cursor()
    try:
        cursor.execute("CREATE DATABASE anonsys_db")
        print('Successfully created anonsys_db Database!')
    except Exception as e:
        print(
            f'Something went wrong creating the database anonsys_db: {e}')
        traceback.print_exc()
    cursor.execute('use anonsys_db;')
    sql = '''CREATE TABLE popcorntime_movie (
                            _id VARCHAR(20),
                            imdb_id VARCHAR(10),
                            title VARCHAR(255),
                            year VARCHAR(4),
                            slug VARCHAR(150),
                            synopsis TEXT,
                            runtime VARCHAR(4),
                            country VARCHAR(4),
                            last_updated FLOAT(16,1),
                            released INT,
                            certification VARCHAR(255),
                            torrents TEXT,
                            trailer VARCHAR(255),
                            genres VARCHAR(255),
                            images TEXT,
                            rating VARCHAR(255),
                            _v TINYINT,
                            PRIMARY KEY(_id)
                            )'''
    try:
        cursor.execute(sql)
        print('Successfully created popcorntime_movie table in anonsys_db Database!')
    except Exception as e:
        print(f'Something went wrong trying to add the popcorntime_movie table: {e}')
        traceback.print_exc()
    cursor.execute("SHOW COLUMNS FROM popcorntime_movie;")
    results = cursor.fetchall()
    for col in results:
        print(col)


if __name__ == '__main__':
    create_db()
