from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = ('created_at',)


class ContentBlockRuInline(admin.StackedInline):
    model = ContentBlock
    fields = ['ru_content', 'block_image', 'video_link']
    min_num = 0
    extra = 1
    suit_classes = 'suit-tab suit-tab-russian'



class ContentBlockOzInline(admin.StackedInline):
    model = ContentBlock
    fields = ['oz_content',]
    min_num = 0
    extra = 1
    suit_classes = 'suit-tab suit-tab-uzbeklat'



class ContentBlockUzInline(admin.StackedInline):
    model = ContentBlock
    fields = ['uz_content',]
    min_num = 0
    extra = 1
    suit_classes = 'suit-tab suit-tab-uzbekcyr'



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    # fields = ('sub_category', 'ru_heading', 'main_image',)
    inlines = [ContentBlockRuInline, ContentBlockOzInline, ContentBlockUzInline]
    # readonly_fields = ['created_at']
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-russian',),
            'fields': ['sub_category', 'tag', 'main_image','ru_heading', 'ru_subheading', 'created_at']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-uzbeklat',),
            'fields': [ 'oz_heading', 'oz_subheading',]}),
        (None, {
            'classes': ('suit-tab', 'suit-tab-uzbekcyr',),
            'fields': [ 'uz_heading', 'uz_subheading',]}),

    ]
    filter_horizontal = ('tag',)
    suit_form_tabs = (('russian', 'Русский'), ('uzbeklat', 'O`zbekcha'), ('uzbekcyr', 'Узбекча'))
    list_filter = ('sub_category', 'sub_category__category', 'tag')
    list_display = ('id', 'ru_heading', 'created_at', 'display')
    list_editable = ('display',)


