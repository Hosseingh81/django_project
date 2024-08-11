from django import forms


class AddquestionForm(forms.Form):
    question = forms.CharField(label="Your question", max_length=100, help_text = "Enter your Name",error_messages = { 'required':"Please Enter your Name"})
    # time=forms.TimeField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))