from __future__ import unicode_literals
from django.db import models
from django import forms
from django.forms import ModelForm
#Added imports
from django.contrib.auth.models import User, Group
from datetime import datetime
from core import views_utils as util
from core import rights
from django.core.exceptions import ValidationError

#=> Auth forms
class UserForm(ModelForm):
	date_joined = forms.DateField(widget=forms.SelectDateWidget(), initial=util.now)
	password = forms.CharField(widget=forms.PasswordInput, required=False)
	password_check = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)
	is_active = forms.BooleanField(required=False, initial=True)

	class Meta:
		model = User
		fields = '__all__'

	def clean_password_check(self):
		password_raw = self.cleaned_data.get('password')
		password_chk = self.cleaned_data.get('password_check')
		#First password but not second
		if not password_chk and password_raw:
			raise forms.ValidationError("You must confirm your password")
		#First and second but differents
		if password_raw != password_chk:
			raise forms.ValidationError("Your passwords do not match")
		#Not updating password
		if self.instance.pk and not password_chk and password_raw:
			pass
		return password_chk

class GroupForm(ModelForm):
	class Meta:
		model = Group
		fields = '__all__'

#=> Companys
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

#=> Queues (ex Departments)
class Queue(models.Model):
	name = models.CharField(max_length=100)
	company_rel = models.ForeignKey('Company', on_delete=models.CASCADE )
	#logo = pending....
	#color  = if needed....
	def __unicode__(self):
		return self.name

class QueueForm(ModelForm):
	class Meta:
		model =  Queue
		fields = '__all__'

#=> Profile
#Review if it's really usefull
class Profile(models.Model):
	user = models.OneToOneField(User)
	queue = models.ForeignKey('Queue',on_delete=models.CASCADE )
	notify_email =  models.BooleanField(default=False)
	avatar =  models.FileField(upload_to='./avatar/')

#=> Groups
#Group's rights
class Rights(models.Model):
	enabled=models.BooleanField(default=True)
	grp_src=models.ForeignKey(Group, related_name = "src_grp", blank=True, null=True)
	queue_dst=models.ForeignKey('Queue', related_name = "dst_queue", blank=True, null=True)
	#Permited actions
	can_view=models.BooleanField(default=False)
	can_create=models.BooleanField(default=False)
	can_delete=models.BooleanField(default=False)
	can_edit=models.BooleanField(default=False)
	can_comment=models.BooleanField(default=False)

	#Check at database state if registry is created or we can create it:
	#If you use the admin, to mantain the non-duplicity of the rules, we make a secondary 
	#check at time to save the object to the DB.
	#Yes, you have 2 querys but this is the unique way to avoid errors if you use the admin
	#panel to insert some righths

	def detect_rights_exists(self, grp, queue):
		return_query={}
		obj_query = Rights.objects.filter(grp_src=grp, queue_dst=queue)
		if obj_query:
			return_query['status'] = True
			return_query['numbers'] = [i.id for i in obj_query]
			return return_query
		else:
			return_query['status'] = False
			return return_query
	
	#Only for new records (self.pk check)		
	def save(self, *args, **kwargs):
		detect_function = self.detect_rights_exists(self.grp_src, self.queue_dst)
		if not self.pk and detect_function['status'] == True:
			raise ValidationError("Rule already created: model output "+str(detect_function['numbers'])+"") 
		else:
			super( Rights, self ).save( *args, **kwargs )


class RightForm(ModelForm):
	class Meta:
		model =  Rights
		fields = '__all__'

	#Check at form stage if registry is created or if we can create it 
	def clean_queue_dst(self):
		detect_function = Rights.detect_rights_exists(Rights(), self.cleaned_data.get('grp_src'), self.cleaned_data.get('queue_dst'))
		#Check if no pk assigned and if detect_function['status'] is True
	 	if not self.instance.pk and detect_function['status']:
	 		raise forms.ValidationError("Rule already created ("+str(detect_function['numbers'][0])+") src=>"+str(self.cleaned_data.get('grp_src'))+" dst=>"+str(self.cleaned_data.get('queue_dst'))+"")
	 	return self.cleaned_data.get('queue_dst')	

#=> States  
class State(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=130)
	numvalue = models.IntegerField(null=True,blank=True,default=0)
	active = models.BooleanField(default=True)
	#color = ColorField()
	def __unicode__(self):
		return self.name

class StateForm(ModelForm):
	class Meta:
		model =  State
		fields = '__all__'		

#=> Prioritys
class Priority(models.Model):
	name = models.CharField(max_length=30)
	#color = ColorField()
	def __unicode__(self):
		return self.name

#=> Tickets
class Ticket(models.Model):
	date = models.DateTimeField(default=datetime.now)
	create_user = models.ForeignKey(User, related_name = "c_user", blank=True, null=True,)
	assigned_user = models.ForeignKey(User, blank=True, null=True, related_name = "a_user")
	assigned_queue = models.ForeignKey('Queue', blank=True, null=True)
	assigned_company = models.ForeignKey('Company', blank=True, null=True)
	subject =  models.CharField(max_length=40)
	body = models.TextField(null=True,blank=True)
	assigned_state = models.ForeignKey(State)
	assigned_prio = models.ForeignKey(Priority)

	def __str__(self):
		return '%s' % (self.id)

class TicketForm(ModelForm):
	# Pass request to a form => http://stackoverflow.com/questions/6325681/passing-a-user-request-to-forms
	def __init__(self, *args, **kwargs):	
		self.request = kwargs.pop("request")
		super(TicketForm, self).__init__(*args, **kwargs)

	class Meta:
		model =  Ticket
		fields = '__all__'

	#Assign the company to the ticket instance
	def clean_assigned_company(self):
		cleared_queue = self.cleaned_data.get('assigned_queue').id
		queue_obj = Queue.objects.get(id=cleared_queue)
		company_to_assign = Company.objects.get(id=queue_obj.company_rel_id)
		return company_to_assign
	
	def clean(self):
		#Some messages
		ruledefined='Some rule defined'
		cantsave='You don\'t have permissions to edit this ticket' 
		cantview='You don\'t have permissions to view this ticket'
		cantcreate='You don\'t have permissions to create this ticket'
		#Some essential vars
		user_obj=self.request.user
		queue_obj=self.cleaned_data.get('assigned_queue')
		#Check if some right is defined for this action
		user_object_rights=rights.get_rights_for_ticket(user=user_obj, queue=queue_obj, ticket_id=None)
		#New ticket
		if not self.instance.id:
			if user_object_rights.can_create != True:
				raise forms.ValidationError(cantcreate)
		#Existing ticket
		else:
			if user_object_rights.can_edit != True:
				raise forms.ValidationError(cantsave)

class Attachment(models.Model):
	ticket_rel = models.ForeignKey(Ticket,null=True, blank=True)
	file_name = models.FileField(upload_to='ticket_files/',null=True, blank=True)


class AttachmentForm(ModelForm):
	class Meta:
		model =  Attachment
		fields = '__all__'
