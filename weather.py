import requests
from datetime import timedelta, date
from pprint import pprint


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)





def weather(city, start_date = date(2020, 2, 2) , end_date = date(2020, 2, 28)):



    location_request = requests.get(f'https://www.metaweather.com/api/location/search/?query={city}')
    
    woeid = location_request.json()[0]['woeid']
    print('woeid = ', woeid)


    weather_measurements = []
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y/%m/%d")
        
        weather_request =  requests.get(f'https://www.metaweather.com/api/location/{woeid}/{date}') 
        weather_measurements = weather_measurements + weather_request.json()
   

    

  
    temp_list = []
  
    for measurement in weather_measurements:
        temp_list.append(measurement['the_temp'])
        
    temp_list.sort()
   
    pprint(temp_list)
    
    print('Максимальная температура за указанный промежуток:', temp_list[-1])
    print('Минимальная температура за указанный промежуток:', temp_list[0])


weather('St Petersburg')