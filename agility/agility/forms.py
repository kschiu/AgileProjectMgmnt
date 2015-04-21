from django import forms

from django.forms.extras.widgets import SelectDateWidget
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
    user = forms.ModelChoiceField(queryset=User.objects.all(),\
            empty_label="Select User", label='Project Owner')

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()

        return cleaned_data

    class Meta:
        model = Project
        exclude = []

class TaskForm(forms.ModelForm):
    user_assigned = forms.ModelChoiceField(queryset=User.objects.all(),\
                    empty_label="Select User")
    sprint = forms.ModelChoiceField(queryset=Sprint.objects.all(),\
                    empty_label="Select Sprint")
    name = forms.CharField(max_length = 160, required=True)
    description = forms.CharField(widget = forms.Textarea)
    hours_spent = forms.IntegerField()
    difficulty = forms.IntegerField()
    github_link = forms.CharField(max_length=160, required=False)
    completed = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        hours_spent = cleaned_data.get('hours_spent')
        difficulty = cleaned_data.get('difficulty')
        if hours_spent < 0:
            raise forms.ValidationError("Hours spent must be greater than 0 hours")
        if difficulty < 0:
            raise forms.ValidationError("Difficulty must be greater than 0.")
        return cleaned_data

    class Meta:
        model = Task
        exclude = []

class SprintForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(),\
                    empty_label="Select Project")
    start_date = forms.DateField(required=True, widget=SelectDateWidget())
    end_date = forms.DateField(required=True, widget=SelectDateWidget())
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    def clean(self):
        cleaned_data = super(SprintForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        users = cleaned_data.get('users')
        if end_date < start_date:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data

    class Meta:
        model = Sprint
        exclude = []

class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length = 160,required=True,\
                label="Add Comment")

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        if len(cleaned_data.get('text')) > 160:
            raise forms.ValidationError("Comment is too long.")
        return cleaned_data

    class Meta:
        model = TaskComment
        exclude = ['user', 'task', 'date_time']

class RetrospectiveForm(forms.ModelForm):
    text = forms.CharField(widget = forms.Textarea)

    class Meta:
        model = Retrospective
        exclude = ['sprint']