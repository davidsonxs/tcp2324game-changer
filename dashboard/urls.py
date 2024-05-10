from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_game, name='create_game'),
    path('home_away_goals/', views.home_away_goals, name='home_away_goals'),
    path('faceoff_wins_per_team_per_period/', views.faceoff_wins_per_team_per_period, name='faceoff_wins_per_team_per_period'),
    path('team_period_performance/', views.team_period_performance, name='team_period_performance'),
    path('team_performance_by_event/', views.team_performance_by_event, name='team_performance_by_event'),
    path('goals_scored_per_team/', views.goals_scored_per_team, name='goals_scored_per_team'),
    path('compare_penalties/', views.compare_penalties, name='compare_penalties'),
    path('', views.index, name='index')
]