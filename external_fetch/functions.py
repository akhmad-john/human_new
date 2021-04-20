import requests
import datetime
from .constants import CURRENCIES

def return_currency_object():
    today =datetime.datetime.today().strftime("%Y-%m-%d")
    for currency in CURRENCIES:
        send_request = requests.get(f'https://cbu.uz/ru/arkhiv-kursov-valyut/json/{currency}/{today}')
        yield {
            "currency": send_request.json()[0]['Ccy'],
            "rate": send_request.json()[0]['Rate']
        }

