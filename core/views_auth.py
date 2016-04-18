#Login file

from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404

def logout_v(request):
	logout(request)
	return redirect("/")

