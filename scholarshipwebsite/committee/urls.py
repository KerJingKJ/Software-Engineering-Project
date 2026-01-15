from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="committee"),
    path("manage/", views.manage, name="manage"),
    path("reviewApprove/", views.reviewApprove, name="reviewApprove"),
    path("create/", views.create_scholarship, name="create_scholarship"),
    path("edit/<int:id>/", views.edit_scholarship, name="edit_scholarship"),
    path("delete/<int:id>/", views.delete_scholarship, name="delete_scholarship"),
]