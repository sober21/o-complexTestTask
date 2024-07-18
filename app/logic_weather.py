"""
Логика получения тепмературы воздуха
"""

import requests
from datetime import datetime


def get_response_from_yandex_api(city: str) -> dict:
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


def get_longitude_and_latitude(coord: str) -> list[float]:
    # Преобразует строку с координатами во float с 2 знаками после запятой и возвращает результат
    # Первое значение - долгота, второе - широта
    return [round(float(i), 2) for i in coord.split()]


# Вот тут и понадобятся координаты, потому что open-meteo отдаёт данные только по координатам
def get_data_temperature(long: float, lat: float) -> dict:
    # Отправляет запрос к API open-meteo.com и возвращает ответ в виде словаря
    # Запрос на текущую температуру(current) и почасовую температуру(hourly) в течении текущих суток(forecast_days)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": "temperature_2m",
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "timezone": "Europe/Moscow",
        "forecast_days": 3
    }
    responses = requests.get(url, params=params)
    return responses.json()


def get_current_temperature(data: dict) -> float:
    return data['current']['temperature_2m']


def get_max_temperature_for_3_days(data: dict) -> list:
    return data['daily']['temperature_2m_max']


def get_min_temperature_for_3_days(data: dict) -> list:
    return data['daily']['temperature_2m_min']


def get_time_for_3_days(data: dict) -> list:
    return data['daily']['time']


def get_data_temperature_for_3_days(minimum: list, maximum: list, dt: list) -> dict:
    # Группирует максмальную и минимальную температуры с соответствующим днём и возвращает результат
    return dict(zip(dt, list(zip(minimum, maximum))))


def main_func_logic_weather(city: str) -> float:
    data_from_yandex_api = get_response_from_yandex_api(city=city)
    coordinates = get_coordinates(d=data_from_yandex_api)
    longitude, latitude = get_longitude_and_latitude(coord=coordinates)
    data_temperature = get_data_temperature(long=longitude, lat=latitude)
    current_temperature = get_current_temperature(data=data_temperature)
    max_temperature = get_max_temperature_for_3_days(data=data_temperature)
    min_temperature = get_min_temperature_for_3_days(data=data_temperature)
    dt = get_time_for_3_days(data=data_temperature)
    res = get_data_temperature_for_3_days(minimum=min_temperature, maximum=max_temperature, dt=dt)
    return res


if __name__ == '__main__':
    # city_name = input('Ввведите название города:')
    print(main_func_logic_weather('Воронеж'))
    # print(get_response_from_yandex_api('Воронеж'))
