from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="tournaments"),
    path("", views.tournaments, name="tournaments"),
    path("<int:id>", views.tournament_details, name="tournament_details"),
    path("generate", views.generate_tournament, name="generate_tournaments"),
]
