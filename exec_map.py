from bs4 import BeautifulSoup
import requests
import folium
import json
import os
import time
import pickle
import branca
import tensorflow
import lxml

def home():
  city = ['AGRINION',
      'ALIARTOS',
      'ANDRAVIDA',
      'ARTA',
      'ATTICA',
      'THESSALONIKI',
      'CHANIA',
      'CHIOS',
      'CYCLADES ISLANDS',
      'DRAMA',
      'EDESSA',
      'ELEFSINA',
      'EVROS',
      'FILIATES',
      'FLORINA',
      'GREVENA',
      'HERAKLEIO',
      'IERAPETRA',
      'IOANNINA',
      'KARDITSA',
      'KARPENISI',
      'KASTORIA',
      'KATERINI',
      'KAVALA',
      'KEFALLONIA',
      'KERKIRA',
      'KILKIS',
      'KOMOTINI',
      'KOS',
      'KOZANI',
      'LAMIA',
      'LARISA',
      'LEYKADA',
      'METHONI',
      'MITILINI',
      'NAFPLIO',
      'NEA ANCHIALOS',
      'PATRA',
      'PREVEZA',
      'RETHYMNON',
      'TRIKALA',
      'TRIPOLI',
      'VEROIA',
      'XANTHI',
      'ZAKINTHOS',
      'EVIA',
      'RHODOS',
      'SERRES',
      'ALEXANDROUPOLI',
      'KOSMAS'
      ]
  url = [
    'https://weather.com/weather/today/l/f3c461145e9d163303b1f6d81bb0e6cf7022d1795ee2789636f806132ccc6887',
    'https://weather.com/weather/today/l/564a252e022c554de7ff5c647a9ecf1371b108f1d8e31eb485f299fe9cc282d0',
    'https://weather.com/weather/today/l/3a3e8cecaa547df1fc60969f44698d1f6c55fd5d6dc143ddbc52ee66c853c367',
    'https://weather.com/weather/today/l/d7276d14e178e1f1bb73acf0a670418a890a743752257c1d57aa2dc3b40db2e4',
    'https://weather.com/weather/today/l/5892dfe2c539df7d42cdbd8f9cfda434f21f6c2a63cec329fa598d4e5aa3d584',
    'https://weather.com/weather/today/l/5e8dd9573df44b0132d3ebf1c7cdfad2688191d767eefab5ee3a85edfe8577aa',
    'https://weather.com/weather/today/l/340284fb4b94675bf1f78b28fb3bb85b057e221cfbd74a647f5dba9ba522162e',
    'https://weather.com/weather/today/l/7e6219e5dd42b9d850ec5767768529abdd686b85639a387afae1725dd87c4f8e',
    'https://weather.com/weather/today/l/ebbc5c0838f4da0433a65415f9f438121f82600295702d2b938293c3813a396c',
    'https://weather.com/weather/today/l/8aebcff6df1aea6d9611bb31bad33829bd48e3ebeb45acfec6ed2d060ea138b5',
    'https://weather.com/weather/today/l/015f6e8d0a4cee9aa2ef30ea781deda9c700597d0b2fd7a019bc17f341cd8192',
    'https://weather.com/weather/today/l/a71d288ea6f38e071cb098318f1b886c8d17d15d6d01fd795b7622388e339230',
    'https://weather.com/weather/today/l/9af701f17a94dce0fad86bad2b1f6d90bfd25f2045b23b837f03040baf124353',
    'https://weather.com/weather/today/l/abc3dafa636f60cd1eafe1b02d7b29c9d1ac51174e61ddad1965846455165e42',
    'https://weather.com/weather/today/l/0c8c9b64abc89e48f04ddf985e2fb41ff831f95958d5296cdcb477ae2a98586e',
    'https://weather.com/weather/today/l/f07ef82b3a79869022e4077c1f04f7b40288575f77313c08cf15f1ff31b6fc4f',
    'https://weather.com/weather/today/l/4f3800462bc69d7213931d2a3ed41b2ea6f1e8ce1925bfdce551292d2d6fdb44',
    'https://weather.com/weather/today/l/ae9dc8310c239deb80e605bf30d5c82012e00e76ac2ce4837cec90e7740f6f9c',
    'https://weather.com/weather/today/l/7a5351e10b7d52f667e9f0a0b71140bd176ef6cd09edf748f7e28a607baeb3e8',
    'https://weather.com/weather/today/l/a4e857eb810a372eebe188fc06c9adcf821e0df8d1ee6cbbdfc5ecf50e979010',
    'https://weather.com/weather/today/l/bf4bbad1530df2cbcc1b4dbf547645f645c2e091244fd9e757874601800dc622',
    'https://weather.com/weather/today/l/44114afd18d51b90206ceecf0e548aa87fe4ccfa9e6e746022ac3bd079d429c5',
    'https://weather.com/weather/today/l/bdaed0eb744208d26b61d9b32959715d3e864decf0c45419d1414a23beb92fc9',
    'https://weather.com/weather/today/l/10cc52a44f182fa8217e9bc9459be6b4242cec49cbb46bb5e045f323bf679197',
    'https://weather.com/weather/today/l/7b023255fc2f362dddc99f5d9b7b47a7acd4a8a038c7f5a0fc46394d92d22809',
    'https://weather.com/weather/today/l/264e45ed143e8bb82f047febaeaf2dcd2a4aa299ba0765e44de11399504447e1',
    'https://weather.com/weather/today/l/a4da9340a16098f33cf08913ea7ccb4c2b4efa4af10999ac51cf2b4c5dc63077',
    'https://weather.com/weather/today/l/190b6f4f88000a8b417cda928c07564297eabf82de2f0c0a659c4446837594c3',
    'https://weather.com/weather/today/l/06d776da1d8b4aa5b32e54c293a2205eae2f52d9276c2646eb115814387157de',
    'https://weather.com/weather/today/l/d890f06b9fb42599d5cbae2b6cf48edc652cdbd78779bee14dd4cddf94c8e063',
    'https://weather.com/weather/today/l/3e2d12f311db37f3c7b24583da612bd94770bb2178bb76e49683931396e9f90f',
    'https://weather.com/weather/today/l/0f1602687f8bdee344b3eebd930d9fb9a8d831e1491b1799d0c9e3fc6db27c6b',
    'https://weather.com/weather/today/l/9531ff702407d64887897f9060a9bccd40bdc0d76408c113e5d4c42fe3f1f638',
    'https://weather.com/weather/today/l/f729cda3cc616efcfe897d3a8c0e390faff7379f25ad9549aa9ab21ee812b06f',
    'https://weather.com/weather/today/l/c23295695fd2d05302b380463665a04de841a5ee9024f8018fd16e91f54e7650',
    'https://weather.com/weather/today/l/5550bb2298fbe0a38036e3c4565349d3530265a735ded45ab3599597ba2ee288',
    'https://weather.com/weather/today/l/faf163f91aebcd3ce8300e29579bf29640cd2c8e5dd4b9772693c48fc849a5c3',
    'https://weather.com/weather/today/l/a8c1d5fa8f854f3e5c626109483f1542b6eb8f29924330ccc44ffc07e3050bd7',
    'https://weather.com/weather/today/l/6f88b8cef64c03bb9d49f464c4f018bd2e1a47b97a176789ce1b98e429f4cf86',
    'https://weather.com/weather/today/l/6ef326738737e257d0398aff4616204e09e6c7a5bcb50754d5a57dd0e73ef8ab',
    'https://weather.com/weather/today/l/fea4d233efd8a39b1185aefc07b8b7f65db047f5ff373f6de62daa6fa88dfc99',
    'https://weather.com/weather/today/l/ffe570225cade5303ca08ac4f9df7c3942bb3618542fd50a3daa9885b054a4c5',
    'https://weather.com/weather/today/l/8f31dcb6141227050e32ce94817d164c606e66a00c7ae89f6c5984239cc9f90c',
    'https://weather.com/weather/today/l/042154cb223601cc19cdb30e4f346f5da99a8521e0a8f90af3bf55fae10317ea',
    'https://weather.com/weather/today/l/06084c28e56fbbf86201be7471cc22c4a943a833fea354d73d6993280b599ab8',
    'https://weather.com/weather/today/l/52c969cb7f3ffb2c75f2777437be9354c5f5840000bb0b2374d1817c3aa5b796',
    'https://weather.com/weather/today/l/f0de8849c0ac9f287c8d68536eb02828142419816360f365c396c7c9782f6819',
    'https://weather.com/weather/today/l/b7d1d8d61e8f4845487c4ba65c76b2e79999fd03df2e1581a8f522083fdf6e07',
    'https://weather.com/weather/today/l/cc6e96f5bb209f76d88348dccb63efa01519ed41cecff748814126a05f1f285c',
    'https://weather.com/weather/today/l/b35d64452d5637580b06e8beda5b6b23701c11eb915c019945f7d4055f236291'
  ]
  location = [
    [38.62139, 21.40778],
    [38.36667, 23.1],
    [37.90588, 21.26936],
    [39.16014, 20.98561],
    [37.97025, 23.72247],
    [40.416665, 23.499998],
    [35.48717, 24.07344],
    [38.36778, 26.13583],
    [37.08333, 25.15],
    [41.15283, 24.1473],
    [40.8026, 22.04751],
    [38.04135, 23.54295],
    [41.433, 26.55],
    [39.36, 20.19],
    [40.78197, 21.40981],
    [40.08452, 21.42744],
    [35.32969, 25.12985],
    [35.01186, 25.74234],
    [39.66486, 20.85189],
    [39.36485, 21.92191],
    [38.91218, 21.79836],
    [40.52165, 21.26341],
    [40.26956, 22.50608],
    [40.93959, 24.40687],
    [38.249999, 20.499998],
    [39.62069, 19.91975],
    [40.99302, 22.87433],
    [41.11917, 25.40535],
    [36.8499966, 27.2333324],
    [40.30069, 21.78896],
    [38.9, 22.43333],
    [39.643452, 22.413208],
    [38.7166638, 20.6499974],
    [37.249999, 21.83333],
    [39.11, 26.55472],
    [37.568497726, 22.78749685],
    [39.28015, 22.81819],
    [38.24444, 21.73444],
    [38.95617, 20.7505],
    [35.36555, 24.48232],
    [39.55493, 21.76837],
    [37.50889, 22.37944],
    [40.52437, 22.20242],
    [41.13488, 24.888],
    [37.7999968, 20.749997],
    [38.499998, 24.0],
    [36.44083, 28.2225],
    [41.08499, 23.54757],
    [40.84995, 25.87644],
    [37.06, 22.44]
  ]
  for tmp in range(0, len(city)):
    time.sleep(2)  # avoid spam detection
    c_city = city[tmp]
    c_url = url[tmp]
    c_location = location[tmp][:]
    if c_city != 'PREVEZA' and c_city != 'ELEFSINA' and c_city != 'VEROIA':
      temperature, wind, dew = scraper(c_city, c_url)
      # to feed the prediction algorithm, and return the probability
      if wind <= 2:  # scale as trained data
        print(wind)
        wind = 2
      probability = predict_model(temperature, wind, dew)
      #probability = probability[0][1]  # For SKlearn
      print(c_city, temperature, wind, dew, probability)
      if probability <= risk_levels.get('very_low'):
        folium.CircleMarker(location=c_location, radius=12, fill=True, fill_opacity=0.3, fill_color='darkgreen',
                  color='darkgreen', tooltip=f"{c_city}: {'Very Low Risk'}").add_to(m)
      elif probability <= risk_levels.get('low'):
        folium.CircleMarker(location=c_location, radius=12, fill=True, fill_opacity=0.6, fill_color='darkgreen', 
                  color='darkgreen', tooltip=f"{c_city}: {'Low Risk'}").add_to(m)
      elif probability <= risk_levels.get('medium'):
        folium.CircleMarker(location=c_location, radius=12, fill=True, fill_opacity=0.6, fill_color='orange',
                  color='orange', tooltip=f"{c_city}: {'Medium Risk'}").add_to(m)
      elif probability <= risk_levels.get('high'):
        folium.CircleMarker(location=c_location, radius=12, fill=True, fill_opacity=0.6, fill_color='darkred',
                  color='darkred', tooltip=f"{c_city}: {'High Risk'}").add_to(m)
      else:
        folium.CircleMarker(location=c_location, radius=12, fill=True, fill_opacity=0.8, fill_color='darkred',
                  color='darkred', tooltip=f"{c_city}: {'Very High Risk'}").add_to(m)
      #folium.LayerControl().add_to(m)
  #m.save('/home/runner/work/bet-scaper/bet-scaper/sa_map.html')
  m.save('map.html')
  
