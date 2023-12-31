from django.shortcuts import render, redirect
# django can handle login, logout and auth, for that import these 
from django.contrib.auth import authenticate, login, logout
# for flash messages when we login or logout
from django.contrib import messages
# to import the form we created in forms.py (the registration/signup form)
# also, import the AddCustomerRecordForm
from .forms import SignUpForm, AddCustomerRecordForm
# importing the Customer datamodel we just created so that we can display all the records
from .models import Customer

# if an object doesnt exist, eg, if we only have two records and we try to manually enter localhost:8000/record/3
from django.core.exceptions import ObjectDoesNotExist



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



# when we want to view a specific record clicking on the ID
# in this, compared to the others, we are not just passing in the request, we also pass the pk
# the passing of primary key is to access a specific record based off the id and it will look like 
# localhost:8000/record/2 where 2 is the record id
def customer_record(request, pk):


    # only make this functionality available if the user is logged in
    # that is, if any person just goes to the url and types localhost:8000/record/2, they should not be able to access it
    if request.user.is_authenticated:
        # retrieve the specific record with the id
        # store into the customer variable, the Customer object with the id which is the primary key (the integer number) we are supposedly passing in with our request
        # initially the variable below was called customer_record, but since the function also has the name customer_record, it would be good to change the variable name just to avoid any confusions
        # while python generally allows us to name the variable and function, the same name, it is good practice not to do so
        # customer_data = Customer.objects.get(id=pk) - this is an original code
        # pass the individual record we retrieved
        # return render(request, 'record.html', {'customer_data': customer_data}) - this is an original code

        # now that we have checked for if the user is logged in,
        # we have to check for another condition such that the int/pk which is getting passed after the localhost:8000/record/1 exists
        # the integer depends on the number of records
        # if one record exists localhost:8000/record/1, this would take to that record
        # if only two records exist and we try to enter localhost:8000/record/3, it must return an error
        # the statements below are for the cases such that people try to manually enter a url like localhost:8000/record/3 (in which something doesnt exist)
        try:
            customer_data = Customer.objects.get(id=pk)
            return render(request, 'record.html', {'customer_data': customer_data})
        # it is so convenient that django provides us with these features
        except ObjectDoesNotExist:
            messages.error(request, "Record does not exist!")
            return redirect('home')
    

    # else if the user is not authenticated
    # throw in an error message when they try to access the page with an id/pk extension in the url
    else:
        messages.error(request, "Login to view records!")
        return redirect('home')



# adding a delete record view
# we are not just passing in the request like in the previous case, but also passing the pk (primary key) to access and delete that specific record
def delete_record(request, pk):

    # first of all check if the user is logged in
    if request.user.is_authenticated:
        # we need to check if the record exists, if the record is already deleted and a user tries to do manual url entry for a record which doesn't exist, we need to return an error statement, or they will get a weird error message
        # for eg: if we have only 3 records of id: 1, 2 and 3 respectively and a user manually goes and types the url http://127.0.0.1:8000/delete_record/4, which does not exist, which means deletion is not possible, we need to display an error message
        try:
            # deleting is fairly simple
            # we get the record details using the GET and pk and store it into a variable
            record_to_delete = Customer.objects.get(id=pk)
            # delete the record
            record_to_delete.delete()
            # send them a flash message after the successful deletion of a record
            messages.info(request, "Record deleted!")
            return redirect('home')
        # and if the record does not exist
        # it is so convenient that django provides us with these features
        except ObjectDoesNotExist:
            messages.error(request, "Record does not exist!")
            return redirect('home')
        
    # else if the user is not logged in
    else:
        messages.error(request, "You do not have the permission!")
        return redirect('home')
    


# to add new records
def add_record(request):
    # store the AddCustomerRecordForm in a variable
    # and check if the request is POST request or else do nothing, just render the page with the form
    form = AddCustomerRecordForm(request.POST or None)
    # inorder to POST this form, we must check if the user is logged in
    if request.user.is_authenticated:
        # now check if the user is POSTing the form or just viewing
        if request.method == "POST":
            # now check if the form is valid / that is, if the user properly entered all the details in the proper format or filled the fields which has required = True
            if form.is_valid():
                form.save()
                messages.success(request, "Customer Record added successfully!")
                # then redirect to the homepage after completion
                return redirect('home')
        # if the user is not POSTing the form, that is, if the user is just visiting the page, pass in the form
        return render(request, "add_record.html", {'form':form})
    # else if the user is not authenticated
    else:
        messages.error(request, "You do not have the permission!")
        return redirect('home')



# update/edit record view
def update_record(request, pk):
    # only let them update the record if they are logged in 
    if request.user.is_authenticated:
        # now to prevent manual url entry and show another error message if the object does not exist
        try:
            # grab the current record
            record_to_update = Customer.objects.get(id=pk)
            # then, display the AddCustomerRecordFrom with already populated fields because we are going to edit it and not start from the scratch
            # for that, we pass in an argument of instance
            # the instance is the record which we obtained using the id, that is, in our case, record_to_update
            form = AddCustomerRecordForm(request.POST or None, instance=record_to_update)
            # now that we got the form, check if the method is POST
            if request.method == "POST":
                # now check if the method is valid
                if form.is_valid():
                    # if yes, save the form
                    form.save()
                    messages.success(request, "Record updated successfully!")
                    return redirect('home')
            # now if the user is not POSTing, we anyways need to show them the form
            else:
                return render(request, "update_record.html", {'form':form})
        # the part which displays error message is they try to access an object which does not exist using the update_record/
        except ObjectDoesNotExist:
            messages.error(request, "Record does not exist!")
            return redirect('home')
    # if the user is not logged in
    else:
        messages.error(request, "You do not have the permission!")
        return redirect('home')

