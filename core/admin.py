from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Company) 
admin.site.register(Department)
admin.site.register(Profile) 
admin.site.register(State)
admin.site.register(Ticket)
