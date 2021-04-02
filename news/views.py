from django.shortcuts import render
from rest_framework import status, viewsets, filters
from .serializers import *
from .models import Category, Article
from rest_framework.response import Response
from django.db.models import F
from .filters import *
from itertools import chain
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
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
            qs = self.queryset\
                .annotate(heading=F('ru_heading'))\
                .annotate(category_name=F('sub_category__category__ru_name'))\
                .annotate(subcategory_name=F('sub_category__ru_name'))\
                .annotate(subheading=F('ru_subheading'))\

            latest_qs = qs\
                .order_by('sub_category__category', '-created_at')\
                .distinct('sub_category__category',)
        serializer = ArticleSerializer(latest_qs, many=True)
        # general_queryset.append(qs)
        print(serializer)
        popular_dict = {
            "category": "Последние",
            "data": serializer.data
        }
        general_queryset.append(popular_dict)

        #others
        categories = Category.objects.all()
        for category in categories:
            category_qs = qs.filter(sub_category__category=category)[:6]
            category_serializer = ArticleSerializer(category_qs, many=True)
            category_dict = {
                "category": category.ru_name,
                "data": category_serializer.data
            }
            general_queryset.append(category_dict)
        return Response(general_queryset)


class ArticleContentView(generics.RetrieveAPIView):
    lookup_url_kwarg = "id"
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.request.LANGUAGE_CODE == 'ru':
            return ArticleDetailRuSerializer
        elif self.request.LANGUAGE_CODE == 'uz':
            return ArticleDetailUzSerializer
        else:
            return ArticleDetailOzSerializer

    # def get_queryset(self):
    #
    #     if self.request.LANGUAGE_CODE == 'ru':
    #         qs = self.queryset \
    #             .annotate(heading=F('ru_heading')) \
    #             .annotate(category_name=F('sub_category__category__ru_name')) \
    #             .annotate(subcategory_name=F('sub_category__ru_name')) \
    #             .annotate(subheading=F('ru_subheading'))\
    #             .annotate(content=F('content_blocks__ru_content')).distinct('id')
    #
    #     return qs






