import sqlite3
import requests
from pprint import pprint
import os



class Data():
    
    country_list = []
    city_list = []
    transport_point_list = []

    def get_api_data(self):
        
        country_request = requests.get('http://api.travelpayouts.com/data/ru/countries.json')
        for country in country_request.json():
            Data.country_list.append((country['code'],country['name'],country['currency'], \
                country['name_translations']['en']))
        

        city_request = requests.get('http://api.travelpayouts.com/data/ru/cities.json')
        for city in city_request.json():
            
            Data.city_list.append((city['code'],city['name'], \
                    city['coordinates']['lon']  if (city.get('coordinates') is not None) else None, \
                        city['coordinates']['lat']  if (city.get('coordinates') is not None) else None, \
                        city['name_translations']['en'],city['country_code']))
        
        transport_point_request = requests.get('http://api.travelpayouts.com/data/ru/airports.json')
        for point in transport_point_request.json():
            Data.transport_point_list.append((point['code'],point['name'], \
                point['iata_type'],point['flightable'],point['name_translations']['en'], \
                point['city_code']))

    def database(self):
        db_filename = 'transport.db'
        schema_filename = 'scheme.sql'

        db_exists = os.path.exists(db_filename)
        conn = sqlite3.connect(db_filename)
    
        if not db_exists:
            print('Creating schema...')
            with open(schema_filename, 'r') as f:
                schema = f.read()
                conn.executescript(schema)
            print('Done')

        try:
            with conn:
                country_query = 'INSERT into country values (?, ?, ?, ?)'
                city_query = 'INSERT into city values(?, ?, ?, ?, ?, ?)'
                transport_point_query = 'INSERT into transport_point values(?, ?, ?, ?, ?, ?)'
                conn.executemany(country_query, Data.country_list)
                conn.executemany(city_query, Data.city_list)
                conn.executemany(transport_point_query, Data.transport_point_list)
        except sqlite3.IntegrityError as e:
            print('Error occured: ', e)

test = Data()
test.get_api_data()
test.database()
#print(test.transport_point_list)