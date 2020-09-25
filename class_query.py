import requests
import api_token
from pprint import pprint
import sqlite3

class query():
    def __init__(self,origin_city):
        self.origin_city = origin_city

    def choosing_random_route(self,origin_city):
        query=f'SELECT departure_airport_iata, arrival_airport_iata, tp1.name_primary, tp2.name_primary, tp1.city_code, tp2.city_code, c1.name_primary, c2.name_primary ' \
            f'FROM routes r ' \
                f'JOIN transport_point tp1 ON r.departure_airport_iata = tp1.point_id ' \
                    f'JOIN transport_point tp2 ON r.arrival_airport_iata = tp2.point_id ' \
                        f'JOIN city c1 on tp1.city_code = c1.city_id ' \
                            f'JOIN city c2 on tp2.city_code = c2.city_id ' \
                                f'WHERE tp1.city_code = "{origin_city}";'
        print(query)
    


q = query('LED')

q.choosing_random_route('LED')