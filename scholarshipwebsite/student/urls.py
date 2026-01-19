from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="application"),
    # path("manage/", views.manage, name="manage"),
    # path("reviewApprove/", views.reviewApprove, name="reviewApprove"),
    path("create/", views.create_application, name="create_scholarship"),
    path("edit/<int:id>/", views.edit_application, name="edit_scholarship"),
    # path("delete/<int:id>/", views.delete_scholarship, name="delete_scholarship"),
    # path("schedule/", views.schedule, name="schedule"),
]