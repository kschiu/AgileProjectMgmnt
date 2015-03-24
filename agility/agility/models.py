from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
	name = models.CharField(max_length=160)
	description = models.TextField()

	def __unicode__(self):
		return 'Project:'+ self.name

class Sprint(models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	retrospective = models.TextField()
	project = models.ForeignKey(Project)

	def __unicode__(self):
		return 'Sprint:'+ (self.start_date).strftime('%m/%d/%Y') \
					+ " " + (self.end_date).strftime('%m/%d/%Y')  

class Task(models.Model):
	name = models.CharField(max_length=160)
	description = models.TextField()
	hours_spent = models.IntegerField()
	user_assigned = models.ForeignKey(User)
	difficulty = models.IntegerField()
	github_link = models.CharField(max_length=160)
	sprint = models.ForeignKey(Sprint)
	#completed = models.BooleanField(default=False)

	def __unicode__(self):
		return 'Task:'+ self.name

