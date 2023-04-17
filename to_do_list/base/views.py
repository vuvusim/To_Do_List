from django.shortcuts import render, redirect
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
# Class view for user creation
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    # This function saves user creation form and if its all filled out login with created user
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # This function redirects user (if loged in) to a main page when it tries to reach register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# class view to make a list of model (Task). 
# LoginMixin allows to see content just for loged in users, if not loged in - redirects to login page
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/tasks_list.html'
    context_object_name = 'tasks_list'

    # Function to filter out tasks for specific user and count not complete tasks for that user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_list'] = context['tasks_list'].filter(user=self.request.user)
        context['count'] = context['tasks_list'].filter(complete=False).count()

        # Search_input filters out the (TaskList) view (search bar)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks_list'] = context['tasks_list'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context
            

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/task_details.html'
    context_object_name = 'task_details'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    context_object_name = 'task_create'

    # This function in this case validate user (submiting the form automatically assigns the 'task' to loged in user)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    context_object_name = 'task_delete'
    template_name = 'base/task_delete.html'


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
