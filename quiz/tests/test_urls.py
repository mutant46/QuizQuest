from django.urls import reverse, resolve
from quiz.views import AllQuizesView, CreateQuizView, QuizDetailView, QuizQuestionCreateView, QuizStatusUpdateView, QuizStatusView, QuizUpdateView



def test_allQuiz_url_resolves():
    url = reverse('quiz:quizes')
    assert resolve(url).func.view_class == AllQuizesView

def test_create_Quiz_url_resolves():
    url = reverse('quiz:create_quiz')
    assert resolve(url).func.view_class == CreateQuizView

def test_add_question_url_resolves():
    url = reverse('quiz:add_question',
                    kwargs={'pk': 1, 'slug' : 'test'})
    assert resolve(url).func.view_class == QuizQuestionCreateView

def test_set_status_url_resolves():
    url = reverse('quiz:quiz_status',
                    kwargs={'pk': 1, 'slug' : 'test'})
    assert resolve(url).func.view_class == QuizStatusView

def test_detail_url_resolves():
    url = reverse('quiz:quiz_detail',
                    kwargs={'slug': 'test', 'pk' : '1'})
    assert resolve(url).func.view_class == QuizDetailView


def test_quiz_edit_url_resolves():
    url = reverse('quiz:edit_quiz',
                    kwargs={'slug': 'test', 'pk' : '1'})
    assert resolve(url).func.view_class == QuizUpdateView


def test_quiz_status_edit_url_resolves():
    url = reverse('quiz:quiz_status_edit',
                    kwargs={'slug': 'test', 'pk' : '1'})
    assert resolve(url).func.view_class == QuizStatusUpdateView