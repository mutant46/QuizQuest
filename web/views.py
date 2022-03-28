from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import *
from .models import Contact
from quiz.models import Category

# Create your views here.


def home(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'web/home.html', context)


class ContactView(CreateView):
    template_name = 'web/contact.html'
    model = Contact
    fields = ['name', 'email', 'message']
    success_url = '/'


class DashboardView(TemplateView):
    template_name = 'web/dashboard.html'
    
