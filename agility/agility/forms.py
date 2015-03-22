from django import forms

from django.contrib.auth.models import User
from models import *

class RegistrationForm(forms.Form):
    username   = forms.CharField(max_length = 20)
    email      = forms.CharField(max_length = 30)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    # Confirms that the username is not already present in the
    # User model database.
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username