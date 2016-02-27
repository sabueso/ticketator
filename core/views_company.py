#Company views: list, create, delete

from django.shortcuts import render
from django.http import HttpResponse


def list_companys(request):
	return HttpResponse("Listing Comnpanys...")