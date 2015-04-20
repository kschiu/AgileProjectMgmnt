from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
	name = models.CharField(max_length=160)
	description = models.TextField()
	user = models.ForeignKey(User)

	def __unicode__(self):
		return 'Project:'+ self.name

class Sprint(models.Model):
	start_date = models.DateField()
	end_date = models.DateField()
	retrospective = models.TextField()
	project = models.ForeignKey(Project)

	def __unicode__(self):
		return self.project.name + ' Sprint: '+ \
				(self.start_date).strftime('%m/%d') \
				+ "-" + (self.end_date).strftime('%m/%d')  

class Task(models.Model):
	name = models.CharField(max_length=160)
	description = models.TextField()
	hours_spent = models.IntegerField()
	user_assigned = models.ForeignKey(User)
	difficulty = models.IntegerField()
	github_link = models.CharField(max_length=160)
	sprint = models.ForeignKey(Sprint)
	completed = models.BooleanField(default=False)

	def __unicode__(self):
		return 'Task:'+ self.name

class TaskComment(models.Model):
	text = models.CharField(max_length=160)
	user = models.ForeignKey(User)
	task = models.ForeignKey(Task)
	date_time = models.DateTimeField()

	def __unicode__(self):
		return 'User:'+ self.user.username + '\n' + self.text