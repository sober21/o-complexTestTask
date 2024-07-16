import requests
import json


import openmeteo_requests

import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error

def get_response_json(city: str) -> dict:
    # Отправляет запрос в Яндекс API и возвращает словарь с данными о запрашиваемом городе(в том числе и координаты)
    res = requests.get(
        f'https://geocode-maps.yandex.ru/1.x/?apikey=c664bfdb-8c58-4bb8-877a-27df0b6e5f29&geocode={city}&format=json')
    data = res.json()
    return data


def get_coordinates(d: dict) -> str:
    # Достаёт из словаря координаты города и возвращает их
    result = ''
    for key, value in d.items():
        if isinstance(value, dict):
            if value.get('pos'):
                result = value['pos']
                break
            else:
                result += get_coordinates(value)
        else:
            if isinstance(value, list):
                value = value[0]
                result += get_coordinates(value)
    return result


if __name__ == '__main__':
    city = input('Ввведите название города:')
    response = get_response_json(city=city)
    coordinates = get_coordinates(response)
    longitude, latitude = [round(float(i), 2) for i in coordinates.split()] # Преобразуем строку с координатами в долготу и широту

    # cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    # retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    # openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 1
    }
    responses = requests.get(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    print(responses.json()['hourly']['temperature_2m'][-1])
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")