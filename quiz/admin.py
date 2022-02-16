from django.contrib import admin
from django.contrib.admin import TabularInline
from .models import Category, Quiz, PrivateQuiz, Question, Answer


'''
Quiz
'''

admin.site.register(Category)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'percentage']
    prepopulated_fields = {'slug': ("name", )}


@admin.register(PrivateQuiz)
class PrivateQuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'percentage']
    prepopulated_fields = {'slug': ("name", )}



'''
Questoin & Answers
'''


class AnswerInLIne(TabularInline):
    model = Answer

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'correct']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'text']
    inlines = [AnswerInLIne]