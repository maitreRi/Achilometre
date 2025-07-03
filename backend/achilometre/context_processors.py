import requests
from datetime import datetime, timedelta
import json


def weather_context(request):
    API_KEY = "2be0182221af4145b08142954250107"
    CITY = "Palma"
    LANGUAGE = "fr"

    normal_values = {
        "uv": 7.0,
        "pm2_5": 23.0,
    }

    def compare(value, normal):
        if value is None:
            return {"value": None, "normal": normal, "class": "text-gray-400"}
        diff = (value - normal) / normal * 100
        if diff > 50:
            return {"value": value, "normal": normal, "class": "text-red-600 font-bold"}
        elif diff < -5:
            return {"value": value, "normal": normal, "class": "text-green-600 font-bold"}
        else:
            return {"value": value, "normal": normal, "class": "text-orange-600 font-bold"}

    weather_data = {}
    history_uv = []
    history_pm25 = []

    # Date today
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]  # 7 jours, du plus ancien au plus récent

    try:
        # Requête météo actuelle (comme avant)
        url_current = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&lang={LANGUAGE}&aqi=yes"
        response = requests.get(url_current, timeout=5)
        data = response.json()
        current = data["current"]
        air_quality = current.get("air_quality", {})



        # Récupérer les heures pour les deux derniers jours
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, -1, -1)]  # hier et aujourd'hui

        for date_str in dates:
            url_hist = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={CITY}&dt={date_str}&aqi=yes"
            resp_hist = requests.get(url_hist, timeout=5)
            hist_data = resp_hist.json()

            hours = hist_data.get("forecast", {}).get("forecastday", [])[0].get("hour", [])
            for hour in hours:
                time = hour.get("time")  # format: "2025-07-02 14:00"
                uv = hour.get("uv")
                pm25 = hour.get("air_quality", {}).get("pm2_5")
                history_uv.append({"time": time, "value": uv})
                history_pm25.append({"time": time, "value": pm25})

        weather_data = {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "localtime": data["location"]["localtime"],
            "temp_c": current["temp_c"],
            "temp_f": current["temp_f"],
            "is_day": current["is_day"],
            "condition_text": current["condition"]["text"],
            "icon": current["condition"]["icon"],
            "wind_kph": current["wind_kph"],
            "humidity": current["humidity"],
            "feelslike_c": current["feelslike_c"],
            "uv": compare(current.get("uv"), normal_values["uv"]),
            "air_quality": {
                "co": compare(air_quality.get("co"), 10000.0),
                "no2": compare(air_quality.get("no2"), 40.0),
                "o3": compare(air_quality.get("o3"), 100.0),
                "pm2_5": compare(air_quality.get("pm2_5"), normal_values["pm2_5"]),
                "pm10": compare(air_quality.get("pm10"), 24.0),
            },
            "history": {
                "uv": history_uv,
            }
        }

    except Exception as e:
        weather_data = {
            "error": f"Erreur météo : {e}"
        }
    history_json = json.dumps(weather_data.get("history", {}))
    return {
        "global_weather": {
            **weather_data,
            "history_json": history_json,
        }
    }
