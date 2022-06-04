from django.contrib import admin
from django.contrib.admin import TabularInline
from .models import Question, Answer


class AnswerInLIne(TabularInline):
    model = Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'correct']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'text']
    inlines = [AnswerInLIne]
