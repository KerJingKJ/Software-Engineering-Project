from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="student"),

    path('notifications/read/', views.mark_all_read, name='mark_all_read'),
    path('notifications/', views.notification_list, name='notification_list'),

    path('eligibility/', views.eligibility_check, name='eligibility_check'),
    
    path("scholarships/", views.scholarship_list, name="scholarship_list"),
    path("scholarships/apply", views.application_form, name="application_form"), # initial create path for applications
    path('scholarship/<int:id>/', views.scholarship_details, name='scholarship_details'),

    # Action to toggle the bookmark
    path('scholarship/<int:scholarship_id>/bookmark/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    
    # "trackApplication"
    path("applications/", views.applications, name="applications"), # view all applications in one page
    
    path('application/<int:id>/', views.application_detail, name='application_detail'), # view application's data
    path('application/<int:id>/reschedule_interview/', views.reschedule_interview, name='reschedule_interview'), # reschedule interview
    path("application/<int:id>/edit/<int:page>", views.edit_application_form, name="edit_application_form"), #edit path
    path("application/<int:id>/status/", views.applicationStatus, name="applicationStatus"), # detailed look into application's status
]