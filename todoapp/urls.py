from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
]
