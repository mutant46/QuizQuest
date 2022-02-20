from django.forms import inlineformset_factory, ModelForm
from django.forms.models import BaseInlineFormSet
from .models import Question, Quiz, Answer
from django.core.exceptions import ValidationError
from .utils import is_empty_form, is_being_edited
from django.db.models import Count



''' ---------------------------------- Answer BaseInlineform and Simple Form ---------------------------------- '''


class BaseAnswerForm(BaseInlineFormSet):
    '''  
    overing the is_valid function to check the number of 
    choices provided 
    '''

    def clean(self):
        super().clean()

        # Atleast one answer should be correct 
        if not any([form.cleaned_data.get('correct') for form in self.forms]):
            raise ValidationError('At least one answer must be correct.')


        # must provide at least all four answers 
        for form in self.forms:
            if not form.cleaned_data.get('text'):
                form.add_error(
                    field = 'text',
                    error = 'This field is required'
                )


AnswerInlineFormSet = inlineformset_factory(
                        Question, 
                        Answer,
                        formset = BaseAnswerForm,
                        fields = ('text', 'correct'), 
                        extra=4 ,max_num=4, 
                        can_delete=False,)


''' --------------------------------- Question BaseInlineform and Simple Form -------------------------- '''

class BaseQuestionFormSet(BaseInlineFormSet):

    '''
    Adding the AnswerForm in  the QuestionForm
    as nested formset
    '''
    
    def add_fields(self, form, index):
        super().add_fields(form, index)

        form.nested = AnswerInlineFormSet(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='answer-%s-%s' % (
                            form.prefix,
                            AnswerInlineFormSet.get_default_prefix()))

    # overring is_valid to check if nested formset is valid
    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
        return result


    # overring clean method
    def clean(self):

        '''
        If question form is empty but answers form has data we 
        should return an error as we can not save the Question
        and no duplication of question is allowed
        '''

        super().clean()

        for form in self.forms:
            # handle duplication of question
            if form.has_changed() and self._qustion_already_exists(form):
                form.add_error(
                    field = None,
                    error = 'Question Already Exits.'
                )
            
            # handle empty question form
            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field = None,
                    error = 'You must provide a question statement.',
                )


    # overiding save method to save the nested forms as well
    def save(self, commit= True):
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)
        
        return result

    # Utility methods
    def _is_adding_nested_inlines_to_empty_form(self, form):
        ''' 
        Is the user trying to add answers choices to a
        question form that is empty?
        '''

        # Check if form containes a nested form
        if not hasattr(form, 'nested'):
            return False
        # Check if whole for is empty
        if not is_empty_form(form):
            return False
        # check if the outer form is in updating state
        if is_being_edited(form):
            return False
        
        return any(not is_empty_form(nested_form) for nested_form in form.nested)


    def _qustion_already_exists(self, form):
        question = form.cleaned_data.get('text')
        if self.instance.questions.filter(text=question).exists():
            return True
        return False



''' Inline formset for Quiz , Question & nested AnswerForm '''
QuestionForm = inlineformset_factory(
                        Quiz,
                        Question,
                        fields = ('text', ),
                        formset=BaseQuestionFormSet,
                        extra=1,
                        can_delete=False
                    )


