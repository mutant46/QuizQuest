from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ResultView,
    TestData,
    CalcTestData
)
urlpatterns = [
    path('quizes/<int:pk>/<slug:slug>/test/data/',
         TestData.as_view(), name='test-quiz-data'),
    path('quizes/<int:pk>/<slug:slug>/test/calculate-result/',
         CalcTestData.as_view(), name='calculate-test-result'),

    path('quiz/<int:pk>/<slug:slug>/',
         ResultView.as_view(), name='test-result-page'),

]
