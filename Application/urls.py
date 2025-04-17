
from django.urls import path

import Application.views as views

urlpatterns = [
    path('', views.index),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout, name='logout'),
]