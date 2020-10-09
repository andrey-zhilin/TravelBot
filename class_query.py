import requests
import api_token
from pprint import pprint
import sqlite3

class query():
    def __init__(self,origin_city):
        self.origin_city = origin_city

    def choosing_random_route(self, origin_city, db_filename='transport.db'):
        """"Рандомно выбирает из базы маршрут по указанному пункту отправления. 
        Записывает в словарь response_dict для выдачи фронуту.
        И в словарь meta_dict для передачи в слудющие функции"""
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
        self.response_dict = {'departure_airport_iata':response[0], 'arrival_airport_iata':response[1], 'departure_airport_name':response[2], 
            'arrival_airport_name':response[3],'departure_city_name':response[4], 'arrival_city_name':response[5],'departure_country_name':response[6], 
                'arrival_country_name':response[7] } # в этом словаре будут содержаться данные для выдачи фронту
        self.meta_dict = {'departure_city_code':response[8], 'arrival_city_code':response[9], 'arrival_city_lon':response[10], 'arrival_city_lat':response[11] } # нужен для передачи значения в функцию по поиску билетов
        return self.meta_dict

    def tickets(self, departure_city_code, arrival_city_code,arrival_city_lon, arrival_city_lat, token=api_token.token_travel):  # IATA код города 
        """"Ищет дешёвые билеты по выбранному направлению. Записывает данные в словарь для выдачи фронату"""
        headers = {'X-Access-Token':token,
        'Accept-Encoding':'gzip, deflate'}
        #url = f'http://api.travelpayouts.com/v1/prices/cheap?origin={departure_city_code}&destination={arrival_city_code}'    
        url = f'http://api.travelpayouts.com/v1/prices/direct?origin={departure_city_code}&destination={arrival_city_code}'
        try:
            response = requests.request("GET",url,headers=headers,timeout=1)
            print(url+'&token='+token)
            #pprint(response.json())

            if response.json()["success"] == True:
                if  response.json()['data']:
                    for flight in response.json()['data'][arrival_city_code].values():
                        airline = flight['airline']
                        departure_time = flight['departure_at']
                        return_time = flight['return_at']
                        flight_number = flight['flight_number']
                        price = flight['price']
                        expire_time = flight['expires_at']
                        print(f'Стоимость: {price} Время вылета: {departure_time} Время возвращение: {return_time} Номер рейса: {flight_number} Авиакомпания: {airline} Истекает: {expire_time}')
                else:
                    print('Empty response')
            else:
                print("Unsuccessful response. Reason:", response.json()['error'] )
        except requests.exceptions.RequestException:
            print('Ошибка при загрузке данных')
    
    def run(self):
        self.tickets(**self.choosing_random_route(self.origin_city))
        
q = query('LED')
q.run()
pprint(q.meta_dict)
pprint(q.response_dict)

# сделать, так, чтобы каждая функция класса обновляла уже созданный словарь response_dict = {route:{None}, tickets: {None}, weather:{None}}