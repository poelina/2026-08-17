from django.contrib import messages  # Для вывода уведомлений 
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy  # Для отложенного построения URL
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Category, Task


class IndexView(View):

    def get(self, request):
        tasks = Task.objects.all()
        
        category_id = request.GET.get('category')
        if category_id:
            tasks = tasks.filter(category_task_id=category_id)

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(is_completed=True).count()
        pending_tasks = total_tasks - completed_tasks

        task_categories = Category.objects.all()

        context = {
            "tasks": tasks,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "categories": task_categories,
        }

        return render(request, "main.html", context) 


class TaskListView(ListView):
    model = Task
    template_name = "main.html" 
    context_object_name = "tasks" 
    ordering = ['is_completed', '-created_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(category_task_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_tasks = self.get_queryset()
        context['total_tasks'] = current_tasks.count()
        context['completed_tasks'] = current_tasks.filter(is_completed=True).count()
        context['pending_tasks'] = context['total_tasks'] - context['completed_tasks']

        context['categories'] = Category.objects.all()
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "taskview.html" 
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Задача: {self.object.title}"
        context['categories'] = Category.objects.all()

        return context
