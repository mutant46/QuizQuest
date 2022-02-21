from django.contrib.auth.models import User
import factory
from faker import Faker
from quiz import models



fake = Faker()



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "testUser"
    email = fake.email()



class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = "testName"




class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Quiz

    name = "testQuiz"
    category = factory.SubFactory(CategoryFactory)
    user = factory.SubFactory(UserFactory)
    image = fake.file_name()
    desc = fake.text()
    creation_date = fake.date()
    time = fake.random_int(min=1, max=100)
    percentage = fake.random_int(min=1, max=100)
    papularity = fake.random_int(min=1, max=100)
    slug = "testQuiz"
    status = fake.random_element(('active', 'draft'))
    difficulity = fake.random_element(('easy', 'medium', 'hard'))




class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question


    quiz = factory.SubFactory(QuizFactory)
    text = "testQuestion"



class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Answer

    question = factory.SubFactory(QuestionFactory)
    text = "testAnswer"
    correct = fake.boolean()



