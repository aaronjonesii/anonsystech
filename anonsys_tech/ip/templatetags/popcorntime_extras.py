from django import template
register = template.Library()

from ip.models import Movies

@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    import datetime
    return datetime.date.fromtimestamp(int(timestamp))


@register.filter('to_json')
def convert_to_json(string):
    import json
    json_str = json.loads(string)
    return json_str


@register.filter('typeof')
def typeof(string, value):
    import json
    if value == 'poster':
        return json.loads(string)['poster']
    elif value == 'fanart':
        return json.loads(string)['fanart']
    elif value == 'banner':
        return json.loads(string)['banner']


@register.simple_tag
def img_url(movie):
    import json
    if 'http' in json.loads(movie.images)['poster']:
        return json.loads(movie.images)['poster']
    else:
        return '/static/popcorntime/img/img_not_available.svg'