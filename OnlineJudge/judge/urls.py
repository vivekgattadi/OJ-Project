from django.urls import path
from . import views

app_name = 'judge'

urlpatterns = [
    path('', views.ListProblems, name='ListProblems'),
    path('ListProblems/<int:question_id>/', views.ShowindividualProblem, name='ShowindividualProblem'),
    path('ListProblems/<int:question_id>/CodeSubmission/', views.CodeSubmission, name='CodeSubmission'),
    path('Leaderboard/', views.Leaderboard, name='Leaderboard'),
]