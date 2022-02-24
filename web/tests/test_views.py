import pytest
from django.urls import reverse, resolve
from web.views import home, policy
from conftest import ViewTestMixin




def test_home_view_status_code(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200

def test_policy_view_status_code(client):
    response = client.get(reverse('policy'))
    assert response.status_code == 200
