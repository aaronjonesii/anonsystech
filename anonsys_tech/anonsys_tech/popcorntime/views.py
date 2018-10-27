from django.http import HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from anonsys_tech.popcorntime.models import Movie
from django.shortcuts import render
from django.db.models import Q
from requests import get
import mysql.connector
import traceback
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

    # Last Added Movies
    movie_list = Movie.objects.order_by('-released')[:500]
    # Most Popular Movies - MYSQL 8.0
    # movie_list = Movie.objects.raw("select * from ip_movies order by json_extract(rating, '$.votes') desc;")[:500]
    paginator = Paginator(movie_list, 54)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    assert isinstance(request, HttpRequest)
    context = {
        'movies': movies,
        'title': 'PopcornTime API Page',
        'page_heading': 'Last Added Movies',
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
    assert isinstance(request, HttpRequest)
    context = {
        'movies': movies,
        'title': f'Search Results for: ',
        'page_heading': f'{len(results)} Search Results Found:',
        'query': query,
    }
    return render(request, 'popcorntime.html', context)


def updatedb(request):
    print("\n---------------Preparing to Update the Movie Database--------------")
    db_connector = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='$ecurity0ff!cer',
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
        print("[!] Movie Database has been updated [!]")
    db.close()
    assert isinstance(request, HttpRequest)
    context = {
        'title': 'Movie Database Maintenance',
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
