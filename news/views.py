from django.shortcuts import render
from rest_framework import status, viewsets, filters
from .serializers import *
from .models import Category, Article
from rest_framework.response import Response
from django.db.models import F
from .filters import *
from itertools import chain
from django.http import HttpResponse, JsonResponse
# Create your views here.

class CategoryriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        print(self.request.LANGUAGE_CODE)
        if self.request.LANGUAGE_CODE == 'ru':
            return CategoryRuSerializer
        elif self.request.LANGUAGE_CODE == 'uz':
            return CategoryUzSerializer
        else:
            return CategoryOzSerializer

class ArticleListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.filter(display=True)
    filter_class = ArticleFilter
    filter_backends = [filters.SearchFilter]
    serializer_class = ArticleSerializer
    search_fields = [
        'content_blocks__ru_content',
        'content_blocks__uz_content',
        'content_blocks__oz_content',
        'ru_heading',
        'uz_heading',
        'oz_heading',
        'ru_subheading',
        'uz_subheading',
        'oz_subheading',
    ]

    # def get_serializer_class(self):
    #     print(self.request.LANGUAGE_CODE)
    #     if self.request.LANGUAGE_CODE == 'ru':
    #         return ArticleRuSerializer
    #     elif self.request.LANGUAGE_CODE == 'uz':
    #         return ArticleUzSerializer
    #     else:
    #         return ArticleOzSerializer

    def list(self, request):
        general_queryset = []
        # latest
        if self.request.LANGUAGE_CODE == 'ru':
            qs = self.queryset \
                .annotate(heading=F('ru_heading'))\
                .order_by('-created_at')[:8]

        # general_queryset.append(qs)
        print(general_queryset)
        popular_dict = {
            "category": "Последние",
            "data": qs.values()
        }
        general_queryset.append(popular_dict)
        return Response(general_queryset)

