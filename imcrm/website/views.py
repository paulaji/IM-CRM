from django.shortcuts import render, redirect
# django can handle login, logout and auth, for that import these 
from django.contrib.auth import authenticate, login, logout
# for flash messages when we login or logout
from django.contrib import messages

# creating homepage view
# adding the login feature to the home page itself
def home(request):
    # we have a form for username and password in the home page, i.e, the login form
    # in the login form if we enter something (POST) and do/invoke the POST method, we need to render 
    # if the method is GET, that is, we are not POSTing anything, we don't need to authenticate the user or anything
    if request.method == 'POST':
        username = request.POST['username'] # username will be whatever we are POSTing in the username column
        password = request.POST['password'] # password will be whatever we are POSTing in the password column
        # now we can use the authenticate of the Django! Again, kudos Django!
        user = authenticate(request, username=username, password=password) # we authenticate the username and password and store them in the user variable
        # next, if the user is actually authenticated,
        if user is not None:
            login(request, user) # login the user!
            messages.success(request, "Login successful!") # flash a message to indicate successful login
            return redirect('home') # we dont need to explicitly type home.html, django will do that for us, we have defined home in urls.py too
        # now is the case where login authenitcation was not successfull!
        else:
            messages.error(request, "Please check your username and password. There was an error logging in!")
            return redirect('home')

    # till now, we have checked whether POST method was done to the login form!
    # if the method is GET, that is, we are simply visiting and not doing anything, we just render the home.html page!
    else:
        return render(request, 'home.html', {})  
        # {} at the end specifies we are not passing any data into the home.html
        # also, django knows that it's home.html will be there in the templates folder that we created! kudos django

# creating logout view
def logout_user(request):
    # we can use the imported logout function from the django auth library
    # it automatically figures out whether a use is logged in and if yes, it can logout
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect('home')
