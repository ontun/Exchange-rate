import requests
import configparser
import json


config = configparser.ConfigParser()
config.read('config.ini')


class APIException(BaseException):
    pass


class APIExceptionLink(APIException):
    def __str__(self):
        return "Неуспешно обработан запрос"


class CurrencyConverter:

    @staticmethod
    def get_price(base, quote, amount):
        try:

            url = f"http://data.fixer.io/api/latest"
            params = {"access_key": config.get('Secret_data', 'API_key_fix')}
            response = requests.get(url, params=params)# параметры запроса
            data = json.loads(response.content)

            if data['success']:# проверка на успешность запроса
                if quote in data['rates'] and base in data['rates']:# проверка на наличие базовой и конвертируемой валюты
                    return float(data["rates"][quote])/float(data["rates"][base]) * amount, 0 # получаем курс валюты
                    # к доллару каждой валюты (базовой и конвертируемой) и делим друг на друга и умножаем на количество
                    # возвращаем цену за валюту и код 0
                else:
                    raise APIException
            else:
                raise APIExceptionLink
        except APIExceptionLink as e:
            print(e)
            return False, 101 # возвращаем False и собственный код ошибки
        except APIException:
            return False, 1# возвращаем False и собственный код ошибки

    @staticmethod
    def get_all_currency():
        try:
            url = f"http://data.fixer.io/api/symbols"
            params = {"access_key": config.get('Secret_data', 'API_key_fix')}
            response = requests.get(url, params=params)# параметры запроса
            data = json.loads(response.content)
            if data['success']:# проверка на успешность запроса
                return json.dumps(data['symbols'])# получение всех валют
            else:
                raise APIExceptionLink
        except APIExceptionLink as e:
            print(e)
            return []
