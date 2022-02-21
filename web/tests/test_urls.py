from web.views import home, policy
from django.urls import reverse, resolve




def test_home_url_resolves():
    """
    Tests that the home url resolves to the home view
    """
    url = reverse('home')
    assert resolve(url).func == home



def test_policy_url_resolves():
    """
    Tests that the policy url resolves to the policy view
    """
    url = reverse('policy')
    assert resolve(url).func == policy