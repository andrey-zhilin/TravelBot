import sqlite3
import requests
from pprint import pprint
import os




def api_query():
    country_list = []
    country_request = requests.get('http://api.travelpayouts.com/data/ru/countries.json')
    for country in country_request.json():
        country_list.append((country['code'],country['name'],country['currency'], \
            country['name_translations']['en']))
    #pprint(country_list)

    city_list = []
    city_request = requests.get('http://api.travelpayouts.com/data/ru/cities.json')
    for city in city_request.json():
        
        city_list.append((city['code'],city['name'], \
                 city['coordinates']['lon']  if (city.get('coordinates') is not None) else None, \
                     city['coordinates']['lat']  if (city.get('coordinates') is not None) else None, \
                      city['name_translations']['en'],city['country_code']))
    #pprint(city_list)
    trasport_point_list =[]
    trasport_point_request = requests.get('http://api.travelpayouts.com/data/ru/airports.json')
    for point in trasport_point_request.json():
        trasport_point_list.append((point['code'],point['name'], \
            point['iata_type'],point['flightable'],point['name_translations']['en'], \
            point['city_code']))
        
    #pprint(trasport_point_list)




def database():
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

#api_query()
database()