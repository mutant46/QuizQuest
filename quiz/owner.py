from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.text import slugify
from django.shortcuts import redirect
from django.http import HttpResponse


''' 
Ownser Views =  Views can only be accessed by the owner of the quiz

'''

class OwnerDetailView(LoginRequiredMixin, DetailView):

    ''' if status is private and user is not owner then
         redirect to home page '''

    def get(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.status == 'private':
            return HttpResponse('<h1>This quiz is private page</h1>')
        return super().get(request, *args, **kwargs)
        



class OwnerCreateView(LoginRequiredMixin, CreateView):

    '''
    adding the user to the quiz object
    '''
    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.slug = slugify(quiz.name)
        quiz.user = self.request.user
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



