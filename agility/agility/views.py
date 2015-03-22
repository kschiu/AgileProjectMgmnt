from agility.models import *

def index(request):
	context = {}
	context['sprint'] = Sprint.objects.all()
	return render(request, 'agility/index.html', context)

def register(request):

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

