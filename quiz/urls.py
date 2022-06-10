from django.urls import path
from .views import (
    QuizSearchView,
    AllQuizesView,
    CreateQuizView,
    QuizDetailView,
    QuizQuestionCreateView,
    QuizStatusView,
    QuizUpdateView,
    QuizStatusUpdateView,
    QuizCategoryView,
    Test,
    CloneQuizView,
)

app_name = 'quiz'
urlpatterns = [
    path('', AllQuizesView.as_view(), name='quizes'),
    path('create/', CreateQuizView.as_view(), name='create_quiz'),
    path('<int:pk>/<slug:slug>/edit/',
         QuizUpdateView.as_view(), name='edit_quiz'),
    path('<int:pk>/<slug:slug>/questions/edit',
         QuizQuestionCreateView.as_view(), name='add_question'),
    path('<int:pk>/<slug:slug>/status/',
         QuizStatusView.as_view(), name='quiz_status'),
    path('<int:pk>/<slug:slug>/status/edit/',
         QuizStatusUpdateView.as_view(), name='quiz_status_edit'),
    path('<int:pk>/<slug:slug>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('category/<str:category>/',
         QuizCategoryView.as_view(), name='quizes_by_category'),
    path('search/', QuizSearchView.as_view(), name='quizes_search'),
    path('<int:pk>/<slug:slug>/test', Test.as_view(), name='test-quiz-page'),
    path('<int:pk>/<slug:slug>/clone',
         CloneQuizView.as_view(), name='clone-quiz'),

]
