from django.shortcuts import render

# creating homepage view
def home(request):
    return render(request, 'home.html', {})  # {} at the end specifies we are not passing any data into the home.html
