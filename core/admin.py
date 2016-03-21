from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Company) 
admin.site.register(Department)
admin.site.register(State)
admin.site.register(Priority)


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id','user','department','notify_email','avatar')
	search_fields = ('username','department')

admin.site.register(Profile,ProfileAdmin) 

class RightsAdmin(admin.ModelAdmin):
	list_display = ('id','grp_src','dpt_dst','can_view','can_create','can_delete','can_edit','can_comment','enabled')
	#search_fields = ('subject','body')

admin.site.register(Rights,RightsAdmin)

class TicketAdmin(admin.ModelAdmin):
	list_display = ('id','date','create_user','subject','assigned_state','assigned_department','assigned_user','assigned_prio')
	search_fields = ('subject','body')

admin.site.register(Ticket,TicketAdmin)
