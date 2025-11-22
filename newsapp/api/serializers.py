from rest_framework import serializers
from newsapp.models import NewsArticle, Category, BreakingAlert, Subscriber


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class NewsArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'content', 'image', 'created_at', 'category']


class BreakingAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreakingAlert
        fields = ['id', 'message', 'is_active']


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email']
