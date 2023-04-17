from django.shortcuts import render
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/tasks_list.html'
    context_object_name = 'tasks_list'

    def grt_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_list'] = context['tasks_list'].filter(user=self.request.user)
        context['count'] = context['tasks_list'].filter(complete=False).count()
        return context
            
        


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/task_details.html'
    context_object_name = 'task_details'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')
    context_object_name = 'task_create'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    context_object_name = 'task_delete'
    template_name = 'base/task_delete.html'


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')
