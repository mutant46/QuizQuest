from django.urls import path
from .views import AllQuizesView, CreateQuizView, QuizDetailView, QuizQuestionCreateView
urlpatterns = [
    path('', AllQuizesView.as_view(), name='quizes'),
    path('create/', CreateQuizView.as_view(), name='create_quiz'),
    path('<str:username>/<int:pk>/add-questions/', QuizQuestionCreateView.as_view(), name = 'add_question'),
    path('<slug:slug>/', QuizDetailView.as_view(), name='quiz_detail'),

]