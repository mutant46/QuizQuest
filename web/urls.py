from django.urls import path
from .views import *
urlpatterns = [
    path("", home, name ='home'),
    path('policy/', policy, name = 'policy'),
]