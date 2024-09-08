from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("add_question/",views.Add_questionView.as_view(),name="add_question"),
    path("add_question/add_choice/",views.AddChoiceView.as_view(),name="add_choice"),
    path("add_question/add_choice/question_saved/",views.show_question_saved_page,name="question_saved"),
]