from rest_framework import serializers
from .models import *


class SubCategoryRuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'ru_name',)


class SubCategoryOzSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'oz_name',)


class SubCategoryUzSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'uz_name',)



class CategoryRuSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryRuSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'ru_name', 'sub_categories',)


class CategoryOzSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryOzSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'oz_name', 'sub_categories',)


class CategoryUzSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryUzSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'uz_name', 'sub_categories',)


class ArticleRuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('ru_heading',)


class ArticleUzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('uz_heading',)


class ArticleOzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('oz_heading',)