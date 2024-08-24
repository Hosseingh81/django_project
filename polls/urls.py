from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:question_id>/vote/", views.VoteView.as_view(), name="vote"),
    path("add_question/",views.Add_questionView.as_view(),name="add_question"),
    path("question_saved/",views.question_saved,name="question_saved")
]