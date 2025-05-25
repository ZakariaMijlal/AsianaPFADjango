from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project-list'),
    path('projects/<int:pk>/', views.project_detail, name='project-detail'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('projects/create/', views.project_create, name='project-create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project-edit'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task-edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task-delete'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project-delete'),
    
]
    
