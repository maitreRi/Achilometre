import requests
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class WeatherView(LoginRequiredMixin, TemplateView):
    template_name = "weather/weather.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        API_KEY = "2be0182221af4145b08142954250107"
        CITY = "Palma"
        LANGUAGE = "fr"

        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&lang={LANGUAGE}&aqi=yes"

        try:
            response = requests.get(url)
            data = response.json()
            context["weather"] = {
                "city": data["location"]["name"],
                "country": data["location"]["country"],
                "localtime": data["location"]["localtime"],
                "temp_c": data["current"]["temp_c"],
                "uv": data["current"]["uv"],
                "condition": data["current"]["condition"]["text"],
                "icon": data["current"]["condition"]["icon"],
                "humidity": data["current"]["humidity"],
                "wind_kph": data["current"]["wind_kph"],
                "feelslike_c": data["current"]["feelslike_c"],
            }
        except Exception as e:
            context["weather_error"] = f"Erreur lors de la récupération des données météo : {e}"

        return context
