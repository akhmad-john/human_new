from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categories', CategoryriesViewSet)
router.register(r'articles', ArticleListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('detail/<int:id>/', ArticleContentView.as_view()),
]