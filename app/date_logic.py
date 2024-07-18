def render_date(dt: str) -> str:
    """
    Преобразует входящую дату и возвращает результат
    :param dt: строка
    :return: результат преобразования

    >>> render_date('2024-03-14')
    '14 Марта'
    """

    _, num_month, day = dt.split('-')
    month = get_russian_name_month(int(num_month))
    my_date = f'{int(day)} {month.capitalize()}'

    return my_date


def get_russian_name_month(num_month: int) -> str:
    """
    Преобразует номер месяца в название месяца на русском языке в родительном падаже и возвращает результат
    :param num_month: номер месяца(1 - январь)
    :return: результат
    """
    dict_months = {1: 'января',
                   2: 'февраля',
                   3: 'марта',
                   4: 'апреля',
                   5: 'мая',
                   6: 'июня',
                   7: 'июля',
                   8: 'августа',
                   9: 'сентября',
                   10: 'октября',
                   11: 'ноября',
                   12: 'декабря'}
    return dict_months[num_month]


if __name__ == '__main__':
    # print(render_date('2024-01-12'))
    pass
