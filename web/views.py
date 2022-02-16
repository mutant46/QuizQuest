from django.http import HttpResponse
from django.shortcuts import render
from django.views import View 
from django.views.generic import *

# Create your views here.


def home(request):
    return render(request, 'web/home.html')

def policy(request):
    return HttpResponse("Policy")
