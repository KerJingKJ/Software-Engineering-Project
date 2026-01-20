from django.urls import path
from . import views
from login import views as login_views
from landingpage import views as landingpage_views
urlpatterns = [
    path("", views.index, name="reviewer"),
    path("review/", views.review, name="review"),
    path("details/", views.details, name="details"),
    path('logout/', login_views.logout_view, name='logout'),
    path("", landingpage_views.index, name='landingpage'),
]