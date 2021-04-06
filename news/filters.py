import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    # category = django_filters.CharFilter(method='filter_categories')
    sub_category = django_filters.NumberFilter(method='filter_subcategories', field_name='sub_category')

    class Meta:
        model = Article
        fields = (
            # 'sub_category__category',
            'sub_category',
        )


    # def filter_categories(self, queryset, name, value):
    #     return queryset.filter(sub_category__category_id=value)

    def filter_subcategories(self, queryset, name, value):
        return queryset.filter(sub_category_id=value)

class ArticleSubcategoryFilter(django_filters.FilterSet):
    ignore = django_filters.CharFilter(method='filter_ignore', field_name='id')

    class Meta:
        model = Article
        fields = (
            'ignore',
        )

    def filter_ignore(self, queryset, name, value):
        ignore_ids = value.split(",")
        ignore_ids_list = [int(x) for x in ignore_ids]
        return queryset.exclude(id__in=ignore_ids_list)

