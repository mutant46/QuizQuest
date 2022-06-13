import re
from django.db import models
from django.contrib.auth.models import User
from web.models import Category


d_choices = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard')
)


class PublicQuizesManager(models.Manager):

    ''' Creating a quiz model manager that return 
        only public quizes '''

    def get_queryset(self):
        return super().get_queryset().filter(status='public')


class PrivateQuizesManager(models.Manager):

    ''' Creating a quiz model manager that returns
        only private quizes '''

    def get_queryset(self):
        return super().get_queryset().filter(status='private')


def set_quiz_image_location(instance, filename):
    return f"{instance.user}/{filename}"


class Quiz(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='quizes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='quizes')
    image = models.ImageField(upload_to=set_quiz_image_location)
    desc = models.CharField(max_length=999)
    creation_date = models.DateField(auto_now_add=True)
    time = models.IntegerField()
    percentage = models.FloatField()
    papularity = models.IntegerField(default=0)
    slug = models.SlugField(max_length=150)
    status = models.CharField(max_length=10,
                              choices=(
                                  ('public', 'Public'),
                                  ('private', 'Private'),
                                  ('draft', 'Draft')),
                              default='draft')
    difficulity = models.CharField(max_length=10,
                                   blank=True,
                                   null=True,
                                   choices=d_choices)
    ratings = models.IntegerField(default=0)
    password = models.CharField(max_length=100, blank=True, null=True)
    valid_thru = models.DateField(blank=True, null=True)

    ''' models managers '''
    objects = models.Manager()
    public = PublicQuizesManager()
    private = PrivateQuizesManager()

    class Meta:
        verbose_name = 'quiz'
        verbose_name_plural = 'quizes'

    def __str__(self):
        return "%s" % self.name

    def total_questions(self):
        return self.questions.count()

    def is_private(self):
        return self.status == 'private'

    def get_questions(self):
        '''
        returns all question related to that quiz
        '''
        return self.questions.all()


class Comment(models.Model):

    ''' Comments Model '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=400)

    def __str__(self):
        return self.text


# class Replies(models.Model):

#     ''' Replies to Comment Model '''

#     quiz = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     text = models.CharField(max_length=400)
