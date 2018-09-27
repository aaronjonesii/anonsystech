from django.shortcuts import render # For each pages method
from django.http import HttpResponse, HttpRequest
from datetime import datetime # For each pages methods
from requests import get # For ipinfo method
from django.http import HttpResponseRedirect, HttpResponseBadRequest

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
        }
    )

def dynamic_page(request, par_ip):

    def ipiinfo(par_ip):
        url = "https://ipinfo.io/"
        resp = get(url+par_ip)
        global sec_infodata
        sec_infodata = resp.json()
        global loc
        try:
            loc = sec_infodata['loc']
        except KeyError:
            loc = '37.235000,-115.811111'

    ipiinfo(par_ip)
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
        }
    )


def popcorntime(request):

    def get_imgURL(movie):
        GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
        usr_agent = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }


    if request.method == 'POST':
        search_ip = request.POST.get('search_ip', None)
        try:
            return HttpResponseRedirect("/ip/%s" % search_ip)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    # full_url = url+path+par
    full_url = "https://tv-v2.api-fetch.website/movies/1?sort=last%20added&1&"
    # full_url = "https://tv-v2.api-fetch.website/movies/1?"
    last_added_data = get(full_url).json()


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'popcorntime/popcorntime.html',
        {
            'last_added_data': last_added_data,
            'title': 'PopcornTime API Page',
        }
    )
