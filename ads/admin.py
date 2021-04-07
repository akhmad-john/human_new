from django.contrib import admin
from .models import Advertisement
# Register your models here.

@admin.register(Advertisement)
class ArticleAdmin(admin.ModelAdmin):
    fields = ('company_name', 'banner', 'ad_type', 'active')
    list_display = ('company_name', 'ad_type', 'click_count', 'active')
    list_editable = ('active',)
