from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .functions import return_currency_object
from .constants import CURRENCIES
# Create your views here.


class CurrencyRateShareView(APIView):
    def get(self, request):
        return Response(return_currency_object(self.request.LANGUAGE_CODE))



class WeatherFetchView(APIView):
    def get(self, request):
        if self.request.LANGUAGE_CODE == 'ru':
            language_code = "ru"
        elif self.request.LANGUAGE_CODE == 'uz':
            language_code = "uz"
        else:
            language_code = "uz"
        headers = {
            'X-RapidAPI-Key': 'bed183b66dmshddd8a5a74c4a091p1eb05djsn72ff595f0259',
            'X-RapidAPI-Host': 'community-open-weather-map.p.rapidapi.com'
        }
        payload = {
            "q": "Tashkent",
            "cnt": "3",
            "lang": language_code,
        }
        url = ""
        send_request = requests.get('https://community-open-weather-map.p.rapidapi.com/weather',
                                    headers=headers
                                    , params=payload
                                )
        dict_to_view = {
            "temperature": 28.5,
            "temp_min": 24.2,
            "temp_max": 30.1,
            "description": "ясно"
        }
        return Response(dict_to_view)
