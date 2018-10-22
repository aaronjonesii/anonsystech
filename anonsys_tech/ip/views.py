from django.shortcuts import render # For each pages method
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from datetime import datetime # For each pages methods
from requests import get # For ipinfo method
from django.contrib import messages
from ip.models import Movies
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import traceback
import json
import mysql.connector
# import json

# Create your views here.
# def index(request):
#     return HttpResponse("Hello there, you are at the index view..")

# Template Views

def index(request):
    if request.method == 'POST':
        search_ip = request.POST.get('search_ip', None)
        try:
            return HttpResponseRedirect("/ip/%s" % search_ip)
        except: print("something went wrong..."); return HttpResponseBadRequest

    return render(
        request,
        'main/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'search_type': 'popcorntime',
        }
    )


def ip(request):
    # Get requestors ip address
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_addr = x_forwarded_for.split(',')[0]
        else:
            ip_addr = request.META.get('REMOTE_ADDR')
        return ip_addr

    def ipinfo():
        # ip = "76.20.137.56"
        ip = get_client_ip(request)
        url = "https://ipinfo.io/"
        resp = get(url+ip)
        global ii_data
        ii_data = resp.json()
        global info_location
        if ip != '127.0.0.1':
            info_location = ii_data['loc']
        else:
            info_location = '37.235000,-115.811111'


    ipinfo()
    # Search IP Form
    if request.method == 'POST':
        search_ip = request.POST.get('search_ip', None)
        try:
            return HttpResponseRedirect("/ip/%s" % search_ip)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'ip/ip.html',
        {
            'ii_data': ii_data,
            'ip': ii_data['ip'],
            # 'ip_addr': '76.20.137.56',
            'info_location': info_location,
            'title': 'IP Lookup Page',
            'year': datetime.now().year,
            'search_type': 'search_ip',
        }
    )


def contact(request):

    if request.method == 'POST':
        search_ip = request.POST.get('search_ip', None)
        try:
            return HttpResponseRedirect("/ip/%s" % search_ip)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'contact/contact.html',
        {
            'title':'Contact Page',
            'year':datetime.now().year,
            'search_type': 'popcorntime',
        }
    )


def dynamic_page(request, par_ip):

    def ipinfo(par_ip):
        url = "https://ipinfo.io/"
        resp = get(url+par_ip)
        global sec_infodata
        sec_infodata = resp.json()
        global loc
        try:
            loc = sec_infodata['loc']
        except KeyError:
            loc = '37.235000,-115.811111'

    ipinfo(par_ip)
    if request.method == 'POST':
        search_ip = request.POST.get('search_ip', None)
        try:
            return HttpResponseRedirect("/ip/%s" % search_ip)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'ip/dynamic.html',
        {
            'location': loc,
            'par_ip': par_ip,
            'sec_infodata': sec_infodata,
            'title':'Dynamic IP Lookup Page',
            'year':datetime.now().year,
            'search_type': 'search_ip',
        }
    )


def popcorntime(request):

    # Search box functionality
    if request.method == 'POST':
        query = request.POST.get('popcorntime', None)
        try:
            return HttpResponseRedirect("/ip/%s" % query)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    # movie_list = Movies.objects.all()[:500]
    # Last Added Movies
    movie_list = Movies.objects.order_by('-released')[:500]
    # Most Popular Movies
    # movie_list = Movies.objects.raw("select * from ip_movies order by json_extract(rating, '$.votes') desc;")[:500]
    # Message
    # messages.info(request, f'{len(movie_list)} SQL results were returned')
    paginator = Paginator(movie_list, 54)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'popcorntime/popcorntime.html',
        {
            'movies': movies,
            'title': 'PopcornTime API Page',
            'page_heading': 'Last Added Movies',
        }
    )


def search(request): # Search box functionality
    if request.method == 'POST':
        query = request.POST.get('popcorntime', None)
        try:
            return HttpResponseRedirect("/ip/%s" % query)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    query = request.GET.get('popcorntime')
    if query:
        results = Movies.objects.filter(Q(title__icontains=query) | Q(synopsis__icontains=query)).order_by('-released')
        # results = Movies.objects.filter(Q(title__icontains=query)).order_by('title')
    else:
        results = Movies.objects.filter(title="Hacker")
    paginator = Paginator(results, 27)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'popcorntime/popcorntime.html',
        {
            'movies': movies,
            'title': f'Search Results for: ',
            'page_heading': f'{len(results)} Search Results Found:',
            'query': query,
        }
    )


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


def updatedb(request):
    print("\n---------------Preparing to Update the Movie Database--------------")
    db_connector = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="$ecurity0ff!cer",
        database='popcorntime_db',  # For existing databases
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
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'popcorntime/updatedb.html',
        {
            'title': 'Movie Database Maintenance',
        }
    )
