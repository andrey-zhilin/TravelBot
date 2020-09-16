import sqlite3
import requests
from pprint import pprint
import os
from requests import RequestException



class Data():
    
    country_list = []
    city_list = []
    transport_point_list = []
    airlines_list = []
    routes_list = []

    def get_api_data(self):
        headers = {'Accept-Encoding':'gzip, deflate'}

        try:
            country_request = requests.get('http://api.travelpayouts.com/data/ru/countries.json',headers,timeout=1)
            for country in country_request.json():
                Data.country_list.append((country['code'],country['name'],country['currency'], \
                    country['name_translations']['en']))
            

            city_request = requests.get('http://api.travelpayouts.com/data/ru/cities.json',headers,timeout=1)
            for city in city_request.json():
                Data.city_list.append((city['code'],city['name'], \
                        city['coordinates']['lon']  if (city.get('coordinates') is not None) else None, \
                            city['coordinates']['lat']  if (city.get('coordinates') is not None) else None, \
                            city['name_translations']['en'],city['country_code']))
            
            transport_point_request = requests.get('http://api.travelpayouts.com/data/ru/airports.json',headers,timeout=1)
            for point in transport_point_request.json():
                Data.transport_point_list.append((point['code'],point['name'], \
                    point['iata_type'],point['flightable'],point['name_translations']['en'], \
                    point['city_code']))

            airlines_request = requests.get('http://api.travelpayouts.com/data/ru/airlines.json',headers,timeout=1)
            for airline in airlines_request.json():
                Data.airlines_list.append((airline['name'],airline['name_translations']['en'],airline['code']))
           
            routes_request = requests.get('http://api.travelpayouts.com/data/routes.json',headers,timeout=1)
            for route in routes_request.json():
                Data.routes_list.append((route['airline_iata'],route['departure_airport_iata'],route['arrival_airport_iata']))
            pprint(Data.routes_list)
        except requests.exceptions.RequestException:
            print('Ошибка при загрузке данных: ', e) 


    def database(self):
        db_filename = 'transport.db'
        schema_filename = 'scheme.sql'

        db_exists = os.path.exists(db_filename)
        conn = sqlite3.connect(db_filename)
       
        if not db_exists:
            
            try:
                print('Creating schema...')
                with open(schema_filename, 'r') as f:
                    schema = f.read()
                    conn.executescript(schema)
                print('Done')
                with conn:
                    country_query = 'INSERT into country values (?, ?, ?, ?)'
                    city_query = 'INSERT into city values(?, ?, ?, ?, ?, ?)'
                    transport_point_query = 'INSERT into transport_point values(?, ?, ?, ?, ?, ?)'
                    airlines_query = 'INSERT into airlines (name_primary,name_en,iata_code) values(?,?,?)'
                    routes_query = 'INSERT into routes (airline_iata,departure_airport_iata,arrival_airport_iata) values(?,?,?)'
                    conn.executemany(country_query, Data.country_list)
                    conn.executemany(city_query, Data.city_list)
                    conn.executemany(transport_point_query, Data.transport_point_list)
                    conn.executemany(airlines_query,Data.airlines_list)
                    conn.executemany(routes_query,Data.routes_list)
            except sqlite3.IntegrityError as e:
                print('Error occured: ', e)

if __name__ == '__main__':
    test = Data()
    test.get_api_data()
    test.database()
    #print(test.transport_point_list)

