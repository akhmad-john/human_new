from django.urls import path
from .views import *



urlpatterns = [
    path('currency/', CurrencyRateShareView.as_view()),
    path('weather/', WeatherFetchView.as_view()),

]