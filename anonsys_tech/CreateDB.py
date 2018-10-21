import mysql.connector
import traceback
import json


def add_movie2tbl(db, movie):
    try:
        cursor = db.cursor()
        table_name = 'ip_movies'
        for key, val in zip(movie.keys(), movie.values()):
            if key == '__v':
                movie['_v'] = movie.pop(f'{key}')
            elif type(val) is dict: movie[key] =  json.dumps(movie[key])
            else: pass
        value_placeholders = ', '.join(['%s'] * len(movie))
        cols = ', '.join(movie.keys())
        sql = f" INSERT IGNORE INTO {table_name} ( {cols} ) VALUES ( {value_placeholders} ); "
        # sql = f" INSERT INTO {table_name} ( {cols} ) VALUES ( {value_placeholders} ) WHERE NOT EXISTS (SELECT _id FROM {table_name} WHERE _id = '{movie['_id']}'); "
        values = tuple(str(val) for val in movie.values())
        cursor.execute(sql, values)
        db.commit()
    except Exception as e:
        print(f"[!] Something went wrong while attempting the insert: {e}")
        traceback.print_exc()


# Create Databse and Table if it does not exist
def create_db():
    db = mysql.connector.connect(
        host="localhost",
        user="username",
        passwd="somepassword", # You need to enter the credentials for the MySQL server
        # database= database_name, # If no db exists, you will get an error
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE popcorntime_db")
    sql = '''CREATE TABLE ip_movies (
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
                            __v TINYINT,
                            PRIMARY KEY(_id)
                            )'''
    cursor.execute(sql)
    print("Successfully created popcorntime_db Databse and ip_movies table for webapp")
    cursor.execute("SHOW COLUMNS FROM ip_movies.popcorntime_db;")
    results = cursor.fetchall()
    for col in results:
        print(col)