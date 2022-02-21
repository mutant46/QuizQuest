import pytest
from quiz.models import Quiz, Category, Question, Answer


# ---------------------- Catrgory tests ----------------------
@pytest.mark.django_db
def test_category_creation(new_category):
    category = new_category
    assert Category.objects.count() == 1

@pytest.mark.django_db
def test_category_str_value(new_category):
    category = new_category
    assert str(category) == 'testName'

# ---------------------- quiz tests ----------------------
@pytest.mark.django_db
def test_new_quiz(new_quiz):
    ''' Checks if the new quiz is created '''  
    assert Quiz.objects.count() == 1


@pytest.mark.django_db
def test_quiz_str_value(new_quiz):
    ''' Checks if the new quiz's string value is generated '''  
    assert str(new_quiz) == 'testQuiz'


@pytest.mark.django_db
def test_quiz_total_questions(new_quiz):
    ''' Checks if the new quiz's total questions is generated '''  
    assert new_quiz.total_questions() == 0

# # ---------------------- question tests ----------------------


@pytest.mark.django_db
def test_new_question_is_created(new_question):
    ''' Checks if the new question is created '''  
    assert Question.objects.count() == 1


@pytest.mark.django_db
def test_new_question_str_value(new_question):
    ''' Checks if the new question's string value is generated '''  
    assert str(new_question) == 'testQuestion'


@pytest.mark.django_db
def test_new_question_associated_answers(new_question):
    ''' Checks if the new question's associated answers are generated '''  
    assert new_question.answers.count() == 0


@pytest.mark.django_db
def test_new_question_correct_answer(new_question):
    ''' Checks if the new question's correct answer is generated '''  
    assert new_question.get_correct_ans().count() == 0


# ---------------------- Answer tests ----------------------


@pytest.mark.django_db
def test_new_answer_generated(new_answer):
    ''' Checks if the new answer is generated '''  
    assert Answer.objects.count() == 1
    assert str(new_answer) == 'testAnswer'
