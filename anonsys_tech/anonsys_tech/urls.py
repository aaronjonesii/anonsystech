"""anonsys_tech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from anonsys_tech.home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('anonsys_tech.home.urls'), name='home'),
    path('contact/', views.contact, name="contact"),
    path('ip/', include('anonsys_tech.ip.urls'), name='ip'),
    path('popcorntime/', include('anonsys_tech.popcorntime.urls'), name='popcorntime'),
    path('pt/', include('anonsys_tech.popcorntime.urls'), name='popcorntime'),
    path('thx/', views.thx, name="thx"),
]
