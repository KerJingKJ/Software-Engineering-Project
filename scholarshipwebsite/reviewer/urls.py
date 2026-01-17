from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="reviewer"),
    path("<int:app_id>/", views.index, name="reviewer_with_id"),
    path("review/", views.review, name="review"),
    path("details/", views.details, name="details"),
]