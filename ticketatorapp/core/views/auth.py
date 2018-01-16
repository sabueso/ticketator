# Login file

from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_v(request):
    logout(request)
    return redirect("/")
