from django import forms
from django.forms import ModelForm, Textarea
from .models import Choice,Question

class AddquestionForm(forms.Form):
    """ 
    this class handels data that user enters in the form, before saved in questions and do some validations on it.
    """
    
    question = forms.RegexField(label="Your question",regex="[a-zA-Z.!?,:;]+$",error_messages={'invalid':"you can't enter numbers.",'required':"please enter your input"},max_length=100)

class AddChoiceForm(ModelForm):
    """
    this class handels data that user enters in the form, before saving it in the database.
    """

    class Meta:

        model= Choice
        fields= ['choice_text','question']
        widgets = {'question': forms.HiddenInput()}

        error_messages = {"choice_text": {"required": "this field can not be empty"}}

        labels= {'choice_text':'input your choice here'}
    def __init__(self, *args, **kwargs):
        q = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if q:
            del self.fields['question']  # Remove the field itself from the form
            self.instance.question = q  # Set the user as the owner





