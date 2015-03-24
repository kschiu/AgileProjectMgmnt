from django import forms

from django.contrib.auth.models import User
from models import *

class RegistrationForm(forms.Form):
    username   = forms.CharField(max_length = 20)
    email      = forms.CharField(max_length = 30)
    first_name = forms.CharField(max_length = 20)
    last_name  = forms.CharField(max_length = 20)
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

class ProjectForm(forms.ModelForm):
    name = forms.CharField(max_length = 160,required=True)
    description = forms.CharField(widget = forms.Textarea)

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()

        return cleaned_data

    class Meta:
        model = Project

class TaskForm(forms.ModelForm):
    user_assigned = forms.ModelChoiceField(queryset=User.objects.all(),\
                    empty_label="Select User")
    sprint = forms.ModelChoiceField(queryset=Sprint.objects.all(),\
                    empty_label="Select Sprint")
    name = forms.CharField(max_length = 160, required=True)
    description = forms.CharField(widget = forms.Textarea)
    hours_spent = forms.IntegerField()
    difficulty = forms.IntegerField()
    github_link = forms.CharField(max_length=160)

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        if hours_spent < 0:
            raise forms.ValidationError("Hours spent must be greater than 0 hours")
        if difficulty < 0:
            raise forms.ValidationError("Difficulty must be greater than 0.")
        return cleaned_data

class SprintForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(),\
                    empty_label="Select Project")
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
    retrospective = forms.CharField(widget = forms.Textarea)

    def clean(self):
        cleaned_data = super(SprintForm, self).clean()
        if end_date < start_date:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data
