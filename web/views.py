from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import *
from .models import Contact
from quiz.models import Quiz, Category
from result.models import Result

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


class PublicQuizListView(ListView):
    template_name = 'web/public_quiz_list.html'
    model = Quiz
    context_object_name = 'quizes'


    def get_queryset(self):
        return super().get_queryset().filter(status = "public" , user=self.request.user)


class PrivateQuizListView(ListView):
    template_name = 'web/private_quiz_list.html'
    model = Quiz
    context_object_name = 'quizes'


    def get_queryset(self):
        return super().get_queryset().filter(status = "private" , user=self.request.user)



class QuizResultView(ListView):
    template_name = 'web/quiz_results.html'
    model = Result
    context_object_name = 'quiz_results'



    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
