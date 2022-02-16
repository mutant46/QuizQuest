from django.shortcuts import render, redirect
from django.views.generic import *
from django.views import View
from .models import Quiz
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import QuestionForm, NewForm




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
    success_url = reverse_lazy('quizes')
    model = Quiz
    fields = ('name', 'category', 'image', 'desc', 'time', 'percentage', 'difficulity')


    '''
    setting up the user field for the quiz
    '''
    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.user = self.request.user
        quiz.save()
        return super().form_valid(form)


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'


class AddQuestionView(LoginRequiredMixin, View):
    ''' 
    Firstly add question formset and then forward to second step
    <str:username>/<slug:slug>/add-questions/
    '''
    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(slug=kwargs.get('slug'))
        if request.user == quiz.user:
            form = NewForm()
            context = {
                'form' : form
                }
            return render(request, 'quiz/add_question.html', context)
        return redirect('home')

    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        quiz = Quiz.objects.get(slug=kwargs.get('slug'))
        if form.is_valid():
            instances = form.save(commit=False)
            for instance in instances:
                instance.quiz = quiz
                instance.save()
            return redirect(reverse_lazy('add_question', kwargs={'username' : quiz.user, 'slug' : quiz.slug}))

        return render(request, 'quiz/add_question.html', {'form' : form})
