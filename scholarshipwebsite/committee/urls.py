from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="committee"),
    path("manage/", views.manage, name="manage"),
    path("create/", views.create, name="create"),
    path("reviewApprove/", views.reviewApprove, name="reviewApprove"),
    path("schedule/", views.schedule, name="schedule"),
]