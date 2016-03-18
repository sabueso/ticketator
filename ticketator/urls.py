from django.conf.urls import include,url
from django.contrib import admin

#Import another modular views
from core import views
from core import views_users as vusers
from core import views_company as vcompanies
from core import views_tickets as vtickets


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^core/', include('core.urls')),

    #Dashboard, main screen spotted
    url(r'^$', views.index),

    #Settings & utilities
    url(r'^settings/$', views.settings, name='tickets-settings'),

    #Users   
    url(r'^settings/user/$', vusers.list_users, name='user-list'),
    url(r'^settings/user/create', vusers.manage_user, name='user-create'),
    url(r'^settings/user/(?P<user_id>\d+)?$', vusers.manage_user, name='user-edit'),

    #Companys
    url(r'^settings/companies/$', vcompanies.list_companies, name='company-list'),
    url(r'^settings/companies/create', vcompanies.manage_company, name='company-create'),
    url(r'^settings/companies/(?P<company_id>\d+)?$', vcompanies.manage_company, name='company-edit'),

    #Tickets
    url(r'^tickets/$', vtickets.list_tickets, name='tickets-list'),
    url(r'^tickets/create', vtickets.manage_ticket, name='tickets-create'),
    url(r'^tickets/(?P<ticket_id>\d+)?$', vtickets.manage_ticket, name='tickets-get'),
        #Filtering view
    url(r'^tickets/state/(?P<state_id>\d+)?$', vtickets.list_tickets, name='tickets-list-state'),

]
