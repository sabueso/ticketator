from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import Company, Queue, State, Priority, User, Ticket
from .models import Rights, UserType

admin.site.register(Company)
admin.site.register(Queue)
admin.site.register(State)
admin.site.register(Priority)

# Custom user render outside the "Auth" module
admin.site.register(User, UserAdmin)


class RightsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'grp_src', 'queue_dst', 'can_view', 'can_create', 'can_delete',
        'can_edit', 'can_comment', 'enabled',
    )

    # search_fields = ('subject','body')

admin.site.register(Rights, RightsAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created', 'create_user', 'subject', 'assigned_state',
        'assigned_queue', 'assigned_user', 'assigned_prio')
    search_fields = ('subject', 'body')

admin.site.register(Ticket, TicketAdmin)

admin.site.register(UserType)
