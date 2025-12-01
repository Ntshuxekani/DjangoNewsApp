from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/like/', views.add_like, name='add_like'),
    path('article/<int:article_id>/comment/', views.add_comment, name='add_comment'),
    path('favorite/<int:article_id>/', views.add_favorite, name='add_favorite'),
    path('subscribe/', views.subscribe, name='subscribe'),  # if you have subscribe view
    # optionally keep api route:
    path('api/news/', views.api_news, name='api_news'),
    path("categories/", views.categories, name="categories"),
    path('trending/', views.trending, name='trending'),
    path('favourites/', views.favourites, name='favourites'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('all-news/', views.all_news, name='all_news'),

]
path('favourite/remove/<int:article_id>/', views.remove_favourite, name='remove_favourite'),