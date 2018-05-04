# -*- coding: utf-8 -*-

import django_filters
from core.models import Ticket


class TicketFilter(django_filters.FilterSet):
    subject = django_filters.CharFilter(lookup_expr='icontains')
    body = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ticket
        fields = ['subject', 'body', 'assigned_state', 'create_user', 'assigned_user']

    def __init__(self, *args, **kwargs):
        super(TicketFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.none()