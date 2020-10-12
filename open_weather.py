import requests
from pprint import pprint
import api_token
import datetime





def weather_request(lat,lon):

    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly&lang=ru&appid={api_token.weather_token}'

    try:
        weather_request = requests.get(url,timeout=0.5)
        curent_temp = weather_request.json()['current']['temp']
        curent_wind_speed = weather_request.json()['current']['wind_speed']

        print(f'Сейчас:\nТемпература воздуха {curent_temp} °C\nСкорость ветра {curent_wind_speed}')

        for day in weather_request.json()['daily']:
            timestamp = day['dt']
            day_temp = day['temp']['day']
            day_temp_min = day['temp']['min']
            day_temp_max = day['temp']['max']
            day_wind_speed = day['wind_speed']
            human_readble_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            for posible_day_weather in day['weather']:
                if day['weather'].index(posible_day_weather) == 0:
                    primary_condition = posible_day_weather['main']
                    primary_condition_description  = posible_day_weather['description']
                    primary_condition_icon = posible_day_weather['icon']
                
                
            print(f"{human_readble_date}: Температура воздуха {day_temp} | Максимум {day_temp_max} °C | Минимум {day_temp_min} °C | Скорость ветра {day_wind_speed} \
                \nВ основном {primary_condition} ({primary_condition_description}) >> Код картинка {primary_condition_icon}" )

    except requests.exceptions.RequestException:
        print("Timeout occured")
    #pprint(weather_request.json())

if __name__ == '__main__':
    lon = 30.315785
    lat = 59.939039
    weather_request(lat,lon)
    