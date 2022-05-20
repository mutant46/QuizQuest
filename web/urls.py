from django.urls import path
from .views import *
urlpatterns = [
    path("", home, name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('public_quiz_list/', PublicQuizListView.as_view(), name='public_quiz_list'),
    path('private_quiz_list/', PrivateQuizListView.as_view(), name='private_quiz_list'),
    path('quiz_results/', QuizResultView.as_view(), name='quiz_results'),
]
