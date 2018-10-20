from django.shortcuts import render # For each pages method
from django.http import HttpResponse, HttpRequest
from datetime import datetime # For each pages methods
from requests import get # For ipinfo method
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from ip.models import Movies
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
            'search_type': 'popcorntime',
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

    movies = Movies.objects.order_by('-released')[:500]
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'popcorntime/popcorntime.html',
        {
            # 'lastadded_movies': lastadded_movies,
            'movies': movies,
            'title': 'PopcornTime API Page',
            'search_type': 'popcorntime',
        }
    )

