from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ip, name='ip'),
    # path('<str:url_ip>', views.dynamic_page, name='dynamic_ip'),
    re_path(r'^(?P<par_ip>(?:(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?)\.){3}(?:0|1[\d]{0,2}|2(?:[0-4]\d?|5[0-5]?|[6-9])?|[3-9]\d?))/$', views.dynamic_page, name='dynamic_page'),
]
