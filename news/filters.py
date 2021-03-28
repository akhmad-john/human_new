import django_filters

class ArticleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method='filter_categories')
    subcategory = django_filters.CharFilter(method='filter_subcategories')

    def filter_categories(self, queryset, name, value):
        return queryset.filter(sub_category__category_id=value)

    def filter_subcategories(self, queryset, name, value):
        return queryset.filter(sub_category_id=value)