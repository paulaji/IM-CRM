from django.db import models

# Create your models here.

# creating a customer data model
class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30)

    # there is a special method in python (used below) in which an object can be represented as a string
    # in this case, it is defined such that it returns a string to represent the customer object we created
    # the string returned is first name + last name which is the full name of the customer
    # so when we call a customer object, it returns a full name string
    def __str__(self):
        return(f"{self.first_name} {self.last_name}")
    
# to register out Customer model we just created in the admin panel, go add this in the admin.py file
