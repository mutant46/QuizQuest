import pytest
from django.urls import reverse
from quiz.views import AllQuizesView
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from conftest import ViewTestMixin
from quiz.views import AllQuizesView, CreateQuizView, CreateQuizView, QuizDetailView, QuizQuestionCreateView, QuizStatusView


# @pytest.mark.django_db
# def test_AllQuizesView_status_code(client):
#     response = client.get(reverse('quiz:quizes'))
#     assert response.status_code == 200

# def test_CreateQuizView_get_user_not_logged_in(client):
#     response = client.get(reverse('quiz:create_quiz'))
#     assert response.status_code == 302

# @pytest.mark.django_db
# def test_CreateQuizView_get_user_logged_in(client, new_user):
#     client.force_login(new_user)
#     response = client.get(reverse('quiz:create_quiz'))
#     assert response.status_code == 200

# def test_createQuizview_post_status_code(client, new_user):
#     client.force_login(new_user)
#     response = client.post(reverse('quiz:create_quiz'))
#     assert response.status_code == 200

# @pytest.mark.django_db
# def test_addQuesionView_get_status_code(client, new_quiz):
#     client.force_login(new_quiz.user)
#     response = client.get(reverse('quiz:add_question', kwargs={'username': new_quiz.user.username , 'pk': new_quiz.pk}))
#     assert response.status_code == 200


# def test_addQuestion_view_post_status_code(client, new_quiz):
#     client.force_login(new_quiz.user)
#     response = client.post(reverse('quiz:add_question', kwargs={'username': new_quiz.user.username , 'pk': new_quiz.pk}))
#     assert response.status_code == 200

# def test_quiz_status_get_status_code(client, new_quiz):
#     client.force_login(new_quiz.user)
#     response = client.get(reverse('quiz:quiz_status', kwargs={'username': new_quiz.user.username , 'pk': new_quiz.pk}))
#     assert response.status_code == 200

# def test_quiz_status_post_status_code(client, new_quiz):
#     client.force_login(new_quiz.user)
#     response = client.post(reverse('quiz:quiz_status', kwargs={'username': new_quiz.user.username , 'pk': new_quiz.pk}))
#     assert response.status_code == 200

