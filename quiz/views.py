from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.views import View
from .models import Quiz
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from .forms import QuestionForm




class AllQuizesView(ListView):
    model = Quiz
    template_name = 'quiz/quizes.html'
    context_object_name = 'quizes'

    '''
    Fetching only active quizes
    '''
    def get_queryset(self):
        return super().get_queryset().filter(status='active')


class CreateQuizView(LoginRequiredMixin, CreateView):
    '''
    Quiz Create View that redirect towards add questions page
    '''

    template_name = 'quiz/create_quiz.html'
    model = Quiz
    fields = ('name', 'category', 'image', 'desc', 'time', 'percentage', 'difficulity')


    # getting the quiz object 
    def get_object(self, queryset=None):
        self.object = super().get_object()

    # setting up the user field for the quiz
    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.user = self.request.user
        quiz.save()
        return super().form_valid(form)

    # success_url redirects to add_questions page
    def get_success_url(self):
        return reverse_lazy('add_question', kwargs={'pk': self.object.id, 'username' : self.object.user.username})



class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'




class QuizQuestionCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):

    model = Quiz
    template_name = 'quiz/add_question.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class= None):
        '''
        Use My Nested InlineFormset nested of the default form for
        quiz model
        '''
        return QuestionForm(**self.get_form_kwargs(),instance=self.object)

    def form_valid(self, form):
        '''
        If form is valid, save the form and redirect to the parent
        quiz detail page
        '''
        form.save()
        messages.success(self.request, 'Questions added successfully')
        return redirect(self.get_success_url())


    def get_success_url(self):
        return reverse_lazy('add_question', kwargs={'pk': self.object.id, 'username': self.object.user.username})
        