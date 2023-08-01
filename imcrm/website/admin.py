from django.contrib import admin
# import the Customer model we created in models.py file
from .models import Customer

# Register your models here.
# register the Customer model
admin.site.register(Customer)
