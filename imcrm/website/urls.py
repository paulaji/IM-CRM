# this file was created after the urls.py was modified to include this file
from django.urls import path
from . import views

urlpatterns = [
    # setting up the route for the homepage
    path('', views.home, name='home'),
]
