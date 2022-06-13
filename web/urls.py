from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('public_quiz_list/', PublicQuizListView.as_view(), name='public_quiz_list'),
    path('draft_quiz_list/', DraftQuizListView.as_view(), name='draft_quiz_list'),
    path('private_quiz_list/', PrivateQuizListView.as_view(),
         name='private_quiz_list'),
    path('private_quiz/<int:id>/submissions/',
         PrivateQuizSubmissionsView.as_view(), name='private_quiz_submissions'),
    path('quiz_results/', QuizResultView.as_view(), name='quiz_results'),
    path('search/', SearchView.as_view(), name='quizes_search'),
]
