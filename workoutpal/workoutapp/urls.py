from django.urls import path
from .import views


urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("workouts", views.show_all),
    path("workouts/create", views.create_workout),
    path("workouts/<int:workout_id>", views.show_one),
    path("workouts/<int:workout_id>/update", views.update),
    path("workouts/<int:workout_id>/delete", views.delete),
    path("favorite/<int:workout_id>", views.favorite),
    path("unfavorite/<int:workout_id>", views.unfavorite),
    path("logout", views.logout)
]