from django.urls import path
from . import views
from login import views as login_views
from landingpage import views as landingpage_views

urlpatterns = [
    path("", views.index, name="reviewer"),
    path("<int:app_id>/", views.review, name="reviewer_with_id"),
    path("review/", views.review, name="review"),
    path("details/", views.details, name="details"),
    path('logout/', login_views.logout_view, name='logout'),
    path("", landingpage_views.index, name='landingpage'),

    #Manage Account URL
    path('changepassword/', login_views.change_password, name='reviewer_change_password'),
    path('changesecurityquestion/', login_views.update_security_questions, name='reviewer_update_security_questions'),

    #Dashboard
    path('api/', views.ChartData.as_view(), name='api_data'),
]