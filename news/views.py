from django.shortcuts import render
from rest_framework import status, viewsets
from .serializers import CategorySerializer
from .models import Category
# Create your views here.

class CategoryriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
