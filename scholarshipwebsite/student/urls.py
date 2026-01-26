from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="student"),
    path("scholarships/", views.scholarship_list, name="scholarship_list"),
    path("scholarships/eligibility/", views.eligibility, name="eligibility"),
    path("scholarships/applicationForm_status/", views.application_form_status, name="applicationForm_status"),
    path("scholarship/<int:id>/details/", views.scholarship_details, name="scholarship_details"),
    # path("scholarship/<int:id>/bookmark/", views.bookmark_scholarship, name="bookmarkScholarship"),
    path("scholarships/bookmark/", views.bookmark_scholarship, name="bookmarkScholarship"),

    path("scholarships/apply", views.application_form, name="applicationForm"), # create path
    path("application/<int:id>/edit/<int:page>", views.edit_application_form, name="edit_application_form"), #edit path
    # path("applicationForm/", views.application_form, name="applicationForm"),
    # path("applicationForm/<int:id>/", views.application_form, name="applicationForm"),
    # path("applicationForm_p2/<int:id>/", views.application_form_p2, name="applicationForm_p2"),
    # path("applicationForm_p3/<int:id>/", views.application_form_p3, name="applicationForm_p3"),
    # path("applicationForm_p4/<int:id>/", views.application_form_p4, name="applicationForm_p4"),
    
    # path("scholarship/<int:id>/applicationForm/", views.application_form, name="applicationForm"),
    # path("scholarship/<int:id>/applicationForm_p2/", views.application_form_p2, name="applicationForm_p2"),
    # path("scholarship/<int:id>/applicationForm_p3/", views.application_form_p3, name="applicationForm_p3"),
    # path("scholarship/<int:id>/applicationForm_p4/", views.application_form_p4, name="applicationForm_p4"),
    path("trackApplication/", views.trackApplication, name="trackApplication")
]