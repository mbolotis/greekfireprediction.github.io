import requests
import folium
import json
import numpy as np
import tensorflow as tf
import time
import os

## API_KEY = os.getenv("WEATHERAPI_KEY")
API_KEY = "50a73089557740eb969222141251707"

if not API_KEY:
    raise RuntimeError("WEATHERAPI_KEY is not set")

cities = [
    'AGRINIO',
    'ALIARTOS',
    'ANDRAVIDA',
    'ARTA',
    'ATTICA',
    'THESSALONIKI',
    'CHANIA',
    'CHIOS',
    'PAROS',
    'DRAMA',
    'EDESSA',
    'ELEFSINA',
    'ORESTIADA',
    'FILIATES',
    'FLORINA',
    'GREVENA',
    'IRAKLEION',
    'AGIOS NIKOLAOS',
    'IOANNINA',
    'KARDITSA',
    'KARPENISI',
    'KASTORIA',
    'KATERINI',
    'KAVALA',
    'KEFALONIA',
    'KERKYRA',
    'KILKIS',
    'KOMOTINI',
    'KOS',
    'KOZANI',
    'LAMIA',
    'LARISA',
    'LEFKADA',
    'METHONI',
    'MYTILINI',
    'NAFPLIO',
    'NEA ANCHIALOS',
    'PATRA',
    'PREVEZA',
    'RETHYMNO',
    'TRIKALA',
    'TRIPOLI',
    'VEROIA',
    'XANTHI',
    'ZAKYNTHOS',
    'CHALKIDA',
    'RHODES',
    'SERRES',
    'ALEXANDROUPOLI',
    'KOSMAS'
]

locations = [
    [38.62139, 21.40778],  # AGRINIO
    [38.36667, 23.1],      # ALIARTOS
    [37.90588, 21.26936],  # ANDRAVIDA
    [39.16014, 21.02561],  # ARTA
    [37.97025, 23.72247],  # ATTICA
    [40.416665, 23.499998],# THESSALONIKI
    [35.48717, 23.9],  # CHANIA
    [38.36778, 26.13583],  # CHIOS
    [37.08333, 25.15],     # PAROS (displayed as CYCLADES ISLANDS)
    [41.2883, 24.1473],   # DRAMA
    [40.8026, 22.04751],   # EDESSA
    [38.04135, 23.54295],  # ELEFSINA
    [41.433, 26.25],       # ORESTIADA
    [39.36, 20.49],        # FILIATES
    [40.78197, 21.40981],  # FLORINA
    [40.0, 21.32744],  # GREVENA
    [35.12, 25.12985],  # IRAKLEION
    [35.01186, 25.74234],  # AGIOS NIKOLAOS
    [39.76486, 20.85189],  # IOANNINA
    [39.35485, 21.92191],  # KARDITSA
    [38.91218, 21.79836],  # KARPENISI
    [40.32165, 21.11],  # KASTORIA
    [40.26956, 22.50608],  # KATERINI
    [40.93959, 24.40687],  # KAVALA
    [38.249999, 20.499998],# KEFALONIA
    [39.62069, 19.91975],  # KERKYRA
    [40.99302, 22.87433],  # KILKIS
    [41.11917, 25.40535],  # KOMOTINI
    [36.8499966, 27.2333324], # KOS
    [40.30069, 21.78896],  # KOZANI
    [38.9, 22.43333],      # LAMIA
    [39.643452, 22.413208],# LARISA
    [38.7166638, 20.6499974], # LEFKADA
    [37.249999, 21.83333], # METHONI
    [39.11, 26.25472],     # MYTILINI
    [37.76, 22.78749685], # NAFPLIO
    [39.28015, 22.81819],  # NEA ANCHIALOS
    [37.94444, 21.93444],  # PATRA
    [38.95617, 20.7505],   # PREVEZA
    [35.36555, 24.48232],  # RETHYMNO
    [39.75493, 21.76837],  # TRIKALA
    [37.50889, 22.37944],  # TRIPOLI
    [40.52437, 22.20242],  # VEROIA
    [41.13488, 24.888],    # XANTHI
    [37.7999968, 20.749997], # ZAKYNTHOS
    [38.499998, 24.0],     # CHALKIDA
    [36.08083, 28.0225],   # RHODES
    [41.08499, 23.54757],  # SERRES
    [41.04995, 25.97644],  # ALEXANDROUPOLI
    [37.06, 22.64]         # KOSMAS
]

