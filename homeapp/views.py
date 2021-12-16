from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth import authenticate, login, logout
from .models import UserProfile

def user_login(request):
   user = UserProfile.objects.all()
   return render(request, 'homeapp/login.html')
