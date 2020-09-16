import requests
import api_token
from pprint import pprint




def tickets(origin, destination,  depart_date, return_date, token=api_token.token_travel, direct=False,):  # IATA код города 
    headers = {'X-Access-Token':token,
    'Accept-Encoding':'gzip, deflate'}
    if direct == False:
        url = f'http://api.travelpayouts.com/v1/prices/cheap?origin={origin}&destination={destination}'
    else:
        url = f'http://api.travelpayouts.com/v1/prices/direct?origin={origin}&destination={destination}&depart_date={depart_date}&return_date={return_date}'
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
        print('Ошибка при загрузке данных: ', e)



if __name__ == '__main__':
    depart_date = '2020-10'
    return_date = '2020-10'
    origin = 'LED'
    destination = 'MOW'
    tickets(origin,destination,depart_date, return_date, direct=False)
