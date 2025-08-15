import os
from django.http import JsonResponse
from django.contrib.staticfiles import finders
from django.views.generic import TemplateView


class LoomisView(TemplateView):
    template_name = "loomis/loomis.html"


def loomis_count(request):
    # Trouver le chemin réel du dossier loomis
    loomis_dir = finders.find("loomis")
    if not loomis_dir or not os.path.isdir(loomis_dir):
        return JsonResponse({"count": 0})

    count = len([
        f for f in os.listdir(loomis_dir)
        if f.startswith("face") and f.lower().endswith(".jpg")
    ])
    return JsonResponse({"count": count})
