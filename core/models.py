from __future__ import unicode_literals
from django.db import models
from django import forms
from django.forms import ModelForm
#Added imports
from django.contrib.auth.models import User
from datetime import datetime
from core import views_utils as util

#Generic views...
#from django.views.generic.edit import CreateView, UpdateView, DeleteView

class UserForm(ModelForm):
	date_joined = forms.DateField(widget=forms.SelectDateWidget(), initial=util.now)
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)
	is_active = forms.BooleanField(required=False, initial=True)
	class Meta:
		model =  User
		fields = '__all__'

	def clean_password_check(self):
		password_raw = self.cleaned_data.get('password')
		password_chk = self.cleaned_data.get('password_check')
		if not password_chk:
			raise forms.ValidationError("You must confirm your password")
		if password_raw != password_chk:
			raise forms.ValidationError("Your passwords do not match")
		return password_chk

# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length=100)
	#More fields will be needed...
	#logo = pending
	#phone = pending
	#address = pending
	def __unicode__(self):
		return self.name

class CompanyForm(ModelForm):
	class Meta:
		model =  Company
		fields = '__all__'

class Department(models.Model):
	name = models.CharField(max_length=100)
	company_rel = models.ForeignKey('Company', on_delete=models.CASCADE )
	#logo = pending....
	#color  = if needed....
	def __unicode__(self):
		return self.name

class DepartmentForm(ModelForm):
	class Meta:
		model =  Department
		fields = '__all__'

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
	assigned_user = models.ForeignKey(User, blank=True, null=True, related_name = "a_user")
	assigned_department = models.ForeignKey('Department', blank=True, null=True)
	assigned_company = models.ForeignKey('Company', blank=True, null=True)
	subject =  models.CharField(max_length=40)
	body = models.TextField(null=True,blank=True)
	assigned_state = models.ForeignKey(State)
	assigned_prio = models.ForeignKey(Priority)
	
	def __str__(self):
		return '%s' % (self.id)

class TicketForm(ModelForm):
	class Meta:
		model =  Ticket
		fields = '__all__'
