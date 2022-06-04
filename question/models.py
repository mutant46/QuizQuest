from django.db import models
from quiz.models import Quiz

# Create your models here.
class Question(models.Model):

    ''' Question association with the quiz '''

    quiz = models.ForeignKey(Quiz,
                on_delete=models.CASCADE,
                related_name='questions')
    text = models.CharField(max_length=300)


    def __str__(self):
        return "%s" % self.text

    def get_answers(self):
        return self.answers.all()

    def get_correct_ans(self):
        return self.answers.get(correct = True)


# ------------------------------------------------------------- 


class Answer(models.Model):

    ''' Answers associated with the questions '''

    question = models.ForeignKey(Question,
                on_delete=models.CASCADE,
                related_name='answers')
    text = models.CharField(max_length=100)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.text