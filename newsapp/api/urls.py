from django.urls import path
from .views import (
    PublishedArticlesAPI,
    ArticleDetailAPI,
    CategoryAPI,
    BreakingAlertAPI,
    SubscribeAPI
)

urlpatterns = [
    path('articles/', PublishedArticlesAPI.as_view(), name='api_articles'),
    path('articles/<int:pk>/', ArticleDetailAPI.as_view(), name='api_article_detail'),
    path('categories/', CategoryAPI.as_view(), name='api_categories'),
    path('breaking/', BreakingAlertAPI.as_view(), name='api_breaking'),
    path('subscribe/', SubscribeAPI.as_view(), name='api_subscribe'),
]
