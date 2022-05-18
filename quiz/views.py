from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views import View
from quiz.utils import generate_random_string
from .models import Quiz
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .forms import QuestionForm, PrivateQuizForm, PublicQuizForm, QuizPublishForm
from .owner import OwnerCreateView, OwnerUpdateView, OwnerQuestionCreateView, OwnerDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import random
from result.models import Result
from .models import Question



class AllQuizesView(ListView):
    model = Quiz
    template_name = 'quiz/quizes.html'
    context_object_name = 'quizes'
    paginate_by = 4

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
    form_class = PublicQuizForm
    def get(self, request, *args, **kwargs):
            status =  request.GET.get('status', "")
            if status == "private":
                self.form_class = PrivateQuizForm
            return super().get(request, *args, **kwargs)


    # getting the quiz object 
    def get_object(self, queryset=None):
        self.object = super().get_object()


    # success_url redirects to add_questions page
    def get_success_url(self):
        return reverse_lazy('quiz:add_question', kwargs={'pk': self.object.id, 'slug' : self.object.slug})



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
                            kwargs={'pk': self.object.id, 'slug': self.object.slug})
        

class QuizStatusView(OwnerUpdateView):
    
    model = Quiz
    form_class = QuizPublishForm
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

        ''' if user settings quiz to public and has
            less than 10 questions '''
            
        if quiz.total_questions() < 3:
            form.add_error(field = None,
                    error = "Public quizes must have atleast 10 questions")
            messages.add_message(
                self.request,
                messages.INFO,
                'add_question'
            )
            return super().form_invalid(form)
        quiz.status = 'public'
        quiz.save()
        return super().form_valid(form)



class QuizUpdateView(OwnerUpdateView):
    model = Quiz
    template_name = 'quiz/create_quiz.html'

    def get_form_class(self):
        ''' If quiz is private return PrivateQuizForm
            else Public '''
        if self.object.is_private():
            return PrivateQuizForm
        return PublicQuizForm


    def get_success_url(self):
        ''' Rediredtin user back to the quiz detail 
            page '''
        return reverse_lazy('quiz:quiz_detail', kwargs={'slug': self.object.slug, 'pk': self.object.pk})



class QuizStatusUpdateView(QuizStatusView):
    form_class = None
    fields = ('status',)


    def form_valid(self, form):
        quiz = form.save(commit=False)

        ''' if user settings quiz to public and has
            less than 10 questions '''

        if quiz.status == 'public' and quiz.total_questions() < 3:
            form.add_error(field = None,
                    error = "Public quizes must have atleast 10 questions")
            messages.add_message(
                self.request,
                messages.INFO,
                'add_question'
            )
            return super().form_invalid(form)

        elif quiz.status == 'private':
            ''' If quiz is private, generate a random password '''
            if not quiz.password:
                quiz.password = generate_random_string()
            quiz.save()
        
        else:
            ''' else quiz is valid for public or 
                is draft '''
            quiz.save()
        
        return super(QuizStatusView, self).form_valid(form)



class QuizCategoryView(ListView):
    model = Quiz
    template_name = 'quiz/quizes.html'
    context_object_name = 'quizes'


    def get_queryset(self):
        return super().get_queryset().filter(category__name=self.kwargs['category'])


class QuizSearchView(ListView):
    model = Quiz
    template_name = 'quiz/quizes.html'
    context_object_name = 'quizes'

    def get_queryset(self):
        return super().get_queryset().filter(name__icontains=self.request.GET['q'])


class Test(LoginRequiredMixin, View):
    '''
    veiw for that test page
    '''
    def get(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, slug=kwargs.get('slug'), pk=kwargs.get('pk'))
        context = {
            'test_quiz': quiz,
        }
        return render(request, 'quiz/test.html', context)


class TestData(LoginRequiredMixin, View):
    '''
    Preparing and sending Question & Answers as json for 
    Quiz.slug = slug 
    '''

    def get(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, slug=kwargs.get('slug'), pk=kwargs.get('pk'))
        questions = []
        for q in quiz.get_questions():
            questions.append({str(q): [a.text for a in q.get_answers()]})
        random.shuffle(questions)
        return JsonResponse({
            'data': questions,
            'time': quiz.time
        })


class CalcTestData(View , LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        '''
        Handling Test data from Ajax , Calculate and return results
        '''

        def handle_result(user, quiz, score):
            '''
            Create or update the results for the user 
            with this quiz 
            '''
            score = score / quiz.total_questions() * 100
            status = 'Pass' if score >= quiz.percentage else 'Fail'
            try:
                retaken = Result.objects.get(user=user, quiz=quiz)
            except Result.DoesNotExist:
                Result.objects.create(user=user, quiz=quiz,
                                      percentage=score, status=status).save()
            else:
                retaken.percentage = score
                retaken.status = status
                retaken.save()

        def prepare_result_list(data, quiz):
            '''
            Comparing User Test data with actual answers 
            & returning result_list
            '''
            result_list = []
            score = 0
            data.pop('csrfmiddlewaretoken')
            for k in data.keys():
                q = Question.objects.get(text=k, quiz = quiz)
                ans = q.get_correct_ans().text
                if data[q.text] != '':
                    if data[q.text][0] == ans:
                        score += 1
                    result_list.append(
                        {str(q): {'correct_answer': ans, 'answerd': data[q.text][0]}})
                else:
                    result_list.append({q.text: "not answered"})
            return score, result_list

        if request.is_ajax():
            quiz = Quiz.objects.get(slug=kwargs.get('slug'), pk=kwargs.get('pk'))
            print(quiz)
            data = dict(request.POST.lists())
            score, result_list = prepare_result_list(data, quiz)
            handle_result(request.user, quiz, score)

        request.session['quiz_result_list'] = result_list
        print(request.session['quiz_result_list'])

        # return redirect('quizes:results', slug=kwargs.get('slug'))
        return JsonResponse({
            'data': result_list,
            # 'next_url': reverse("quizes:results", args=(kwargs.get('slug'),))
        })
