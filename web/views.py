from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import *
from .models import Contact, Category
from quiz.models import Quiz
from result.models import Result
from book.models import Book


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
        return super().get_queryset().filter(status="public", user=self.request.user)


class PrivateQuizListView(ListView):
    template_name = 'web/private_quiz_list.html'
    model = Quiz
    context_object_name = 'quizes'

    def get_queryset(self):
        return super().get_queryset().filter(status="private", user=self.request.user)


class DraftQuizListView(ListView):
    template_name = 'web/draft_list.html'
    model = Quiz
    context_object_name = 'quizes'

    def get_queryset(self):
        return super().get_queryset().filter(status="draft", user=self.request.user)


class QuizResultView(ListView):
    template_name = 'web/quiz_results.html'
    model = Result
    context_object_name = 'quiz_results'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class PrivateQuizSubmissionsView(ListView):
    template_name = 'web/private_submit.html'
    model = Result
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = Quiz.objects.get(id=self.kwargs['id'])
        return context

    def get_queryset(self):
        return super().get_queryset().filter(quiz_id=self.kwargs['id'])


class SearchView(ListView):
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        type = request.GET.get('type')
        if type == 'quiz':
            context = {
                'quizes': Quiz.objects.filter(name__icontains=query)
            }
            return render(request, 'web/filter_quizes.html', context)
        else:
            context = {
                'books': Book.objects.filter(title__icontains=query)
            }
            return render(request, "web/filter_books.html", context)
