from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 
import uuid


class Category(models.Model):
    name = models.CharField(max_length = 150)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return "%s" % self.name

#difficulities choices
d_choices = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard')
)

def set_quiz_image_location(instance, filename):
    return f"{instance.user}/{instance.name}/{filename}"

class Quiz(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category,
                on_delete=models.PROTECT,
                related_name = 'quizes')
    user = models.ForeignKey(User,
                on_delete=models.CASCADE,
                related_name='quizes')
    image = models.ImageField(upload_to=set_quiz_image_location)
    desc = models.CharField(max_length=999)
    creation_date = models.DateField(auto_now_add=True)
    time = models.IntegerField()
    percentage =  models.FloatField()
    papularity = models.IntegerField(default = 0)
    slug = models.SlugField(max_length=150)
    status = models.CharField(max_length=10, choices=(('active', 'Active'), ('draft', 'Draft')), default='draft')
    difficulity = models.CharField(max_length=10,
                blank = True,
                null = True,
                choices = d_choices)

    class Meta:
        verbose_name = 'quiz'
        verbose_name_plural = 'quizes'

    def __str__(self):
        return "%s" % self.name

    def total_question(self):
        return self.questions.count()

    '''
    settings the slug field for the quiz with its name
    '''
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, *kwargs)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz,
                on_delete=models.CASCADE,
                related_name='questions')
    text = models.CharField(max_length=300)


    def __str__(self):
        return "%s" % self.text


    def get_correct_ans(self):
        return self.answers.all().filter(correct = True)


class PrivateQuiz(Quiz):
    quiz_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


    class Meta:
        verbose_name = 'Private_quiz'
        verbose_name_plural = 'Private_quizes'



class Answer(models.Model):
    question = models.ForeignKey(Question,
                on_delete=models.CASCADE,
                related_name='answers')
    text = models.CharField(max_length=100)
    correct = models.BooleanField(default=False)

    def __srt__(self):
        return "%s" % self.text


