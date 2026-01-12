from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.index, name="login"),
    path("signup/", views.signup, name="signup"),
    path("securityquestion/", views.securityquestion, name="securityquestion"),
]