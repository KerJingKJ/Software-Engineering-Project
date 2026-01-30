from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="student"),
    path("scholarshipList/", views.scholarship_list, name="scholarship_list"),
    path('bookmarkScholarship/', views.bookmark_list, name='bookmark_list'),
    path("applicationForm_status/", views.application_form_status, name="applicationForm_status"),
    path("trackApplication/", views.trackApplication, name="trackApplication"),
    # Page to view details
    path('scholarship/details/<int:scholarship_id>/', views.scholarship_details, name='scholarship_details'),
    
    # Action to toggle the bookmark
    path('scholarship/bookmark/toggle/<int:scholarship_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('scholarship/bookmarks/', views.bookmark_list, name='bookmark_list'),
    path('eligibility/', views.eligibility_check, name='eligibility_check'),

    path("scholarships/apply", views.application_form, name="applicationForm"), # create path
    path("application/<int:id>/edit/<int:page>", views.edit_application_form, name="edit_application_form"), #edit path
]