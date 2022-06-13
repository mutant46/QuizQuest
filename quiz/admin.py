from django.contrib import admin
from .models import Quiz, Comment


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'percentage']
    prepopulated_fields = {'slug': ("name", )}


@admin.register(Comment)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'text', 'user']
