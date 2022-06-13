from django import forms
from .models import Quiz, Comment


''' ---------------------------------- Quiz Create View Form---------------------------------- '''


class PublicQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'category', 'image', 'desc',
                  'time', 'percentage', 'difficulity']


class PrivateQuizForm(forms.ModelForm):
    valid_thru = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Quiz
        fields = ['name', 'category', 'image', 'desc',
                  'time', 'percentage', 'difficulity', 'valid_thru']


''' ---------------------------------- Quiz Status UpdateView Form---------------------------------- '''


class QuizPublishForm(forms.ModelForm):
    status = forms.CharField(
        widget=forms.HiddenInput(attrs={'value': 'public'}))

    class Meta:
        model = Quiz
        fields = ['status']


class CommentForm(forms.Form):
    text = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={
            'rows': 5,
        }
    ))
