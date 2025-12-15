from django.urls import path
from .views import login_view, logout_json, csrf_token, test_url

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_json, name="logout"),
    path("csrf/", csrf_token, name="csrf_token"),
    path("test_url/", test_url, name="test_url"),
]
