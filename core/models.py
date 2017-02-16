#  -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django import forms
from django.forms import ModelForm
# Added imports
from django.contrib.auth.models import User, Group
from datetime import datetime
from core import views_utils as util
from core import rights
from django.core.exceptions import ValidationError
# Extending the Django User's model
from django.contrib.auth.models import AbstractUser

# Logger class
from core.views_logs import logger


class TimeStampedModelMixin(models.Model):
    """
    Abstract Mixin model to add timestamp
    """
    # Timestamp
    created = models.DateTimeField(u"Date created", auto_now_add=True)
    updated = models.DateTimeField(
        u"Date updated", auto_now=True, db_index=True)

    class Meta:
        abstract = True


# => UserType (OP or simple user)
class UserType(TimeStampedModelMixin):
    status = models.CharField(max_length=20)

    def __unicode__(self):
        return self.status


# Extending base User class
# https://micropyramid.com/blog/how-to-create-custom-user-model-in-django/
class User(AbstractUser):
    status_rel = models.ForeignKey(
        UserType, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.FileField(upload_to='avatar/', null=True, blank=True)
    rssfeed = models.CharField(max_length=400, null=True, blank=True)

    # If is_superuser comes with NULL value, set it to FALSE
    # (we use a personalized form and if not checked, comes as NULL)
    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.is_superuser = False
        super(User, self).save(*args, **kwargs)


# => Auth forms
class UserForm(ModelForm):
    date_joined = forms.DateField(
        widget=forms.SelectDateWidget(), input_formats=['%d/%m/%Y'],initial=util.now)
    password_first = forms.CharField(
        label='Initial Password', widget=forms.PasswordInput,
        required=False,initial='')
    password_check = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput,
        required=False,initial='')
    is_active = forms.BooleanField(required=False, initial=True)

    # is_superuser = forms.BooleanField(initial=False)
    # Pass request to query wich user is trying ot modify the object User
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        #fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff',
        #                    'is_active', 'rssfeed', ]
        exclude = ['password']

    def clean_password_check(self):
        password_raw = self.cleaned_data.get('password_first')
        password_chk = self.cleaned_data.get('password_check')
        # First password but not second
        if not password_chk and password_raw:
            raise forms.ValidationError("You must confirm your password")
        # First and second but differents
        elif password_raw != password_chk:
            raise forms.ValidationError("Your passwords do not match")
        # Not updating password
        elif self.instance.pk and password_chk == "" and password_raw == "":
            pass
        else:
            return password_chk

    # Only admin can set is_superuser to TRUE or change it to normal users
    def clean_is_superuser(self):
        cleaned_superuser = self.cleaned_data.get('is_superuser')
        # If we return a simple "HttpResponse" and the cleaned data
        # we can raise the error for debug purpouses
        # return HttpResponse(cleaned_superuser)
        user_obj = self.request.user
        # If user exists
        if self.instance.pk:
            # If modifier is not admin
            if user_obj.username != 'admin':
                # Do nothing, return original instance
                return self.instance.is_superuser
            else:
                # If admin, get the submitted value in the form and clean_it
                self.is_superuser = cleaned_superuser
                return self.is_superuser

    def clean_last_login(self):
        return self.instance.last_login


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


# => Companys
class Company(TimeStampedModelMixin):
    name = models.CharField(max_length=100)
    # More fields will be needed...
    logo = models.FileField(upload_to='logo/')

    # phone = pending
    # address = pending
    def __unicode__(self):
        return self.name


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


# => Queues (ex Departments)
class Queue(TimeStampedModelMixin):
    name = models.CharField(max_length=100)
    shortcode = models.CharField(max_length=10)
    description = models.CharField(max_length=30, null=True, blank=True)
    company_rel = models.ForeignKey(Company, on_delete=models.CASCADE)
    # logo = pending....
    # color  = if needed....

    def __unicode__(self):
        return self.name


class QueueForm(ModelForm):
    class Meta:
        model = Queue
        fields = '__all__'


# => Groups
# Group's rights
class Rights(TimeStampedModelMixin):
    enabled = models.BooleanField(default=True)
    grp_src = models.ForeignKey(
        Group, related_name="src_grp", blank=True, null=True)
    queue_dst = models.ForeignKey(
        Queue, related_name="dst_queue", blank=True, null=True)
    # Permited actions
    can_view = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_comment = models.BooleanField(default=False)

    ''''
    Check at database state if registry is created or we can create it:
    If you use the admin, to mantain the non-duplicity of the rules, we make a
    secondary check at time to save the object to the DB.
    Yes, you have 2 querys but this is the unique way to avoid errors if you
    use the admin panel to insert some righths
    '''

    def detect_rights_exists(self, grp, queue):
        return_query = {}
        obj_query = Rights.objects.filter(grp_src=grp, queue_dst=queue)
        if obj_query:
            return_query['status'] = True
            return_query['numbers'] = [i.id for i in obj_query]
            return return_query
        else:
            return_query['status'] = False
            return return_query

    # Only for new records (self.pk check)
    def save(self, *args, **kwargs):
        detect_function = self.detect_rights_exists(
            self.grp_src, self.queue_dst)
        if not self.pk and detect_function['status']:
            raise ValidationError(
                "Rule already created: model output " + str(
                    detect_function['numbers']) + "")
        else:
            super(Rights, self).save(*args, **kwargs)


