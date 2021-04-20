from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .functions import return_currency_object
from .constants import CURRENCIES
# Create your views here.


class CurrencyRateShareView(APIView):
    def get(self, request):
        return Response(return_currency_object())
