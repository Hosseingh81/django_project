from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class AddquestionForm(forms.Form):
    question = forms.CharField(label="Your question", max_length=2,validators=[validators.RegexValidator(regex="[a-zA-Z]+$")],error_messages={"RegexValidator":"sag"})
    if question is None:
        print("sag")
    elif question is not None:
        print(question.validators)