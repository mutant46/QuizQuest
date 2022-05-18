from django.urls import path
from .views import (
    ResultView
)
app_name = 'result'
urlpatterns = [
    path('result/', ResultView.as_view(), name='test-result-page'),
]