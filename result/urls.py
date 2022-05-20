from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ResultView
)
urlpatterns = [
    path('quiz/<int:pk>/<slug:slug>/', ResultView.as_view(), name='test-result-page'),

]
