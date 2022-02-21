import pytest
from django.test import Client
from pytest_factoryboy import register
from quiz.tests.factories import UserFactory, CategoryFactory, QuizFactory, QuestionFactory, AnswerFactory


@pytest.fixture
def client():
    return Client()


register(UserFactory)
register(CategoryFactory)
register(QuizFactory)
register(QuestionFactory)
register(AnswerFactory)


@pytest.fixture
def new_category(category_factory):
    category = category_factory.create()
    return category

@pytest.fixture()
def new_quiz(db, quiz_factory): 
    quiz = quiz_factory.create()
    return quiz


@pytest.fixture()
def new_question(db, question_factory):
    question = question_factory.create()
    return question


@pytest.fixture()
def new_answer(db, answer_factory):
    answer = answer_factory.create()
    return answer




