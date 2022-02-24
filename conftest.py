from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import RequestFactory
from django.urls import resolve
from django.urls.exceptions import Resolver404
from django.urls import reverse
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
def new_user(db, user_factory):
    user =  user_factory.create()
    return user


@pytest.fixture
def new_category(db, category_factory):
    category = category_factory.create()
    return category

@pytest.fixture
def new_quiz(db, quiz_factory): 
    quiz = quiz_factory.create()
    return quiz


@pytest.fixture
def new_question(db, question_factory):
    question = question_factory.create()
    return question


@pytest.fixture
def new_answer(db, answer_factory):
    answer = answer_factory.create()
    return answer




# ---------------------   Mixins for test -------------------------- 
@pytest.mark.django_db
class ViewTestMixin(object):
    """Mixin with shortcuts for view tests."""
    longMessage = True  # More verbose error messages


    def get_view_kwargs(self):
        """
        Returns a dictionary representing the view's kwargs, if  
        necessary.

        If the URL of this view is constructed via kwargs, you can 
        override this method and return the proper kwargs for the 
        test.

        """
        return {}

    def get_response(self, method, user, args, kwargs):
        """Creates a request and a response object."""
        factory = RequestFactory()
        req = getattr(factory, method)('/')
        req.user = user if user else AnonymousUser()
        return self.view_class.as_view()(req, *args, **kwargs)

    def is_callable(
        self,
        user=None,
        post=False,
        to=False,
        args=[],
        kwargs={},
    ):
        """Initiates a call and tests the outcome."""
        view_kwargs = kwargs or self.get_view_kwargs()
        resp = self.get_response(
            'post' if post else 'get',
            user=user,
            args=args,
            kwargs=view_kwargs,
        )
        if to:
            assert resp.status_code in [301, 302]
        else:
            assert resp.status_code == 200


