from django.urls import path
from .views import login_view, logout_json

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_json, name="logout"),
]
