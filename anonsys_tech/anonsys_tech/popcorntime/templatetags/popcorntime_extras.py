from django import template
register = template.Library()

from anonsys_tech.popcorntime.models import Movie


@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    import datetime
    return datetime.date.fromtimestamp(int(timestamp))
    

# Return movie image poster
@register.simple_tag
def img_url(movie):
    import json
    if 'http' in json.loads(movie.images)['poster']:
        return json.loads(movie.images)['poster']
    else:
        return '/static/popcorntime/img/img_not_available.png'


# For Magnet downlaod link:
@register.simple_tag
def mag_link(movie):
    import json
    if '1080p' in json.loads(movie.torrents)['en']:
        return json.loads(movie.torrents)['en']['1080p']['url']
    elif '720p' in json.loads(movie.torrents)['en']:
        return json.loads(movie.torrents)['en']['720p']['url']
