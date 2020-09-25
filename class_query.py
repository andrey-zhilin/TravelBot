import requests
import api_token
from pprint import pprint
import sqlite3

class query():
    def __init__(self,origin_city):
        self.origin_city = origin_city

    def city_resolver(self):
    


q = query('LED')

q.tickets()