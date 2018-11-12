from pathlib import Path
import mysql.connector
import traceback
import datetime
import os

db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd=os.environ['DJANGO_DATABASE_PWD'],
    )
cursor = db.cursor()

# Create Databse and Table if it does not exist
def create_db(cursor):
    try:
        cursor.execute("CREATE DATABASE anonsys_db")
        print('Successfully created anonsys_db Database!')
    except Exception as e:
        print(
            f'Something went wrong creating the database anonsys_db:\n\t{e}')
        # traceback.print_exc()
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
        print(f'Something went wrong trying to add the popcorntime_movie table:\n\t{e}')
        # traceback.print_exc()
    cursor.execute("SHOW COLUMNS FROM popcorntime_movie;")
    results = cursor.fetchall()
    for col in results:
        print(col)


def add_newentry(file, dbmoviecount):
    datestamp = datetime.datetime.now().strftime('%c')
    with open(file, 'r+') as open_file:
        file_data = open_file.read()
        open_file.seek(0, 0)
        new_entry = f"{datestamp}, {dbmoviecount}"
        open_file.write(new_entry+'\n'+file_data)
        print(f"Added new entry to file: {str(file)}")


def movie_count(cursor):
    cursor.execute('SELECT COUNT(*) FROM anonsys_db.popcorntime_movie;')
    x = cursor.fetchall()
    for (i,) in x:
        dbmoviecount = i
    try:
        file = Path('anonsys_tech/anonsys_tech/popcorntime/moviecount')
        if file.exists() and file.read_text():
            open_file = open(file, 'r+')
            read_file = open_file.readlines()
            line_number = 1
            for line in read_file:
                try:
                    linedatestamp, linemoviecount = line.split(',')
                except ValueError as vale:
                    print(f'Improper data in file: {str(file)}\n Erasing and Adding proper data to file..')
                    open_file.truncate(0)
                    add_newentry(file, dbmoviecount)
                    break
                if line_number == 1:
                    if dbmoviecount > int(linemoviecount):
                        new_movies = dbmoviecount - int(linemoviecount)
                        print(f'{new_movies} new movies were accounted for in the new entry..')
                        add_newentry(file, dbmoviecount)
                    elif dbmoviecount == int(linemoviecount):
                        print('MovieCount file is up to date...')
                line_number += 1
        elif file.exists() and not file.read_text():
            print('File is currently empty')
            add_newentry(file, dbmoviecount)
        else:
            print(f"{str(file)} does not exist, Creating file now..")
            file.touch()
            print('File created successfully..')
            add_newentry(file, dbmoviecount)
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()


if __name__ == '__main__':
    create_db(cursor)
    movie_count(cursor)
