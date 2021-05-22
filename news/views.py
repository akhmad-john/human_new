from django.shortcuts import render
from rest_framework import status, viewsets, filters
from .serializers import *
from .models import Category, Article
from rest_framework.response import Response
from django.db.models import F, Max
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
            qs = self.queryset \
                .exclude(ru_heading__isnull=True) \
                .exclude(ru_heading__exact='') \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = self.queryset \
                .exclude(uz_heading__isnull=True) \
                .exclude(uz_heading__exact='') \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
        else:
            qs = self.queryset \
                .exclude(oz_heading__isnull=True) \
                .exclude(oz_heading__exact='') \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))

        return qs


class ArticleListHomeView(generics.ListAPIView):
    queryset = Article.objects.filter(display=True)
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        general_queryset = []

        if self.request.LANGUAGE_CODE == 'ru':
            qs = self.queryset \
                .exclude(ru_heading__isnull=True) \
                .exclude(ru_heading__exact='') \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
            latest_section_name = "Последние новости"
            popular_section_name = "Популярные новости"
            video_section_name = "Видео"
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = self.queryset \
                .exclude(uz_heading__isnull=True) \
                .exclude(uz_heading__exact='') \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
            latest_section_name = "Сўнгги хабарлар"
            popular_section_name = "Оммабоп"
            video_section_name = "Видео"
        else:
            qs = self.queryset \
                .exclude(oz_heading__isnull=True) \
                .exclude(oz_heading__exact='') \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))
            latest_section_name = "Latest news"
            popular_section_name = "Popular"
            video_section_name = "Video"

        # latest
        latest_qs = qs \
                        .order_by('-created_at')[:5]


        serializer_latest = ArticleSerializer(latest_qs, many=True)

        excepted_ids = [d['id'] for d in serializer_latest.data]
        latest_dict = {
            "category": latest_section_name,
            "style": 1,
            "data": serializer_latest.data
        }
        general_queryset.append(latest_dict)

        # most popular
        popular_qs = qs.order_by('sub_category', 'view_count') \
                         .distinct('sub_category', ) \
                         .exclude(id__in=excepted_ids)[:6]
        serializer_popular = ArticleSerializer(popular_qs, many=True)

        excepted_ids += [d['id'] for d in serializer_popular.data]
        popular_dict = {
            "category": popular_section_name,
            "style": 2,
            "data": serializer_popular.data
        }
        general_queryset.append(popular_dict)

        # video block
        video_qs = qs \
                       .filter(content_blocks__video_link__isnull=False) \
                       .values('heading', 'subheading', 'content_blocks__video_link').distinct(
            'content_blocks__video_link')[:10]
        video_dict = {
            "category": video_section_name,
            "style": 3,
            "data": video_qs
        }

        # others
        categories = Category.objects.filter(home_display=True)
        for category in categories:
            category_qs = qs.filter(sub_category__category=category).exclude(id__in=excepted_ids)[:6]
            category_serializer = ArticleSerializer(category_qs, many=True)
            if self.request.LANGUAGE_CODE == 'ru':
                category_name = category.ru_name
            elif self.request.LANGUAGE_CODE == 'uz':
                category_name = category.uz_name
            else:
                category_name = category.oz_name
            category_dict = {
                "category": category_name,
                "style": 2,
                "data": category_serializer.data
            }
            general_queryset.append(category_dict)
        general_queryset.append(video_dict)
        return Response(general_queryset)


