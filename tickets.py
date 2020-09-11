import requests
import api_token
from pprint import pprint

url  = 'http://api.travelpayouts.com/v2/prices/latest?currency=rub&period_type=year&page=1&limit=30&show_to_affiliates=true&sorting=price'
print(url)


def tickets(token=api_token.token_travel):
    headers = {'X-Access-Token':token,
    'Accept-Encoding':'gzip, deflate'}
    response = requests.request("GET",url,headers=headers)
    pprint(response.json())

tickets()