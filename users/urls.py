from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('users/delete/', views.user_delete, name='user-delete'),
]