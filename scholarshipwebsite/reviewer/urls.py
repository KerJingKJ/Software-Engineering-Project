from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="reviewer"),
    path("review/", views.review, name="review"),
    path("details/", views.details, name="details"),
]