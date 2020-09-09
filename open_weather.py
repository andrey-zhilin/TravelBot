import requests
from pprint import pprint
import api_token
import datetime

lon = 30.315785
lat = 59.939039

url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly&appid={api_token.weather_token}'

weather_request = requests.get(url)
curent_temp = weather_request.json()['current']['temp']
curent_wind_speed = weather_request.json()['current']['wind_speed']

print(f'Сейчас:\nТемпература воздуха {curent_temp} °C\nСкорость ветра {curent_wind_speed}')

for day in weather_request.json()['daily']:
    timestamp = day['dt']
    day_temp = day['temp']['day']
    day_temp_min = day['temp']['min']
    day_temp_max = day['temp']['max']
    day_wind_speed = day['wind_speed']
    human_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    print(f"{human_date}: Температура воздуха {day_temp} | Максимум {day_temp_max} °C | Минимум {day_temp_min} °C | Скорость ветра {day_wind_speed}")
    
#pprint(weather_request.json())