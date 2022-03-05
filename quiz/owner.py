from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.text import slugify
from django.shortcuts import redirect
from .utils import generate_random_string
from django.views import View
from django.urls import reverse_lazy

''' 
Ownser Views =  Views can only be accessed by the owner of the quiz

'''

class OwnerDetailView(DetailView):

    ''' if status is private assert the password
        specified as the url parameter '''

    def check_password(self, pwd):
        return self.get_object().password == pwd

    def get(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.is_private():
            pwd = self.check_password(request.GET.get('pwd', ''))
            if not pwd:
                return redirect('quiz:quizes')
        return super().get(request, *args, **kwargs)
        


class OwnerCreateView(LoginRequiredMixin, CreateView):

    '''
    adding the user to the quiz object
    '''
    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.slug = slugify(quiz.name)
        quiz.user = self.request.user
        if self.request.GET.get('status') == 'private':
            quiz.status = 'private'
            quiz.password = generate_random_string()
        quiz.save()
        return super().form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):

    '''
    filtering the queryset to only show the quiz 
    that belongs to the user 
    '''

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OwnerQuestionCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):

    '''
    filtering the queryset so only owner of the quiz
    can add the questions
    '''

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)



