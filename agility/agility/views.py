import datetime
from agility.models import *
from agility.forms import *
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.core.urlresolvers import reverse
from django.contrib.messages import error

@login_required
def index(request, msg=None):
	context = {}
	if (msg != None):
		context['msg'] = msg
	context['sprints'] = Sprint.objects.filter(users__username=request.user.username)
	context['projects'] = Project.objects.filter(user=request.user)
	context['upcoming_tasks'] = Task.objects.filter(user_assigned=request.user, completed=False).all()
	context['user'] = request.user
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

	new_user = User.objects.create_user(username=form.cleaned_data['username'],
										email=form.cleaned_data['email'],
										first_name=form.cleaned_data['first_name'],
										last_name=form.cleaned_data['last_name'],
										password=form.cleaned_data['password1'])
	new_user.save()
	context['user'] = new_user
	# Logs in the new user and redirects
	new_user = authenticate(username=form.cleaned_data['username'],
							password=form.cleaned_data['password1'])
	login(request, new_user)
	return render(request, 'agility/index.html', context)

@login_required
@transaction.atomic
def create_task(request):
	context = {}

	if request.method == 'GET':
		context['form'] = TaskForm()
		return render(request, 'agility/create_task.html' ,context)

	form = TaskForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'agility/create_task.html', context)

	new_task = Task.objects.create(name=form.cleaned_data['name'], \
					description=form.cleaned_data['description'], \
					hours_spent=form.cleaned_data['hours_spent'], \
					difficulty=form.cleaned_data['difficulty'], \
					user_assigned=form.cleaned_data['user_assigned'], \
					sprint=form.cleaned_data['sprint'],\
					github_link=form.cleaned_data['github_link'],\
					completed=form.cleaned_data['completed'])
	new_task.save()
	return redirect(reverse('view_task', kwargs={'id':new_task.id}))

@login_required
@transaction.atomic
def create_project(request):
	context = {}

	if request.method == 'GET':
		context['form'] = ProjectForm()
		return render(request, 'agility/create_project.html', context)

	form = ProjectForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'agility/create_project.html', context)

	new_project = Project.objects.create(name=form.cleaned_data['name'], \
					description=form.cleaned_data['description'],\
					user=form.cleaned_data['user'])
	new_project.save()
	return redirect(reverse('index'))

@login_required
@transaction.atomic
def create_sprint(request):
	context = {}

	if request.method == 'GET':
		context['form'] = SprintForm()
		return render(request, 'agility/create_sprint.html', context)

	form = SprintForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'agility/create_sprint.html', context)

	new_sprint = Sprint.objects.create(project=form.cleaned_data['project'], \
					start_date=form.cleaned_data['start_date'], \
					end_date=form.cleaned_data['end_date'])
	new_sprint.save()
	new_sprint.users.add(*form.cleaned_data['users'])
	return redirect(reverse('view_project', kwargs={'id':form.cleaned_data['project'].id}))

@login_required
@transaction.atomic
def create_retrospective(request):
	context = {}

	if request.method == 'GET':
		context['form'] = RetrospectiveForm()
		return render(request, 'agility/create_retrospective.html', context)

	form = RetrospectiveForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'agility/create_retrospective.html', context)

	new_retro = Retrospective.objects.create(sprint=form.cleaned_data['sprint'], \
					retrospective=form.cleaned_data['retrospective'])
	new_retro.save()
	return redirect(reverse('sprint_analytics', kwargs={'id':form.cleaned_data['sprint'].id}))


@login_required
@transaction.atomic
def edit_project(request, id):
	project = get_object_or_404(Project, id=id)
	if not project:
		raise Http404

	if request.method == 'GET':
		form = ProjectForm(instance=project)
		context = { 'form': form, 'id': id }
		return render(request, 'agility/edit_project.html', context)

	project = Project.objects.select_for_update().get(id=id)
	form = ProjectForm(request.POST, instance=project)
	if not form.is_valid():
		context = { 'form': form, 'id': id }
		return render(request, 'agility/edit_project.html', context)

	form.save()

	context = {
		'message': 'Project Updated',
		'form'   : form,
		'id'     : id,
	}
	return render(request, 'agility/edit_project.html', context)

@login_required
@transaction.atomic
def edit_task(request, id):
	task = get_object_or_404(Task, id=id)
	if not task:
		raise Http404

	if request.method == 'GET':
		form = TaskForm(instance=task)
		context = { 'form': form, 'id': id }
		return render(request, 'agility/edit_task.html', context)

	task = Task.objects.select_for_update().get(id=id)
	form = TaskForm(request.POST, instance=task)
	if not form.is_valid():
		context = { 'form': form, 'id': id }
		return render(request, 'agility/edit_task.html', context)

	form.save()

	context = {
		'message': 'Task Updated',
		'form'   : form,
		'id'     : id,
	}
	return render(request, 'agility/edit_task.html', context)

