import requests
import folium
import json
import numpy as np
import tensorflow
import time
import os

API_KEY = os.getenv("WEATHERAPI_KEY")

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
    [39.16014, 20.98561],  # ARTA
    [37.97025, 23.72247],  # ATTICA
    [40.416665, 23.499998],# THESSALONIKI
    [35.48717, 24.07344],  # CHANIA
    [38.36778, 26.13583],  # CHIOS
    [37.08333, 25.15],     # CYCLADES ISLANDS
    [41.15283, 24.1473],   # DRAMA
    [40.8026, 22.04751],   # EDESSA
    [38.04135, 23.54295],  # ELEFSINA
    [41.433, 26.55],       # ORESTIADA
    [39.36, 20.19],        # FILIATES
    [40.78197, 21.40981],  # FLORINA
    [40.08452, 21.42744],  # GREVENA
    [35.32969, 25.12985],  # IRAKLEION
    [35.01186, 25.74234],  # AGIOS NIKOLAOS
    [39.66486, 20.85189],  # IOANNINA
    [39.36485, 21.92191],  # KARDITSA
    [38.91218, 21.79836],  # KARPENISI
    [40.52165, 21.26341],  # KASTORIA
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
    [39.11, 26.55472],     # MYTILINI
    [37.568497726, 22.78749685], # NAFPLIO
    [39.28015, 22.81819],  # NEA ANCHIALOS
    [38.24444, 21.73444],  # PATRA
    [38.95617, 20.7505],   # PREVEZA
    [35.36555, 24.48232],  # RETHYMNO
    [39.55493, 21.76837],  # TRIKALA
    [37.50889, 22.37944],  # TRIPOLI
    [40.52437, 22.20242],  # VEROIA
    [41.13488, 24.888],    # XANTHI
    [37.7999968, 20.749997], # ZAKYNTHOS
    [38.499998, 24.0],     # CHALKIDA
    [36.44083, 28.2225],   # RHODOS
    [41.08499, 23.54757],  # SERRES
    [40.84995, 25.87644],  # ALEXANDROUPOLI
    [37.06, 22.44]         # KOSMAS
]


risk_levels = {
    'very_low': 0.15,
    'low': 0.30,
    'medium': 0.50,
    'high': 0.60,
    'very_high': 0.70
}

# ==========================
# WeatherAPI-based function
# ==========================
def get_weather(city):
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {"key": API_KEY, "q": city + ",GR", "days": 2, "aqi": "no", "alerts": "no"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    forecast_days = data["forecast"]["forecastday"]
    if len(forecast_days) < 2:
        raise ValueError(f"No forecast for next day for {city}")

    next_day = forecast_days[1]

    # Get 14:00 hour
    hour_data = None
    for hour in next_day["hour"]:
        if hour["time"].split(" ")[1] == "14:00":
            hour_data = hour
            break

    if hour_data is None:
        raise ValueError(f"14:00 hour not found for {city}")

    temp_c = hour_data["temp_c"]
    dew_c = hour_data["dewpoint_c"]
    wind_mph = hour_data["wind_mph"]
    wind_ms = round(wind_mph / 2.237, 2)

    if wind_ms < 2:
        wind_ms = 2

    return temp_c, wind_ms, dew_c

########################
# ==========================
# Main mapping and prediction
# ==========================

greece_bounds = [[34.8, 19.0], [41.8, 26.5]]

m = folium.Map(
    location=[38.0, 19.0],
    zoom_start=6,
    max_bounds=True,      # restrict panning outside bounds
    min_zoom=6,
    max_zoom=6,
    no_touch=True,
    zoom_control=False,
    doubleClickZoom=False,
    scrollWheelZoom=False,
    dragging=False,
    tiles='OpenStreetMap' # Esri.WorldPhysical , Esri.WorldTopoMap
)

# Apply the bounds
m.fit_bounds([[35.0, 32.0], [42.0, 15.0]])


# Optional: add a rectangle to visualize bounds
#folium.Rectangle(
#    bounds=greece_bounds,
#    color='blue',
#    fill=False,
#).add_to(m)
##################################

clf = tensorflow.keras.models.load_model('working_model/nn_model_1.h5', compile=False)

for city, loc in zip(cities, locations):
    # Skip specific cities if needed
    if city in ['PREVEZA', 'ELEFSINA', 'VEROIA']:
        continue

    try:
        temperature, wind, dew = get_weather(city)
        print(f"{city}: Temp={temperature}°C, Wind={wind} m/s, Dew={dew}°C")

        # Normalize wind if required by prediction model
        if wind <= 2:
            wind = 2

        # Predict probability
        x = np.array([[temperature, wind, dew]], dtype=np.float32)
        probability = clf.predict(x)[0][0]  # adjust depending on model output

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

        # Add marker to map
        folium.CircleMarker(
            location=loc,
            radius=12,
            fill=True,
            fill_opacity=opacity,
            fill_color=color,
            color=color,
            tooltip=f"{city}: {label}"
        ).add_to(m)

    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")

m.save('map.html')
