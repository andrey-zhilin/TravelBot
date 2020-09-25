import requests
import api_token
from pprint import pprint
import sqlite3




def tickets(origin, destination,  depart_date, return_date, token=api_token.token_travel, direct=False,):  # IATA код города 
    headers = {'X-Access-Token':token,
    'Accept-Encoding':'gzip, deflate'}
    if direct :
        url = f'http://api.travelpayouts.com/v1/prices/direct?origin={origin}&destination={destination}&depart_date={depart_date}&return_date={return_date}'
    else:
        url = f'http://api.travelpayouts.com/v1/prices/cheap?origin={origin}&destination={destination}'
        
    try:
        
        response = requests.request("GET",url,headers=headers,timeout=1)
        print(url+'&token='+token)
        pprint(response.json())

        if response.json()["success"] == True:
            if  response.json()['data']:
                for flight in response.json()['data'][destination].values():
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

def city_resolver(input_symbols, db_filename='transport.db'):
    """"Возвращает данные по городам, по фрагменту введенного названия города"""
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    query = f'SELECT city.name_primary, city_id, country.name_primary ' \
        f'FROM city JOIN country WHERE (city.name_primary LIKE \'{input_symbols.capitalize()}%\' OR city.name_primary LIKE \'%{input_symbols.lower()}%\') ' \
            f'AND city.country_code == country.country_id LIMIT(5);'
    print(query)
    cursor.execute(query)
    response = cursor.fetchmany(5)
    city_dict = {line[0]: {'code':line[1], 'country': line[2]} for line in response}
    print(city_dict)
    return city_dict

if __name__ == '__main__':
    depart_date = '2020-10'
    return_date = '2020-10'
    origin = 'LED'
    destination = 'LWN'
    tickets(origin,destination,depart_date, return_date, direct=False)
    city_resolver("моск")
