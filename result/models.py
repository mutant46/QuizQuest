from django.db import models
from django.contrib.auth.models import User
from quiz.models import Quiz
# Create your models here.


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='quiz')
    percentage = models.FloatField()
    status = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return f"{self.user}"
