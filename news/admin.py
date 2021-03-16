from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


class ContentBlockRuInline(admin.StackedInline):
    model = ContentBlock
    fields = ['ru_content', 'block_image',]
    min_num = 0
    suit_classes = 'suit-tab suit-tab-russian'



class ContentBlockOzInline(admin.StackedInline):
    model = ContentBlock
    fields = ['oz_content',]
    min_num = 0
    suit_classes = 'suit-tab suit-tab-uzbeklat'



class ContentBlockUzInline(admin.StackedInline):
    model = ContentBlock
    fields = ['uz_content',]
    min_num = 0
    suit_classes = 'suit-tab suit-tab-uzbekcyr'



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    # fields = ('sub_category', 'ru_heading', 'main_image',)
    inlines = [ContentBlockRuInline, ContentBlockOzInline, ContentBlockUzInline]

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-russian',),
            'fields': ['sub_category', 'main_image','ru_heading', 'ru_subheading',]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-uzbeklat',),
            'fields': [ 'oz_heading', 'oz_subheading',]}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-uzbekcyr',),
            'fields': [ 'uz_heading', 'uz_subheading',]}),

    ]
       

    suit_form_tabs = (('russian', 'Русский'), ('uzbeklat', 'O`zbekcha'), ('uzbekcyr', 'Узбекча'))


