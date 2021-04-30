import requests
import datetime
from .constants import CURRENCIES


def return_currency_object(language_code):
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    for currency in CURRENCIES:
        send_request = requests.get(f'https://cbu.uz/ru/arkhiv-kursov-valyut/json/{currency}/{today}')
        if language_code == 'ru':
            currency_name = send_request.json()[0]['CcyNm_RU']
        elif language_code == 'uz':
            currency_name = send_request.json()[0]['CcyNm_UZC']
        else:
            currency_name = send_request.json()[0]['CcyNm_UZ']
        yield {
            "currency_name": currency_name,
            "currency_code": send_request.json()[0]['Ccy'],
            "rate": send_request.json()[0]['Rate'],
            "diff": send_request.json()[0]['Diff'],
        }
