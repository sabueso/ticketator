from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


# Auth
from django.contrib.auth import views as auth_views

import core.signals

# Import some modular views
from core import views
from core import views_users as vusers
from core import views_company as vcompanies
from core import views_queues as vqueues
from core import views_tickets as vtickets
from core import views_group as vgroup
from core import views_right as vright
from core import views_auth as vauth
from core import views_states as vstates
from core import views_search as vsearch
from core import views_priority as vpriorities


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^core/', include('core.urls')),

    # Dashboard, main screen spotted
    url(r'^$', views.index),

    # Settings & utilities
    url(r'^settings/$', views.settings, name='tickets-settings'),

    # Auth
    url(r'^login$', auth_views.login, {'template_name': 'auth/login.html'}, name='login'),

    url(r'^logoff', vauth.logout_v, name='logout'),

    # Users
    url(r'^settings/user/$', vusers.list_users, name='user-list'),
    url(r'^settings/user/create', vusers.manage_user, name='user-create'),
    url(r'^settings/user/(?P<user_id>\d+)?$', vusers.manage_user, name='user-edit'),
    url(r'^settings/user/delete/(?P<user_id>\d+)?$', vusers.delete_user, name='user-delete'),

    # Groups
    url(r'^settings/groups/$', vgroup.list_groups, name='group-list'),
    url(r'^settings/groups/create', vgroup.manage_group, name='group-create'),
    url(r'^settings/groups/(?P<group_id>\d+)?$', vgroup.manage_group, name='group-edit'),

    # Rights
    url(r'^settings/rights/$', vright.list_rights, name='right-list'),
    url(r'^settings/rights/create', vright.manage_right, name='right-create'),
    url(r'^settings/rights/(?P<right_id>\d+)?$', vright.manage_right, name='right-edit'),

    # States
    url(r'^settings/state/$', vstates.list_state, name='state-list'),
    url(r'^settings/state/create', vstates.manage_state, name='state-create'),
    url(r'^settings/state/delete/(?P<state_id>\d+)?$', vstates.delete_state, name='state-delete'),
    url(r'^settings/state/(?P<state_id>\d+)?$', vstates.manage_state, name='state-edit'),

    # Companys
    url(r'^settings/companies/$', vcompanies.list_companies, name='company-list'),
    url(r'^settings/companies/create', vcompanies.manage_company, name='company-create'),
    url(r'^settings/companies/(?P<company_id>\d+)?$',
        vcompanies.manage_company, name='company-edit'),

    # Priorities
    url(r'^settings/priorities/$', vpriorities.list_priorities, name='priority-list'),
    url(r'^settings/priorities/create', vpriorities.manage_priority, name='priority-create'),
    url(r'^settings/priorities/(?P<priority_id>\d+)?$',
        vpriorities.manage_priority, name='priority-edit'),

    # queues
    url(r'^settings/queue/$', vqueues.list_queues, name='queues-list'),
    url(r'^settings/queue/create', vqueues.manage_queue, name='queues-create'),
    url(r'^settings/queue/delete/(?P<queue_id>\d+)?$', vqueues.delete_queue, name='queue-delete'),
    url(r'^settings/queue/(?P<queue_id>\d+)?$', vqueues.manage_queue, name='queues-edit'),

    # Tickets
    url(r'^tickets/(?P<assigned_state>\d+)?$$', vtickets.list_tickets, name='tickets-list'),
    url(r'^tickets/create-new-dev', vtickets.manage_ticket_dev, name='tickets-create-dev'),
    # url(r'^tickets/create-new', vtickets.manage_ticket, name='tickets-create'),
    url(r'^tickets/edit-dev/(?P<ticket_id>\d+)?$',
        vtickets.manage_ticket_dev, name='tickets-edit-dev'),
    url(r'^tickets/view/(?P<ticket_id>\d+)?$',
        vtickets.view_ticket, name='view_ticket'),
    # url(r'^tickets/edit/(?P<ticket_id>\d+)?$', vtickets.manage_ticket, name='tickets-edit'),
    # url(r'^tickets/view/(?P<ticket_id>\d+)?$', vtickets.view_ticket, name='tickets-view'),
    url(r'^tickets/delete/(?P<ticket_id>\d+)?$', vtickets.delete_ticket, name='tickets-delete'),
    # Listing tickets
    # url(r'^tickets/list/?/?$', vtickets.list_tickets, name='tickets-list-state'),
    # Filtering states
    url(r'^tickets/state/(?P<state_id>\d+)?$', vtickets.list_tickets, name='tickets-list-state'),
    # Filtering queues
    url(r'^tickets/queue/(?P<queue_id>\d+)?$', vtickets.list_tickets, name='tickets-list-state'),
    # Comments post
    url(r'^tickets/add_comment/(?P<ticket_id>\d+)$',
        vtickets.add_comment_jx, name='tickets-add-comment'),
    url(r'^tickets/get_comments/(?P<ticket_id>\d+)$',
        vtickets.get_comments_jx, name='tickets-get-comments'),
    url(r'^tickets/del_comment/$', vtickets.del_comment_jx, name='tickets-del-comment'),
    # Post percentage
    url(r'^tickets/set_percentage/(?P<ticket_id>\d+)/range/$',
        vtickets.set_percentage_jx, name='tickets-set-percentage'),
    url(r'^tickets/state/(?P<state_id>\d+)?$', vtickets.list_tickets, name='tickets-list-state'),
    url(r'^tickets/get_percentage/(?P<ticket_id>\d+)$',
        vtickets.get_percentage_jx, name='tickets-get-percentage'),

    # Microtask post
    url(r'^tickets/add_microtask/(?P<ticket_id>\d+)$',
        vtickets.add_microtask_jx, name='tickets-add-microtask'),
    url(r'^tickets/get_microtask/(?P<mk_id>\d+)$',
        vtickets.get_microtask_jx, name='tickets-get-microtask'),
    url(r'^tickets/get_microtasks/(?P<ticket_id>\d+)$',
        vtickets.get_microtasks_jx, name='tickets-get-microtasks'),
    url(r'^tickets/del_microtask/$', vtickets.del_microtask_jx, name='tickets-del-microtasks'),

    # Search
    url(r'^search/$', vsearch.main_search, name='search'),

]

#  Add url to serve media elements on development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