def scraper(city, url):
  html_text = requests.get(url).text
  soup = BeautifulSoup(html_text, 'lxml')

  temperature_links = ("TodayDetailsCard--feelsLikeTempValue--2aogo", "CurrentConditions--tempValue--MHmYY", "CurrentConditions--tempValue--1RYJJ", "CurrentConditions--tempValue--3a50n", "CurrentConditions--tempValue--zUBSz", "TodayDetailsCard--feelsLikeTempValue--8WgHV", "DetailsSummary--tempValue--XM5sZ")
  wind_links = ("Wind--windWrapper--1Va1P undefined", "Wind--windWrapper--3Ly7c undefined", "Wind--windWrapper--Ps7cP undefined", "Wind--windWrapper--3aqXJ undefined", "Wind--windWrapper--NsCjc undefined")
  dew_links = ('ListItem--listItem--1r7mf WeatherDetailsListItem--WeatherDetailsListItem--3w7Gx', 'WeatherDetailsListItem--wxData--kK35q', 'WeatherDetailsListItem--wxData--23DP5', 'WeatherDetailsListItem--wxData--2bzvn', 'WeatherDetailsListItem--wxData--2s6HT', "WeatherDetailsListItem--wxData--lW-7H")
  
  temperature = None
  wind = None
  dew = []

  for i in temperature_links:
    temperature = soup.find(class_=i)
    if temperature != None:
      break

  for i in wind_links:
    wind = soup.find(class_=i)
    if wind != None:
      break

  for i in dew_links:
    dew = soup.find_all('div', i)
    if dew != []:
      break

  if temperature == None:
    print(temperature)
    raise IndexError("TEMPERATURE: New Entry - Check Page Source at weather.com") 
  if wind == None:
    raise IndexError("WIND: New Entry - Check Page Source at weather.com") 
  if dew == []:
    raise IndexError("DEW: New Entry - Check Page Source at weather.com") 
              
              
  dew_point = dew[3].span.text              
  wind_speed = ''
  pos = 0

  for i in wind.text:
    if i + wind.text[pos + 1] + wind.text[pos + 2] == 'mph' and pos < len(wind.text) - 1:
      wind_speed = wind.text[pos - 3:pos - 1]
      try:
        wind_speed = float(wind_speed)
        break
      except ValueError:
        wind_speed = float(wind.text[pos - 2:pos - 1])
        break
      except IndexError:
        wind_speed = 10.0  # catch corner cases
        break
    else:
      pos += 1
  temperature_value = float(temperature.text[:-1])
  dew_value = float(dew_point[:-1])
  temperature_value = round((temperature_value - 32) / 1.8, 2)
  wind_speed = round(wind_speed / 2.237)
  dew_value = round((dew_value - 32) / 1.8, 2)
  return temperature_value, wind_speed, dew_value

def predict_model(temperature, wind, dew):
  clf = tensorflow.keras.models.load_model('working_model/nn_model_1.h5', compile=False)  # For Keras
  prediction = clf.predict([[temperature, wind, dew]])
  #prediction = clf.predict_proba([[temperature, wind, dew]])
  return prediction
if __name__ == "__main__":
  with open('world-countries.json') as handle:
    country_geo = json.loads(handle.read())
  for i in country_geo['features']:
    if i['properties']['name'] == 'Greece':
      country = i
      break
  m = folium.Map(location=[37.97025, 24.12247],
           zoom_start=6,
           no_touch=True,
           zoom_control=False,
           doubleClickZoom=False,
           scrollWheelZoom=False,
           dragging=False)
  risk_levels = {
    'very_low': 0.15,
    'low': 0.30,
    'medium': 0.50,
    'high': 0.60,
    'very_high': 0.70
  }
  
home()
