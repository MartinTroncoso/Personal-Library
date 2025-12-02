from django.urls import path

import Application.views as views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("biblioteca", views.biblioteca_view, name="biblioteca"),
    path("add_libro", views.add_libro_view, name="add_libro"),
    path("libro/<int:id>", views.libro_view, name="libro"),
    path("delete_libro/<int:id>", views.delete_libro_view, name="delete_libro"),
    path("libro_del_dia", views.libro_del_dia_view, name="libro_del_dia"),
    path("csrf", views.csrf, name="csrf"),
    path("test-error", views.test_error, name="test-error"),
]
