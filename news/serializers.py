from rest_framework import serializers
from .models import *


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'sub_categories',)


class ArticleRuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('ru_heading',)


class ArticleUzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('uz_heading',)