from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="student"),
    path("scholarshipList/", views.scholarship_list, name="scholarship_list"),
    path('bookmarkScholarship/', views.bookmark_list, name='bookmark_list'),
    path("applicationForm/", views.application_form, name="applicationForm"),
    path("applicationForm_p2/", views.application_form_p2, name="applicationForm_p2"),
    path("applicationForm_p3/", views.application_form_p3, name="applicationForm_p3"),
    path("applicationForm_p4/", views.application_form_p4, name="applicationForm_p4"),
    path("applicationForm_status/", views.application_form_status, name="applicationForm_status"),
    path("trackApplication/", views.track, name="trackApplication"),
    # Page to view details
    path('scholarship/details/<int:scholarship_id>/', views.scholarship_details, name='scholarship_details'),
    
    # Action to toggle the bookmark
    path('scholarship/bookmark/toggle/<int:scholarship_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('scholarship/bookmarks/', views.bookmark_list, name='bookmark_list'),
    path('eligibility/', views.eligibility_check, name='eligibility_check'),

]