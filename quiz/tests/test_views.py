import pytest
from quiz.views import AllQuizesView
from django.test import TestCase
from conftest import ViewTestMixin
from quiz.views import AllQuizesView, CreateQuizView,  QuizDetailView, QuizQuestionCreateView, QuizStatusView, QuizUpdateView, QuizStatusUpdateView


class TestQuizListView(ViewTestMixin):
    view_class = AllQuizesView

    def test_AllQuizesView_status_code(self):
        self.is_callable()


class TestQuizCreateView(ViewTestMixin):
    view_class = CreateQuizView

    def test_CreateQuizView_user_not_loged_in(self):
        self.is_callable(to=True)

    def test_CreateQuizView_user_loged_in(self, new_user):
        self.is_callable(user=new_user)

    def test_create_post_status_code(self, new_user):
        self.is_callable(post=True, user=new_user)


class TestAddQuestionView(ViewTestMixin):
    view_class = QuizQuestionCreateView

    def get_view_kwargs(self):
        return {'pk': '1'}

    def test_add_question_user_not_loged_in(self):
        self.is_callable(to=True)

    def test_add_question_get_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user)

    def test_add_question_post_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user, post=True)


class TestQuizStatusView(ViewTestMixin):
    view_class = QuizStatusView

    def get_view_kwargs(self):
        return {'pk': '1'}

    def test_set_status_user_not_loged_in(self):
        self.is_callable(to=True)

    def test_set_status_get_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user)

    def test_set_status_post_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user, post=True)


class TestQuizDetailView(ViewTestMixin):
    view_class = QuizDetailView

    def get_view_kwargs(self):
        return {'pk': '1', 'slug': 'testQuiz'}

    def test_quiz_detail_get_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user)


class TestQuizEditView(ViewTestMixin):

    view_class = QuizUpdateView

    def get_view_kwargs(self):
        return {'pk': '1', 'slug': 'testQuiz'}

    def test_quiz_edit_user_not_loged_in(self):
        self.is_callable(to=True)

    def test_quiz_edit_get_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user)

    def test_quiz_edit_post_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user, post=True)


class TestQuizStatusUpdateView(ViewTestMixin):

    view_class = QuizStatusUpdateView

    def get_view_kwargs(self):
        return {'pk': '1', 'slug': 'testQuiz'}

    def test_quiz_status_update_user_not_loged_in(self):
        self.is_callable(to=True)

    def test_quiz_status_update_get_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user)

    def test_quiz_status_update_post_status_code(self, new_quiz):
        self.is_callable(user=new_quiz.user, post=True)
