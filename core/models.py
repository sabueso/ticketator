from __future__ import unicode_literals
from django.db import models
from django import forms
from django.forms import ModelForm
#Added imports
from django.contrib.auth.models import User
from datetime import datetime
from core import views_utils as util

#TO-DO imports
#from colorfield.fields import ColorField

#Generic views...
#from django.views.generic.edit import CreateView, UpdateView, DeleteView

class UserForm(ModelForm):
	date_joined = forms.DateField(widget=forms.SelectDateWidget(), initial=util.now)
	class Meta:
		model =  User
		fields = ['password','last_login','is_superuser','username','first_name','last_name','email','is_staff','is_active','date_joined']

# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length=100)
	#More fields will be needed...
	
	def __unicode__(self):
		return self.name

class Department(models.Model):
	company_rel = models.ForeignKey('Company', on_delete=models.CASCADE )
	name = models.CharField(max_length=100)
	#logo = pending....
	#color  = if needed....
	def __unicode__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User)
	department = models.ForeignKey('Department',on_delete=models.CASCADE )
	notify_email =  models.BooleanField(default=False)
	avatar =  models.FileField(upload_to='./avatar/')

  
class State(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=130)
	numvalue = models.IntegerField(null=True,blank=True,default=0)
	active = models.BooleanField(default=True)
	#color = ColorField()
	def __unicode__(self):
		return self.name

class Priority(models.Model):
	name = models.CharField(max_length=30)
	#color = ColorField()
	def __unicode__(self):
		return self.name

class Ticket(models.Model):
	date = models.DateTimeField(default=datetime.now)
	create_user = models.ForeignKey(User, related_name = "c_user", blank=True, null=True,)
	assigned_department = models.ForeignKey('Department', blank=True, null=True)
	assigned_user = models.ForeignKey(User, blank=True, null=True, related_name = "a_user")
	subject =  models.CharField(max_length=40)
	body = models.TextField(null=True,blank=True)
	assigned_state = models.ForeignKey(State)
	assigned_prio = models.ForeignKey(Priority)
	
	def __str__(self):
		return '%s' % (self.id)

class TicketForm(ModelForm):
	class Meta:
		model =  Ticket
		fields = ['date','create_user','assigned_department','assigned_user','subject','body','assigned_state','assigned_prio']
