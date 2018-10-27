from django.urls import path
from . import views

urlpatterns = [
    path('', views.popcorntime, name='popcorntime'),
    path('search/', views.search, name='search'),
    path('updatedb', views.updatedb, name='updatedb'),
]
