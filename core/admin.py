from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Company) 
admin.site.register(Department)
admin.site.register(State)


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id','user','department','notify_email','avatar')
	search_fields = ('username','department')

admin.site.register(Profile,ProfileAdmin) 



class TicketAdmin(admin.ModelAdmin):
	list_display = ('id','date','create_user','subject','assigned_state','assigned_department','assigned_user')
	search_fields = ('subject','body')

admin.site.register(Ticket,TicketAdmin)
