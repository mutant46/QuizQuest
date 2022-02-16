from django.forms import modelformset_factory, formset_factory
from django import forms
from .models import Question


class QuestionAnswerForm(forms.Form):
    question = forms.CharField(max_length=200)
    answer1 = forms.CharField(max_length=20)
    answer2 = forms.CharField(max_length=20)
    answer3 = forms.CharField(max_length=20)


NewForm = formset_factory(QuestionAnswerForm, extra= 1)


QuestionForm = modelformset_factory(Question, fields = ('text', ), extra=2)
