from django.utils import timezone
# from datetime import datetime
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from django import forms


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.pub_date <= now
    def is_string(self):
        if type(self.question_text)==str:
            return True
        else:
            return False

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text
# Create your models here.

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
