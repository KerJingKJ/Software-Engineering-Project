from django.urls import path
from . import views
from login import views as login_views 
urlpatterns = [
    path("", views.index, name="committee"),
    path("manage/", views.manage, name="manage"),
    path("reviewApprove/", views.reviewApprove, name="reviewApprove"),
    path("create/", views.create_scholarship, name="create_scholarship"),
    path("edit/<int:id>/", views.edit_scholarship, name="edit_scholarship"),
    path("delete/<int:id>/", views.delete_scholarship, name="delete_scholarship"),
    
    # Application Review URLs
    path("application/<int:id>/details/", views.view_application_details, name="view_application_details"),
    path("application/<int:id>/family/", views.view_family_background, name="view_family_background"),
    path("application/<int:id>/interview/", views.schedule_interview, name="schedule_interview"),
    path("application/<int:id>/decision/", views.decision_page, name="decision_page"),


    #Manage Account URL
    path('manageAccount', login_views.manage_account, name='manageAccount'),
]