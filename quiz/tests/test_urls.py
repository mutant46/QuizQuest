from django.urls import reverse, resolve
from quiz.views import AllQuizesView, CreateQuizView, QuizDetailView, QuizQuestionCreateView, QuizStatusView



def test_allQuiz_url_resolves():
    url = reverse('quizes')
    assert resolve(url).func.view_class == AllQuizesView

def test_create_Quiz_url_resolves():
    url = reverse('create_quiz')
    assert resolve(url).func.view_class == CreateQuizView

def test_add_question_url_resolves():
    url = reverse('add_question', kwargs={'username': 'test', 'pk': 1})
    assert resolve(url).func.view_class == QuizQuestionCreateView

def test_set_status_url_resolves():
    url = reverse('quiz_status', kwargs={'username': 'test', 'pk': 1})
    assert resolve(url).func.view_class == QuizStatusView

def test_detail_url_resolves():
    url = reverse('quiz_detail', kwargs={'slug': 'test'})
    assert resolve(url).func.view_class == QuizDetailView
