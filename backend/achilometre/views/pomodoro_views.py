from django.views.generic import TemplateView


class PomodoroView(TemplateView):
    template_name = "pomodoro/pomodoro.html"
