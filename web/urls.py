from django.urls import path
from .views import *
urlpatterns = [
    path("", home, name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
]
