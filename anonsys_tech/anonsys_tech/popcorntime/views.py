from django.http import HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from anonsys_tech.popcorntime.models import Movie
from django.db.models.expressions import RawSQL
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.contrib import messages
from .apps import add_newentry
from django.db.models import Q
from pathlib import Path
from requests import get
import mysql.connector
import traceback
import datetime
import json
import os

# Create your views here.


def popcorntime(request):

        # Search box functionality
    if request.method == 'POST':
        query = request.POST.get('popcorntime', None)
        try:
            return HttpResponseRedirect("/ip/%s" % query)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    # Recently Released Movies
    movie_list = Movie.objects.order_by('-released')[:500]
    # movie_list = Movie.objects.order_by(RawSQL('rating->>%s', ('votes',)))
    # Most Popular Movies - MYSQL 8.0
    # movie_list = Movie.objects.raw("select * from ip_movies order by json_extract(rating, '$.votes') desc;")[:500]
    paginator = Paginator(movie_list, 54)
    page = request.GET.get('page')
    movies = paginator.get_page(page)

    warning_msg = "Remember to use a secure connection!"

    assert isinstance(request, HttpRequest)
    context = {
        'movies': movies,
        'title': 'PopcornTime API Page',
        'page_heading': 'Recently Released Movies',
        'warning_msg': warning_msg,
    }
    return render(request, 'popcorntime.html', context)


def search(request):  # Search box functionality
    query = request.GET.get('popcorntime')
    if query:
        results = Movie.objects.filter(Q(title__icontains=query) | Q(synopsis__icontains=query)).order_by('-released')
        # results = Movie.objects.filter(Q(title__icontains=query)).order_by('title')
    else:
        results = Movie.objects.filter(title="Hacker")
    paginator = Paginator(results, 27)
    page = request.GET.get('page')
    movies = paginator.get_page(page)

    warning_msg = "Remember to use a secure connection!"

    assert isinstance(request, HttpRequest)
    context = {
        'movies': movies,
        'title': f'Search Results for: ',
        'page_heading': f'{len(results)} Search Results Found:',
        'query': query,
        'warning_msg': warning_msg,
    }
    return render(request, 'popcorntime.html', context)


def updatedb(request):
    time = datetime.datetime.now().strftime("%c")
    ip = get_client_ip(request)
    print("\n---------------Preparing to Update the Movie Database--------------")
    db_connector = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['DJANGO_DATABASE_PWD'],
        database='anonsys_db',  # For existing databases
    )
    db = db_connector
    print("\tGathering movies now..")
    film_type = "movie"  # Can only be Anime, Movie, or Show
    url = "https://tv-v2.api-fetch.website/exports/" + film_type
    data = get(url)
    if data.status_code == 200:
        movie_list = []
        for bytes_line in data.iter_lines():
            string_line = bytes_line.decode()
            json_movie = json.loads(string_line)
            movie_list.append(json_movie)
        print("\tUpdating Database if movie does not exist..")
        for movie in movie_list:
            add_movie2tbl(db, movie)

        # Get #/movies
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM anonsys_db.popcorntime_movie;')
        x = cursor.fetchall()
        for (i,) in x:
            dbmoviecount = i

        # Compare #/movies
        file = Path('anonsys_tech/anonsys_tech/popcorntime/moviecount')
        with open(file, 'r+') as open_file:
            read_file = open_file.readlines()
            line_number = 1
            for line in read_file:
                try:
                    linedatestamp, linemoviecount = line.split(',')
                except ValueError:
                    print(f'Improper data in file: {str(file)}\n Erasing and Adding proper data to file..')
                    open_file.truncate(0)
                    add_newentry(file, dbmoviecount)
                    break
                global new_movies
                if line_number == 1:
                    if dbmoviecount > int(linemoviecount):
                        add_newentry(file, dbmoviecount)
                        new_movies = dbmoviecount - int(linemoviecount)
                        print(f'{new_movies} new movies were added to the db..')
                    elif dbmoviecount == int(linemoviecount):
                        new_movies = None
                        print('No new movies were added to the db.')
                line_number += 1

        subject = "Movie Database Update SUCCESS"
        if new_movies == None:
            body = f"Movie Database Successfully Updated By: {ip}\n No new movies were added to the db..\n{time}"
        else:
            body = f"Movie Database Successfully Updated By: {ip}\n {new_movies} new movies were added to the db..\n{time}"
        print("[!] Movie Database has been updated, now sending email notification... [!]")
    else:
        subject = "Movie Database Update FAIL"
        body = f"Movie Database Update Attempted By: {ip}\n {time}\nSomething went wrong: {data.status_code}\n{data.content}"
        pass
    db.close()
        

    from_email = "database@anonsys.tech"
    to_list = ["admin@anonsys.tech"]
    bcc = ["support@anonsys.tech"]
    email = EmailMessage(subject=subject, body=body, from_email=from_email, to=to_list, bcc=bcc)
    email.send()
    print(f"Successfully sent Email to the following recipients: {email.recipients()}")
    assert isinstance(request, HttpRequest)
    context = {
        'title': 'Movie Database Maintenance',
        'new_movies': 0 if new_movies == None else new_movies,
    }
    return render(request, 'updatedb.html', context)


def add_movie2tbl(db, movie):
    try:
        cursor = db.cursor()
        table_name = 'popcorntime_movie'
        for key, val in zip(movie.keys(), movie.values()):
            if key == '__v':
                movie['_v'] = movie.pop(f'{key}')
            elif type(val) is dict:
                movie[key] = json.dumps(movie[key])
            else:
                pass
        value_placeholders = ', '.join(['%s'] * len(movie))
        cols = ', '.join(movie.keys())
        sql = f" INSERT IGNORE INTO {table_name} ( {cols} ) VALUES ( {value_placeholders} ); "
        values = tuple(str(val) for val in movie.values())
        cursor.execute(sql, values)
        db.commit()
    except Exception as e:
        print(f"[!] Something went wrong while attempting the insert: {e}")
        traceback.print_exc()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]
    else:
        ip_addr = request.META.get('REMOTE_ADDR')
    return ip_addr
