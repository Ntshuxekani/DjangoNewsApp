from django.contrib import admin
from .models import Category, NewsArticle, BreakingAlert, Subscriber, Comment, Like

@admin.action(description="Mark selected articles as Published")
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Mark selected articles as Unpublished")
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "created_at", "is_published"]
    list_filter = ["category", "is_published", "created_at"]
    search_fields = ["title", "content"]
    actions = [make_published, make_unpublished]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'is_published', 'views', 'likes_count')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'content')

@admin.register(BreakingAlert)
class BreakingAlertAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_active', 'updated_at')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author_name', 'created_at', 'is_public')
    list_filter = ('is_public',)
    search_fields = ('author_name', 'content')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'session_key', 'ip_address', 'created_at')