risk_levels = {
    'very_low': 0.15,
    'low': 0.30,
    'medium': 0.50,
    'high': 0.60,
    'very_high': 0.70
}

# Display-name overrides for map/tooltips (API query still uses the original city name)
display_names = {
    'PAROS': 'CYCLADES ISLANDS',
    'PATRA': 'ACHAIA'
}

def get_weather_hours(city, target_hours=None):
    # Collect next-day hourly weather for the given hours and return a list of dicts
    if target_hours is None:
        target_hours = [f"{h:02d}:00" for h in range(7, 19)]  # 07:00..18:00

    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {"key": API_KEY, "q": f"{city},GR", "days": 2, "aqi": "no", "alerts": "no"}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    forecast_days = data["forecast"]["forecastday"]
    if len(forecast_days) < 2:
        raise ValueError(f"No forecast for next day for {city}")

    next_day = forecast_days[1]

    results = []
    for hour in next_day["hour"]:
        hhmm = hour["time"].split(" ")[1]  # e.g., "14:00"
        if hhmm in target_hours:
            temp_c = float(hour["temp_c"])
            dew_c = float(hour["dewpoint_c"])
            wind_mph = float(hour["wind_mph"])
            wind_ms = round(wind_mph / 2.237, 2)
            wind_ms = max(wind_ms, 2.0)  # clamp if model expects min 2 m/s
            results.append({"time": hhmm, "temp": temp_c, "dew": dew_c, "wind": wind_ms})

    if not results:
        raise ValueError(f"No target hours found for {city}")

    return results

## Map setup
greece_bounds = [[34.8, 19.0], [41.8, 26.5]]
m = folium.Map(location=[37.97025, 24.12247],
               zoom_start=6,
               no_touch=True,
               zoom_control=False,
               doubleClickZoom=False,
               scrollWheelZoom=False,
               dragging=False)

m.fit_bounds(greece_bounds)

## Load model
clf = tf.keras.models.load_model('working_model/nn_model_1.h5', compile=False)

for city, loc in zip(cities, locations):
    # Skip specific cities if needed
    if city in ['PREVEZA', 'ELEFSINA', 'VEROIA']:
        continue

    try:
        hourly = get_weather_hours(city)  # list of dicts: time, temp, dew, wind

        best_time = None
        probability = None

        for h in hourly:
            x = np.array([[h["temp"], h["wind"], h["dew"]]], dtype=np.float32)
            prob = float(clf.predict(x, verbose=0)[0][0])
            if probability is None or prob > probability:
                probability = prob
                best_time = h["time"]

        # Determine color and opacity
        if probability <= risk_levels['very_low']:
            color = 'darkgreen'
            opacity = 0.3
            label = 'Very Low Risk'
        elif probability <= risk_levels['low']:
            color = 'darkgreen'
            opacity = 0.6
            label = 'Low Risk'
        elif probability <= risk_levels['medium']:
            color = 'orange'
            opacity = 0.6
            label = 'Medium Risk'
        elif probability <= risk_levels['high']:
            color = 'darkred'
            opacity = 0.6
            label = 'High Risk'
        else:
            color = 'darkred'
            opacity = 0.8
            label = 'Very High Risk'

        display_city = display_names.get(city, city)

        folium.CircleMarker(
            location=loc,
            radius=12,
            fill=True,
            fill_opacity=opacity,
            fill_color=color,
            color=color,
            tooltip=f"{display_city}: {label}"
        ).add_to(m)

        print(f"{display_city}: best hour={best_time}, probability={probability:.3f}")

    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")

m.save('map.html')