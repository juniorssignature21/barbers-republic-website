from django.urls import path
from . import views as app_views

app_name = "app"

urlpatterns = [
    path("", app_views.index, name="index"),
    path("about/", app_views.about, name="about"),
    path("register_user/", app_views.register_user, name="register_user"),
    path("login_user/", app_views.login_user, name="login_user"),
    path("logout_user/", app_views.logout_user, name="logout_user"),
]
