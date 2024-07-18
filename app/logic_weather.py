"""
Логика получения тепмературы воздуха
"""

import requests

from app.date_logic import render_date


def get_data_city_from_yandex_api(city: str) -> dict:
    # Отправляет запрос в Яндекс API и возвращает словарь с данными о запрашиваемом городе(в том числе и координаты)
    res = requests.get(
        f'https://geocode-maps.yandex.ru/1.x/?apikey=c664bfdb-8c58-4bb8-877a-27df0b6e5f29&geocode={city}&format=json')

    return res.json()


def get_coordinates(d: dict) -> str:
    # Достаёт из словаря координаты города и возвращает их
    # Это рекурсивная функция, потому что словарь может быть разной вложенности в зависимости от города
    result = ''
    try:
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
    except Exception:
        result = 'В нашей базе нет населённого пункта с таким названием. Попробуйте ещё раз.'
    return result


def get_longitude_and_latitude(coord: str) -> list[float]:
    # Преобразует строку с координатами во float с 2 знаками после запятой и возвращает результат
    # Первое значение - долгота, второе - широта
    if coord == 'В нашей базе нет населённого пункта с таким названием. Попробуйте ещё раз.':
        return [0.0, 0.0]
    return [round(float(i), 2) for i in coord.split()]


# Вот тут и понадобятся координаты, потому что open-meteo отдаёт данные только по координатам(широта, долгота)
def get_data_temperature_from_open_meteo(long: float, lat: float, count: int = 7) -> dict:
    # Отправляет запрос к API open-meteo.com и возвращает ответ в виде словаря
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": "temperature_2m",
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "timezone": "Europe/Moscow",
        "forecast_days": count
    }
    responses = requests.get(url, params=params)
    return responses.json()


def get_current_temperature(data: dict) -> float:
    return data['current']['temperature_2m']


def get_list_max_temperature(data: dict) -> list:
    return data['daily']['temperature_2m_max']


def get_list_min_temperature(data: dict) -> list:
    return data['daily']['temperature_2m_min']


def get_list_date(data: dict) -> list:
    # Получает, преобразует и возвращает даты, которым соответсвуют температуры
    result = [render_date(dt) for dt in data['daily']['time']]
    return result


def get_data_temperature_for_n_days(minimum: list, maximum: list, dt: list) -> dict:
    # Группирует максмальную и минимальную температуры с соответствующим днём и возвращает результат
    return dict(zip(dt, list(zip(minimum, maximum))))


def main_func_logic_weather(city: str) -> tuple:
    # Вызывает все функции из этого модуля и возвращает текущую температуру, а так же минимальную
    # и максимальную температуру в ближайшие N дней
    data_from_yandex_api = get_data_city_from_yandex_api(city=city)
    coordinates = get_coordinates(d=data_from_yandex_api)
    longitude, latitude = get_longitude_and_latitude(coord=coordinates)
    data_temperature = get_data_temperature_from_open_meteo(long=longitude, lat=latitude)
    current_temperature = get_current_temperature(data=data_temperature)
    max_temperature = get_list_max_temperature(data=data_temperature)
    min_temperature = get_list_min_temperature(data=data_temperature)
    dt = get_list_date(data=data_temperature)
    res = get_data_temperature_for_n_days(minimum=min_temperature, maximum=max_temperature, dt=dt)
    return current_temperature, res


if __name__ == '__main__':
    # cur, data1 = main_func_logic_weather('Воронеж')
    # print(f'Текущая температура: {cur}')
    # for k, v in data1.items():
    #     print(f'{k}: минимум - {v[0]}, максимум - {v[1]}')
    pass
