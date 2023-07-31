# using the django built-in registration/CreateUserForm to create registration forms!
# after creating forms, we can go to views.py and just call what we created
# again kudos Django!!!

# importing the user creation form from django!
from django.contrib.auth.forms import UserCreationForm

# importing user model to create users in user model type
from django.contrib.auth.models import User

# importing forms from Django
from django import forms

# creating a class which inherits UserCreationForm we just imported
class SignUpForm(UserCreationForm):

    # NOTE: Django's UserCreationForm class includes the fields username, password1 and password2 by default
    # we inherited the UserCreationForm class in the current class, SignUpForm class we are working on

    # now we create other fields which are not included in the UserCreationForm
    # we won't be giving any labels, instead we will be giving placeholders for appropriate widgets, widget example would be a text input box
    # inside each widget, say for example, text input box, we can give attributes, for example, placeholder can be an attribute
    # if we declare class as form control, it is a bootstrap property which makes it appeared as styled
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"email address"}))
    first_name = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"firstname"}))
    last_name = forms.CharField(label="", max_length=25, widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"lastname"}))

    # now we decalre a Meta class to define how the form should be processed and additional information about the form etc.
    # Meta class is a way to give metadata to the form
    # Meta class is a nested or inner class because it comes inside the SignUpForm class
    class Meta:
        # now we declare what data model the form is associated with
        model = User
        # now we declare the order in which the fields of the form should appear
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    # init is a special method or can be called a constructor/object/instance of a class
    # this constructor is called when we want to create an object of class SignUpForm
    # in our case, SignUpForm is inheriting from UserCreationForm, therefore we may not want to use every properites of the class UserCreationForm, but may want to customize it and use it! so, for this customization, we use the init method
    # self refers to that specific instance we are creating
    # it can be used to access or modify the instance
    # args is non-keyword arguments we would like to pass
    # kwargs is keyword arguments we would like to pass
    # by calling super, we allow SignUpForm to inherit and utilize properties of the UserCreationForm class, the super class from which we are deriving SignUpForm class whilst also allowing us to make the necessary customizations
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # till now, we had fields email, firstname and lastname which are default to the UserCreationForm
        # we inherited those
        # now we want to customize our class SignUpForm by adding few more fields

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. Enter a unique username. This will be used for your login. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'enter your password'
        self.fields['password1'].widget.label = ''
        self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Enter a strong password.</small></span>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 're-enter your password'
        self.fields['password2'].widget.label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Re-enter your password for confirmation.</small></span>'



