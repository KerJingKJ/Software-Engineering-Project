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
    
    
    path("application/<int:id>/details/", views.view_application_details, name="view_application_details"),
    path("application/<int:id>/family/", views.view_family_background, name="view_family_background"),
    path("application/<int:id>/interview/", views.schedule_interview, name="schedule_interview"),
    path("application/<int:id>/decision/", views.decision_page, name="decision_page"),
    path("application/<int:id>/mark/", views.view_reviewer_mark, name="view_reviewer_mark"),
    
    path('changepassword/', login_views.change_password, name='committee_change_password'),
    path('changesecurityquestion/', login_views.update_security_questions, name='committee_update_security_questions'),

    
    path('api/', views.ChartData.as_view(), name='committee_api_data'),
    path('api/admin', views.AdminChartData.as_view(), name='admin_api_data'),

    #notification
    path("notification/markasread/", views.committee_mark_all_read, name="committee_mark_all_read"),
    
]