"""ticketator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin

#Import another modular views
from core import views
from core import views_users as vusers
from core import views_company as vcompanys
from core import views_tickets as vtickets


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^core/', include('core.urls')),

    #Dashboard, main screen spotted
    url(r'^$', views.index),

    #Users
    url(r'^core/users/list/', vusers.list_users, name='user-list'),

    #Companys
    url(r'^core/companys/list/', vcompanys.list_companys, name='company-list'),

    #Tickets
    url(r'^tickets/', vtickets.list_tickets, name='tickets-list'),
]
