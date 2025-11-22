from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from newsapp.models import NewsArticle, Category, BreakingAlert, Subscriber
from .serializers import (
    NewsArticleSerializer,
    CategorySerializer,
    BreakingAlertSerializer,
    SubscriberSerializer
)


class PublishedArticlesAPI(ListAPIView):
    serializer_class = NewsArticleSerializer

    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True).order_by('-created_at')


class ArticleDetailAPI(RetrieveAPIView):
    queryset = NewsArticle.objects.filter(is_published=True)
    serializer_class = NewsArticleSerializer


class CategoryAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BreakingAlertAPI(ListAPIView):
    queryset = BreakingAlert.objects.filter(is_active=True)
    serializer_class = BreakingAlertSerializer


class SubscribeAPI(CreateAPIView):
    serializer_class = SubscriberSerializer
