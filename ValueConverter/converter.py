import lxml.html
import requests
from config import *
import json


class ApiError(Exception):
    pass


class Convertor:
    @staticmethod
    def chek_len(mes):
        if len(mes) == 0:
            raise ApiError(f'Недостаточно входных данных')

    @staticmethod
    def get_price(mes):
        Convertor.chek_len(mes)
        try:
            if ',' in mes[-1]:
                mes[-1] = mes[-1].replace(',', '.')
            amount = float(mes[-1])
            del mes[-1]
        except:
            raise ApiError(f'Необходимо ввести корректное количество волюты')

        Convertor.chek_len(mes)

        for i in range(1, len(mes)):
             if ' '.join(mes[:i]) in value:
                base = ' '.join(mes[:i])
                del mes[:i]
                break

        Convertor.chek_len(mes)

        try:
            if base:
                pass
        except:
            raise ApiError('Некоректно введена исходнаяая валюта')

        quote = ' '.join(mes)
        if quote not in value:
            raise ApiError('Некоректно введена искомая валюта')

        if base == quote:
            raise ApiError('Введите различные валюты')

        r = requests.get(f'https://www.cbr-xml-daily.ru/latest.js?fbase=RUB&rates=USD')
        texts = json.loads(r.content)

        if base == 'Российский рубль':
            first_value = 1
        else:
            first_value = texts['rates'][value[base]]

        if quote == 'Российский рубль':
            second_value = 1
        else:
            second_value = texts['rates'][value[quote]]
        new_price = second_value / first_value * float(amount)
        return [base, quote, amount, new_price]