from django.shortcuts import render
from geopy import GoogleV3
import requests, datetime, json, os
from django.shortcuts import redirect


def index(request):
    #временне данные
    place = 'Харків'
    adres = 'Харьков, Родниковая9а'

    lat = str(25.7617)
    lon = str(-80.1918)



    # Получение имен картинок
    place_image_in_static = os.listdir('weather/static/weather/images')
    names_images = []
    for name in place_image_in_static:
        name_place_image_in_static = name.split(".")[0]
        print(name_place_image_in_static)
        names_images.append(name_place_image_in_static)
        print('names_images', names_images)

        # Настройка кнопок с местом
        if request.GET.get('place'):
            place = request.GET.get('place')
            print('place по Get параметрам', place)

        # Настройка о получению места
        if request.method == 'POST':
            place = request.POST['place']
            print('POST')

        location = GoogleV3(api_key='AIzaSyDi_HeAAJ9AfpJns9PLZdJsfGhOeNx7e9c').geocode(place)

        try:
            lat = str(location.latitude)
            lon = str(location.longitude)
            adres = location.address
            print('Address:', adres)

        # обработка исключений
        except AttributeError as error_message:
            print("Error: geocode failed on input %s with message %s" % (location, error_message))
            adres = ''
            location = 'Miami'
            place = '''Не знайдено. Подивіться погоду в Майямі.'''
            lat = str(25.7617)
            lon = str(-80.1918)
            print(location)

        real_ip = request.META.get('HTTP_X_REAL_IP')
        print('real_ip', real_ip)


    #Получение данных с openweathermap
    key = "64b63acfeeb28579404f7511a3580c4b"
    url_kharkiv_96 = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + lat + '&lon=' + lon + '&units=metric&exclude=minutely,hourly&appid=' + key
    data_kharkiv_96 = requests.get(url_kharkiv_96).json()
    current_time = datetime.datetime.fromtimestamp(int(data_kharkiv_96['current']['dt']))
    today = current_time.strftime('%Y - %m  - %d')
    temp_now = data_kharkiv_96['current']['temp']
    icon_now = data_kharkiv_96['current']['weather'][0]['icon']
    icon_now_link = 'http://openweathermap.org/img/wn/' + icon_now + '.png'
    date_7 = []
    for i in range(0, 8):
        date = datetime.datetime.fromtimestamp(int(data_kharkiv_96['daily'][i]['dt']))
        date = date.strftime('%b %d')

        moon_phase = data_kharkiv_96['daily'][i]['moon_phase']
        temp_day = (data_kharkiv_96['daily'][i]['temp']).get('day')
        temp_min = (data_kharkiv_96['daily'][i]['temp']).get('min')
        temp_max = (data_kharkiv_96['daily'][i]['temp']).get('max')
        temp_night = (data_kharkiv_96['daily'][i]['temp']).get('night')
        temp_eve = (data_kharkiv_96['daily'][i]['temp']).get('eve')
        temp_morn = (data_kharkiv_96['daily'][i]['temp']).get('morn')

        temp_day_feels = (data_kharkiv_96['daily'][i]['feels_like']).get('day')
        temp_night_feels = (data_kharkiv_96['daily'][i]['feels_like']).get('night')
        temp_eve_feels = (data_kharkiv_96['daily'][i]['feels_like']).get('eve')
        temp_morn_feels = (data_kharkiv_96['daily'][i]['feels_like']).get('morn')

        pressure = data_kharkiv_96['daily'][i]['pressure']
        dew_point = data_kharkiv_96['daily'][i]['dew_point']
        wind_speed = data_kharkiv_96['daily'][i]['wind_speed']
        wind_gust = data_kharkiv_96['daily'][i]['wind_gust']

        pop = int(100 * data_kharkiv_96['daily'][i]['pop'])

        day_week = datetime.datetime.fromtimestamp(int(data_kharkiv_96['daily'][i]['sunrise'])).strftime(" %a ")
        sunrise = datetime.datetime.fromtimestamp(int(data_kharkiv_96['daily'][i]['sunrise'])).strftime(" %a ")

        if 'rain' in data_kharkiv_96['daily'][i]:
            rain = '☂ ' + str(data_kharkiv_96['daily'][i]['rain']) + 'мм'
        else:
            rain = 'no rain'


        icon = data_kharkiv_96['daily'][i]['weather'][0]['icon']
        icon_link = 'http://openweathermap.org/img/wn/' + icon + '.png'

        daily = [date, temp_day, temp_morn, temp_eve, temp_night, temp_min, temp_max,
                 temp_day_feels, temp_morn_feels, temp_eve_feels, temp_night_feels,
                 moon_phase, icon_link, i, pressure, dew_point, wind_speed, wind_gust, sunrise, pop, day_week, rain]
        date_7.append(daily)

    context = {'all_data_96': data_kharkiv_96,
               'current_time': datetime.datetime.fromtimestamp(int(data_kharkiv_96['current']['dt'])),
               'temp_now': temp_now,
               'moon_phase': moon_phase,
               'temp_feel_now': data_kharkiv_96['current']['feels_like'],
               'date_7': date_7,
               'place': place,
               'adres': adres,
               'lat': lat,
               'lon': lon,
#               'json_m': json_my,
#               'real_ip': real_ip,
               'place_image_in_static': place_image_in_static,
               'names_images': names_images,
               }

    return render(request, 'weather/index.html', context)

