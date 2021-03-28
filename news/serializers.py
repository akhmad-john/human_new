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
    class Meta:
        model = Category
        fields = ('id', 'uz_name', 'sub_categories',)



class ArticleRuSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    sub_category = serializers.SerializerMethodField('get_sub_category')
    class Meta:
        model = Article
        fields = ('ru_heading', 'ru_subheading', 'main_image', 'category', 'sub_category')

    def get_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "ru_name": obj.sub_category.category.ru_name
        }

    def get_sub_category(self, obj):
        return {
            "id": obj.sub_category.id,
            "ru_name": obj.sub_category.ru_name
        }


class ArticleUzSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    sub_category = serializers.SerializerMethodField('get_sub_category')

    class Meta:
        model = Article
        fields = ('uz_heading', 'uz_subheading', 'main_image', 'category', 'sub_category')

    def get_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "uz_name": obj.sub_category.category.uz_name
        }

    def get_sub_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "uz_name": obj.sub_category.uz_name
        }

class ArticleOzSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    sub_category = serializers.SerializerMethodField('get_sub_category')

    class Meta:
        model = Article
        fields = ('oz_heading', 'oz_subheading', 'main_image', 'category', 'sub_category')

    def get_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "oz_name": obj.sub_category.category.oz_name
        }

    def get_sub_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "roz_name": obj.sub_category.oz_name
        }