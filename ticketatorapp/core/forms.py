from django import forms

from . import (
    models,
    rights,
    logs as logger,
    utils as util
)


# => Auth forms
class UserForm(forms.ModelForm):
    date_joined = forms.DateField(
        widget=forms.SelectDateWidget(),
        input_formats=['%d/%m/%Y'],
        initial=util.now
    )
    password_first = forms.CharField(
        label='Initial Password',
        widget=forms.PasswordInput,
        required=False,
        initial=''
    )
    password_check = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        required=False,
        initial=''
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True
    )

    # is_superuser = forms.BooleanField(initial=False)
    # Pass request to query wich user is trying ot modify the object User
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.User
        # fields = [
        #     'username',
        #     'first_name',
        #     'last_name',
        #     'email',
        #     'is_superuser',
        #     'is_staff',
        #     'is_active',
        #     'rssfeed',
        # ]
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


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = '__all__'


class QueueForm(forms.ModelForm):
    class Meta:
        model = models.Queue
        fields = '__all__'


class RightForm(forms.ModelForm):
    class Meta:
        model = models.Rights
        fields = '__all__'

    # Check at form stage if registry is created or if we can create it
    def clean_queue_dst(self):
        detect_function = models.Rights.detect_rights_exists(
            models.Rights(), self.cleaned_data.get('grp_src'),
            self.cleaned_data.get('queue_dst'))
        # Check if no pk assigned and if detect_function['status'] is True
        if not self.instance.pk and detect_function['status']:
            raise forms.ValidationError(
                "Rule already created (" + str(detect_function['numbers'][0]) + ") src=>" +
                str(self.cleaned_data.get('grp_src')) +
                " dst=>" + str(self.cleaned_data.get('queue_dst')) + "")
        return self.cleaned_data.get('queue_dst')


class StateForm(forms.ModelForm):
    class Meta:
        model = models.State
        fields = '__all__'


class PriorityForm(forms.ModelForm):
    class Meta:
        model = models.Priority
        fields = '__all__'


class TicketForm(forms.ModelForm):
    #  Pass request to a form => http://stackoverflow.com/questions/6325681/
    #  passing-a-user-request-to-forms
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(TicketForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Ticket
        fields = '__all__'
        # exclude = ['date']
        widgets = {
            'labels': forms.TextInput(attrs={'placeholder': 'Add labels separated by comma'})
        }

    """
    We log all importante changes in fields to be tracked
    The field_checker test if both are the same and if it found changes, call "logger" passing data
    TODO: Maybe, "if self.instance.pk is not None:" can be improved to not call
    all  times to make the check (and save N checks at save time)
    """

    def clean_assigned_state(self):
        if self.instance.pk is not None:   # new instance only
            self.field_checker(str(self.instance.assigned_state), str(
                self.cleaned_data.get('assigned_state')))
        return self.cleaned_data.get('assigned_state')

    """
    Check if the new queue assigned is permited...
    """
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

    """
    Error codes:
    """

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

    """
    Functions:
    Check source=>destiny object and if it's not the same, log clean_it
    """

    def field_checker(self, source=None, destiny=None, destiny_name=None):
        if source != destiny:
            logger.logger(self.instance, self.request.user, "Changed", destiny)
            pass

    def clean(self):
        # Some essential vars
        user_obj = self.request.user
        cleaned_data = self.cleaned_data
        queue_obj = cleaned_data.get('assigned_queue')

        """Check creation"""
        if not self.instance.pk:
            user_object_rights = rights.get_rights_for_ticket(
                user=user_obj, queue=queue_obj, ticket_id=None)
            if not user_object_rights.can_create:
                raise forms.ValidationError(self.clean_error_cantcreate())

        """Check edition"""
        if self.instance.pk:
            user_object_rights = rights.get_rights_for_ticket(
                user=user_obj, queue=queue_obj, ticket_id=self.instance.id)
            if not user_object_rights.can_edit:
                raise forms.ValidationError(self.clean_error_cantedit())

        """Force to assign company"""
        cleaned_data['assigned_company'] = queue_obj.company_rel

        #  """Put percentage 100% when closed ticket is detected"""
        #  if cleaned_data['assigned_state'].id ==  3:
        #      self.instance.percentage = int(100)


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = models.Attachment
        fields = '__all__'
