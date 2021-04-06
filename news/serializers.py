from rest_framework import serializers
from .models import *


# Subcategory Serializers
class SubCategoryRuSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="ru_name")

    class Meta:
        model = SubCategory
        fields = ('id', 'name',)


class SubCategoryOzSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="oz_name")

    class Meta:
        model = SubCategory
        fields = ('id', 'name',)


class SubCategoryUzSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="uz_name")

    class Meta:
        model = SubCategory
        fields = ('id', 'name',)


# Category Serializers
class CategoryRuSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryRuSerializer(many=True)
    name = serializers.CharField(source="ru_name")

    class Meta:
        model = Category
        fields = ('id', 'name', 'sub_categories',)


class CategoryOzSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryOzSerializer(many=True)
    name = serializers.CharField(source="oz_name")

    class Meta:
        model = Category
        fields = ('id', 'name', 'sub_categories',)


class CategoryUzSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryUzSerializer(many=True)
    name = serializers.CharField(source="uz_name")

    class Meta:
        model = Category
        fields = ('id', 'name', 'sub_categories',)


# Article serializers
class ArticleRuSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    sub_category = serializers.SerializerMethodField('get_sub_category')
    heading = serializers.CharField(source='ru_heading')
    subheading = serializers.CharField(source='ru_subheading')

    class Meta:
        model = Article
        fields = ('heading', 'subheading', 'main_image', 'category', 'sub_category')

    def get_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "name": obj.sub_category.category.ru_name
        }

    def get_sub_category(self, obj):
        return {
            "id": obj.sub_category.id,
            "name": obj.sub_category.ru_name
        }


class ArticleSerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField('get_category')
    # sub_category = serializers.SerializerMethodField('get_sub_category')
    heading = serializers.CharField()
    subheading = serializers.CharField()
    category_name = serializers.CharField()
    subcategory_name = serializers.CharField()

    class Meta:
        model = Article
        fields = (
            'id',
            'heading',
            'subheading',
            'main_image',
            'category_name',
            'subcategory_name',
            'created_at',
            'view_count',
        )

    # def get_category(self, obj):
    #     return {
    #         "id": obj.sub_category.category.id,
    #         "name": self.category_name
    #     }

    # def get_sub_category(self, obj):
    #     return {
    #         "id": obj.sub_category.category.id,
    #         "name": obj.sub_category.uz_name
    #     }


class ArticleUzSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    sub_category = serializers.SerializerMethodField('get_sub_category')
    heading = serializers.CharField(source='uz_heading')
    subheading = serializers.CharField(source='uz_subheading')

    class Meta:
        model = Article
        fields = ('heading', 'subheading', 'main_image', 'category', 'sub_category', )

    def get_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "name": obj.sub_category.category.uz_name
        }

    def get_sub_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "name": obj.sub_category.uz_name
        }


class ArticleOzSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    sub_category = serializers.SerializerMethodField('get_sub_category')
    heading = serializers.CharField(source='oz_heading')
    subheading = serializers.CharField(source='oz_subheading')
    class Meta:
        model = Article
        fields = ('heading', 'subheading', 'main_image', 'category', 'sub_category')

    def get_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "name": obj.sub_category.category.oz_name
        }

    def get_sub_category(self, obj):
        return {
            "id": obj.sub_category.category.id,
            "name": obj.sub_category.oz_name
        }


class ContentBlockRuSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='ru_content')
    class Meta:
        model = ContentBlock
        fields = ('content', 'block_image', 'video_link')


class ContentBlockUzSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='uz_content')
    class Meta:
        model = ContentBlock
        fields = ('content', 'block_image', 'video_link')


class ContentBlockOzSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source='oz_content')
    class Meta:
        model = ContentBlock
        fields = ('content', 'block_image', 'video_link')


class ArticleDetailRuSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(source='ru_heading')
    subheading = serializers.CharField(source='ru_subheading')
    content_blocks = ContentBlockRuSerializer(many=True)
    class Meta:
        model = Article
        fields = ('heading', 'subheading', 'content_blocks')


class ArticleDetailRuSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(source='ru_heading')
    subheading = serializers.CharField(source='ru_subheading')
    content_blocks = ContentBlockRuSerializer(many=True)

    class Meta:
        model = Article
        fields = ('heading', 'main_image', 'subheading', 'content_blocks')


class ArticleDetailUzSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(source='uz_heading')
    subheading = serializers.CharField(source='uz_subheading')
    content_blocks = ContentBlockUzSerializer(many=True)

    class Meta:
        model = Article
        fields = ('heading', 'main_image', 'subheading', 'content_blocks')


class ArticleDetailOzSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(source='oz_heading')
    subheading = serializers.CharField(source='oz_subheading')
    content_blocks = ContentBlockRuSerializer(many=True)
    class Meta:
        model = Article
        fields = ('heading', 'main_image', 'subheading', 'content_blocks')