# this file was created after the urls.py was modified to include this file
from django.urls import path
from . import views

urlpatterns = [
    # setting up the route for the homepage
    path('', views.home, name='home'),
    # setting up the route for login and logout
    # we are calling the routes login_user and logout_user because login and logout are keywords from a library that we will import, refer to the views.py for clarification
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # manually writing a register user functionality, we can always use the django admin panel to add more users
    path('register/', views.register_user, name="register"),
    # when we want to specifically look at a record
    # for say, when we click on a specific record ID, it takes to that record
    # in this, we pass in int (integer) as pk (primary key), why int? because the id of each record is an integer
    path('record/<int:pk>', views.customer_record, name="record")
]
