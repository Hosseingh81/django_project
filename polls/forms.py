from django import forms
from django.forms import ModelForm, Textarea
from .models import Choice

class AddquestionForm(forms.Form):
    """ 
    this class handels data that user enters in the form, before saved in questions and do some validations on it.
    """
    
    question = forms.RegexField(label="Your question",regex="[a-zA-Z.!?,:;]+$",error_messages={'invalid':"invalied value",'required':"please enter your input"},max_length=100)

class AddChoiceForm(ModelForm):
    """
    this class handels data that user enters in the form, before saving it in the database.
    """

    class Meta:

        model= Choice
        fields= ['choice_text']


        error_messages = {"choice_text": {"required": "this field can not be empty"}}

        labels= {'choice_text':'input your choice here'}



