from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.index, name="login"),
    path("signup/", views.signup, name="signup"),
    path("securityquestion/", views.securityquestion, name="securityquestion"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("verify_question/", views.verify_question, name="verify_question"),
    path("reset_password_confirm/", views.reset_password_confirm, name="reset_password_confirm"),
    path("setup_profile/", views.setup_profile, name="setup_profile"),
]