from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
    path('api/news/', views.api_news, name='api_news'),
    path("subscribe/", views.subscribe, name="subscribe"),
]
