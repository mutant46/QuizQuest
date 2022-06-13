from django.shortcuts import render
from django.views.generic import ListView
from .models import Book
# Create your views here.


class BookListView(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 4