class RightForm(ModelForm):
    class Meta:
        model = Rights
        fields = '__all__'

    # Check at form stage if registry is created or if we can create it
    def clean_queue_dst(self):
        detect_function = Rights.detect_rights_exists(
            Rights(), self.cleaned_data.get('grp_src'),
            self.cleaned_data.get('queue_dst'))
        # Check if no pk assigned and if detect_function['status'] is True
        if not self.instance.pk and detect_function['status']:
            raise forms.ValidationError(
                "Rule already created (" + str(detect_function['numbers'][0]) + ") src=>" +
                str(self.cleaned_data.get('grp_src')) +
                " dst=>" + str(self.cleaned_data.get('queue_dst')) + "")
        return self.cleaned_data.get('queue_dst')


# => States
class State(TimeStampedModelMixin):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150, null=True, blank=True)
    active = models.BooleanField(default=True)
    color = models.CharField(default='008ac6', max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.color.startswith("# "):
            self.color = self.color[1:]
        super(State, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class StateForm(ModelForm):
    class Meta:
        model = State
        fields = '__all__'


# => Prioritys
class Priority(TimeStampedModelMixin):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = '__all__'


# => Inventory Servers/PC
class InventoryGroup(TimeStampedModelMixin):
    name = models.CharField(max_length=100)
    company_rel = models.ForeignKey(Company, null=True)


class Inventory(TimeStampedModelMixin):
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(protocol='ipv4')
    group_rel = models.ForeignKey(InventoryGroup, null=True)


# => Tickets
class Ticket(TimeStampedModelMixin):
    create_user = models.ForeignKey(
        User, related_name="c_user", blank=True, null=True,)
    subject = models.CharField(max_length=40)
    body = models.TextField(null=True, blank=True)
    assigned_user = models.ForeignKey(
        User, blank=True, null=True, related_name="a_user")
    assigned_queue = models.ForeignKey(Queue, blank=True, null=True)
    assigned_company = models.ForeignKey(Company, blank=True, null=True)
    assigned_state = models.ForeignKey(State)
    assigned_prio = models.ForeignKey(Priority)
    assigned_inventory = models.ForeignKey(Inventory, null=True, blank=True)
    percentage = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.id)

    '''Return a empty string to avoid problems in JSON serialization'''
    def str_assigned_user_name(self):
        try:
            assigned_user_data = "" + str(self.assigned_user.first_name) + \
                " " + str(self.assigned_user.last_name) + ""
        except:
            assigned_user_data = ""
        return assigned_user_data

    def str_creator_user_name(self):
        try:
            creator_user_data = "" + str(self.create_user.first_name) + " " + \
                str(self.create_user.last_name) + ""
        except:
            creator_user_data = ""
        return creator_user_data

    def as_json(self):
        return dict(
            id=str(self.id),
            date=str(self.created.strftime('%d-%m-%Y %H:%M')),
            subject_data=str(self.subject.encode('utf8')),
            body_data=str(self.body.encode('utf8')),
            state_data=str(self.assigned_state.name),
            state_data_id=str(self.assigned_state.id),
            state_color_data=str(self.assigned_state.color),
            percentage_data=str(self.percentage),
            queue_shortcode=str(self.assigned_queue.shortcode),
            priority=str(self.assigned_prio),
            create_user=self.str_creator_user_name(),
            assigned_user_data=self.str_assigned_user_name(),)


class TicketForm(ModelForm):
    #  Pass request to a form => http://stackoverflow.com/questions/6325681/
    #  passing-a-user-request-to-forms
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(TicketForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = '__all__'
        # exclude = ['date']

    '''
    We log all importante changes in fields to be tracked
    The field_checker test if both are the same and if it found changes, call "logger" passing data
    TODO: Maybe, "if self.instance.pk is not None:" can be improved to not call
    all  times to make the check (and save N checks at save time)
    '''

    def clean_assigned_state(self):
        if self.instance.pk is not None:   # new instance only
            self.field_checker(str(self.instance.assigned_state), str(
                self.cleaned_data.get('assigned_state')))
        return self.cleaned_data.get('assigned_state')

    '''
    Check if the new queue assigned is permited...
    '''
    def clean_assigned_queue(self):
        if self.instance.pk is not None:   # new instance only
            user_object_rights = rights.get_rights_for_ticket(
                user=self.request.user,
                queue=self.cleaned_data.get('assigned_queue'), ticket_id=None)
            if not user_object_rights.can_create:
                raise forms.ValidationError(self.clean_error_cantcreate())
            else:
                self.field_checker(
                    str(self.instance.assigned_queue),
                    str(self.cleaned_data.get('assigned_queue')))
        return self.cleaned_data.get('assigned_queue')

    def clean_assigned_user(self):
        if self.instance.pk is not None:   # new instance only
            self.field_checker(self.instance.assigned_user, self.cleaned_data.get('assigned_user'))
        return self.cleaned_data.get('assigned_user')

    def clean_subject(self):
        if self.instance.pk is not None:  # new instance only
            self.field_checker(self.instance.subject, self.cleaned_data.get('subject'))
        return self.cleaned_data.get('subject')

    def clean_body(self):
        if self.instance.pk is not None:  # new instance only
            self.field_checker(self.instance.body, self.cleaned_data.get('body'))
        return self.cleaned_data.get('body')

    '''
    Error codes:
    '''

    def clean_error_cantedit(self):
        cantedit = 'You don\'t have permissions to edit this ticket'
        return cantedit

    def clean_error_cantview(self):
        cantview = 'You don\'t have permissions to view this ticket'
        return cantview

    def clean_error_cantcreate(self):
        cantcreate = 'You don\'t have permissions to create this ticket'
        return cantcreate

    def clean_error_cantsave(self):
        cantsave = 'You don\'t have permissions to save this ticket'
        return cantsave

    '''
    Functions:
    Check source=>destiny object and if it's not the same, log clean_it
    '''

    def field_checker(self, source=None, destiny=None, destiny_name=None):
        if source != destiny:
            logger(self.instance, self.request.user, "Changed", destiny)
            pass

    def clean(self):
        # Some essential vars
        user_obj = self.request.user
        cleaned_data = self.cleaned_data
        queue_obj = cleaned_data.get('assigned_queue')

        '''Check creation'''
        if not self.instance.pk:
            user_object_rights = rights.get_rights_for_ticket(
                user=user_obj, queue=queue_obj, ticket_id=None)
            if not user_object_rights.can_create:
                raise forms.ValidationError(self.clean_error_cantcreate())

        '''Check edition'''
        if self.instance.pk:
            user_object_rights = rights.get_rights_for_ticket(
                user=user_obj, queue=queue_obj, ticket_id=self.instance.id)
            if not user_object_rights.can_edit:
                raise forms.ValidationError(self.clean_error_cantedit())

        '''Force to assign company'''
        cleaned_data['assigned_company'] = queue_obj.company_rel

        #  '''Put percentage 100% when closed ticket is detected'''
        #  if cleaned_data['assigned_state'].id ==  3:
        #      self.instance.percentage = int(100)


# => Attachments
#  Method to store tickets attachments inside folders called with related ticket id
def get_attachment_upload_path(instance, filename):
    return os.path.join("ticket_files/%s" % instance.ticket_rel.id, filename)


class Attachment(TimeStampedModelMixin):

    ticket_rel = models.ForeignKey(Ticket, null=True, blank=True)
    file_name = models.FileField(
        upload_to=get_attachment_upload_path, null=True, blank=True)


class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        fields = '__all__'


# => Comments
class Comments(TimeStampedModelMixin):
    ticket_rel = models.ForeignKey(Ticket, related_name='ticket_rel_comm')
    user_rel = models.ForeignKey(User, related_name='user_rel_comm')
    comment = models.TextField(null=True, blank=True)
    private = models.BooleanField(default=False)

    '''Return this dict to avoid the NO-NESTED objects in serialize library'''

    def as_json(self, request):
        if request.user.id == self.user_rel.id or request.user.is_superuser:
            delete_comment = True
        else:
            delete_comment = False

        return dict(
            human_name="" + self.user_rel.username + "",
            avatar_data=str(self.user_rel.avatar),
            # UTF8 in order to avoid encoding problems
            comment_data=str(self.comment.encode('utf8')),
            id=str(self.id),
            delete_comment=str(delete_comment),
            date_data=str(self.created.strftime('%Y-%m-%d %H:%M')))


class Microtasks(TimeStampedModelMixin):
    ticket_rel = models.ForeignKey(Ticket, related_name='ticket_rel_mtask')
    subject = models.CharField(max_length=40)
    body = models.TextField(null=True, blank=True)
    assigned_state = models.ForeignKey(State, null=True, blank=True)
    percentage = models.IntegerField(default=0, blank=True, null=True)

    def as_json(self):
        return dict(
            # UTF8 in order to avoid encoding problems
            id=str(self.id),
            subject_data=str(self.subject.encode('utf8')),
            body_data=str(self.body.encode('utf8')),
            state_data=str(self.assigned_state),
            state_data_id=str(self.assigned_state.id),
            state_color_data=str(self.assigned_state.color),
            date_data=str(self.created.strftime('%d/%m/%y %H:%M:%S')),
            percentage_data=int(self.percentage))


class Logs(TimeStampedModelMixin):
    log_ticket = models.ForeignKey(Ticket, related_name='ticket_log')
    log_user = models.ForeignKey(User, related_name='user_log')
    log_action = models.CharField(max_length=200)
    log_destiny = models.CharField(max_length=200)
