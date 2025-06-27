from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect


def custom_logout(request):
    logout(request)
    return redirect('login')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks_list.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'status']
    template_name = 'todos/task_form.html'

    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'status']
    template_name = 'todos/tasks_list.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todos/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
