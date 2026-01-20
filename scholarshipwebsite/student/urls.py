from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="student"),
    path("scholarshipList/", views.scholarship_list, name="scholarship_list"),
    path("scholarshipDetails/", views.scholarship_details, name="scholarship_details"),
    path("bookmarkScholarship/", views.bookmark_scholarship, name="bookmarkScholarship"),
    path("eligibility/", views.eligibility, name="eligibility"),
    path("applicationForm/", views.application_form, name="applicationForm"),
    path("applicationForm_p2/", views.application_form_p2, name="applicationForm_p2"),
    path("applicationForm_p3/", views.application_form_p3, name="applicationForm_p3"),
    path("applicationForm_p4/", views.application_form_p4, name="applicationForm_p4"),
    path("applicationForm_status/", views.application_form_status, name="applicationForm_status"),
    path("trackApplication/", views.track, name="trackApplication")
]