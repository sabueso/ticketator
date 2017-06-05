from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Ticket
from django.contrib.auth import get_user_model
from core import rights
from util import query_view

from rssfetcher import DashboardFeed

# User model alias due
User = get_user_model()

# Create your views here.


@login_required
def index(request):
    '''
    Ticket listing
    '''
    queues = rights.get_queues_as_q_for_ticket_model(request.user)
    # We pass always granted_queues as a roundup to query_view requirements
    open_tickets = query_view(
        Ticket, request.GET, granted_queues=queues, assigned_state=1, limit=5)
    pending_tickets = query_view(
        Ticket, request.GET, granted_queues=queues, assigned_state=2, limit=5)
    my_tickets = query_view(
        Ticket, request.GET, granted_queues=queues, assigned_user_id=request.user.id, limit=5)

    rssdata = User.objects.get(id=request.user.id).rssfeed
    if rssdata:
        rssfeed = DashboardFeed(rssdata).fetcher()
    return render(request, 'dashboard/dashboard.html', locals())


@login_required
def settings(request):
    return render(request, 'settings/settings.html')


def default_404(request):
    response = render(request, '404/404.html', {},)
    response.status_code = 404
    return response