@login_required
@transaction.atomic
def edit_sprint(request, id):
	sprint = get_object_or_404(Sprint, id=id)
	if not sprint:
		raise Http404

	if request.method == 'GET':
		form = SprintForm(instance=sprint)
		context = { 'form': form, 'id': id }
		return render(request, 'agility/edit_sprint.html', context)

	sprint = Sprint.objects.select_for_update().get(id=id)
	form = SprintForm(request.POST, instance=sprint)
	if not form.is_valid():
		context = { 'form': form, 'id': id }
		return render(request, 'agility/edit_sprint.html', context)

	form.save()

	context = {
		'message': 'Sprint Updated',
		'form'   : form,
		'id'     : id,
	}
	return render(request, 'agility/edit_sprint.html', context)

@login_required
def view_project(request, id):
	context = {}
	project = get_object_or_404(Project, id=id)
	if not project:
		raise Http404
	context['project'] = project
	context['sprints'] = Sprint.objects.filter(project=project).all().order_by('-start_date')
	return render(request, 'agility/view_project.html', context)

@login_required
def view_sprint(request, id):
	context = {}
	sprint = get_object_or_404(Sprint, id=id)
	if not sprint:
		raise Http404
	context['sprint'] = sprint
	context['users'] = sprint.users.all()
	context['upcoming_tasks'] = Task.objects.filter(sprint=sprint, completed=False).all()
	context['completed_tasks'] = Task.objects.filter(sprint=sprint, completed=True).all()
	return render(request, 'agility/view_sprint.html', context)

@login_required
def view_task(request, id):
	context = {}
	context['request'] = request
	task = get_object_or_404(Task, id=id)
	if not task:
		raise Http404
	context['task'] = task
	context['comments'] = TaskComment.objects.filter(task=task).all().order_by('date_time')

	if request.method == 'GET':
		context['form'] = CommentForm()
		return render(request, 'agility/view_task.html', context)

	form = CommentForm(request.POST)
	context['form'] = form

	return render(request, 'agility/view_task.html', context)

@login_required
@transaction.atomic
def delete_project(request, id):
	project = get_object_or_404(Project, id=id)
	project.delete()
	error(request, 'Project successfully deleted!')
	return redirect(reverse('index'))

@login_required
@transaction.atomic
def delete_sprint(request, id):
	sprint = get_object_or_404(Sprint, id=id)
	sprint.delete()
	error(request, 'Sprint successfully deleted!')
	return redirect(reverse('index'))

@login_required
@transaction.atomic
def delete_task(request, id):
	task = get_object_or_404(Task, id=id)
	task.delete()
	error(request, 'Task successfully deleted!')
	return redirect(reverse('index'))

@login_required
@transaction.atomic
def add_comment(request, id):
	context = {}

	form = CommentForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return redirect(reverse('view_task', kwargs={'id': id}))

	new_comment = TaskComment.objects.create(text=form.cleaned_data['text'], \
						user=request.user, \
						task=Task.objects.get(id=id),\
						date_time=datetime.datetime.now())
					
	new_comment.save()
	return redirect(reverse('view_task', kwargs={'id': id}))

@login_required
@transaction.atomic
def delete_comment(request, id):
	context = {}
	comment = get_object_or_404(TaskComment, id=id)
	task_id = comment.task.id

	if comment.user == request.user:
		comment.delete()
		error(request, "Comment successfully deleted!")
		return redirect(reverse('view_task', kwargs={'id': task_id}))

	error(request, "Cannot delete another user's task")
	return redirect(reverse('view_task', kwargs={'id': task_id}))

@login_required
def sprint_analytics(request, id):
	context = {}
	# context['request'] = request
	sprint = get_object_or_404(Sprint, id=id)
	if not sprint:
		raise Http404

	avg_difficulty = []
	avg_hours = []

	context['tasks'] = Task.objects.filter(sprint=sprint).all()
	context['completed_tasks'] = Task.objects.filter(sprint=sprint, completed=True).all()
	context['incomplete_tasks'] = Task.objects.filter(sprint=sprint, completed=False).all()
	context['user_tasks'] = Task.objects.filter(sprint=sprint, user_assigned=request.user)

	#GET ALL THE HOURS AND DIFFICULTIES OF TASKS
	for task in context['tasks']:
		avg_difficulty.append(task.difficulty)
		avg_hours.append(task.hours_spent)

	context['avg_difficulty'] = sum(avg_difficulty) / float(len(avg_difficulty))
	context['avg_hours'] = sum(avg_hours) / float(len(avg_hours))
	context['total_hours'] = sum(avg_hours)
	context['num_total_tasks'] = Task.objects.filter(sprint=sprint).count()
	context['num_comp_tasks'] = ((Task.objects.filter(sprint=sprint, completed=True).count()) / float(context['num_total_tasks'])) * 100
	context['num_incomp_tasks'] = ((Task.objects.filter(sprint=sprint, completed=False).count()) / float(context['num_total_tasks'])) * 100
	context['num_user_tasks'] = ((Task.objects.filter(sprint=sprint, user_assigned=request.user).count()) / float(context['num_total_tasks'])) * 100
	
	return render(request, 'agility/sprint_analytics.html', context)