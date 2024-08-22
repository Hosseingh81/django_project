from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question,Vote
from django.views import generic
from django.utils import timezone
from .forms import AddquestionForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import MultipleObjectMixin

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """ 
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())





class VoteView(generic.ListView, SuccessMessageMixin):
    template_name="polls/results.html"
    pk_url_kwarg='question_id'
    http_method_names=['get','post']
    success_message="your vote has been saved seccssfuly"
    def post(self,request,question_id):
        request=self.request
        voting_user=request.user
        voting_choice=Choice.objects.get(id=request.POST["choice"])
        print("in post,voting choice",voting_choice)
        self.v=Vote.objects.create(user=voting_user,choice=voting_choice)
        # print("invotepost",self.question)
        print("inpost,v:",self.v)
        self.v.save()
        return self
    
    def get_queryset(self):
        self.question=get_object_or_404(Question,id=self.kwargs['question_id'])
        print("in get queryset:", Question.objects.filter(id=self.question.id))
        return Question.objects.filter(id=self.question.id)
    
    def get_context_data(self, **kwargs):
        context=super(VoteView,self).get_context_data(**kwargs)
        context['question']=self.question
        print("in get context data", context)
        return context
    

        

    




# def vote(request,question_id):
#     voted_question=get_object_or_404(Question,pk=question_id)
#     voted_user=request.user
#     voted_choice=Choice.objects.get(id=request.POST["choice"])
#     same_users_vote=Vote.objects.filter(user=request.user)
#     same_users_vote.filter(choice=voted_choice)
#     for x in same_users_vote:
#         vote_question=x.choice.question
#     if request.user.is_authenticated :
#         if len(same_users_vote)==0 :
#             v=Vote(user=voted_user,choice=voted_choice)      
#             v.save()
#             return render(request,"polls/results.html",{"question":voted_question})
#         elif vote_question!=voted_question:
#             v=Vote(user=voted_user,choice=voted_choice)      
#             v.save()
#             return render(request,"polls/results.html",{"question":voted_question})
#         else:
#             return HttpResponse("you can't vote more than onece!")
#     else:
#         return HttpResponse("please login first.")
    


# class Add_questionView(generic.CreateView):
#     form_model=AddquestionForm
#     template_name="polls/add_question.html"
#     success_url='polls/question_saved.html'






























# def add_question(request):# this func passes the needed agruements to the add_question.html
#     # if this is a POST request we need to process the form data
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = AddquestionForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             question=form.cleaned_data['question']
#             Question.objects.create(question_text=question,pub_date=timezone.now())
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponse("thanks")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form= AddquestionForm()
#         return render(request, "polls/add_question.html", {"form": form})



# Create your views here.