class ArticlesPerCategoryView(generics.ListAPIView):
    lookup_url_kwarg = "category_id"
    queryset = Article.objects.filter(display=True)
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        general_queryset = []
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        qs = self.queryset.filter(sub_category__category_id=category_id)
        if self.request.LANGUAGE_CODE == 'ru':
            qs = qs \
                .exclude(ru_heading__isnull=True) \
                .exclude(ru_heading__exact='') \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
            latest_section_name = "Последние новости"
            popular_section_name = "Популярные новости"
            video_section_name = "Видео"
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = qs \
                .exclude(uz_heading__isnull=True) \
                .exclude(uz_heading__exact='') \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
            latest_section_name = "Сўнги хабарлар"
            popular_section_name = "Оммабоп"
            video_section_name = "Видео"
        else:
            qs = qs \
                .exclude(oz_heading__isnull=True) \
                .exclude(oz_heading__exact='') \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))
            latest_section_name = "Latest news"
            popular_section_name = "Popular"
            video_section_name = "Video"

        # latest
        latest_qs = qs \
                        .order_by('sub_category', '-created_at') \
                        .distinct('sub_category', )[:5]
        serializer_latest = ArticleSerializer(latest_qs, many=True)

        excepted_ids = [d['id'] for d in serializer_latest.data]

        latest_dict = {
            "category": latest_section_name,
            "style": 1,
            "data": serializer_latest.data
        }
        general_queryset.append(latest_dict)

        # most popular
        popular_qs = qs.order_by('view_count').exclude(id__in=excepted_ids)[:6]
        serializer_popular = ArticleSerializer(popular_qs, many=True)

        excepted_ids += [d['id'] for d in serializer_popular.data]
        popular_dict = {
            "category": popular_section_name,
            "style": 2,
            "data": serializer_popular.data
        }
        general_queryset.append(popular_dict)

        # video block
        video_qs = qs \
                       .filter(content_blocks__video_link__isnull=False, sub_category__category_id=category_id) \
                       .values('heading', 'subheading', 'content_blocks__video_link').distinct(
            'content_blocks__video_link')[:10]
        video_dict = {
            "category": video_section_name,
            "style": 3,
            "data": video_qs
        }

        # others
        sub_categories = SubCategory.objects.filter(home_display=True, category_id=category_id)
        for sub_category in sub_categories:
            sub_category_qs = qs.filter(sub_category=sub_category).exclude(id__in=excepted_ids)[:6]
            sub_category_serializer = ArticleSerializer(sub_category_qs, many=True)
            sub_category_dict = {
                "category": sub_category.ru_name,
                "style": 2,
                "data": sub_category_serializer.data
            }
            general_queryset.append(sub_category_dict)
        general_queryset.append(video_dict)
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
                .exclude(ru_heading__isnull=True) \
                .exclude(ru_heading__exact='') \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
            latest_section_name = "Последние новости"
            popular_section_name = "Популярные новости"
            video_section_name = "Видео"
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = qs \
                .exclude(uz_heading__isnull=True) \
                .exclude(uz_heading__exact='') \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
            latest_section_name = "Сўнги хабарлар"
            popular_section_name = "Оммабоп"
            video_section_name = "Видео"
        else:
            qs = qs \
                .exclude(oz_heading__isnull=True) \
                .exclude(oz_heading__exact='') \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))
            latest_section_name = "Latest news"
            popular_section_name = "Popular"
            video_section_name = "Video"

        # latest
        latest_qs = qs \
                        .order_by('sub_category', '-created_at')[:6]
        serializer_latest = ArticleSerializer(latest_qs, many=True)

        excepted_ids = [d['id'] for d in serializer_latest.data]

        latest_dict = {
            "category": latest_section_name,
            "style": 1,
            "data": serializer_latest.data
        }
        general_queryset.append(latest_dict)

        # most popular
        popular_qs = qs.order_by('view_count').exclude(id__in=excepted_ids)[:6]
        serializer_popular = ArticleSerializer(popular_qs, many=True)

        excepted_ids += [d['id'] for d in serializer_popular.data]
        popular_dict = {
            "category": popular_section_name,
            "style": 2,
            "data": serializer_popular.data
        }
        general_queryset.append(popular_dict)

        # video block
        # video block
        video_qs = qs \
                       .filter(content_blocks__video_link__isnull=False, sub_category_id=subcategory_id) \
                       .values('heading', 'subheading', 'content_blocks__video_link').distinct(
            'content_blocks__video_link')[:10]
        video_dict = {
            "category": video_section_name,
            "style": 3,
            "data": video_qs
        }
        general_queryset.append(video_dict)
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
            qs = qs \
                .exclude(ru_heading__isnull=True) \
                .exclude(ru_heading__exact='') \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
        elif self.request.LANGUAGE_CODE == 'uz':
            qs = qs \
                .exclude(uz_heading__isnull=True) \
                .exclude(uz_heading__exact='') \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
        else:
            qs = qs \
                .exclude(oz_heading__isnull=True) \
                .exclude(oz_heading__exact='') \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))

        serializer = ArticleSerializer(data=qs, many=True)
        serializer.is_valid()
        return qs


# class ArticleContentView(generics.RetrieveAPIView):
#     lookup_url_kwarg = "id"
#     queryset = Article.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.LANGUAGE_CODE == 'ru':
#             return ArticleDetailRuSerializer
#         elif self.request.LANGUAGE_CODE == 'uz':
#             return ArticleDetailUzSerializer
#         else:
#             return ArticleDetailOzSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#
#
#
#         obj = self.get_object()
#         obj.view_count = obj.view_count + 1
#         obj.save(update_fields=("view_count", ))
#         return Response(self.request.)


class ArticleContentView(generics.RetrieveAPIView):
    lookup_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs.get(self.lookup_url_kwarg)
        article = Article.objects.get(id=article_id)
        subcategory_id = article.sub_category.id
        recommended_qs = Article.objects\
            .filter(sub_category_id=subcategory_id, display=True) \
            .exclude(id=article_id)
        if self.request.LANGUAGE_CODE == 'ru':
            detail_serializer = ArticleDetailRuSerializer
            recommended_qs = recommended_qs \
                .exclude(ru_heading__isnull=True) \
                .exclude(ru_heading__exact='') \
                .order_by('-created_at')[:6] \
                .annotate(heading=F('ru_heading')) \
                .annotate(category_name=F('sub_category__category__ru_name')) \
                .annotate(subcategory_name=F('sub_category__ru_name')) \
                .annotate(subheading=F('ru_subheading'))
        elif self.request.LANGUAGE_CODE == 'uz':
            detail_serializer = ArticleDetailUzSerializer
            recommended_qs = recommended_qs \
                .exclude(uz_heading__isnull=True) \
                .exclude(uz_heading__exact='') \
                .order_by('-created_at')[:6] \
                .annotate(heading=F('uz_heading')) \
                .annotate(category_name=F('sub_category__category__uz_name')) \
                .annotate(subcategory_name=F('sub_category__uz_name')) \
                .annotate(subheading=F('uz_subheading'))
        else:
            detail_serializer = ArticleDetailOzSerializer
            recommended_qs = recommended_qs \
                .exclude(oz_heading__isnull=True) \
                .exclude(oz_heading__exact='') \
                .order_by('-created_at')[:6] \
                .annotate(heading=F('oz_heading')) \
                .annotate(category_name=F('sub_category__category__oz_name')) \
                .annotate(subcategory_name=F('sub_category__oz_name')) \
                .annotate(subheading=F('oz_subheading'))

        article_serializer = detail_serializer(article)

        recommended_serializer = ArticleSerializer(recommended_qs, many=True)

        data_to_send = article_serializer.data
        data_to_send.update({"recomended": recommended_serializer.data})


        article.view_count += 1
        article.save()

        return Response(data_to_send)
