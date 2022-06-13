from unicodedata import category
from django.db import models
from web.models import Category
# Create your models here.


class Book(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    image = models.ImageField(upload_to='books/images', blank=True)
    author = models.CharField(max_length=100)
    file = models.FileField(upload_to='books/')
    publish_date = models.DateField()

    def __str__(self):
        return self.title
