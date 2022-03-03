import string
import random


def is_empty_form(form):
    """
    A form is considered empty if it passes its validation,
    but doesn't have any data.

    This is primarily used in formsets, when you want to
    validate if an individual form is empty (extra_form).
    """
    if form.is_valid() and not form.cleaned_data:
        return True
    else: 
        return False


def is_being_edited(form):

    '''
    Does the form have a model instance attached and it's not being added?
    '''

    if form.instance and not form.instance._state.adding:
        return True
        
    else:
        # Either the form has no instance attached or
        # it has an instance that is being added.
        return False


def generate_random_string(length=30):
    '''
    Generate a random string of a given length
    '''
    return ''.join(random.choice(string.ascii_letters) for i in range(length))