import requests


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


def get_data_temperature(long: float, lat: float) -> dict:
    # Отправляет запрос к API open-meteo.com и возвращает ответ в виде словаря
    # Запрос на текущую температуру(current) и почасовую температуру(hourly) в течении текущих суток(forecast_days)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": "temperature_2m",
        "forecast_days": 1,
        "current": "temperature_2m"
    }
    responses = requests.get(url, params=params)
    return responses.json()


def get_current_temperature(data: dict) -> float:
    return data['current']['temperature_2m']


def get_temperature_for_the_near_future(data: dict) -> list:
    return data['hourly']['temperature_2m']


def get_time_for_the_near_future(data: dict) -> list:
    return data['hourly']['time']


def main_logic(city: str) -> float:
    data_from_yandex_api = get_response_from_yandex_api(city=city)
    coordinates = get_coordinates(d=data_from_yandex_api)
    longitude, latitude = get_longitude_and_latitude(coord=coordinates)
    data_temperature = get_data_temperature(long=longitude, lat=latitude)
    current_temperature = get_current_temperature(data=data_temperature)
    near_future_temperature = get_temperature_for_the_near_future(data=data_temperature)
    near_future_time = get_time_for_the_near_future(data=data_temperature)
    return current_temperature


if __name__ == '__main__':
    city_name = input('Ввведите название города:')
    main_logic(city_name)
