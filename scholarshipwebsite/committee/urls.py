from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="committee"),
    path("manage/", views.manage, name="manage"),
    path("reviewApprove/", views.reviewApprove, name="reviewApprove"),
    path("create/", views.create_scholarship, name="create_scholarship"),
]