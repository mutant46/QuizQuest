from django.urls import path
from .views import AllQuizesView, CreateQuizView, QuizDetailView, QuizQuestionCreateView, QuizStatusView

app_name = 'quiz'
urlpatterns = [
    path('', AllQuizesView.as_view(), name='quizes'),
    path('create/', CreateQuizView.as_view(), name='create_quiz'),
    path('<int:pk>/questions/add', QuizQuestionCreateView.as_view(), name = 'add_question'),
    path('<int:pk>/status/', QuizStatusView.as_view(), name = 'quiz_status'),
    path('<int:pk>/<slug:slug>/', QuizDetailView.as_view(), name='quiz_detail'),
]