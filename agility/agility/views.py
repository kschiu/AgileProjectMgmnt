import datetime
from agility.models import *
from agility.forms import *
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction

@login_required
def index(request):
	context = {}
	context['sprint'] = Sprint.objects.all()
	return render(request, 'agility/index.html', context)

@transaction.atomic
def register(request):
	context = {}

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'agility/register.html', context)

	# Creates a bound form from the request POST parameters and makes the 
	# form available in the request context dictionary.
	form = RegistrationForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'agility/register.html', context)

	# At this point, the form data is valid.  Register the user.
	new_user = User.objects.create_user(username=form.cleaned_data['username'],
										email=form.cleaned_data['email'],
										first_name=form.cleaned_data['first_name'],
										last_name=form.cleaned_data['last_name'],
										password=form.cleaned_data['password1'])
	new_user.save()
	return render(request, 'agility/index.html', context)

@transaction.atomic
def create_task(request):
	context = {}

	if request.method == 'GET':
		context['form'] = TaskForm()
		return render(request, 'agility/create_task.html' ,context)

	form = TaskForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'agility/create_task.html', context)

	new_task = Task.objects.create(name=form.cleaned_data['name'], \
					description=form.cleaned_data['description'], \
					hours_spent=form.cleaned_data['hours_spent'], \
					difficulty=form.cleaned_data['difficulty'], \
					user_assigned=form.cleaned_data['user_assigned'], \
					github_link=form.cleaned_data['github_link'])
	new_task.save()
	return render(request, 'agility/index.html', context)

@transaction.atomic
def create_project(request):
	context = {}

	if request.method == 'GET':
		context['form'] = ProjectForm()
		return render(request, 'agility/create_project.html', context)

	form = ProjectForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'agility/create_project.html', context)

	new_project = Project.objects.create(name=form.cleaned_data['name'], \
					description=form.cleaned_data['description'])
	new_project.save()
	return render(request, 'agility/index.html', context)

def create_sprint(reqest):
	context = {}

	if request.method == 'GET':
		context['form'] = SprintForm()
		return render(request, 'agility/create_sprint.html', context)

	form = SprintForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'agility/create_sprint.html', context)

	new_sprint = Sprint.objects.create(name=form.cleaned_data['name'], \
					description=form.cleaned_data['description'])
	new_sprint.save()
	return render(request, 'agility/index.html', context)


