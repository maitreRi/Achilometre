from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ..models import Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time
from django.utils.timezone import now, make_aware
import json


def add_task_api(request):
    try:
        data = json.loads(request.body)
        title = data.get("title")
        due_date_str = data.get("due_date")

        if not title or not due_date_str:
            return JsonResponse({"success": False, "error": "Données incomplètes"})

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

        # Création de la tâche liée à l'utilisateur connecté
        task = Task.objects.create(
            title=title,
            due_date=due_date,
            user=request.user
        )

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@csrf_exempt
@require_POST
def toggle_task_status(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    task.status = 'done' if task.status != 'done' else 'todo'
    task.save()
    return JsonResponse({'success': True})


def custom_logout(request):
    logout(request)
    return redirect('login')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todos/tasks_list.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user,
                                   status__in=['todo', 'in_progress'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_dt = now()  # ✅ timezone-aware
        tasks = list(context['object_list'])

        for task in tasks:
            due_datetime = make_aware(datetime.combine(task.due_date, time.min))
            total_duration = (due_datetime - task.created_at).total_seconds()
            remaining_duration = (due_datetime - now_dt).total_seconds()

            if total_duration > 0:
                percentage_left = max(0, min(100, int((remaining_duration / total_duration) * 100)))
            else:
                percentage_left = 0

            task.percentage_left = percentage_left

        context['object_list'] = tasks
        context['completed_tasks'] = Task.objects.filter(user=self.request.user, status='done')
        context['now'] = now_dt
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'status']
    template_name = 'todos/task_form.html'

    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Tâche créée avec succès.")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'status']
    template_name = 'todos/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, "Tâche mise à jour avec succès.")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todos/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Tâche supprimée avec succès.")
        return super().delete(request, *args, **kwargs)
