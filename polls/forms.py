from django import forms

class AddquestionForm(forms.Form):
    """ 
    this class handels data that user enters in the form, before saved in questions and do some validations on it.
    """
    question = forms.RegexField(label="Your question",regex="[a-zA-Z.!?,:;]+$",error_messages={'invalid':"invalied value",'required':"please enter your input"},max_length=100)
class AddChoiceForm(forms.Form):
    """
    this class handels data that user enters in the form, before saving it in the database.
    """
    choice_text=forms.CharField(label='choice_text',error_messages={"required":"this field can't be empty."})