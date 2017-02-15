from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import checkUserExists

INV_REQ = "invalidRequest5987@@!#inv_req"

def checkUsernameExists(request):
    if request.method == 'POST':
        username = request.POST['username']
        if username:
            if checkUserExists(username):
                return HttpResponse("NO")
            return HttpResponse("YES")
    return HttpResponse(INV_REQ)