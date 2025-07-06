from django.views.generic import TemplateView
from datetime import date
from achilometre.models import Task
from achilometre.context_processors import weather_context
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.urls import reverse


class HomeView(TemplateView):
    template_name = "home/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer toutes les tâches
        task_events = [
            {
                "title": f"📝 {(task.title)}",
                "start": task.due_date.isoformat(),
                "url": reverse("task_edit", args=[task.id]),
                "color": task.color
            }
            for task in Task.objects.all()
        ]

        # Récupérer la météo (UV)
        weather_events = []
        try:
            weather = weather_context(self.request)["global_weather"]

            uv_entries = weather.get("history", {}).get("uv", [])

            if uv_entries:
                # Trouver l'entrée avec la valeur UV max
                max_uv_entry = max(uv_entries, key=lambda x: x["value"])
                weather_events.append({
                    "title": f"☀ UV max {max_uv_entry['value']}",
                    "start": max_uv_entry["time"][:10]  # format 'YYYY-MM-DD'
                })
        except Exception as e:
            # En cas d’erreur, ne rien faire ou logger l’erreur
            print(f"Erreur récupération météo : {e}")

        # Fusionner événements tâches + météo UV max
        context["calendar_events"] = json.dumps(task_events + weather_events, cls=DjangoJSONEncoder, ensure_ascii=False)

        # Ajouter météo courante et tâches du jour pour template
        context["weather"] = weather_context(self.request)["global_weather"]
        today = date.today()
        context["today_tasks"] = Task.objects.filter(due_date=today)

        return context
