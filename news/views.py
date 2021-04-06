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
from human_uz.pagination import CustomPagination
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
    filter_backends = [
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend
    ]
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

    def get_queryset(self):
        if self.request.LANGUAGE_CODE == 'ru':
            qs = self.queryset\
                .annotate(heading=F('ru_heading'))\
                .annotate(category_name=F('sub_category__category__ru_name'))\
                .annotate(subcategory_name=F('sub_category__ru_name'))\
                .annotate(subheading=F('ru_subheading'))
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = self.queryset\
                .annotate(heading=F('uz_heading'))\
                .annotate(category_name=F('sub_category__category__uz_name'))\
                .annotate(subcategory_name=F('sub_category__uz_name'))\
                .annotate(subheading=F('uz_subheading'))
        else:
            qs = self.queryset\
                .annotate(heading=F('oz_heading'))\
                .annotate(category_name=F('sub_category__category__oz_name'))\
                .annotate(subcategory_name=F('sub_category__oz_name'))\
                .annotate(subheading=F('oz_subheading'))

        return qs






class ArticleListHomeView(generics.ListAPIView):
    queryset = Article.objects.filter(display=True)
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        general_queryset = []
        # latest
        if self.request.LANGUAGE_CODE == 'ru':
            qs = self.queryset \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = self.queryset \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
        else:
            qs = self.queryset \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))

        latest_qs = qs \
            .order_by('sub_category__category', '-created_at') \
            .distinct('sub_category__category', )
        serializer = ArticleSerializer(latest_qs, many=True)

        excepted_ids = [d['id'] for d in serializer.data]
        # general_queryset.append(qs)

        latest_dict = {
            "category": "Последние",
            "style": 1,
            "data": serializer.data
        }
        general_queryset.append(latest_dict)

        # others
        categories = Category.objects.filter(home_display=True)
        for category in categories:
            category_qs = qs.filter(sub_category__category=category).exclude(id__in=excepted_ids)[:6]
            category_serializer = ArticleSerializer(category_qs, many=True)
            category_dict = {
                "category": category.ru_name,
                "style": 2,
                "data": category_serializer.data
            }
            general_queryset.append(category_dict)
        return Response(general_queryset)


class ArticlesPerCategoryView(generics.ListAPIView):
    lookup_url_kwarg = "category_id"
    queryset = Article.objects.filter(display=True)
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        general_queryset = []
        # latest
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        qs = self.queryset.filter(sub_category__category_id=category_id)
        if self.request.LANGUAGE_CODE == 'ru':
            qs = qs \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = self.queryset \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
        else:
            qs = self.queryset \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))

        latest_qs = qs \
            .order_by('sub_category', '-created_at') \
            .distinct('sub_category', )
        serializer = ArticleSerializer(latest_qs, many=True)

        excepted_ids = [d['id'] for d in serializer.data]


        latest_dict = {
            "category": "Последние",
            "data": serializer.data
        }
        general_queryset.append(latest_dict)

        # others
        sub_categories = SubCategory.objects.filter(home_display=True, category_id=category_id)
        for sub_category in sub_categories:
            sub_category_qs = qs.filter(sub_category=sub_category).exclude(id__in=excepted_ids)[:6]
            sub_category_serializer = ArticleSerializer(sub_category_qs, many=True)
            sub_category_dict = {
                "category": sub_category.ru_name,
                "data": sub_category_serializer.data
            }
            general_queryset.append(sub_category_dict)
        return Response(general_queryset)


class ArticlesPerSubCategoryView(generics.ListAPIView):
    lookup_url_kwarg = "subcategory_id"
    queryset = Article.objects.filter(display=True)
    serializer_class = ArticleSerializer


    def list(self, request, *args, **kwargs):
        general_queryset = []
        # latest
        subcategory_id = self.kwargs.get(self.lookup_url_kwarg)
        qs = self.queryset.filter(sub_category_id=subcategory_id)
        if self.request.LANGUAGE_CODE == 'ru':
            qs = qs \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = self.queryset \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
        else:
            qs = self.queryset \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))

        latest_qs = qs \
            .order_by('sub_category', '-created_at') \
            .distinct('sub_category', )
        serializer = ArticleSerializer(latest_qs, many=True)


        latest_dict = {
            "category": "Последние",
            "data": serializer.data
        }
        general_queryset.append(latest_dict)

        return Response(general_queryset)


class ArticleBySybcategoriesPaginatedView(generics.ListAPIView):
    queryset = Article.objects.filter(display=True)
    lookup_url_kwarg = "subcategory_id"
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    filter_class = ArticleSubcategoryFilter
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend
    ]

    def get_queryset(self):
        subcategory_id = self.kwargs.get(self.lookup_url_kwarg)
        qs = self.queryset.filter(sub_category_id=subcategory_id)
        if self.request.LANGUAGE_CODE == 'ru':
            qs = qs\
                .annotate(heading=F('ru_heading'))\
                .annotate(category_name=F('sub_category__category__ru_name'))\
                .annotate(subcategory_name=F('sub_category__ru_name'))\
                .annotate(subheading=F('ru_subheading'))
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = qs\
                .annotate(heading=F('uz_heading'))\
                .annotate(category_name=F('sub_category__category__uz_name'))\
                .annotate(subcategory_name=F('sub_category__uz_name'))\
                .annotate(subheading=F('uz_subheading'))
        else:
            qs = qs\
                .annotate(heading=F('oz_heading'))\
                .annotate(category_name=F('sub_category__category__oz_name'))\
                .annotate(subcategory_name=F('sub_category__oz_name'))\
                .annotate(subheading=F('oz_subheading'))

        return qs


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

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1
        obj.save(update_fields=("view_count", ))
        return super().retrieve(request, *args, **kwargs)

