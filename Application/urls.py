
from django.urls import path

import Application.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('biblioteca', views.biblioteca_view, name='biblioteca'),
    path('add_libro', views.add_libro_view, name='add_libro'),
    path('libro/<int:id>', views.libro_view, name='libro'),
    path('delete_libro/<int:id>', views.delete_libro_view, name='delete_libro'),
]