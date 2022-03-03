from ast import Param
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views import View
from .models import Quiz
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import QuestionForm
from .owner import OwnerCreateView, OwnerUpdateView, OwnerQuestionCreateView, OwnerDetailView
from .utils import generate_random_string



class AllQuizesView(ListView):
    model = Quiz
    template_name = 'quiz/quizes.html'
    context_object_name = 'quizes'

    '''
    Fetching only public quizes
    '''
    def get_queryset(self):
        return self.model.public.all()


class CreateQuizView(OwnerCreateView):
    '''
    Quiz Create View that redirect towards add questions page
    '''

    template_name = 'quiz/create_quiz.html'
    model = Quiz
    fields = ('name', 'category', 'image', 'desc', 'time', 'percentage', 'difficulity')


    # getting the quiz object 
    def get_object(self, queryset=None):
        self.object = super().get_object()


    # success_url redirects to add_questions page
    def get_success_url(self):
        return reverse_lazy('quiz:add_question', kwargs={'pk': self.object.id})



class QuizDetailView(OwnerDetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'




class QuizQuestionCreateView(OwnerQuestionCreateView):

    model = Quiz
    template_name = 'quiz/add_question.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        if self.object.user != request.user:
            return redirect('quiz:quizes')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Quiz.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class= None):
        '''
        Use My Nested InlineFormset nested of the default form for
        quiz model
        '''
        return QuestionForm(**self.get_form_kwargs(),
                            instance=self.object)

    def form_valid(self, form):
        '''
        If form is valid, save the form and redirect to the parent
        quiz detail page
        '''
        form.save()
        messages.success(self.request, 'Questions added successfully')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('quiz:add_question',
                            kwargs={'pk': self.object.id})
        

class QuizStatusView(OwnerUpdateView):
    
    model = Quiz
    fields = ('status',)
    template_name = 'quiz/quiz_status.html'

    #redirecting to quiz detail page
    def get_success_url(self):

        ''' adding passwoerd to the url if the quiz is private '''
        url = reverse_lazy('quiz:quiz_detail',
                            kwargs= {
                                'slug' : self.object.slug,
                                'pk' : self.object.pk})
        if self.object.is_private():
            url += '?pwd=' + self.object.password
        
        return url

    # only quiz with more the 10 questions can be published
    def form_valid(self, form):
        quiz = form.save(commit=False)

        ''' if quiz is published and has less than 10 questions
            and setting up password if the quiz is private '''
            
        if quiz.total_questions() < 3:
            form.add_error(field = None,
                    error = "Public quizes must have atleast 10 questions")
            messages.add_message(
                self.request,
                messages.INFO,
                'add_question'
            )
            return super().form_invalid(form)

        elif form.has_changed() and quiz.is_private():
            quiz.password = generate_random_string()
        return super().form_valid(form)



