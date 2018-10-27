from django.shortcuts import render
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from requests import get
from datetime import datetime
import json

# Create your views here.


def ip(request):

    ipinfo(request)

    if request.method == 'POST':
        search_ip = request.POST.get('search_ip', None)
        try:
            return HttpResponseRedirect("/ip/%s" % search_ip)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    assert isinstance(request, HttpRequest)
    context = {
        'title': 'IP Lookup Page',
        'search_type': 'search_ip',
        'visitor_data': visitor_data,
        'ip': visitor_data['ip'],
        'info_location': info_location,
        'search_type': 'search_ip',
    }
    return render(request, 'ip.html', context)


def dynamic_page(request, query_ip):

    def ipinfo(query_ip):
        url = "https://ipinfo.io/"
        resp = get(url+query_ip)
        global sec_infodata
        sec_infodata = resp.json()
        global loc
        try:
            loc = sec_infodata['loc']
        except KeyError:
            loc = '37.235000,-115.811111'

    ipinfo(query_ip)
    if request.method == 'POST':
        search_ip = request.POST.get('search_ip', None)
        try:
            return HttpResponseRedirect("/ip/%s" % search_ip)
        except:
            print("something went wrong...")
            return HttpResponseBadRequest

    assert isinstance(request, HttpRequest)
    context = {
        'location': loc,
        'query_ip': query_ip,
        'sec_infodata': sec_infodata,
        'title': 'Dynamic IP Lookup Page',
        'year': datetime.now().year,
        'search_type': 'search_ip',
    }
    return render(request,'dynamic.html',context)


def ipinfo(request):
    ip = get_client_ip(request)
    url = "https://ipinfo.io/"
    resp = get(url+ip)
    global visitor_data
    visitor_data = resp.json()
    global info_location
    if ip != '127.0.0.1':
        info_location = visitor_data['loc']
    else:
        info_location = '37.235000,-115.811111'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]
    else:
        ip_addr = request.META.get('REMOTE_ADDR')
    return ip_addr


