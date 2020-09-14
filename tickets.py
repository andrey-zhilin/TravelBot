import requests
import api_token
from pprint import pprint




def tickets(token=api_token.token_travel, direct=False, origin, destination):
    headers = {'X-Access-Token':token,
    'Accept-Encoding':'gzip, deflate'}
    response = requests.request("GET",url,headers=headers)
    pprint(response.json())

tickets()

if __name__ == '__main__':
    origin = 'LED'
    destination = 'HKT'
    tickets(origin,destination)