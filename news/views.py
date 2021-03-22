from django.shortcuts import render
from rest_framework import status, viewsets
from .serializers import *
from .models import Category, Article
from rest_framework.response import Response

# Create your views here.

class CategoryriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    
    def get_serializer_class(self):
        print(self.request.LANGUAGE_CODE)
        if self.request.LANGUAGE_CODE == 'ru':
            return ArticleRuSerializer
        elif self.request.LANGUAGE_CODE == 'uz':
            return ArticleUzSerializer
        else:
            return Response({'asd':'sdfs'})
