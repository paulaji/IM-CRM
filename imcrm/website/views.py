from django.shortcuts import render, redirect
# django can handle login, logout and auth, for that import these 
from django.contrib.auth import authenticate, login, logout
# for flash messages when we login or logout
from django.contrib import messages
# to import the form we created in forms.py (the registration/signup form)
from .forms import SignUpForm
# importing the Customer datamodel we just created so that we can display all the records
from .models import Customer



# creating homepage view
# adding the login feature to the home page itself
def home(request):


    # grabbing all customer records to display them
    customers = Customer.objects.all()


    # we have a form for username and password in the home page, i.e, the login form
    # in the login form if we enter something (POST) and do/invoke the POST method, we need to render 
    # if the method is GET, that is, we are not POSTing (submitting) anything, we don't need to authenticate the user or anything
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
        # passing the customers variable which contains all the customer records we inserted into the table
        # since the method is not POST, and if we are getting the home.html rendered, it means that we are logged in and we can pass the customers variable such that all customer objects we created can be displayed
        return render(request, 'home.html', {'customers': customers})  
        # if {} comes at the end, it specifies we are not passing any data into the home.html
        # also, django knows that it's home.html will be there in the templates folder that we created! kudos django



# creating logout view
def logout_user(request):
    # we can use the imported logout function from the django auth library
    # it automatically figures out whether a use is logged in and if yes, it can logout
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect('home')



# creating register user view
def register_user(request):


    if request.method == "POST":
        # by passing request.POST as parameter, the SignUpForm will be populated with the data the user is POSTing
        form = SignUpForm(request.POST)
        # first check if whatever the user typed in the form is valid
        if form.is_valid():
            form.save()
            # to login and authenticate the user immediately after the user registers, cause why not!
            # django has method for that too
            # for that first, use the cleaned_data method of django to take out the username and password seperately
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # after getting username and password, authenticate them in!
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        
        
    # else, if the user is not posting and is just visiting the register page,
    else:
        # we simply pass in the form without the POST method
        form = SignUpForm()
        # we render register.html template
        # render and redirect work differently
        # in this part, user is not POSTing anything, therefore we need to render the register.html and provide an empty form
        # therefore we pass in / create the form instance {'form': form}
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})



    
