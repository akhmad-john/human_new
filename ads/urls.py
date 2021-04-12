from django.urls import path
from .views import *



urlpatterns = [
    path('', AdDisplayView.as_view()),

]