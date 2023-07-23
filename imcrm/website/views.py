from django.shortcuts import render
# django can handle login, logout and auth, for that import these 
from django.contrib.auth import authenticate, login, logout
# for flash messages when we login or logout
from django.contrib import messages

# creating homepage view
def home(request):
    return render(request, 'home.html', {})  # {} at the end specifies we are not passing any data into the home.html
    # also, django knows that it's home.html will be there in the templates folder that we created! kudos django

# creating login view
def login_user(request):
    pass

# creating logout view
def logout_user(request):
    pass
