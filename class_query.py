import requests
import api_token
import re
from pprint import pprint
import sqlite3
from datetime import datetime 

def human_readable_date(input, failed_iso=True, timestamp=False):
    """"Превращает дату в формат %Y-%m-%d-%H:%M:%S """
    if failed_iso:
        input = input.replace("Z","")    
        return datetime.fromisoformat(input).strftime('%Y-%m-%d-%H:%M:%S')
    if timestamp:
        return datetime.fromtimestamp(input).strftime('%Y-%m-%d')
        


class query():
    def __init__(self,origin_city):
        self.response_dict = {'success': False,'route': None, 'weather': None, 'tickets': None}  # в этом словаре будут содержаться данные для выдачи фронту
        self.meta_dict = {'departure_city_code':None, 'arrival_city_code':None, 'arrival_city_lon':None, 'arrival_city_lat':None }
        self.origin_city = origin_city
        self.init_validator(self.origin_city)

    def init_validator(self, input):
        regex = '^[A-Z,a-z]+$'
        match = re.search(regex,input)
        if match:
            self.meta_dict.update({'Failed': False})
        else:
            self.meta_dict.update({'Failed': True})
            self.response_dict.update({'success': False,'reason': 'Input origin Failed'})

    def choosing_random_route(self, origin_city, db_filename='transport.db'):
        """"Рандомно выбирает из базы маршрут по указанному пункту отправления. 
        Записывает в словарь response_dict для выдачи фронуту.
        И в словарь meta_dict для передачи в слудющие функции"""
        if  self.meta_dict['Failed']:
            return self.meta_dict
        try:
            connection = sqlite3.connect(db_filename)
            cursor = connection.cursor()
            query=f'SELECT departure_airport_iata, arrival_airport_iata, ' \
                f'departure_tp.name_primary, arrival_tp.name_primary, '\
                    f'departure_city.name_primary, arrival_city.name_primary, ' \
                        f'departure_coutry.name_primary, arrival_country.name_primary, ' \
                            f'departure_tp.city_code, arrival_tp.city_code, arrival_city.coordinates_lon, arrival_city.coordinates_lat FROM routes r ' \
                                f'INNER JOIN transport_point departure_tp ON r.departure_airport_iata = departure_tp.point_id ' \
                                    f'INNER JOIN transport_point arrival_tp ON r.arrival_airport_iata = arrival_tp.point_id ' \
                                        f'INNER JOIN city departure_city on departure_tp.city_code = departure_city.city_id ' \
                                            f'INNER JOIN city arrival_city on arrival_tp.city_code = arrival_city.city_id ' \
                                                f'INNER JOIN country departure_coutry on departure_city.country_code = departure_coutry.country_id ' \
                                                        f'INNER JOIN country arrival_country on arrival_city.country_code = arrival_country.country_id ' \
                                                            f'WHERE departure_tp.city_code = "{origin_city}" ORDER BY RANDOM() LIMIT(1); '
        
            #print(query)
            cursor.execute(query)
            response = cursor.fetchone()
            if response is not None:
                self.response_dict.update({'route': {'departure_airport_iata':response[0], 'arrival_airport_iata':response[1], 'departure_airport_name':response[2], 
                    'arrival_airport_name':response[3],'departure_city_name':response[4], 'arrival_city_name':response[5],'departure_country_name':response[6], 
                        'arrival_country_name':response[7] }})
                self.meta_dict.update({'departure_city_code':response[8], 'arrival_city_code':response[9], 'arrival_city_lon':response[10], 'arrival_city_lat':response[11] }) # нужен для передачи значения в функцию по поиску билетов
                return self.meta_dict
            else:
                
                self.response_dict.update({'success': False,'reason': 'No such source transport point'})
                return self.meta_dict

        except sqlite3.Error as e:
            self.response_dict.update({'success': False, 'reason':str(e)})
            return self.meta_dict
            
    def weather_and_tickets(self, departure_city_code, arrival_city_code,arrival_city_lon, arrival_city_lat, token=api_token.token_travel, Failed=False):
        if Failed:
            return self.response_dict

        def tickets(self):  # IATA код города 
            """"Ищет дешёвые билеты по выбранному направлению. Записывает данные в словарь для выдачи фронту"""
            headers = {'X-Access-Token':token,
            'Accept-Encoding':'gzip, deflate'} 
            url = f'http://api.travelpayouts.com/v1/prices/direct?origin={departure_city_code}&destination={arrival_city_code}'
            
            try:
                response = requests.request("GET",url,headers=headers,timeout=1)
                #print(url+'&token='+token)
                #pprint(response.json())

                if response.json()['success'] :
                    if  response.json()['data']:
                        for flight in response.json()['data'][arrival_city_code].values():
                            airline = flight['airline']
                            departure_time = human_readable_date(flight['departure_at'])
                            return_time = human_readable_date(flight['return_at'])
                            flight_number = flight['flight_number']
                            price = flight['price']
                            expire_time = human_readable_date(flight['expires_at'])
                            self.response_dict.update({'tickets':{'airline':airline,'departure_time':departure_time,
                                'return_time':return_time,'flight_number':flight_number,'price':price,'expire_time':expire_time}})
                            print(f'Стоимость: {price} Время вылета: {departure_time} Время возвращение: {return_time} Номер рейса: {flight_number} Авиакомпания: {airline} Истекает: {expire_time}')
                    else:
                        print('Empty response')
                else:
                    print("Unsuccessful response. Reason:", response.json()['error'] )
            except requests.exceptions.RequestException:
                print('Ошибка при загрузке данных')

        def weather_request(self):
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={arrival_city_lat}&lon={arrival_city_lon}&units=metric&exclude=minutely,hourly&lang=ru&appid={api_token.weather_token}'
            print(url)
            weather_list =[]
            try:
                weather_request = requests.get(url,timeout=0.5)
                
                for day in weather_request.json()['daily']:
                    day_temp = day['temp']['day']
                    day_temp_min = day['temp']['min']
                    day_temp_max = day['temp']['max']
                    day_wind_speed = day['wind_speed']
                    date = human_readable_date(input=day['dt'],failed_iso=False, timestamp=True)

                    for posible_day_weather in day['weather']:
                        if day['weather'].index(posible_day_weather) == 0:
                            primary_condition = posible_day_weather['main']
                            primary_condition_description  = posible_day_weather['description']
                            primary_condition_icon = posible_day_weather['icon']
                            weather_list.append({'date':date,'day_temp':day_temp,'day_temp_min':day_temp_min,
                                'day_temp_max':day_temp_max,'day_wind_speed':day_wind_speed,
                                    'primary_condition':primary_condition,'primary_condition_description':primary_condition_description,
                                        'primary_condition_icon':primary_condition_icon})
                            break        
                    #print(f"{date}: Температура воздуха {day_temp} | Максимум {day_temp_max} °C | Минимум {day_temp_min} °C | Скорость ветра {day_wind_speed} \
                    #    \nВ основном {primary_condition} ({primary_condition_description}) >> Код картинка {primary_condition_icon}" )
                
                self.response_dict.update({'weather':weather_list})
            except requests.exceptions.RequestException:
                print("Timeout occured")
                        
        tickets(self)
        weather_request(self)

    def run(self):
        self.weather_and_tickets(**self.choosing_random_route(self.origin_city))


if __name__ == '__main__':
    q = query('LED')
    q.run()
    pprint(q.response_dict)
   

